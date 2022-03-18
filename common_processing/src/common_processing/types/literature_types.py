import pandera as pa
from pandera.engines.numpy_engine import Object
from pandera.typing import Series
from typing_extensions import TypedDict


class TripleItem(TypedDict):
    triple_id: str
    triple_label: str


class LiteratureEvidenceDf(pa.SchemaModel):
    pubmed_id: Series[str]
    triple_id: Series[str]
    triple_lower: Series[str]
    sentence: Series[str]
    title: Series[str]
    doi: Series[str]
    year: Series[int]
    type: Series[Object]
    abstract: Series[str]


class LiteratureLiteEvidenceDf(pa.SchemaModel):
    pubmed_id: Series[str]
    triple_id: Series[str]
    triple_lower: Series[str]
