import pandas as pd
from common_processing import scores
from common_processing.scores import types
from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/scores/assoc", response_model=types.AssocScoresResponse,
)
async def get_assoc_scores(data: types.AssocScoresRequests):
    assoc_evidence = pd.DataFrame([_.dict() for _ in data.assoc_evidence])
    query_subject_term = data.query_subject_term
    query_object_term = data.query_object_term
    ontology_subject_mapping = pd.DataFrame(
        [_.dict() for _ in data.ontology_subject_mapping]
    )
    ontology_object_mapping = pd.DataFrame(
        [_.dict() for _ in data.ontology_object_mapping]
    )
    trait_subject_mapping = pd.DataFrame(
        [_.dict() for _ in data.trait_subject_mapping]
    )
    trait_object_mapping = pd.DataFrame(
        [_.dict() for _ in data.trait_object_mapping]
    )
    res_df = scores.make_assoc_scores(
        assoc_evidence=assoc_evidence,
        query_subject_term=query_subject_term,
        query_object_term=query_object_term,
        ontology_subject_mapping=ontology_subject_mapping,
        ontology_object_mapping=ontology_object_mapping,
        trait_subject_mapping=trait_subject_mapping,
        trait_object_mapping=trait_object_mapping,
    )
    res = {"data": res_df.to_dict(orient="records")}
    return res


@router.post(
    "/scores/triples", response_model=types.TripleScoresResponse,
)
async def get_triple_scores(data: types.TripleScoresRequests):
    triple_evidence = pd.DataFrame([_.dict() for _ in data.triple_evidence])
    query_subject_term = data.query_subject_term
    query_object_term = data.query_object_term
    ontology_subject_mapping = pd.DataFrame(
        [_.dict() for _ in data.ontology_subject_mapping]
    )
    ontology_object_mapping = pd.DataFrame(
        [_.dict() for _ in data.ontology_object_mapping]
    )
    umls_subject_mapping = pd.DataFrame(
        [_.dict() for _ in data.umls_subject_mapping]
    )
    umls_object_mapping = pd.DataFrame(
        [_.dict() for _ in data.umls_object_mapping]
    )
    res_df = scores.make_triple_scores(
        triple_evidence=triple_evidence,
        query_subject_term=query_subject_term,
        query_object_term=query_object_term,
        ontology_subject_mapping=ontology_subject_mapping,
        ontology_object_mapping=ontology_object_mapping,
        umls_subject_mapping=umls_subject_mapping,
        umls_object_mapping=umls_object_mapping,
    )
    res = {"data": res_df.to_dict(orient="records")}
    return res
