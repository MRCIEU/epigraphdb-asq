from typing import List

import pandas as pd
import pandera as pa
import requests
from loguru import logger
from pandera.typing import DataFrame, Series


class MedlineDf(pa.SchemaModel):
    doi: Series[str]
    title: Series[str]
    timestamp: Series[str]
    abstract: Series[str]
    year: Series[int]
    pmid: Series[str]
    type: Series[str]


def medline_query(lit_id_list: List[str], url: str) -> DataFrame[MedlineDf]:

    url = "{url}/pubmed/general-search".format(url=url)
    data = {"pmids": lit_id_list, "type": "text"}
    r = requests.post(url, json=data)
    r.raise_for_status()
    results = r.json()
    if len(results) == 0:
        logger.debug(f"empty df, {lit_id_list=}")
        empty_df = MedlineDf.example(size=1).iloc[:0, :].copy()
        return empty_df
    df = pd.json_normalize(results)
    return df
