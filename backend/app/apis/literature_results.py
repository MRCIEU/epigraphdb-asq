from functools import partial
from typing import List, Optional

import pandas as pd
from common_processing import literature_evidence
from common_processing.funcs import ner
from fastapi import APIRouter

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


@router.post(
    "/evidence/literature-lite",
    response_model=Optional[response_models.LiteratureLiteEvidenceResponse],  # type: ignore
)
# @cache(namespace="evidence_literature_lite")
async def get_literature_lite(  # noqa
    data: request_models.LiteratureLiteRequests,
) -> Optional[types.LiteratureLiteEvidence]:
    triple_items = [_.dict() for _ in data.triple_items]
    literature_processor = literature_evidence.LiteratureLiteEvidenceProcessor(
        config=config
    )
    literature_processor.process(triples=triple_items)
    evidence_df = literature_processor.evidence_df
    evidence_data = evidence_df.to_dict(orient="records")
    res: types.LiteratureLiteEvidence = {
        "data": evidence_data,
    }
    return res


@router.post(
    "/evidence/literature",
    response_model=Optional[response_models.LiteratureEvidenceResponse],  # type: ignore
)
# @cache(namespace="evidence_literature")
async def get_literature(  # noqa
    data: request_models.LiteratureRequests,
) -> Optional[types.LiteratureEvidence]:
    triple_items = [_.dict() for _ in data.triple_items]
    literature_processor = literature_evidence.LiteratureEvidenceProcessor(
        config=config
    )
    literature_processor.process(
        triples=triple_items,
        num_items_per_triple=data.num_literature_items_per_triple,
    )
    evidence_df = literature_processor.evidence_df
    html_text = make_html_text(
        evidence_df=evidence_df,
        triple_subject_term=data.triple_subject_term,
        triple_object_term=data.triple_object_term,
        claim_subject_term=data.claim_subject_term,
        claim_object_term=data.claim_object_term,
    )
    evidence_data = evidence_df.to_dict(orient="records")
    res: types.LiteratureEvidence = {
        "data": evidence_data,
        "html_text": html_text,
    }
    return res


def make_html_text(
    evidence_df: pd.DataFrame,
    triple_subject_term: Optional[str],
    triple_object_term: Optional[str],
    claim_subject_term: Optional[str],
    claim_object_term: Optional[str],
) -> List[types.LiteratureEvidenceHtmlText]:
    render = partial(
        ner.format_ent_mentions,
        triple_subject_term=triple_subject_term,
        triple_object_term=triple_object_term,
        claim_subject_term=claim_subject_term,
        claim_object_term=claim_object_term,
    )
    sents: List[types.LiteratureEvidenceHtmlText] = [
        {
            "idx": idx,
            "title_text": render(sent=_["title"]),
            "sentence": render(sent=_["sentence"]),
            "abstract": render(sent=_["abstract"]),
        }
        for idx, _ in evidence_df.iterrows()
    ]
    return sents
