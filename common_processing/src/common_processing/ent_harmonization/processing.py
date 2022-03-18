import sqlite3
from typing import Any, Dict, List, Optional

import pandas as pd
import pandera as pa
import requests
from pandera.typing import DataFrame, Series

from ..funcs import ent_filters
from ..types import Config, ent_types


class QueryCandidateDf(pa.SchemaModel):
    id: Series[str]
    name: Series[str]
    text: Series[str]
    score: Series[float]
    meta_node: Series[str]


class SimilarityScoresDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    similarity_score: Series[float]


class IdentityScoresDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    identity_score: Series[float]


class IcScoresDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    ic_score: Series[float]


@pa.check_types
def efo_similarity_candidates(
    term: str, limit: int, similarity_score_threshold: float, config: Config
) -> Optional[DataFrame[SimilarityScoresDf]]:
    url = "{url}/query/text".format(url=config.epigraphdb_neural_url)
    params: Dict[str, Any] = {
        "text": term,
        "asis": False,
        "include_meta_nodes": ["Efo"],
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    query_df: DataFrame[QueryCandidateDf] = pd.DataFrame(r.json()["results"])
    if len(query_df) == 0:
        return None
    res: DataFrame[SimilarityScoresDf] = query_df.rename(
        columns={
            "id": "ent_id",
            "name": "ent_term",
            "score": "similarity_score",
        }
    ).query(f"similarity_score > {similarity_score_threshold}")
    if len(res) == 0:
        return None
    return res


@pa.check_types
def efo_ic_scores(
    ent_ids: List[str],
    config: Config,
    ic_score_threshold: Optional[float] = None,
) -> DataFrame[IcScoresDf]:
    db_path = config.data_path / "efo" / "epigraphdb_efo.db"
    ent_ids_expr = str(ent_ids).replace("[", "(").replace("]", ")")
    query = f"""
    SELECT efo_term, efo_id, ic_score FROM IC
    WHERE efo_id IN {ent_ids_expr}
    """
    with sqlite3.connect(db_path) as conn:
        query_df = pd.read_sql(query, conn)

    df = query_df.rename(columns={"efo_id": "ent_id", "efo_term": "ent_term"})
    if ic_score_threshold is not None:
        df = df.query(f"ic_score > {ic_score_threshold}")
    return df


@pa.check_types
def efo_identity_scores(
    reference_term: str, ents: List[ent_types.BaseEnt], config: Config,
) -> DataFrame[IdentityScoresDf]:
    target_terms = [_["ent_term"] for _ in ents]
    text_pairs = {
        "text_1": [reference_term for _ in target_terms],
        "text_2": [_ for _ in target_terms],
    }
    url = "{url}/inference".format(url=config.neural_transformers_url)
    r = requests.post(
        url,
        json={"text_1": text_pairs["text_1"], "text_2": text_pairs["text_2"]},
    )
    r.raise_for_status()
    scores = r.json()
    res = pd.DataFrame(ents).assign(identity_score=scores)
    return res


@pa.check_types
def gwas_similarity_candidates(
    ent_id: str, limit: int, similarity_score_threshold: float, config: Config
) -> Optional[DataFrame[SimilarityScoresDf]]:
    url = "{url}/query/entity".format(url=config.epigraphdb_neural_url)
    params: Dict[str, Any] = {
        "entity_id": ent_id,
        "meta_node": "Efo",
        "include_meta_nodes": ["Gwas"],
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    query_df: DataFrame[QueryCandidateDf] = pd.DataFrame(r.json()["results"])
    if len(query_df) == 0:
        return None
    res: DataFrame[SimilarityScoresDf] = query_df.rename(
        columns={
            "id": "ent_id",
            "name": "ent_term",
            "score": "similarity_score",
        }
    ).query(f"similarity_score > {similarity_score_threshold}")
    if len(res) == 0:
        return None
    return res


@pa.check_types
def umls_similarity_candidates_on_efo(
    ent_id: str, limit: int, similarity_score_threshold: float, config: Config
) -> Optional[DataFrame[SimilarityScoresDf]]:
    url = "{url}/query/entity".format(url=config.epigraphdb_neural_url)
    params: Dict[str, Any] = {
        "entity_id": ent_id,
        "meta_node": "Efo",
        "include_meta_nodes": ["Literatureterm"],
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    query_df: DataFrame[QueryCandidateDf] = pd.DataFrame(r.json()["results"])
    if len(query_df) == 0:
        return None
    res: DataFrame[SimilarityScoresDf] = query_df.rename(
        columns={
            "id": "ent_id",
            "name": "ent_term",
            "score": "similarity_score",
        }
    ).query(f"similarity_score > {similarity_score_threshold}")
    if len(res) == 0:
        return None
    return res


@pa.check_types
def umls_similarity_candidates_on_umls(
    umls_term: str,
    limit: int,
    similarity_score_threshold: float,
    config: Config,
) -> Optional[DataFrame[SimilarityScoresDf]]:
    url = "{url}/query/text".format(url=config.epigraphdb_neural_url)
    params: Dict[str, Any] = {
        "text": umls_term,
        "include_meta_nodes": ["Literatureterm"],
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    query_df: DataFrame[QueryCandidateDf] = pd.DataFrame(r.json()["results"])
    if len(query_df) == 0:
        return None
    res: DataFrame[SimilarityScoresDf] = query_df.rename(
        columns={
            "id": "ent_id",
            "name": "ent_term",
            "score": "similarity_score",
        }
    ).query(f"similarity_score > {similarity_score_threshold}")
    if len(res) == 0:
        return None
    return res


def traits_filter_ents_by_predicates(
    ents: List[ent_types.BaseEnt],
    funcs: List[ent_types.FilterFunc] = [ent_filters.prefix_filter],
) -> List[ent_types.BaseEnt]:
    ent_id_list = [_["ent_id"] for _ in ents]
    composed_func = ent_filters.compose(funcs)
    filtered_ent_id_list = composed_func(ent_id_list)
    filtered_ents = [_ for _ in ents if _["ent_id"] in filtered_ent_id_list]
    return filtered_ents
