import pandera as pa
from pandera.typing import Series
from typing_extensions import TypedDict


class TripleDf(pa.SchemaModel):
    # subject
    sub_id: Series[str]
    sub_term: Series[str]
    sub_type: Series[str]
    sub_text: Series[str]
    sub_neg: Series[bool]
    sub_confidence_score: Series[int]
    sub_start_pos: Series[int]
    sub_end_pos: Series[int]
    # pred
    pred_type: Series[str]
    pred: Series[str]
    pred_start_pos: Series[int]
    pred_end_pos: Series[int]
    # object
    obj_id: Series[str]
    obj_term: Series[str]
    obj_type: Series[str]
    obj_text: Series[str]
    obj_neg: Series[bool]
    obj_confidence_score: Series[int]
    obj_start_pos: Series[int]
    obj_end_pos: Series[int]
    # others
    text: Series[str]
    triple_text: Series[str]


class TripleDfFinal(TripleDf):
    idx: Series[int]


class TripleItem(TypedDict):
    idx: int
    # subject
    sub_id: str
    sub_term: str
    sub_type: str
    sub_text: str
    sub_neg: bool
    sub_confidence_score: int
    sub_start_pos: int
    sub_end_pos: int
    # pred
    pred_type: str
    pred: str
    pred_start_pos: int
    pred_end_pos: int
    # object
    obj_id: str
    obj_term: str
    obj_type: str
    obj_text: str
    obj_neg: bool
    obj_confidence_score: int
    obj_start_pos: int
    obj_end_pos: int
    # others
    text: str
    triple_text: str
