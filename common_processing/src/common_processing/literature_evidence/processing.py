from typing import List, Optional

import pandas as pd
import pandera as pa
import requests
from loguru import logger
from pandera.engines.numpy_engine import Object
from pandera.typing import DataFrame, Series

from ..types import Config, literature_types


class _LiteratureInfoQueryDf(pa.SchemaModel):
    literature_issn: Optional[Series[str]] = pa.Field(
        alias="literature.issn", nullable=True,
    )
    literature__name: Series[str] = pa.Field(alias="literature._name")
    literature_year: Optional[Series[int]] = pa.Field(
        alias="literature.year", nullable=True, coerce=True
    )
    # NOTE: actual dtype is List[str]
    literature__source: Series[Object] = pa.Field(alias="literature._source")
    literature_id: Series[str] = pa.Field(alias="literature.id")
    literature__id: Series[str] = pa.Field(alias="literature._id")
    literature_dp: Optional[Series[str]] = pa.Field(
        alias="literature.dp", nullable=True,
    )
    literature_edat: Optional[Series[str]] = pa.Field(
        alias="literature.edat", nullable=True,
    )


class _LiteratureInfoDf(_LiteratureInfoQueryDf):
    triple_id: Series[str]
    triple_lower: Series[str]


class _PubmedDf(pa.SchemaModel):
    pubmed_id: Series[str]
    triple_id: Series[str]
    triple_lower: Series[str]


class _SentenceQueryDf(pa.SchemaModel):
    PREDICATION_ID: Series[int]
    SENTENCE_ID: Series[int]
    PMID: Series[int]
    PREDICATE: Series[str]
    SUBJECT_CUI: Series[str]
    SUBJECT_NAME: Series[str]
    SUBJECT_SEMTYPE: Series[str]
    OBJECT_CUI: Series[str]
    OBJECT_NAME: Series[str]
    OBJECT_SEMTYPE: Series[str]
    SUB_PRED_OBJ: Series[str]
    TYPE: Series[str]
    NUMBER: Series[int]
    SENT_START_INDEX: Series[int]
    SENTENCE: Series[str]
    SENT_END_INDEX: Series[int]
    ISSN: Series[str]
    DP: Series[str]
    EDAT: Series[str]
    PYEAR: Series[int]


class _SentenceDf(_SentenceQueryDf):
    pass


class _FulltextQueryDf(pa.SchemaModel):
    doi: Series[str]
    title: Series[str]
    timestamp: Series[str]
    abstract: Series[str]
    year: Series[int]
    pmid: Series[str]
    type: Series[str]


class _FulltextDf(_FulltextQueryDf):
    pass


@pa.check_types
def get_literature_info_df(
    triple_items: List[literature_types.TripleItem], config: Config,
) -> DataFrame[_LiteratureInfoDf]:
    @pa.check_types
    def _query(triple_id: str,) -> DataFrame[_LiteratureInfoQueryDf]:
        # NOTE: currently limited to SEMMEDDB
        # MAYBE: drop hard coded literature limit
        query_template = """
        MATCH (triple:LiteratureTriple)-[r:SEMMEDDB_TO_LIT]->(literature:Literature)
        WHERE triple._id = "{id}"
        RETURN
            literature
        LIMIT 20
        """
        query = query_template.format(id=triple_id)
        url = "{url}/cypher".format(url=config.epigraphdb_api_url)
        r = requests.post(url, json={"query": query})
        r.raise_for_status()
        results = r.json()["results"]
        if len(results) == 0:
            logger.debug(f"empty df, {triple_id=}")
            empty_df = (
                _LiteratureInfoQueryDf.example(size=1).iloc[:0, :].copy()
            )
            return empty_df
        query_df = pd.json_normalize(results)
        return query_df

    literature_info_df = pd.concat(
        [
            _query(triple_id=_["triple_id"]).assign(
                triple_id=_["triple_id"],
                triple_lower=_["triple_label"].lower(),
            )
            for _ in triple_items
        ]
    ).reset_index(drop=True)
    logger.info(f"{len(literature_info_df)=}")
    logger.info(f"{literature_info_df.groupby('triple_lower').size()=}")
    return literature_info_df


@pa.check_types
def make_pubmed_df(
    literature_df: DataFrame[_LiteratureInfoDf],
    num_items_per_triple: Optional[int],
) -> DataFrame[_PubmedDf]:
    """This is a lite version of literature_df,
    which is used to connect with sentence_df and fulltext_df
    """
    if num_items_per_triple is not None:
        pubmed_df = (
            literature_df.groupby("triple_id")
            .head(num_items_per_triple)
            .reset_index(drop=True)[
                ["literature._id", "triple_id", "triple_lower"]
            ]
            .rename(columns={"literature._id": "pubmed_id"})
        )
    else:
        pubmed_df = literature_df[
            ["literature._id", "triple_id", "triple_lower"]
        ].rename(columns={"literature._id": "pubmed_id"})
    return pubmed_df


@pa.check_types
def get_sentence_df(
    pubmed_df: DataFrame[_PubmedDf], config: Config
) -> DataFrame[_SentenceDf]:
    @pa.check_types
    def _query(lit_id: str, triple_lower: str) -> DataFrame[_SentenceQueryDf]:
        url = "{url}/sentence/".format(url=config.melodi_presto_api_url)
        r = requests.post(url, json={"pmid": str(lit_id)})
        r.raise_for_status()
        results = r.json()["data"]
        df = pd.json_normalize(results)
        if len(results) == 0:
            logger.debug(f"empty df {lit_id=} {triple_lower=}")
            empty_df = _SentenceQueryDf.example(size=1).iloc[:0, :].copy()
            return empty_df
        else:
            df = df[
                df["SUB_PRED_OBJ"].apply(lambda x: x.lower() == triple_lower)
            ]
            return df

    sentence_df = pd.concat(
        [
            _query(lit_id=_["pubmed_id"], triple_lower=_["triple_lower"])
            for _ in pubmed_df.to_dict(orient="records")
        ]
    ).reset_index(drop=True)
    return sentence_df


@pa.check_types
def get_fulltext_df(
    sentence_df: DataFrame[_SentenceDf], config: Config,
) -> DataFrame[_FulltextDf]:
    def _query(lit_id_list: List[str],) -> DataFrame[_FulltextQueryDf]:
        url = "{url}/pubmed/".format(url=config.text_base_api_url)
        data = {"pmids": lit_id_list, "type": "text"}
        r = requests.post(url, json=data)
        r.raise_for_status()
        results = r.json()
        if len(results) == 0:
            logger.debug(f"empty df, {lit_id_list=}")
            empty_df = _FulltextQueryDf.example(size=1).iloc[:0, :].copy()
            return empty_df
        df = pd.json_normalize(results)
        return df

    lit_id_list = sentence_df["PMID"].astype(str).tolist()
    fulltext_df = _query(lit_id_list=lit_id_list)
    return fulltext_df


@pa.check_types
def make_literature_evidence_df(
    pubmed_df: DataFrame[_PubmedDf],
    sentence_df: DataFrame[_SentenceDf],
    fulltext_df: DataFrame[_FulltextDf],
) -> DataFrame[literature_types.LiteratureEvidenceDf]:
    df = (
        pubmed_df.assign(pubmed_id=lambda df: df["pubmed_id"].astype(str))
        .merge(
            sentence_df[["PMID", "SENTENCE"]]
            .rename(columns={"PMID": "pubmed_id", "SENTENCE": "sentence"})
            .assign(pubmed_id=lambda df: df["pubmed_id"].astype(str)),
            how="inner",
            left_on="pubmed_id",
            right_on="pubmed_id",
        )
        .merge(
            fulltext_df[["title", "doi", "year", "pmid", "type", "abstract"]]
            .rename(columns={"pmid": "pubmed_id"})
            .assign(pubmed_id=lambda df: df["pubmed_id"].astype(str)),
            how="inner",
            left_on="pubmed_id",
            right_on="pubmed_id",
        )
    )
    return df
