from pathlib import Path

import pandas as pd
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs import biorxiv_fetch
from analysis.funcs.generic import format_doi_str

from icecream import ic  # noqa
from loguru import logger  # noqa

DATA_ROOT = utils.find_data_root()
ECHO_STEP = 10


def format_abstract(abstract: str) -> str:
    # remove empty lines
    lines = abstract.split("\n")
    non_empty_lines = [_ for _ in lines if _.strip() != ""]
    formatted = "\n".join(non_empty_lines)
    return formatted


def write_abstract(
    idx: int, total: int, docs_dir: Path, doc_name: str, abstract: str
) -> None:
    output_file = docs_dir / doc_name
    formatted_abstract = format_abstract(abstract)
    if idx % ECHO_STEP == 0:
        logger.info(f"{idx} / {total} Write: {output_file}")
    with output_file.open("w") as f:
        f.write(formatted_abstract)


class MakeAbstractsFlow(FlowSpec):

    INTERVAL = Parameter(
        "interval",
        help="period interval",
        default="2020-10-01/2020-10-31",
    )

    @step
    def start(self):
        self.interval_str = biorxiv_fetch.interval_str(self.INTERVAL)
        self.data_dir = DATA_ROOT / "medrxiv_experiments" / self.interval_str
        self.abstracts_dir = self.data_dir / "abstracts"
        self.docs_dir = self.abstracts_dir / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.data_dir=}
        {self.docs_dir=}
        """
        )
        self.next(self.make_abstracts)

    @step
    def make_abstracts(self):
        abstract_file = self.data_dir / "medrxiv_abstracts_processed.csv"
        info_df_file = self.abstracts_dir / "info.csv"
        abstract_df = pd.read_csv(abstract_file).assign(
            doc_name=lambda df: df["doi"]
            .apply(format_doi_str)
            .apply(lambda x: f"{x}_doc.txt")
        )
        info_df = abstract_df[["doi", "doc_name"]]
        info_df.to_csv(info_df_file, index=False)
        items = abstract_df.to_dict(orient="records")
        for idx, item in enumerate(items):
            write_abstract(
                idx=idx,
                total=len(items),
                docs_dir=self.docs_dir,
                doc_name=item["doc_name"],
                abstract=item["abstract"],
            )
        self.next(self.end)

    @step
    def end(self):
        "Done."


if __name__ == "__main__":
    MakeAbstractsFlow()
