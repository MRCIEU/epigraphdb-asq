import pandas as pd
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs import biorxiv_fetch

from icecream import ic  # noqa
from loguru import logger  # noqa


DATA_ROOT = utils.find_data_root()


class GetSample(FlowSpec):

    INTERVAL = Parameter(
        "interval",
        help="period interval",
        default="2020-10-01/2020-10-31",
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
        self.interval_str = biorxiv_fetch.interval_str(self.INTERVAL)
        self.data_dir = DATA_ROOT / "medrxiv_experiments" / self.interval_str
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.MAX_ITEMS_PER_PAGE = 100

        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.OVERWRITE=}
        """
        )
        self.next(self.fetch_interval_docs)

    @step
    def fetch_interval_docs(self):
        """
        Get a df of dois, given an INTERVAL
        """
        self.interval_docs_raw_file = (
            self.data_dir / "medrxiv_abstracts_raw.csv"
        )
        if self.OVERWRITE or not self.interval_docs_raw_file.exists():
            self.interval_docs_df = biorxiv_fetch.make_interval_docs_df(
                interval=self.INTERVAL,
                max_items_per_page=self.MAX_ITEMS_PER_PAGE,
                url_template=biorxiv_fetch.medrxiv_interval_template,
            )
            self.interval_docs_df.to_csv(
                self.interval_docs_raw_file, index=False
            )
        else:
            self.interval_docs_df = pd.read_csv(self.interval_docs_raw_file)
        print(self.interval_docs_df.info())
        print(self.interval_docs_df)
        self.next(self.process_interval_docs)

    @step
    def process_interval_docs(self):
        self.interval_docs_processed_file = (
            self.data_dir / "medrxiv_abstracts_processed.csv"
        )
        if self.OVERWRITE or not self.interval_docs_processed_file.exists():
            self.interval_docs_processed_df = (
                self.interval_docs_df.drop_duplicates(
                    subset=["doi"]
                ).reset_index(drop=True)
            )
            self.interval_docs_processed_df.to_csv(
                self.interval_docs_processed_file, index=False
            )
        else:
            self.interval_docs_processed_df = pd.read_csv(
                self.interval_docs_processed_df
            )
        print(self.interval_docs_processed_df.info())
        print(self.interval_docs_processed_df)
        self.next(self.end)

    @step
    def end(self):
        "Done."
        logger.info("Done.")


if __name__ == "__main__":
    GetSample()
