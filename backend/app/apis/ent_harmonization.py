from typing import List, Optional

from common_processing import ent_harmonization
from common_processing.resources.epigraphdb import (
    ENT_URL_TEMPLATE,
    META_ENT_URL_TEMPLATE,
)
from common_processing.types import ent_types
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


@router.post(
    "/ent_harmonization/ontology_ents",
    response_model=Optional[response_models.OntologyHarmonizationResponse],  # type: ignore
)
@cache(namespace="ent_harmonization_ontology_ents")
async def ontology_ents(
    data: request_models.ClaimEntRequest,
) -> Optional[types.OntologyResults]:
    ontology_ent_harmonizer = ent_harmonization.OntologyEntHarmonizer(
        config=config
    )
    harmonization_status = ontology_ent_harmonizer.harmonize(
        ent_id=data.ent_id,
        ent_term=data.ent_term,
        similarity_score_threshold=data.similarity_threshold,
        num_similarity_candidates=data.num_ent_candidates,
    )
    if not harmonization_status:
        return None
    candidates: List[types.AnnotatedOntologyEnt] = _annotate_efo(
        ontology_ent_harmonizer.candidates
    )
    ents: List[types.AnnotatedOntologyEnt] = _annotate_efo(
        ontology_ent_harmonizer.ents
    )
    res: types.OntologyResults = {"candidates": candidates, "ents": ents}
    return res


@router.post(
    "/ent_harmonization/trait_ents",
    response_model=Optional[response_models.PostOntologyEntResponse],  # type: ignore
)
@cache(namespace="ent_harmonization_trait_ents")
async def trait_ents(
    data: request_models.TraitEntRequest,
) -> Optional[types.PostOntologyEntResults]:
    ontology_ents = [_.dict() for _ in data.ents]
    phenotype_ent_harmonizer = ent_harmonization.PhenotypeEntHarmonizer(
        config=config
    )
    harmonization_status = phenotype_ent_harmonizer.harmonize(
        ontology_ents=ontology_ents,
        pred_term=data.pred_term,
        num_similarity_candidates=data.num_ent_candidates,
        similarity_score_threshold=data.similarity_threshold,
    )
    if not harmonization_status:
        return None
    ents: List[ent_types.BaseEnt] = phenotype_ent_harmonizer.ents
    ents_df = phenotype_ent_harmonizer.ents_df
    annotated_ents = [_annotate_ent(_, meta_ent="Gwas") for _ in ents]
    detail_data: List[types.DetailEntItem] = ents_df.assign(
        ent_url=lambda df: df["ent_id"].apply(
            lambda ent_id: _get_ent_url(ent_id=ent_id, meta_ent="Gwas")
        ),
        meta_ent_url=_get_meta_ent_url(meta_ent="Gwas"),
        ref_ent_url=lambda df: df["ref_ent_id"].apply(
            lambda ent_id: _get_ent_url(ent_id=ent_id, meta_ent="Efo")
        ),
        ref_meta_ent_url=_get_meta_ent_url(meta_ent="Efo"),
    ).to_dict(orient="records")
    res: types.PostOntologyEntResults = {
        "ents": annotated_ents,
        "detail_data": detail_data,
    }
    return res


@router.post(
    "/ent_harmonization/umls_ents",
    response_model=Optional[response_models.PostOntologyEntResponse],  # type: ignore
)
@cache(namespace="ent_harmonization_umls_ents")
async def umls_ents(
    data: request_models.UmlsEntRequest,
) -> Optional[types.PostOntologyEntResults]:
    query_umls_ent = data.query_umls_ent.dict()
    ontology_ents = [_.dict() for _ in data.ontology_ents]
    umls_ent_harmonizer = ent_harmonization.UmlsEntHarmonizer(config=config)
    harmonization_status = umls_ent_harmonizer.harmonize(
        umls_ent=query_umls_ent,
        ontology_ents=ontology_ents,
        num_similarity_candidates=data.num_similarity_candidates,
        similarity_score_threshold=data.similarity_score_threshold,
    )
    if not harmonization_status:
        return None
    ents: List[ent_types.BaseEnt] = umls_ent_harmonizer.ents
    ents_df = umls_ent_harmonizer.ents_df
    annotated_ents = [
        _annotate_ent(_, meta_ent="LiteratureTerm") for _ in ents
    ]
    detail_data: List[types.DetailEntItem] = ents_df.assign(
        ent_url=lambda df: df["ent_id"].apply(
            lambda ent_id: _get_ent_url(
                ent_id=ent_id, meta_ent="LiteratureTerm"
            )
        ),
        meta_ent_url=_get_meta_ent_url(meta_ent="LiteratureTerm"),
        ref_ent_url=lambda df: df.apply(
            lambda row: _get_ent_url(ent_id=row["ref_ent_id"], meta_ent="Efo")
            if row["ref_meta_ent"] == "Efo"
            else "",
            axis=1,
        ),
        ref_meta_ent_url=lambda df: df.apply(
            lambda row: _get_meta_ent_url(meta_ent="Efo")
            if row["ref_meta_ent"] == "Efo"
            else "",
            axis=1,
        ),
    ).to_dict(orient="records")
    res: types.PostOntologyEntResults = {
        "ents": annotated_ents,
        "detail_data": detail_data,
    }
    return res


def _annotate_efo(
    efo_ents: List[ent_types.OntologyEnt],
) -> List[types.AnnotatedOntologyEnt]:
    for _ in efo_ents:
        _["url"] = _get_ent_url(ent_id=_["ent_id"], meta_ent="Efo")
    return efo_ents


def _annotate_ent(
    ent: ent_types.BaseEnt, meta_ent: str
) -> types.AnnotatedBaseEnt:
    ent["url"] = _get_ent_url(ent_id=ent["ent_id"], meta_ent=meta_ent)
    return ent


def _get_ent_url(ent_id: str, meta_ent: str) -> Optional[str]:
    res = ENT_URL_TEMPLATE.format(meta_ent=meta_ent, ent_id=ent_id)
    return res


def _get_meta_ent_url(meta_ent: str) -> Optional[str]:
    res = META_ENT_URL_TEMPLATE.format(meta_ent=meta_ent)
    return res
