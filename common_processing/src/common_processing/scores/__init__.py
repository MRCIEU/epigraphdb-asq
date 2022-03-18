from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from . import types


@pa.check_types
def make_assoc_scores(
    assoc_evidence: DataFrame[types.AssocEvidenceDf],
    query_subject_term: str,
    query_object_term: str,
    ontology_subject_mapping: DataFrame[types.OntologyMappingDf],
    ontology_object_mapping: DataFrame[types.OntologyMappingDf],
    trait_subject_mapping: DataFrame[types.TraitMappingDf],
    trait_object_mapping: DataFrame[types.TraitMappingDf],
) -> DataFrame[types.ScoredAssocEvidenceDf]:
    if len(assoc_evidence) == 0:
        empty_df = (
            types.ScoredAssocEvidenceDf.example(size=1).iloc[:0, :].copy()
        )
        return empty_df
    subject_mapping_df = _make_trait_mapping_df(
        query_term=query_subject_term,
        ontology_mapping_df=ontology_subject_mapping,
        trait_mapping_df=trait_subject_mapping,
    )
    object_mapping_df = _make_trait_mapping_df(
        query_term=query_object_term,
        ontology_mapping_df=ontology_object_mapping,
        trait_mapping_df=trait_object_mapping,
    )
    scored_assoc_evidence_df = (
        assoc_evidence.merge(
            subject_mapping_df.rename(
                columns={
                    "mapping_score": "subject_mapping_score",
                    "data": "subject_mapping_data",
                }
            ),
            left_on="subject_id",
            right_index=True,
        )
        .merge(
            object_mapping_df.rename(
                columns={
                    "mapping_score": "object_mapping_score",
                    "data": "object_mapping_data",
                }
            ),
            left_on="object_id",
            right_index=True,
        )
        .assign(
            mapping_score=lambda df: df.apply(
                lambda row: (
                    row["subject_mapping_score"] * row["object_mapping_score"]
                ),
                axis=1,
            ),
            assoc_score=lambda df: df.apply(
                lambda row: _make_assoc_score(
                    effect_size=row["effect_size"], se=row["se"]
                ),
                axis=1,
            ),
            mapping_data=lambda df: df.apply(
                lambda row: {
                    "subject_mapping_score": row["subject_mapping_score"],
                    "object_mapping_score": row["object_mapping_score"],
                    "subject_mapping_data": row["subject_mapping_data"],
                    "object_mapping_data": row["object_mapping_data"],
                },
                axis=1,
            ),
        )
        .dropna()
        .drop(
            columns=[
                "subject_mapping_score",
                "object_mapping_score",
                "subject_mapping_data",
                "object_mapping_data",
            ]
        )
        .assign(
            evidence_score=lambda df: df.apply(
                lambda row: row["mapping_score"] * row["assoc_score"], axis=1
            )
        )
        .reset_index(drop=True)
    )
    return scored_assoc_evidence_df


@pa.check_types
def make_triple_scores(
    triple_evidence: DataFrame[types.TripleEvidenceDf],
    query_subject_term: str,
    query_object_term: str,
    ontology_subject_mapping: DataFrame[types.OntologyMappingDf],
    ontology_object_mapping: DataFrame[types.OntologyMappingDf],
    umls_subject_mapping: DataFrame[types.UmlsMappingDf],
    umls_object_mapping: DataFrame[types.UmlsMappingDf],
) -> DataFrame[types.ScoredTripleEvidenceDf]:
    if len(triple_evidence) == 0:
        empty_df = (
            types.ScoredTripleEvidenceDf.example(size=1).iloc[:0, :].copy()
        )
        return empty_df
    subject_mapping_df = _make_umls_mapping_df(
        query_term=query_subject_term,
        ontology_mapping_df=ontology_subject_mapping,
        umls_mapping_df=umls_subject_mapping,
    )
    object_mapping_df = _make_umls_mapping_df(
        query_term=query_object_term,
        ontology_mapping_df=ontology_object_mapping,
        umls_mapping_df=umls_object_mapping,
    )
    scored_triple_evidence_df = (
        triple_evidence.merge(
            subject_mapping_df.reset_index(drop=False).rename(
                columns={
                    "ent_id": "ent_subject_id",
                    "mapping_score": "subject_mapping_score",
                    "data": "subject_mapping_data",
                }
            ),
            on=["ent_subject_id"],
        )
        .merge(
            object_mapping_df.reset_index(drop=False).rename(
                columns={
                    "ent_id": "ent_object_id",
                    "mapping_score": "object_mapping_score",
                    "data": "object_mapping_data",
                }
            ),
            on=["ent_object_id"],
        )
        .assign(
            mapping_score=lambda df: df.apply(
                lambda row: (
                    row["subject_mapping_score"] * row["object_mapping_score"]
                ),
                axis=1,
            ),
            triple_score=lambda df: df.apply(
                lambda row: _make_triple_score(
                    literature_count=row["literature_count"]
                ),
                axis=1,
            ),
            mapping_data=lambda df: df.apply(
                lambda row: {
                    "subject_mapping_score": row["subject_mapping_score"],
                    "object_mapping_score": row["object_mapping_score"],
                    "subject_mapping_data": row["subject_mapping_data"],
                    "object_mapping_data": row["object_mapping_data"],
                },
                axis=1,
            ),
        )
        .drop(
            columns=[
                "subject_mapping_score",
                "object_mapping_score",
                "subject_mapping_data",
                "object_mapping_data",
            ]
        )
        .assign(
            evidence_score=lambda df: df.apply(
                lambda row: row["mapping_score"] * row["triple_score"], axis=1
            )
        )
        .reset_index(drop=True)
    )
    return scored_triple_evidence_df


@pa.check_types
def _make_trait_mapping_df(
    query_term: str,
    ontology_mapping_df: DataFrame[types.OntologyMappingDf],
    trait_mapping_df: DataFrame[types.TraitMappingDf],
) -> pd.DataFrame:
    mapping_df = (
        trait_mapping_df.merge(
            ontology_mapping_df[["ent_id", "similarity_score"]].rename(
                columns={
                    "ent_id": "ref_ent_id",
                    "similarity_score": "ref_similarity_score",
                }
            ),
            on=["ref_ent_id"],
        )
        .assign(
            query_term=query_term,
            mapping_score=lambda df: df.apply(
                lambda row: row["similarity_score"]
                * row["ref_similarity_score"],
                axis=1,
            ),
        )
        .assign(data=lambda df: df.apply(lambda row: row.to_dict(), axis=1))
        .groupby("ent_id")
        .agg({"mapping_score": "max", "data": lambda s: s.to_list()})
    )
    return mapping_df


@pa.check_types
def _make_umls_mapping_df(
    query_term: str,
    ontology_mapping_df: DataFrame[types.OntologyMappingDf],
    umls_mapping_df: DataFrame[types.UmlsMappingDf],
) -> pd.DataFrame:
    mapping_df = (
        umls_mapping_df.merge(
            ontology_mapping_df[["ent_id", "similarity_score"]].rename(
                columns={
                    "ent_id": "ref_ent_id",
                    "similarity_score": "ref_similarity_score",
                }
            ),
            how="left",
            on=["ref_ent_id"],
        )
        .replace({np.nan: 1})
        .assign(
            query_term=query_term,
            mapping_score=lambda df: df.apply(
                lambda row: row["similarity_score"]
                * row["ref_similarity_score"],
                axis=1,
            ),
        )
        .assign(data=lambda df: df.apply(lambda row: row.to_dict(), axis=1))
        .groupby("ent_id")
        .agg({"mapping_score": "max", "data": lambda s: s.to_list()})
    )
    return mapping_df


def _make_assoc_score(effect_size: float, se: float) -> Optional[float]:
    if np.isclose(se, 0):
        return None
    if np.isclose(effect_size / se, 0):
        return None
    res = max(0, 1 + np.log10(np.abs(effect_size / se)))
    return res


def _make_triple_score(literature_count: int) -> float:
    return max(0, 1 + np.log10(literature_count))
