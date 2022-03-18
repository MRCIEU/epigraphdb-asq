import pandera as pa
from pandera.engines.numpy_engine import Object
from pandera.typing import Series


class AssocEvidenceQueryDf(pa.SchemaModel):
    source_id: Series[str]
    source_term: Series[str]
    target_id: Series[str]
    target_term: Series[str]
    meta_rel: Series[str]
    effect_size: Series[float]
    se: Series[float] = pa.Field(nullable=True)
    pval: Series[float] = pa.Field(nullable=True)
    rel_data: Series[Object]


class AssocEvidenceDf(pa.SchemaModel):
    subject_id: Series[str]
    subject_term: Series[str]
    object_id: Series[str]
    object_term: Series[str]
    meta_rel: Series[str]
    direction: Series[str]
    effect_size: Series[float]
    se: Series[float] = pa.Field(nullable=True)
    pval: Series[float] = pa.Field(nullable=True)
    rel_data: Series[Object]
