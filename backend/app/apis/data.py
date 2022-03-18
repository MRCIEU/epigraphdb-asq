import json
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
import pandera as pa
import requests
from common_processing.ent_harmonization.processing import efo_ic_scores
from common_processing.resources.epigraphdb import ENT_URL_TEMPLATE
from common_processing.types import Config
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pandera.typing import DataFrame, Series
from pydantic import BaseModel
from pydash import py_
from typing_extensions import TypedDict

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


class BaseEnt(TypedDict):
    ent_id: str
    ent_term: str


class BaseEntResponse(BaseModel):
    ent_id: str
    ent_term: str


class EfoDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    ent_url: Series[str]
    ic_score: Series[float]
    ent_type: Series[str]
    ref_ent_id: Series[str]


class EfoDataResDataItem(TypedDict):
    ent_id: str
    ent_term: str
    ent_url: str
    ic_score: float
    ent_type: str
    ref_ent_id: str


class SimilarityScoreItem(TypedDict):
    source_ent_id: str
    source_ent_term: str
    target_ent_id: str
    target_ent_term: str
    similarity_score: float


class EfoDataResItem(TypedDict):
    ent_id: str
    efo_data: List[EfoDataResDataItem]
    query_ents: List[BaseEnt]
    similarity_scores: List[SimilarityScoreItem]


OntologyDataRes = List[EfoDataResItem]


class OntologyDataRequest(BaseModel):
    ent_ids: List[str]
    query_terms: List[str] = []


class EfoDataResDataResponseItem(BaseModel):
    ent_id: str
    ent_term: str
    ent_url: str
    ic_score: float
    ent_type: str
    ref_ent_id: str


class SimilarityScoreResponseItem(BaseModel):
    source_ent_id: str
    source_ent_term: str
    target_ent_id: str
    target_ent_term: str
    similarity_score: float


class EfoDataResponseItem(BaseModel):
    ent_id: str
    efo_data: List[EfoDataResDataResponseItem]
    query_ents: List[BaseEntResponse]
    similarity_scores: List[SimilarityScoreResponseItem]


OntologyDataResponse = List[EfoDataResponseItem]


@router.post(
    "/data/efo_ic_scores", response_model=response_models.EfoIcResponse
)
async def get_efo_ic_scores(
    data: request_models.EfoIcRequest,
) -> types.EfoIcRes:
    ent_ids = data.ent_ids
    df = efo_ic_scores(ent_ids=ent_ids, config=config)
    res: types.EfoIcRes = df.to_dict(orient="records")
    return res


@router.post("/data/ontology", response_model=OntologyDataResponse)
async def get_ontology_data(data: OntologyDataRequest) -> OntologyDataRes:
    ent_ids = data.ent_ids
    query_terms = data.query_terms
    query_ents: List[BaseEnt] = [
        {"ent_id": f"query-ent-{idx}", "ent_term": _}
        for idx, _ in enumerate(query_terms)
    ]
    efo_df = pd.DataFrame(
        [
            {
                "ent_id": _,
                "efo_data": _get_efo_data(ent_id=_, config=config).to_dict(
                    orient="records"
                ),
                "query_ents": query_ents,
            }
            for _ in ent_ids
        ]
    )
    sim_scores = _make_similarity_scores(efo_df=efo_df, query_ents=query_ents)
    efo_df = efo_df.assign(
        # only subset entities related to the specific efo
        similarity_scores=lambda df: df.apply(
            lambda row: _make_similarity_score_subset(
                similarity_scores=sim_scores, efo_data=row["efo_data"]
            ),
            axis=1,
        ),
    )
    res: OntologyDataRes = efo_df.to_dict(orient="records")
    return res


@router.get(
    "/data/prompt/literature-term", response_model=List[BaseEntResponse]
)
async def get_prompt_literature_term(q: str) -> List[BaseEnt]:
    url = config.epigraphdb_web_backend_url + "/search/quick/node"
    params: Dict[str, Any] = {
        "q": q,
        "size": 20,
        "meta_node": "LiteratureTerm",
    }
    r = requests.get(url=url, params=params)
    r.raise_for_status()
    r_data = r.json()
    res: List[BaseEnt] = [
        {"ent_id": _["id"]["id"], "ent_term": _["name"]} for _ in r_data
    ]
    return res


@router.get("/data/analysis-results")
@cache(namespace="analysis-results")
async def get_analysis_results():
    data_path = Path("/data") / "analysis-artifacts" / "case_data_flat.json"
    assert data_path.exists()
    with data_path.open() as f:
        res = json.load(f)
    return res


@pa.check_types
def _get_efo_data(ent_id: str, config: Config) -> DataFrame[EfoDf]:
    @pa.check_types
    def _query(query: str, ent_type: str, config: Config) -> DataFrame[EfoDf]:
        url = "{url}/cypher".format(url=config.epigraphdb_api_url)
        r = requests.post(url, json={"query": query})
        r.raise_for_status()
        results = r.json()["results"]
        if len(results) == 0:
            empty_df = EfoDf.example(size=1).iloc[:0, :].copy()
            return empty_df
        else:
            df = pd.json_normalize(results).assign(
                ref_ent_id=ent_id,
                ent_type=ent_type,
                ent_url=lambda df: df["ent_id"].apply(
                    lambda ent_id: ENT_URL_TEMPLATE.format(
                        meta_ent="Efo", ent_id=ent_id
                    )
                ),
            )
            ic_df = efo_ic_scores(
                ent_ids=df["ent_id"].tolist(),
                config=config,
                ic_score_threshold=None,
            )
            df = df.merge(ic_df[["ent_id", "ic_score"]], on="ent_id")
        return df

    self_query = """
    MATCH (efo:Efo)
    WHERE efo._id = "{ent_id}"
    RETURN
        efo._id AS ent_id,
        efo._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    parents_query = """
    MATCH (parent:Efo)-[r:EFO_CHILD_OF]->(ref:Efo)
    WHERE ref._id = "{ent_id}"
    RETURN
        parent._id AS ent_id,
        parent._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    # ancestors_query_base = """
    # MATCH (ancestor:Efo)-[r:EFO_CHILD_OF]->(parent:Efo)
    # WHERE parent._id IN [{parent_id_list}]
    # RETURN
    #     ancestor._id AS ent_id,
    #     ancestor._name AS ent_term,
    #     parent._id as parent_ref_id
    # LIMIT 10
    # """
    children_query = """
    MATCH (ref:Efo)-[r:EFO_CHILD_OF]->(child:Efo)
    WHERE ref._id = "{ent_id}"
    RETURN
        child._id AS ent_id,
        child._name AS ent_term
    LIMIT 10
    """.format(
        ent_id=ent_id
    )
    self_df = _query(self_query, ent_type="ontology_self", config=config)
    parents_df = _query(
        parents_query, ent_type="ontology_parent", config=config
    )
    if len(parents_df) > 0:
        parent_ents = parents_df["ent_id"].drop_duplicates().tolist()
        # ancestors_query = ancestors_query_base.format(
        #     parent_id_list=",".join([f"'{_}'" for _ in parent_ents])
        # )
        # ancestors_df = (
        #     _query(
        #         ancestors_query, ent_type="ontology_ancestor", config=config
        #     )
        #     .drop(columns=["ref_ent_id"])
        #     .rename(columns={"parent_ref_id": "ref_ent_id"})
        # )
        origin_df = pd.concat(
            [
                _get_efo_shortest_from_origin(ent_id=_, config=config)
                for _ in parent_ents
            ]
        )
    else:
        # ancestors_df = pd.DataFrame()
        origin_df = pd.DataFrame()
    children_df = _query(
        children_query, ent_type="ontology_child", config=config
    )
    res = pd.concat(
        # [self_df, parents_df, ancestors_df, origin_df, children_df]
        [self_df, parents_df, origin_df, children_df]
    )
    return res


@pa.check_types
def _get_efo_shortest_from_origin(
    ent_id: str, config: Config
) -> DataFrame[EfoDf]:
    root_id = "http://www.ebi.ac.uk/efo/EFO_0000001"
    query = """
    MATCH
        (root:Efo {{_id: "{root_id}"}}),
        (ref:Efo {{_id: "{ent_id}"}}),
        p = shortestPath((root)-[:EFO_CHILD_OF*]->(ref))
    WITH p
    WHERE length(p) > 1
    RETURN p
    """.format(
        root_id=root_id, ent_id=ent_id
    )
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    r = requests.post(url, json={"query": query})
    r.raise_for_status()
    results = r.json()["results"]
    if len(results) == 0:
        empty_df = EfoDf.example(size=1).iloc[:0, :].copy()
        return empty_df
    else:
        raw_nodes = results[0]["p"]["_nodes"]
        nodes = [
            {
                "ent_id": raw_nodes[idx]["_id"],
                "ent_term": raw_nodes[idx]["_name"],
                "ref_ent_id": raw_nodes[(idx + 1)]["_id"],
            }
            for idx in range(len(raw_nodes) - 1)
        ]
        nodes_df = pd.DataFrame(nodes).assign(
            ent_type="ontology_ancestor",
            ent_url=lambda df: df["ent_id"].apply(
                lambda ent_id: ENT_URL_TEMPLATE.format(
                    meta_ent="Efo", ent_id=ent_id
                )
            ),
        )
        ic_df = efo_ic_scores(
            ent_ids=nodes_df["ent_id"].tolist(),
            config=config,
            ic_score_threshold=None,
        )
        nodes_df = nodes_df.merge(ic_df[["ent_id", "ic_score"]], on="ent_id")
        return nodes_df


def _make_similarity_scores(efo_df: pd.DataFrame, query_ents: List[BaseEnt]):
    def _get_sim_score(term1: str, term2: str) -> float:
        url = config.neural_models_url + "/nlp/similarity"
        params: Dict[str, Union[str, bool]] = {
            "text1": term1,
            "text2": term2,
            "asis": False,
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        res = r.json()
        return res

    efo_ents = (
        py_.chain(
            [
                [
                    {"ent_id": __["ent_id"], "ent_term": __["ent_term"]}
                    for __ in _["efo_data"]
                ]
                for idx, _ in efo_df.iterrows()
            ]
        )
        .flatten()
        .uniq_by(lambda item: item["ent_id"])
        .value()
    )
    sim_scores = (
        py_.chain(
            [
                [
                    {
                        "source_ent_id": source["ent_id"],
                        "source_ent_term": source["ent_term"],
                        "target_ent_id": target["ent_id"],
                        "target_ent_term": target["ent_term"],
                        "similarity_score": _get_sim_score(
                            term1=source["ent_term"], term2=target["ent_term"]
                        ),
                    }
                    for target in query_ents
                ]
                for source in efo_ents
            ]
        )
        .flatten()
        .value()
    )
    return sim_scores


def _make_similarity_score_subset(
    similarity_scores: List[SimilarityScoreItem],
    efo_data: List[EfoDataResDataItem],
) -> List[SimilarityScoreItem]:
    efo_ids = set([_["ent_id"] for _ in efo_data])
    sim_source_efo_ids = set([_["source_ent_id"] for _ in similarity_scores])
    subset_efo_ids = list(efo_ids.intersection(sim_source_efo_ids))
    subset_scores = [
        _ for _ in similarity_scores if _["source_ent_id"] in subset_efo_ids
    ]
    return subset_scores
