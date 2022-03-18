from typing import List, Optional

from pydantic import BaseModel

from app.settings import params


class ClaimTextRequest(BaseModel):
    claim_text: str


class EntRequest(BaseModel):
    ent_id: str
    ent_term: str


class ClaimEntRequest(BaseModel):
    ent_id: str
    ent_term: str
    num_ent_candidates: int = params.NUM_SIMILARITY_CANDIDATES_EFO
    similarity_threshold: float = params.SIM_THRESHOLD_EFO


class TriplesRequests(BaseModel):
    subject_ents: List[EntRequest]
    object_ents: List[EntRequest]
    pred_term: str
    evidence_type: str = "supporting"


class TraitEntRequest(BaseModel):
    ents: List[EntRequest]
    pred_term: str = "CAUSES"
    num_ent_candidates: int = params.NUM_SIMILARITY_CANDIDATES_TRAIT
    similarity_threshold: float = params.SIM_THRESHOLD_TRAIT


class UmlsEntRequest(BaseModel):
    query_umls_ent: EntRequest
    ontology_ents: List[EntRequest]
    num_similarity_candidates: int = params.NUM_SIMILARITY_CANDIDATES_UMLS
    similarity_score_threshold: float = params.SIM_THRESHOLD_UMLS


class TripleItemRequest(BaseModel):
    triple_id: str
    triple_label: str


class LiteratureLiteRequests(BaseModel):
    triple_items: List[TripleItemRequest]


class LiteratureRequests(BaseModel):
    triple_items: List[TripleItemRequest]
    num_literature_items_per_triple: int = params.NUM_LITERATURE_ITEMS_PER_TRIPLE
    # these at the moment is simply used to highlight query terms on web app
    triple_subject_term: Optional[str] = None
    triple_object_term: Optional[str] = None
    claim_subject_term: Optional[str] = None
    claim_object_term: Optional[str] = None


class EfoIcRequest(BaseModel):
    ent_ids: List[str]


class AssocRequests(BaseModel):
    subject_ents: List[EntRequest]
    object_ents: List[EntRequest]
    pval_threshold: float = 1e-2
    pred_term: str = "CAUSES"
    evidence_type: str = "supporting"
