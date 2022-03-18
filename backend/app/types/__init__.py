from typing import Any, Dict, List, Optional, Union

from common_processing.types import ent_types, semrep_types
from typing_extensions import TypedDict


class TripleData(TypedDict):
    data: List[semrep_types.TripleItem]
    html: List[Dict[str, Union[int, str]]]
    invalid_triples: List[semrep_types.TripleItem]
    claim_text: List[str]


class AnnotatedBaseEnt(ent_types.BaseEnt):
    url: Optional[str]  # NOTE: placeholder


class AnnotatedOntologyEnt(ent_types.OntologyEnt):
    url: Optional[str]  # NOTE: placeholder


class AnnotatedPhenotypeEnt(ent_types.PhenotypeEnt):
    url: Optional[str]  # NOTE: placeholder


class DetailEntItem(TypedDict):
    ent_id: str
    ent_term: str
    ent_url: Optional[str]
    meta_ent: str
    meta_ent_url: Optional[str]
    ref_ent_id: str
    ref_ent_term: str
    ref_ent_url: Optional[str]
    ref_meta_ent: str
    ref_meta_ent_url: Optional[str]
    similarity_score: float


class PostOntologyEntResults(TypedDict):
    ents: List[AnnotatedBaseEnt]
    detail_data: List[DetailEntItem]


class OntologyResults(TypedDict):
    candidates: List[AnnotatedOntologyEnt]
    ents: List[AnnotatedOntologyEnt]


class GroupedTraitCandidates(TypedDict):
    ontology_ent: ent_types.OntologyEnt
    candidates: List[AnnotatedPhenotypeEnt]


class TraitResults(TypedDict):
    grouped_candidates: List[GroupedTraitCandidates]
    ents: List[AnnotatedBaseEnt]


class TripleEvidence(TypedDict):
    triple_id: str
    triple_label: str
    triple_lower: str
    triple_subject_id: str
    triple_subject: str
    triple_object_id: str
    triple_object: str
    triple_predicate: str
    ent_subject_id: str
    ent_object_id: str
    ent_subject_term: str
    ent_object_term: str
    direction: str
    literature_count: int


class LiteratureEvidenceData(TypedDict):
    abstract: str
    doi: str
    pubmed_id: str
    title: str
    triple_id: str
    triple_lower: str
    type: str
    year: int


class LiteratureLiteEvidenceData(TypedDict):
    pubmed_id: str
    triple_id: str
    triple_lower: str


class LiteratureEvidenceHtmlText(TypedDict):
    idx: int
    title_text: str
    abstract: str
    sentence: str


class LiteratureEvidence(TypedDict):
    data: List[LiteratureEvidenceData]
    html_text: List[LiteratureEvidenceHtmlText]


class LiteratureLiteEvidence(TypedDict):
    data: List[LiteratureLiteEvidenceData]


class EfoIcItem(TypedDict):
    ent_term: str
    ent_id: str
    ic_score: float


EfoIcRes = List[EfoIcItem]


class AssocEvidenceDataItem(TypedDict):
    subject_id: str
    subject_term: str
    object_id: str
    object_term: str
    meta_rel: str
    direction: str
    effect_size: float
    se: float
    pval: float
    rel_data: Any


class AssocEvidence(TypedDict):
    data: List[AssocEvidenceDataItem]
