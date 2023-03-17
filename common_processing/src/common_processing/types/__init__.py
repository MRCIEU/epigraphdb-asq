from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    semrep_api_url: str
    melodi_presto_api_url: str
    medline_api_url: str
    epigraphdb_api_url: str
    epigraphdb_web_backend_url: str
    epigraphdb_neural_url: str
    neural_transformers_url: str
    neural_models_url: str
    epigraphdb_es_url: str
    backend_url: str
    data_path: Path


@dataclass
class Params:
    # ent, efo
    NUM_SIMILARITY_CANDIDATES_EFO: int = 30
    SIM_THRESHOLD_EFO: float = 0.7
    IC_THRESHOLD_EFO: float = 0.6  # roughly at "carcinoma"
    IDENTITY_THRESHOLD: float = 1.5
    # downstream ent, umls
    NUM_SIMILARITY_CANDIDATES_UMLS: int = 20
    SIM_THRESHOLD_UMLS: float = 0.7
    # downstream ent, gwas traits
    NUM_SIMILARITY_CANDIDATES_TRAIT: int = 20
    SIM_THRESHOLD_TRAIT: float = 0.7
    # triple evidence
    # literature evidence
    NUM_LITERATURE_ITEMS_PER_TRIPLE: int = 10
    # assoc evidence
    ASSOC_PVAL_THRESHOLD: float = 1e-2
