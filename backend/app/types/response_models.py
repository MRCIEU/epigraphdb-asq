from typing import List

from pydantic import BaseModel, create_model_from_typeddict

from app import types

from .request_models import EntRequest

TripleDataResponse = create_model_from_typeddict(types.TripleData)  # type: ignore

OntologyEntResponseItem = create_model_from_typeddict(types.AnnotatedOntologyEnt)  # type: ignore

PhenotypeEntResponseItem = create_model_from_typeddict(types.AnnotatedPhenotypeEnt)  # type: ignore

PhenotypeEntResponse = List[PhenotypeEntResponseItem]  # type: ignore


# NOTE: do not use model conversion when it contains other typeddict...
class TraitCandidatesResponseItem(BaseModel):
    ontology_ent: EntRequest
    candidates: List[PhenotypeEntResponseItem]  # type: ignore


class OntologyHarmonizationResponse(BaseModel):
    candidates: List[OntologyEntResponseItem]  # type: ignore
    ents: List[OntologyEntResponseItem]  # type: ignore


class TraitHarmonizationResponse(BaseModel):
    grouped_candidates: List[TraitCandidatesResponseItem]  # type: ignore
    ents: List[PhenotypeEntResponseItem]  # type: ignore


TripleEvidenceResponseItem = create_model_from_typeddict(
    types.TripleEvidence  # type: ignore
)

TripleEvidenceResponse = List[TripleEvidenceResponseItem]  # type: ignore


LiteratureEvidenceResponse = create_model_from_typeddict(
    types.LiteratureEvidence  # type: ignore
)

LiteratureLiteEvidenceResponse = create_model_from_typeddict(
    types.LiteratureLiteEvidence  # type: ignore
)

EfoIcResponseItem = create_model_from_typeddict(types.EfoIcItem)  # type: ignore

EfoIcResponse = List[EfoIcResponseItem]  # type: ignore

AssocEvidenceResponseDataItem = create_model_from_typeddict(
    types.AssocEvidenceDataItem  # type: ignore
)


class AssocEvidenceResponse(BaseModel):
    data: List[AssocEvidenceResponseDataItem]  # type: ignore


PostOntologyEntResponse = create_model_from_typeddict(
    types.PostOntologyEntResults  # type: ignore
)
