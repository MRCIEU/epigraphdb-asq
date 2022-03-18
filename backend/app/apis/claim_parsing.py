from typing import Dict, List, Union

import pysbd
from common_processing import claim_parsing
from common_processing.types import semrep_types
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app import types
from app.settings import config
from app.types import request_models, response_models

router = APIRouter()


segmenter = pysbd.Segmenter(language="en", clean=False)


@router.post(
    "/claim_parsing/parse", response_model=response_models.TripleDataResponse
)
@cache(namespace="claim_triples")
async def parse_text_to_triples(
    data: request_models.ClaimTextRequest,
) -> types.TripleData:
    claim_parser = claim_parsing.ClaimParser(config=config)
    claim_parser.parse_claim(claim_text=data.claim_text)
    semrep_triples: List[semrep_types.TripleItem] = claim_parser.triple_items
    invalid_triples: List[
        semrep_types.TripleItem
    ] = claim_parser.invalid_triple_items
    html_text: List[Dict[str, Union[int, str]]] = claim_parser.html_text
    segmented_text = segmenter.segment(data.claim_text)
    res: types.TripleData = {
        "data": semrep_triples,
        "html": html_text,
        "invalid_triples": invalid_triples,
        "claim_text": segmented_text,
    }
    return res
