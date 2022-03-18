import pandera as pa
from pandera.typing import Series


class TripleQueryDf(pa.SchemaModel):
    triple_subject_id: Series[str] = pa.Field(alias="triple.subject_id")
    triple_predicate: Series[str] = pa.Field(alias="triple.predicate")
    triple__name: Series[str] = pa.Field(alias="triple._name")
    triple_name: Series[str] = pa.Field(alias="triple.name")
    triple__source: Series[str] = pa.Field(alias="triple._source")
    triple_id: Series[str] = pa.Field(alias="triple.id")
    triple__id: Series[str] = pa.Field(alias="triple._id")
    triple_object_id: Series[str] = pa.Field(alias="triple.object_id")


class TripleEvidenceDf(pa.SchemaModel):
    triple_id: Series[str]
    triple_label: Series[str]
    triple_lower: Series[str]
    triple_subject_id: Series[str]
    triple_subject: Series[str]
    triple_object_id: Series[str]
    triple_object: Series[str]
    triple_predicate: Series[str]
    ent_subject_id: Series[str]
    ent_object_id: Series[str]
    ent_subject_term: Series[str]
    ent_object_term: Series[str]
    direction: Series[str]
    literature_count: Series[int]
