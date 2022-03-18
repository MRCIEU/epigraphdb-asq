from typing import List

from common_processing import triple_evidence
from fastapi import APIRouter

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


@router.post(
    "/evidence/triples", response_model=response_models.TripleEvidenceResponse
)
# @cache(namespace="evidence_triples")
async def get_triples(
    data: request_models.TriplesRequests,
) -> List[types.TripleEvidence]:
    subject_ents = [_.dict() for _ in data.subject_ents]
    object_ents = [_.dict() for _ in data.object_ents]
    processor = triple_evidence.TripleEvidenceProcessor(config=config)
    processor.process(
        evidence_type=data.evidence_type,
        subject_ents=subject_ents,
        object_ents=object_ents,
        pred_term=data.pred_term,
    )
    evidence_df = processor.evidence_df
    res: List[types.TripleEvidence] = evidence_df.to_dict(orient="records")
    return res
