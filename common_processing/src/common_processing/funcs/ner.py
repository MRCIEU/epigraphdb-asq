import re
from typing import Optional, Tuple

from ipymarkup.span import format_span_box_markup


def format_triple_in_sent(
    sent: str,
    subject_term: str,
    object_term: str,
    predicate_term: str,
    subject_pos: Tuple[int, int],
    object_pos: Tuple[int, int],
    predicate_pos: Tuple[int, int],
) -> str:
    """Given the relevant triple info, highlight them in the text"""
    spans = [
        subject_pos + (subject_term,),
        object_pos + (object_term,),
        predicate_pos + (predicate_term,),
    ]
    # lines returns generator
    lines = format_span_box_markup(sent, spans)
    res = "".join(lines)
    return res


def format_ent_mentions(
    sent: str,
    triple_subject_term: Optional[str],
    triple_object_term: Optional[str],
    claim_subject_term: Optional[str],
    claim_object_term: Optional[str],
) -> str:
    def _format_ent_spans(sent: str, ent: str, prefix: str):
        start_pos = [
            match.start() for match in re.finditer(ent.lower(), sent.lower())
        ]
        end_pos = [_ + len(ent) for _ in start_pos]
        spans = [
            (_, end_pos[idx], "{prefix}".format(prefix=prefix))
            for idx, _ in enumerate(start_pos)
        ]
        return spans

    # If triple terms are char-level similar to claim terms, then
    # ignore them for better readability
    claim_terms = [
        _.lower()
        for _ in [claim_subject_term, claim_object_term]
        if _ is not None
    ]
    if triple_subject_term is not None:
        triple_subject_term = (
            None
            if triple_subject_term.lower() in claim_terms
            else triple_subject_term
        )
    if triple_object_term is not None:
        triple_object_term = (
            None
            if triple_object_term.lower() in claim_terms
            else triple_object_term
        )

    triple_subject_spans = (
        _format_ent_spans(
            sent=sent, ent=triple_subject_term, prefix="Triple subject"
        )
        if triple_subject_term is not None
        else []
    )
    triple_object_spans = (
        _format_ent_spans(
            sent=sent, ent=triple_object_term, prefix="Triple object"
        )
        if triple_object_term is not None
        else []
    )
    claim_subject_spans = (
        _format_ent_spans(
            sent=sent, ent=claim_subject_term, prefix="Claim subject"
        )
        if claim_subject_term is not None
        else []
    )
    claim_object_spans = (
        _format_ent_spans(
            sent=sent, ent=claim_object_term, prefix="Claim object"
        )
        if claim_object_term is not None
        else []
    )

    spans = (
        claim_subject_spans
        + claim_object_spans
        + triple_subject_spans
        + triple_object_spans
    )
    lines = format_span_box_markup(sent, spans)
    res = "".join(lines)
    return res
