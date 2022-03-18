from typing import List, Optional

import pandas as pd
import pandera as pa
import requests
from common_processing.literature_evidence.processing import (
    get_literature_info_df,
    make_pubmed_df,
)
from common_processing.types import Config, literature_types, triples_types
from pandera.typing import DataFrame


@pa.check_types
def get_triples(
    subject_ids: List[str],
    object_ids: List[str],
    umls_pred: str,
    direction: str,
    config: Config,
) -> Optional[DataFrame[triples_types.TripleEvidenceDf]]:
    triple_query_df = _query_ids(
        subject_ids=subject_ids,
        object_ids=object_ids,
        umls_pred=umls_pred,
        config=config,
    )
    if triple_query_df is None or len(triple_query_df) == 0:
        return None
    assert triple_query_df is not None  # mypy
    triple_df: pd.DataFrame = triple_query_df
    triple_df = triple_df.assign(
        triple_subject=lambda df: df.apply(
            lambda row: _split_triple_term_lower(
                triple=row["triple._name"],
                predicate=row["triple.predicate"],
                term="subject",
            ),
            axis=1,
        ),
        triple_object=lambda df: df.apply(
            lambda row: _split_triple_term_lower(
                triple=row["triple._name"],
                predicate=row["triple.predicate"],
                term="object",
            ),
            axis=1,
        ),
        triple_lower=lambda df: df.apply(
            lambda row: "{subject}:{pred}:{object}".format(
                subject=row["triple_subject"].lower(),
                pred=row["triple.predicate"].lower(),
                object=row["triple_object"].lower(),
            ),
            axis=1,
        ),
    ).rename(
        columns={
            "triple._id": "triple_id",
            "triple.subject_id": "triple_subject_id",
            "triple.object_id": "triple_object_id",
            "triple.predicate": "triple_predicate",
            "triple._name": "triple_label",
        }
    )[
        [
            "triple_id",
            "triple_label",
            "triple_lower",
            "triple_subject_id",
            "triple_subject",
            "triple_object_id",
            "triple_object",
            "triple_predicate",
        ]
    ]
    if direction == "forward":
        triple_df = triple_df.assign(
            ent_subject_id=lambda df: df["triple_subject_id"],
            ent_subject_term=lambda df: df["triple_subject"],
            ent_object_id=lambda df: df["triple_object_id"],
            ent_object_term=lambda df: df["triple_object"],
            direction="forward",
        )
    else:
        triple_df = triple_df.assign(
            ent_subject_id=lambda df: df["triple_object_id"],
            ent_subject_term=lambda df: df["triple_object"],
            ent_object_id=lambda df: df["triple_subject_id"],
            ent_object_term=lambda df: df["triple_subject"],
            direction="backward",
        )
    triple_items = (
        triple_df[["triple_id", "triple_lower"]]
        .rename(columns={"triple_lower": "triple_label"})
        .to_dict(orient="records")
    )
    literature_count_df = _make_literature_count_df(
        triple_items=triple_items, config=config
    )
    triple_df = triple_df.merge(literature_count_df, on=["triple_id"])
    return triple_df


def _make_literature_count_df(
    triple_items: List[literature_types.TripleItem], config: Config
) -> pd.DataFrame:
    literature_info_df = get_literature_info_df(
        triple_items=triple_items, config=config
    )
    pubmed_df = make_pubmed_df(
        literature_df=literature_info_df, num_items_per_triple=None
    )
    if len(pubmed_df) == 0:
        empty_df = pd.DataFrame(
            [
                {"triple_id": _["triple_id"], "literature_count": 0}
                for _ in triple_items
            ]
        )
        return empty_df
    res_df = (
        pubmed_df.groupby("triple_id")
        .size()
        .to_frame(name="literature_count")
        .reset_index(drop=False)
    )
    return res_df


@pa.check_types
def _query_ids(
    subject_ids: List[str],
    object_ids: List[str],
    umls_pred: str,
    config: Config,
) -> Optional[DataFrame[triples_types.TripleQueryDf]]:
    query = """
    MATCH (triple:LiteratureTriple)
    WHERE triple.subject_id IN {subject_ids}
    AND triple.object_id IN {object_ids}
    AND triple.predicate = "{pred}"
    RETURN triple
    """.format(
        subject_ids=str(subject_ids),
        object_ids=str(object_ids),
        pred=umls_pred,
    )

    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    params = {"query": query}
    r = requests.post(url, json=params)
    r.raise_for_status()
    query_df = pd.json_normalize(r.json()["results"])
    if len(query_df) == 0:
        return None
    return query_df


def _split_triple_term_lower(triple: str, predicate: str, term: str) -> str:
    if term == "subject":
        res = triple.split(predicate)[0].strip()
    elif term == "object":
        res = triple.split(predicate)[1].strip()
    return res
