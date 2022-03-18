import pandas as pd
import requests

from .types import Config


def get_assoc_data_causation(
    source_id_list, target_id_list, pval: float, config: Config
):
    query = """
    MATCH (source:Gwas)-[r:MR_EVE_MR]->(target:Gwas)
    WHERE
        r.pval < {pval}
        AND source._id IN [{source_id_list}]
        AND target._id IN [{target_id_list}]
    RETURN
        source, r, target
    """.format(
        source_id_list=",".join([f"'{_}'" for _ in source_id_list]),
        target_id_list=",".join([f"'{_}'" for _ in target_id_list]),
        pval=pval,
    )
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    data = {"query": query}
    r = requests.post(url, json=data)
    r.raise_for_status()
    res = pd.json_normalize(r.json()["results"])
    return res


def get_assoc_data_additional(source_id_list, target_id_list, config: Config):
    assoc_meta_rels = ["PRS", "GENETIC_COR", "OBS_COR"]
    query = """
    MATCH (source:Gwas)-[r]-(target:Gwas)
    WHERE
        type(r) IN [{assoc_meta_rels}]
        AND source._id IN [{source_id_list}]
        AND target._id IN [{target_id_list}]
    RETURN
        source, type(r) AS r_type, r, target
    """.format(
        source_id_list=",".join([f"'{_}'" for _ in source_id_list]),
        target_id_list=",".join([f"'{_}'" for _ in target_id_list]),
        assoc_meta_rels=",".join([f"'{_}'" for _ in assoc_meta_rels]),
    )
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    data = {"query": query}
    r = requests.post(url, json=data)
    r.raise_for_status()
    res = pd.json_normalize(r.json()["results"])
    return res
