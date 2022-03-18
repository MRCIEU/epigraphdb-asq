import sqlite3
from typing import Any, Dict

import pandas as pd
import ray
import requests
from nxontology import NXOntology

from analysis import utils
from analysis.settings import config

from icecream import ic  # noqa
from loguru import logger  # noqa
from pydash import py_  # noqa

from metaflow import Flow, FlowSpec, Parameter, step  # noqa


DATA_ROOT = utils.find_data_root()
BATCH_LOG_STEP = 500


def get_efo_nodes_size(url: str) -> int:
    query = """
    MATCH (efo:Efo)
    RETURN size(collect(DISTINCT efo)) AS n_nodes
    """
    payload = {"query": query}
    r = requests.post(f"{url}/cypher", json=payload)
    r.raise_for_status()
    res = r.json()["results"]
    return res[0]["n_nodes"]


def get_efo_rels_size(url: str) -> int:
    query = """
    MATCH (efo:Efo)-[r:EFO_CHILD_OF]->(parent_efo:Efo)
    RETURN size(collect(DISTINCT r)) AS n_rels
    """
    payload = {"query": query}
    r = requests.post(f"{url}/cypher", json=payload)
    r.raise_for_status()
    res = r.json()["results"]
    return res[0]["n_rels"]


@ray.remote
def get_efo_nodes(url: str, skip: int, size: int) -> Dict[str, Any]:
    if skip % BATCH_LOG_STEP == 0:
        logger.info(f"efo_nodes {skip=} start")
    query = f"""
    MATCH (efo:Efo)
    RETURN efo
    SKIP {skip}
    LIMIT {size}
    """
    payload = {"query": query}
    r = requests.post(f"{url}/cypher", json=payload)
    r.raise_for_status()
    res = r.json()["results"]
    return res


@ray.remote
def get_efo_rels(url: str, skip: int, size: int) -> Dict[str, Any]:
    if skip % BATCH_LOG_STEP == 0:
        logger.info(f"efo_rels {skip=}")
    query = f"""
    MATCH (efo:Efo)-[r:EFO_CHILD_OF]->(parent_efo:Efo)
    RETURN
        efo {{.id}},
        parent_efo {{.id}}
    SKIP {skip}
    LIMIT {size}
    """
    payload = {"query": query}
    r = requests.post(f"{url}/cypher", json=payload)
    r.raise_for_status()
    res = r.json()["results"]
    return res


@ray.remote
def calc_efo_ic(
    item: Dict[str, Any], nxo: NXOntology, idx: int, total: int
) -> Dict[str, Any]:
    if idx % BATCH_LOG_STEP == 0:
        logger.info(f"#{idx}/{total}")
    ic_score = nxo.node_info(item["efo_term"]).intrinsic_ic_sanchez_scaled
    res = {
        "efo_term": item["efo_term"],
        "efo_id": item["efo_id"],
        "ic_score": ic_score,
    }
    return res


class EfoProcessing(FlowSpec):
    NUM_WORKERS = Parameter(
        "num_workers",
        help="Number of cpu workers",
        default=16,
    )
    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        default=False,
    )

    @step
    def start(self):
        "Init."
        logger.info("Start.")

        self.DATA_DIR = DATA_ROOT / "efo"
        self.API_URL = config.epigraphdb_api_url
        logger.info(
            f"""Params

        {self.NUM_WORKERS=}
        {self.OVERWRITE=}
        {self.API_URL=}
        {self.DATA_DIR=}
        """
        )
        ray.init(num_cpus=self.NUM_WORKERS)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.EFO_NODES_FILE = self.DATA_DIR / "efo_nodes.csv"
        self.EFO_RELS_FILE = self.DATA_DIR / "efo_rels.csv"
        self.next(self.get_efo_init)

    @step
    def get_efo_init(self):
        self.efo_nodes_size: int = get_efo_nodes_size(url=self.API_URL)
        ic(self.efo_nodes_size)
        self.efo_rels_size: int = get_efo_rels_size(url=self.API_URL)
        ic(self.efo_rels_size)
        self.next(self.get_efo_nodes, self.get_efo_rels)

    @step
    def get_efo_nodes(self):
        batch_size = 1_000
        efo_nodes_futures = [
            get_efo_nodes.remote(
                url=self.API_URL,
                skip=skip,
                size=batch_size,
            )
            for skip in range(0, self.efo_nodes_size + 1, batch_size)
        ]
        self.efo_nodes_list = ray.get(efo_nodes_futures)
        ic(len(self.efo_nodes_list))
        ic(self.efo_nodes_list[0])
        self.next(self.make_efo_graph)

    @step
    def get_efo_rels(self):
        batch_size = 1_000
        efo_rels_futures = [
            get_efo_rels.remote(
                url=self.API_URL,
                skip=skip,
                size=batch_size,
            )
            for skip in range(0, self.efo_rels_size + 1, batch_size)
        ]
        self.efo_rels_list = ray.get(efo_rels_futures)
        ic(len(self.efo_rels_list))
        ic(self.efo_rels_list[0])
        self.next(self.make_efo_graph)

    @step
    def make_efo_graph(self, inputs):
        # Drop source as it is a list, and not work well with drop_dupes
        self.merge_artifacts(inputs)
        self.efo_nodes = (
            pd.json_normalize(py_.flatten(inputs.get_efo_nodes.efo_nodes_list))
            .drop(columns=["efo._source"])
            .drop_duplicates()
        )
        ic(self.efo_nodes.info())
        if not self.EFO_NODES_FILE.exists() or self.OVERWRITE:
            logger.info(f"Write to {self.EFO_NODES_FILE}")
            self.efo_nodes.to_csv(self.EFO_NODES_FILE, index=False)
        self.efo_rels = pd.json_normalize(
            py_.flatten(inputs.get_efo_rels.efo_rels_list)
        ).drop_duplicates()
        ic(self.efo_rels.info())
        if not self.EFO_RELS_FILE.exists() or self.OVERWRITE:
            logger.info(f"Write to {self.EFO_RELS_FILE}")
            self.efo_rels.to_csv(self.EFO_RELS_FILE, index=False)
        self.next(self.make_efo_ic)

    @step
    def make_efo_ic(self):
        # NOTE: as had checked there is a good id-name mapping, so can use name as an id
        rels_df = self.efo_rels.merge(
            self.efo_nodes[["efo._name", "efo._id"]].rename(
                columns={"efo._name": "node", "efo._id": "efo.id"}
            ),
            left_on="efo.id",
            right_on="efo.id",
        ).merge(
            self.efo_nodes[["efo._name", "efo._id"]].rename(
                columns={
                    "efo._name": "parent_node",
                    "efo._id": "parent_efo.id",
                }
            ),
            left_on="parent_efo.id",
            right_on="parent_efo.id",
        )
        logger.info("Init nxo graph")
        nxo = NXOntology()
        nxo.graph.add_edges_from(
            [
                (row["node"], row["parent_node"])
                for idx, row in rels_df.iterrows()
            ]
        )
        ic
        logger.info("calc ic start")
        efo_items = (
            self.efo_nodes[["efo._name", "efo._id"]]
            .rename(columns={"efo._name": "efo_term", "efo._id": "efo_id"})
            .to_dict(orient="records")
        )
        ic_futures = [
            calc_efo_ic.remote(item=_, nxo=nxo, idx=idx, total=len(efo_items))
            for idx, _ in enumerate(efo_items)
        ]
        self.ic_list = ray.get(ic_futures)
        self.ic_df = pd.DataFrame(self.ic_list)
        ic(self.ic_df.info())
        logger.info("calc ic end")
        self.IC_FILE = self.DATA_DIR / "ic.csv"
        if not self.IC_FILE.exists() or self.OVERWRITE:
            logger.info(f"Write to {self.IC_FILE}")
            self.ic_df.to_csv(self.IC_FILE, index=False)
        self.next(self.save)

    @step
    def save(self):
        self.EFO_DB_FILE = self.DATA_DIR / "epigraphdb_efo.db"
        if not self.EFO_DB_FILE.exists() or self.OVERWRITE:
            logger.info(f"write to {self.EFO_DB_FILE}")
            with sqlite3.connect(self.EFO_DB_FILE) as conn:
                logger.info("NODES")
                self.efo_nodes.to_sql(
                    "NODES",
                    conn,
                    index=True,
                    index_label="idx",
                    if_exists="replace",
                )
                logger.info("RELS")
                self.efo_rels.to_sql(
                    "RELS",
                    conn,
                    index=True,
                    index_label="idx",
                    if_exists="replace",
                )
                logger.info("IC")
                self.ic_df.to_sql(
                    "IC",
                    conn,
                    index=True,
                    index_label="idx",
                    if_exists="replace",
                )
        self.next(self.end)

    @step
    def end(self):
        "Finish."
        logger.info("Done.")


if __name__ == "__main__":
    EfoProcessing()
