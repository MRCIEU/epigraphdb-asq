import json
from typing import Any, Dict

import ray
from loguru import logger
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs import biorxiv_fetch

DATA_ROOT = utils.find_data_root()


@ray.remote
def content_by_doi_verbose(idx: int, doi: str, total: int) -> Dict[str, Any]:
    STEP = 200
    if idx % STEP == 0:
        logger.info(f"{idx} / {total}")
    data = biorxiv_fetch.content_by_doi(doi=doi)
    res = {
        "doi": doi,
        "data": data,
    }
    return res


class GetSample(FlowSpec):
    """
    Get a sample of biorxiv dois with multiple updated versions
    over an interval
    """

    INTERVAL = Parameter(
        "interval",
        help="period interval",
        default="2020-08-01/2021-08-31",
    )
    NUM_WORKERS = Parameter(
        "num_workers",
        help="Number of cpu workers",
        default=8,
    )
    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        default=False,
    )

    @step
    def start(self):
        "Init"
        logger.info("Start.")
        self.data_dir = DATA_ROOT / "biorxiv_experiments"
        self.data_dir.mkdir(exist_ok=True)
        self.MAX_ITEMS_PER_PAGE = 100

        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.NUM_WORKERS=}
        {self.OVERWRITE=}
        """
        )
        ray.init(num_cpus=self.NUM_WORKERS)
        self.next(self.make_interval_docs)

    @step
    def make_interval_docs(self):
        """
        Get a df of dois
        """
        self.updated_docs_df = biorxiv_fetch.make_updated_docs_df(
            interval=self.INTERVAL, max_items_per_page=self.MAX_ITEMS_PER_PAGE
        )
        self.next(self.make_interval_metadata)

    @step
    def make_interval_metadata(self):
        """
        Get the metadata of those dois
        """
        self.doi_list = self.updated_docs_df["doi"].tolist()
        # NOTE: ray requires a list structure
        details_futures = [
            content_by_doi_verbose.remote(
                idx=idx, doi=doi, total=len(self.doi_list)
            )
            for idx, doi in enumerate(self.doi_list)
        ]
        # self.details = ray.get(details_futures)
        details_list = ray.get(details_futures)
        self.details = {_["doi"]: _["data"] for _ in details_list}
        self.next(self.end)

    @step
    def end(self):
        "Wrap up and write files."
        interval_file_str = biorxiv_fetch.interval_str(self.INTERVAL)

        self.interval_docs_file = (
            self.data_dir / f"interval_docs_{interval_file_str}.csv"
        )
        if not self.interval_docs_file.exists() or self.OVERWRITE:
            self.updated_docs_df.to_csv(self.interval_docs_file, index=False)

        self.details_file = self.data_dir / f"details_{interval_file_str}.json"
        if not self.details_file.exists() or self.OVERWRITE:
            with self.details_file.open("w") as f:
                json.dump(self.details, f)
        logger.info("Done.")


if __name__ == "__main__":
    GetSample()
