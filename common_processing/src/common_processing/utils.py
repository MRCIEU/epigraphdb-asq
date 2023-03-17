import requests
from loguru import logger
from pydantic import validate_arguments

from .types import Config


@validate_arguments
def check_component_status(config: Config, verbose: bool = False):
    if verbose:
        logger.info(f"{config=}")
    r = requests.get(f"{config.semrep_api_url}/status")
    semrep_api_url_status = r.ok
    melodi_presto_status = requests.post(
        "{url}/components/melodi-presto".format(
            url=config.epigraphdb_web_backend_url
        ),
        json={"endpoint": "/status/", "method": "GET", "params": None},
    ).json()
    text_base_status = requests.get(f"{config.medline_api_url}/ping").json()
    epigraphdb_api_status = requests.get(
        f"{config.epigraphdb_api_url}/ping"
    ).json()
    epigraphdb_web_backend_status = requests.get(
        f"{config.epigraphdb_web_backend_url}/ping"
    ).json()
    epigraphdb_es_info = requests.get(f"{config.epigraphdb_es_url}").json()
    if verbose:
        logger.info(f"{epigraphdb_es_info=}")
    epigraphdb_es_status = len(epigraphdb_es_info) > 0
    epigraphdb_neural_status = requests.get(
        f"{config.epigraphdb_neural_url}/ping"
    ).json()
    neural_models_status = requests.get(
        f"{config.neural_models_url}/ping"
    ).json()
    neural_transformers_status = requests.get(
        f"{config.neural_transformers_url}/ping"
    ).json()
    data_path_status = config.data_path.exists()
    res = {
        "semrep_api_url": semrep_api_url_status,
        "melodi_presto": melodi_presto_status,
        "text_base": text_base_status,
        "epigraphdb_api": epigraphdb_api_status,
        "epigraphdb_web_backend": epigraphdb_web_backend_status,
        "epigraphdb_es": epigraphdb_es_status,
        "epigraphdb_neural": epigraphdb_neural_status,
        "neural_models": neural_models_status,
        "neural_transformers": neural_transformers_status,
        "data_path": data_path_status,
    }
    logger.info(f"{res=}")
    return res
