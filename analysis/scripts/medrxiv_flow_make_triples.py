import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
from common_processing.claim_parsing import processing
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs.generic import interval_str

from icecream import ic  # noqa
from loguru import logger  # noqa

DATA_ROOT = utils.find_data_root()
ECHO_STEP = 10


def make_triple_dict(
    idx: int,
    total: int,
    doi: str,
    doc_name: str,
    abstracts_semrep_output_dir: Path,
) -> Dict[str, Any]:
    logger.info(f"#{idx} / {total}, {doi=}")
    empty = True
    success = False
    triples = []
    invalid_triples = []

    results_file = abstracts_semrep_output_dir / doc_name
    if results_file.exists():
        with results_file.open("r") as f:
            semrep_raw_results = f.read().split("\n")
        if len(semrep_raw_results) >= 0:
            success = True
            triple_df_pre_filter = processing.get_triple_df(semrep_raw_results)
            if len(triple_df_pre_filter) > 0:
                triple_df = (
                    processing.filter_preds(triple_df_pre_filter)
                    .reset_index(drop=True)
                    .reset_index(drop=False)
                    .rename(columns={"index": "idx"})
                )
                triples = triple_df.to_dict(orient="records")
                invalid_triple_df = (
                    triple_df_pre_filter[
                        ~triple_df_pre_filter["triple_text"].isin(
                            triple_df["triple_text"]
                        )
                    ]
                    .reset_index(drop=True)
                    .reset_index(drop=False)
                    .rename(columns={"index": "idx"})
                )
                invalid_triples = invalid_triple_df.to_dict(orient="records")
                empty = len(triples) == 0
    else:
        logger.warning(f"{results_file} not exist")

    res = {
        "doi": doi,
        # triples able to proceed to next analysis steps
        "triples": triples,
        # triples without further processing
        "invalid_triples": invalid_triples,
        # semrep able to parse document
        "success": success,
        # len(triples) == 0
        "empty": empty,
    }
    return res


class MakeTripleFlow(FlowSpec):

    INTERVAL = Parameter(
        "interval",
        help="period interval",
        default="2020-10-01/2020-10-31",
    )
    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        is_flag=True,
    )

    @step
    def start(self):
        "Init"
        self.interval_str = interval_str(self.INTERVAL)
        self.data_dir = DATA_ROOT / "medrxiv_experiments" / self.interval_str

        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.OVERWRITE=}
        {self.data_dir=}
        """
        )
        self.next(self.setup)

    @step
    def setup(self):
        self.next(self.make_triples)

    @step
    def make_triples(self):
        self.triple_file = self.data_dir / "triples.json"

        if self.OVERWRITE or not self.triple_file.exists():
            abstracts_dir = self.data_dir / "abstracts"
            abstracts_semrep_output_dir = abstracts_dir / "output"
            assert abstracts_dir.exists()
            assert abstracts_semrep_output_dir.exists()

            info_file = abstracts_dir / "info.csv"
            logger.info(f"Read {info_file=}")
            info_dict = pd.read_csv(info_file).to_dict(orient="records")

            self.triples = [
                make_triple_dict(
                    idx=idx,
                    total=len(info_dict),
                    doi=_["doi"],
                    doc_name=_["doc_name"],
                    abstracts_semrep_output_dir=abstracts_semrep_output_dir,
                )
                for idx, _ in enumerate(info_dict)
            ]

            logger.info("Make triples done.")
            with self.triple_file.open("w") as f:
                json.dump(self.triples, f)

        else:
            with self.triple_file.open("r") as f:
                self.triples = json.load(f)
        self.next(self.summary)

    @step
    def summary(self):
        num_success = pd.Series([_["success"] for _ in self.triples]).sum()
        success_rate = num_success / len(self.triples)
        num_empty = pd.Series(
            [_["empty"] for _ in self.triples if _["empty"] is not None]
        ).sum()
        empty_rate = num_empty / len(self.triples)
        logger.info(f"{num_success=}, {success_rate=}")
        logger.info(f"{num_empty=}, {empty_rate=}")
        self.next(self.end)

    @step
    def end(self):
        "Done."


if __name__ == "__main__":
    MakeTripleFlow()
