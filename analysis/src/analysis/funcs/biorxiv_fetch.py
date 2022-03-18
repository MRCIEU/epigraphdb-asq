import pandas as pd
import requests
from pydash import py_

from .utils import interval_str  # noqa

biorxiv_doi_details_template = (
    "https://api.biorxiv.org/details/biorxiv/{doi}/na/json"
)
biorxiv_interval_template = (
    "https://api.biorxiv.org/details/biorxiv/{interval}/{cursor}/json"
)
medrxiv_doi_details_template = (
    "https://api.biorxiv.org/details/medrxiv/{doi}/na/json"
)
medrxiv_interval_template = (
    "https://api.biorxiv.org/details/medrxiv/{interval}/{cursor}/json"
)


def make_updated_docs_df(
    interval: str, max_items_per_page: int
) -> pd.DataFrame:
    cursor = 0
    idx = 0
    interval_collections = []
    while True:
        print(f"{idx}")
        collection = content_by_interval(interval=interval, cursor=cursor)
        valid_collection = py_.compact([filter_items(_) for _ in collection])
        interval_collections.append(valid_collection)
        if len(collection) < max_items_per_page:
            break
        cursor += max_items_per_page
        idx += 1
    interval_updated_docs = py_(interval_collections).flatten().value()
    updated_docs_df = pd.DataFrame(interval_updated_docs).drop_duplicates()
    return updated_docs_df


def make_interval_docs_df(
    interval: str,
    max_items_per_page: int = 100,
    url_template: str = biorxiv_interval_template,
):
    cursor = 0
    idx = 0
    interval_collections = []
    while True:
        print(f"{idx}")
        collection = content_by_interval(
            interval=interval, cursor=cursor, url_template=url_template
        )
        interval_collections.append(collection)
        if len(collection) < max_items_per_page:
            break
        cursor += max_items_per_page
        idx += 1
    interval_updated_docs = py_(interval_collections).flatten().value()
    updated_docs_df = pd.DataFrame(interval_updated_docs).drop_duplicates()
    return updated_docs_df


def content_by_interval(
    interval: str,
    cursor: int = 0,
    url_template: str = biorxiv_interval_template,
):
    url = url_template.format(interval=interval, cursor=cursor)
    r = requests.get(url)
    r.raise_for_status()
    res = r.json()["collection"]
    return res


def filter_items(item):
    if int(item["version"]) == 1:
        return None
    else:
        res = {"doi": item["doi"]}
        return res


def content_by_doi(doi: str):
    url_template = "https://api.biorxiv.org/details/biorxiv/{doi}/na/json"
    url = url_template.format(doi=doi)
    r = requests.get(url)
    r.raise_for_status()
    res = r.json()["collection"]
    return res
