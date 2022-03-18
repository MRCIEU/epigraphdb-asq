from pathlib import Path

from common_processing.types import Config, Params
from environs import Env

env = Env()
env.read_env()

# dependent urls
config = Config(
    semrep_api_url=env("DOCKER_SEMREP_API_URL"),
    melodi_presto_api_url=env("DOCKER_MELODI_PRESTO_API_URL"),
    text_base_api_url=env("DOCKER_TEXT_BASE_API_URL"),
    epigraphdb_api_url=env("DOCKER_EPIGRAPHDB_API_URL"),
    epigraphdb_web_backend_url=env("DOCKER_EPIGRAPHDB_WEB_BACKEND_URL"),
    epigraphdb_neural_url=env("DOCKER_EPIGRAPHDB_NEURAL_URL"),
    neural_transformers_url=env("DOCKER_NEURAL_TRANSFORMERS_URL"),
    neural_models_url=env("DOCKER_NEURAL_MODELS_URL"),
    epigraphdb_es_url=env("DOCKER_EPIGRAPHDB_ES_URL"),
    backend_url=env("DOCKER_BACKEND_URL"),
    data_path=Path("/data"),
)

params = Params()
