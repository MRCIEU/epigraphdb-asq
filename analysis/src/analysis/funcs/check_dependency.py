import requests
from icecream import ic

from analysis.settings import config


def check_component_status(verbose: bool = False):
    if verbose:
        ic(config.semrep_api_url)
        ic(config.melodi_presto_api_url)
        ic(config.text_base_api_url)
        ic(config.epigraphdb_api_url)
        ic(config.epigraphdb_web_backend_url)
        ic(config.epigraphdb_es_url)
        ic(config.epigraphdb_neural_url)
        ic(config.neural_models_url)
        ic(config.neural_transformers_url)
    r = requests.get(f"{config.semrep_api_url}/status")
    semrep_api_url_status = r.ok
    melodi_presto_status = requests.get(
        f"{config.melodi_presto_api_url}/status/"
    ).json()
    text_base_status = requests.get(
        f"{config.text_base_api_url}/status/"
    ).json()
    epigraphdb_api_status = requests.get(
        f"{config.epigraphdb_api_url}/ping"
    ).json()
    epigraphdb_web_backend_status = requests.get(
        f"{config.epigraphdb_web_backend_url}/ping"
    ).json()
    epigraphdb_es_info = requests.get(f"{config.epigraphdb_es_url}").json()
    if verbose:
        ic(epigraphdb_es_info)
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
    }
    ic(res)
    return res
