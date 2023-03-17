from functools import partial
from typing import Callable, Dict, List

import pandas as pd
import pandera as pa
import requests
from loguru import logger
from pandera.typing import DataFrame

from ..resources import epigraphdb
from ..types import Config, assoc_types


def get_evidence_results(
    subject_ids: List[str],
    object_ids: List[str],
    evidence_type: str,
    pred_term: str,
    pval_threshold: float,
    config: Config,
) -> DataFrame[assoc_types.AssocEvidenceDf]:
    pred_func_maps: Dict[str, Dict[str, Callable]] = {
        "directional": {
            "supporting": directional_supporting,
            "contradictory_directional_type1": directional_contradictory_type1,
            "contradictory_directional_type2": directional_contradictory_type2,
            "generic_directional": directional_generic,
        },
        "undirectional": {
            "supporting": undirectional_supporting,
            "contradictory_undirectional": undirectional_contradictory,
        },
    }
    if pred_term in ["CAUSES", "TREATS", "AFFECTS"]:
        pred_term_harmonized = "directional"
    else:
        pred_term_harmonized = "undirectional"
    evidence_func = partial(
        pred_func_maps[pred_term_harmonized][evidence_type],
        pval_threshold=pval_threshold,
        config=config,
    )
    result_df = evidence_func(
        subject_ids=subject_ids,
        object_ids=object_ids,
    )
    logger.info(f"{len(result_df)}")
    logger.info(f"{result_df.groupby('meta_rel').size()}")
    return result_df


@pa.check_types
def _query_cypher(
    query: str, config: Config
) -> DataFrame[assoc_types.AssocEvidenceQueryDf]:
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    data = {"query": query}
    r = requests.post(url, json=data)
    r.raise_for_status()
    results = r.json()["results"]
    if len(results) == 0:
        example_df = assoc_types.AssocEvidenceQueryDf.example(size=1)
        empty_df = example_df.iloc[:0, :].copy()
        return empty_df
    res = pd.DataFrame(results)
    return res


def _list_to_str(items: List[str]) -> str:
    res = ",".join([f"'{_}'" for _ in items])
    return res


def directional_supporting(
    subject_ids: List[str],
    object_ids: List[str],
    pval_threshold: float,
    config: Config,
    **kwargs,
):
    pval_clause_mreve = f"AND r.pval <= {pval_threshold}"
    mreve_query = epigraphdb.MR_EVE_MR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=pval_clause_mreve,
        arrow=">",
    )
    df = _query_cypher(query=mreve_query, config=config)
    result_df = df.rename(
        columns={
            "source_id": "subject_id",
            "source_term": "subject_term",
            "target_id": "object_id",
            "target_term": "object_term",
        }
    ).assign(direction="forward")
    return result_df


def directional_contradictory_type1(
    subject_ids: List[str],
    object_ids: List[str],
    pval_threshold: float,
    config: Config,
    **kwargs,
):
    pval_clause_mreve = f"AND r.pval <= {pval_threshold}"
    mreve_query = epigraphdb.MR_EVE_MR_TEMPLATE.format(
        source_id_list=_list_to_str(object_ids),
        target_id_list=_list_to_str(subject_ids),
        pval_clause=pval_clause_mreve,
        arrow=">",
    )
    df = _query_cypher(query=mreve_query, config=config)
    result_df = df.rename(
        columns={
            "source_id": "object_id",
            "source_term": "object_term",
            "target_id": "subject_id",
            "target_term": "subject_term",
        }
    ).assign(direction="reverse")
    return result_df


def directional_contradictory_type2(
    subject_ids: List[str],
    object_ids: List[str],
    pval_threshold: float,
    config: Config,
    **kwargs,
):
    pval_clause_mreve = f"AND r.pval > {pval_threshold}"
    mreve_query = epigraphdb.MR_EVE_MR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=pval_clause_mreve,
        arrow="",
    )
    df = _query_cypher(query=mreve_query, config=config)
    result_df = df.rename(
        columns={
            "source_id": "subject_id",
            "source_term": "subject_term",
            "target_id": "object_id",
            "target_term": "object_term",
        }
    ).assign(direction="forward")
    return result_df


def directional_generic(
    subject_ids: List[str],
    object_ids: List[str],
    config: Config,
    **kwargs,
):
    prs_query = epigraphdb.PRS_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause="",
    )
    prs_df = _query_cypher(query=prs_query, config=config)
    gen_cor_query = epigraphdb.GEN_COR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause="",
    )
    gen_cor_df = _query_cypher(query=gen_cor_query, config=config)
    df_list = [prs_df, gen_cor_df]
    result_df = (
        pd.concat(df_list)
        .rename(
            columns={
                "source_id": "subject_id",
                "source_term": "subject_term",
                "target_id": "object_id",
                "target_term": "object_term",
            }
        )
        .assign(direction="undirectional")
    )
    return result_df


def undirectional_supporting(
    subject_ids: List[str],
    object_ids: List[str],
    pval_threshold: float,
    config: Config,
    **kwargs,
):
    mreve_query = epigraphdb.MR_EVE_MR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.pval <= {pval_threshold}",
        arrow="",
    )
    mreve_df = _query_cypher(query=mreve_query, config=config)
    prs_query = epigraphdb.PRS_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.p <= {pval_threshold}",
    )
    prs_df = _query_cypher(query=prs_query, config=config)
    gen_cor_query = epigraphdb.GEN_COR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.p <= {pval_threshold}",
    )
    gen_cor_df = _query_cypher(query=gen_cor_query, config=config)
    df_list = [prs_df, gen_cor_df, mreve_df]
    result_df = (
        pd.concat(df_list)
        .rename(
            columns={
                "source_id": "subject_id",
                "source_term": "subject_term",
                "target_id": "object_id",
                "target_term": "object_term",
            }
        )
        .assign(direction="undirectional")
    )
    return result_df


def undirectional_contradictory(
    subject_ids: List[str],
    object_ids: List[str],
    pval_threshold: float,
    config: Config,
    **kwargs,
):
    mreve_query = epigraphdb.MR_EVE_MR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.pval > {pval_threshold}",
        arrow="",
    )
    mreve_df = _query_cypher(query=mreve_query, config=config)
    prs_query = epigraphdb.PRS_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.p > {pval_threshold}",
    )
    prs_df = _query_cypher(query=prs_query, config=config)
    gen_cor_query = epigraphdb.GEN_COR_TEMPLATE.format(
        source_id_list=_list_to_str(subject_ids),
        target_id_list=_list_to_str(object_ids),
        pval_clause=f"AND r.p > {pval_threshold}",
    )
    gen_cor_df = _query_cypher(query=gen_cor_query, config=config)
    df_list = [prs_df, gen_cor_df, mreve_df]
    result_df = (
        pd.concat(df_list)
        .rename(
            columns={
                "source_id": "subject_id",
                "source_term": "subject_term",
                "target_id": "object_id",
                "target_term": "object_term",
            }
        )
        .assign(direction="undirectional")
    )
    return result_df
