from typing import Any, Dict, List

import pandera as pa
from pandera.engines.numpy_engine import Object
from pandera.typing import Series
from pydantic import BaseModel


class AssocEvidenceDf(pa.SchemaModel):
    idx: Series[int]
    subject_id: Series[str]
    subject_term: Series[str]
    object_id: Series[str]
    object_term: Series[str]
    effect_size: Series[float]
    se: Series[float]
    pval: Series[float]


class TripleEvidenceDf(pa.SchemaModel):
    idx: Series[int]
    ent_subject_id: Series[str]
    ent_subject_term: Series[str]
    ent_object_id: Series[str]
    ent_object_term: Series[str]
    literature_count: Series[int]


class ScoredAssocEvidenceDf(AssocEvidenceDf):
    mapping_score: Series[float]
    assoc_score: Series[float]
    evidence_score: Series[float]
    mapping_data: Series[Object]


class ScoredTripleEvidenceDf(TripleEvidenceDf):
    mapping_score: Series[float]
    triple_score: Series[float]
    evidence_score: Series[float]
    mapping_data: Series[Object]


class OntologyMappingDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    similarity_score: Series[float] = pa.Field(coerce=True)
    identity_score: Series[float] = pa.Field(coerce=True)
    ic_score: Series[float] = pa.Field(coerce=True)


class TraitMappingDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    ref_ent_id: Series[str]
    ref_ent_term: Series[str]
    similarity_score: Series[float] = pa.Field(coerce=True)


class UmlsMappingDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    ref_ent_id: Series[str]
    ref_ent_term: Series[str]
    ref_meta_ent: Series[str]
    similarity_score: Series[float] = pa.Field(coerce=True)


class AssocEvidenceItem(BaseModel):
    idx: int
    subject_id: str
    subject_term: str
    object_id: str
    object_term: str
    effect_size: float
    se: float
    pval: float


class ScoredAssocEvidenceItem(AssocEvidenceItem):
    mapping_score: float
    assoc_score: float
    evidence_score: float
    mapping_data: Dict[str, Any]


class TripleEvidenceItem(BaseModel):
    idx: int
    ent_subject_id: str
    ent_subject_term: str
    ent_object_id: str
    ent_object_term: str
    literature_count: int


class ScoredTripleEvidenceItem(TripleEvidenceItem):
    mapping_score: float
    triple_score: float
    evidence_score: float
    mapping_data: Dict[str, Any]


class OntologyMappingItem(BaseModel):
    ent_id: str
    ent_term: str
    similarity_score: float
    identity_score: float
    ic_score: float


class TraitMappingItem(BaseModel):
    ent_id: str
    ent_term: str
    ref_ent_id: str
    ref_ent_term: str
    similarity_score: float


class UmlsMappingItem(BaseModel):
    ent_id: str
    ent_term: str
    ref_ent_id: str
    ref_ent_term: str
    ref_meta_ent: str
    similarity_score: float


class AssocScoresRequests(BaseModel):
    assoc_evidence: List[AssocEvidenceItem]
    query_subject_term: str
    query_object_term: str
    ontology_subject_mapping: List[OntologyMappingItem]
    ontology_object_mapping: List[OntologyMappingItem]
    trait_subject_mapping: List[TraitMappingItem]
    trait_object_mapping: List[TraitMappingItem]


class AssocScoresResponse(BaseModel):
    data: List[ScoredAssocEvidenceItem]


class TripleScoresRequests(BaseModel):
    triple_evidence: List[TripleEvidenceItem]
    query_subject_term: str
    query_object_term: str
    ontology_subject_mapping: List[OntologyMappingItem]
    ontology_object_mapping: List[OntologyMappingItem]
    umls_subject_mapping: List[UmlsMappingItem]
    umls_object_mapping: List[UmlsMappingItem]


class TripleScoresResponse(BaseModel):
    data: List[ScoredTripleEvidenceItem]
