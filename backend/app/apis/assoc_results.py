from typing import List, Optional

from common_processing import assoc_evidence
from fastapi import APIRouter

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


@router.post(
    "/evidence/association",
    response_model=Optional[response_models.AssocEvidenceResponse],  # type: ignore
)
# @cache(namespace="evidence_assoc")
async def get_assoc(data: request_models.AssocRequests) -> types.AssocEvidence:
    subject_ents = [_.dict() for _ in data.subject_ents]
    object_ents = [_.dict() for _ in data.object_ents]
    assoc_processor = assoc_evidence.AssocEvidenceProcessor(config=config)
    assoc_processor.process(
        evidence_type=data.evidence_type,
        pred_term=data.pred_term,
        subject_ents=subject_ents,
        object_ents=object_ents,
        pval_threshold=data.pval_threshold,
    )
    evidence_df = assoc_processor.evidence_df
    evidence_data: List[types.AssocEvidenceDataItem] = (
        evidence_df.dropna().to_dict(orient="records")
        if evidence_df is not None
        else []
    )
    res: types.AssocEvidence = {"data": evidence_data}
    return res
