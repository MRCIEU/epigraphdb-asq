from pathlib import Path
from typing import Any, Callable, Dict, List

import ray
from bs4 import BeautifulSoup
from metaflow import Flow, FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs import biorxiv_fetch, biorxiv_scraping

from icecream import ic  # noqa
from loguru import logger  # noqa


DATA_ROOT = utils.find_data_root()
UPSTREAM_FLOW_NAME = "GetSample"
STEP = 8


def extract_details(item: List[Dict[str, Any]]) -> List[int]:
    versions = [int(_["version"]) for _ in item]
    return versions


def format_doi_str(doi: str) -> str:
    doi_str = doi.replace("/", "__")
    return doi_str


def get_version_html(
    doi: str, ver: int, html_dir: Path, overwrite: bool = False
) -> bool:
    doi_str = format_doi_str(doi=doi)
    output_dir = html_dir / doi_str
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"version_{ver:02}.html"
    if output_file.exists() and not overwrite:
        return True
    try:
        html_content = biorxiv_scraping.get_full_text(doi=doi, ver=ver)
        soup = BeautifulSoup(html_content, "html.parser")
        fulltext = biorxiv_scraping.find_fulltext(soup)
        if fulltext:
            with output_file.open("w") as f:
                f.write(fulltext)
    except:
        return False
    return True


def parse_doc(
    doi: str,
    html_doc_file: Path,
    text_dir: Path,
    discussion_dir: Path,
    abstract_dir: Path,
    overwrite: bool = False,
) -> bool:
    def _parse(
        html_doc: str,
        output_file: Path,
        parse_func: Callable,
        overwrite: bool = False,
    ) -> bool:
        if output_file.exists() and not overwrite:
            return True
        else:
            output_file.parent.mkdir(exist_ok=True, parents=True)
            try:
                text = parse_func(html_doc)
                assert text
                with output_file.open("w") as f:
                    f.write(text)
            except:
                return False
        return True

    doi_str = format_doi_str(doi=doi)
    base_name = html_doc_file.stem
    output_file_full = text_dir / doi_str / f"{base_name}.txt"
    output_file_discussion = discussion_dir / doi_str / f"{base_name}.txt"
    output_file_abstract = abstract_dir / doi_str / f"{base_name}.txt"
    with html_doc_file.open("r") as f:
        html_doc = f.read()
    full_res = _parse(
        html_doc=html_doc,
        output_file=output_file_full,
        parse_func=biorxiv_scraping.parse_to_text,
        overwrite=overwrite,
    )
    discussion_res = _parse(
        html_doc=html_doc,
        output_file=output_file_discussion,
        parse_func=biorxiv_scraping.find_discussion_text,
        overwrite=overwrite,
    )
    abstract_res = _parse(
        html_doc=html_doc,
        output_file=output_file_abstract,
        parse_func=biorxiv_scraping.find_abstract_text,
        overwrite=overwrite,
    )
    # NOTE: this is not very useful
    res_list = [full_res, discussion_res, abstract_res]
    res = sum(res_list) == len(res_list)
    return res


@ray.remote
def get_doi_docs(
    idx: int, total: int, doi: str, html_dir: Path, versions: List[int]
) -> Dict:
    if idx % STEP == 0:
        logger.info(f"{idx} / {total}: {doi=}")
    fetch_res = [
        get_version_html(doi=doi, ver=_, html_dir=html_dir) for _ in versions
    ]
    # assert every version gets fetched
    result = sum(fetch_res) == len(versions)
    res = {"doi": doi, "result": result}
    return res


@ray.remote
def parse_docs(
    idx: int,
    total: int,
    doi: str,
    html_dir: Path,
    text_dir: Path,
    discussion_dir: Path,
    abstract_dir: Path,
) -> Dict:
    if idx % STEP == 0:
        logger.info(f"{idx} / {total}: {doi=}")
    doi_str = format_doi_str(doi=doi)
    html_dir = html_dir / doi_str
    html_doc_files = [_ for _ in html_dir.iterdir() if _.suffix == ".html"]
    parsing_res = [
        parse_doc(
            doi=doi,
            html_doc_file=_,
            text_dir=text_dir,
            discussion_dir=discussion_dir,
            abstract_dir=abstract_dir,
        )
        for _ in html_doc_files
    ]
    result = sum(parsing_res) == len(parsing_res)
    res = {"doi": doi, "result": result}
    return res


class BiorxivScraping(FlowSpec):
    """
    Fetch and scrape biorxiv pages.
    """

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
        self.LIMIT = 1000
        logger.info(
            f"""Params
        {self.NUM_WORKERS=}
        {self.OVERWRITE=}
        """
        )
        self.next(self.setup)

    @step
    def setup(self):
        upstream_run = Flow(UPSTREAM_FLOW_NAME).latest_successful_run
        # dirs
        self.interval = upstream_run["end"].task.data.INTERVAL
        interval_file_str = biorxiv_fetch.interval_str(self.interval)
        self.output_html_dir = DATA_ROOT / interval_file_str / "html"
        self.output_text_dir = DATA_ROOT / interval_file_str / "fulltext"
        self.output_discussion_dir = (
            DATA_ROOT / interval_file_str / "discussion"
        )
        self.output_abstract_dir = DATA_ROOT / interval_file_str / "abstract"
        for _ in [
            self.output_html_dir,
            self.output_text_dir,
            self.output_discussion_dir,
            self.output_abstract_dir,
        ]:
            _.mkdir(parents=True, exist_ok=True)
        # upstream data
        details = upstream_run["end"].task.data.details
        doi_list = upstream_run["end"].task.data.doi_list
        full_doi_list = list(details.keys())
        self.details_simple = [
            {"doi": _, "versions": extract_details(details[_])}
            for _ in doi_list
            if _ in full_doi_list
        ]
        # rest of init
        ray.init(num_cpus=self.NUM_WORKERS)
        self.next(self.fetching)

    @step
    def fetching(self):
        html_fetch_futures = [
            get_doi_docs.remote(
                idx=idx,
                total=len(self.details_simple),
                doi=_["doi"],
                versions=_["versions"],
                html_dir=self.output_html_dir,
            )
            for idx, _ in enumerate(self.details_simple)
        ]
        self.html_fetch_res = ray.get(html_fetch_futures)
        ic(len(self.html_fetch_res))
        self.fetch_failed = [
            _["doi"] for _ in self.html_fetch_res if not _["result"]
        ]
        ic(self.fetch_failed)
        self.next(self.parsing)

    @step
    def parsing(self):
        parsing_futures = [
            parse_docs.remote(
                idx=idx,
                total=len(self.details_simple),
                doi=_["doi"],
                html_dir=self.output_html_dir,
                text_dir=self.output_text_dir,
                discussion_dir=self.output_discussion_dir,
                abstract_dir=self.output_abstract_dir,
            )
            for idx, _ in enumerate(self.details_simple)
        ]
        self.parsing_res = ray.get(parsing_futures)
        ic(len(self.parsing_res))
        self.parsing_failed = [
            _["doi"] for _ in self.parsing_res if not _["result"]
        ]
        ic(self.parsing_failed)
        self.next(self.end)

    @step
    def end(self):
        "Finish"
        logger.info("Done.")


if __name__ == "__main__":
    BiorxivScraping()
