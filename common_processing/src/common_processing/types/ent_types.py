from typing import Callable, List

import pandera as pa
from pandera.typing import Series
from typing_extensions import TypedDict


class BaseEnt(TypedDict):
    ent_id: str
    ent_term: str


class OntologyEnt(BaseEnt, total=False):
    similarity_score: float
    identity_score: float
    ic_score: float


class PhenotypeEnt(BaseEnt, total=False):
    similarity_score: float


class OntologyEntDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    similarity_score: Series[float]
    identity_score: Series[float]
    ic_score: Series[float]


class PhenotypeSimilarityScoreDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    ref_ent_id: Series[str]
    ref_ent_term: Series[str]
    ref_meta_ent: Series[str]
    similarity_score: Series[float]


class PhenotypeEntDf(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    meta_ent: Series[str]
    ref_ent_id: Series[str]
    ref_ent_term: Series[str]
    ref_meta_ent: Series[str]
    similarity_score: Series[float]


class GroupedTraitEnts(TypedDict):
    ontology_ent: BaseEnt
    ents: List[PhenotypeEnt]


FilterFunc = Callable[[List[str]], List[str]]
