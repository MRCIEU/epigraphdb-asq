from common_processing.types import Config, Params
from environs import Env

from .utils import find_data_root

env = Env()
env.read_env()


config = Config(
    semrep_api_url=env("ANALYSIS_SEMREP_API_URL"),
    melodi_presto_api_url=env("ANALYSIS_MELODI_PRESTO_API_URL"),
    medline_api_url=env("ANALYSIS_MEDLINE_API_URL"),
    epigraphdb_api_url=env("ANALYSIS_EPIGRAPHDB_API_URL"),
    epigraphdb_web_backend_url=env("ANALYSIS_EPIGRAPHDB_WEB_BACKEND_URL"),
    epigraphdb_neural_url=env("ANALYSIS_EPIGRAPHDB_NEURAL_URL"),
    neural_transformers_url=env("ANALYSIS_NEURAL_TRANSFORMERS_URL"),
    neural_models_url=env("ANALYSIS_NEURAL_MODELS_URL"),
    epigraphdb_es_url=env("ANALYSIS_EPIGRAPHDB_ES_URL"),
    backend_url=env("ANALYSIS_BACKEND_URL"),
    data_path=find_data_root(),
)

params = Params(
    # ent, efo
    SIM_THRESHOLD_EFO=0.7,
    NUM_SIMILARITY_CANDIDATES_EFO=10,
    IC_THRESHOLD_EFO=0.6,  # roughly at "carcinoma"
    IDENTITY_THRESHOLD=1.5,
    # downstream ent, umls
    SIM_THRESHOLD_UMLS=0.7,
    NUM_SIMILARITY_CANDIDATES_UMLS=20,
    # downstream ent, gwas traits
    SIM_THRESHOLD_TRAIT=0.7,
    NUM_SIMILARITY_CANDIDATES_TRAIT=20,
    # triple evidence
    # literature evidence
    NUM_LITERATURE_ITEMS_PER_TRIPLE=10,
    # assoc evidence
    ASSOC_PVAL_THRESHOLD=1e-2,
)
