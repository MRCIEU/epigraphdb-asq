from typing import Callable, List

import requests
from loguru import logger

from ..types import Config

from icecream import ic  # noqa
from pydash import py_  # noqa


PREFIXES = ["ukb-", "ieu-"]


def compose(funcs: List[Callable[[List[str]], List[str]]]):
    """
    compose([foo, bar, quax]) => quax(bar(foo(X)))
    """

    def inner(args):
        for func in reversed(funcs):
            args = func(args)
        return args

    return inner


def prefix_filter(ent_ids: List[str], **kwargs) -> List[str]:
    def _filter(ent_ids: List[str], prefix: str) -> List[str]:
        ent_ids = py_.compact(
            [_ if _.startswith(prefix) else None for _ in ent_ids]
        )
        if verbose:
            logger.info(f"Done prefix filter `{prefix}`, {len(ent_ids)=}")
        return ent_ids

    verbose = kwargs["verbose"] if "verbose" in kwargs.keys() else True
    if verbose:
        logger.info(f"Begin filter by prefix, {len(ent_ids)=}")
    filtered = [_filter(ent_ids=ent_ids, prefix=prefix) for prefix in PREFIXES]
    ent_ids = py_.chain(filtered).flatten().uniq().value()
    if verbose:
        logger.info(f"Done filter by prefix, {len(ent_ids)=}")
    return ent_ids


# NOTE: this func needs to be partialled on the `config` arg
def exist_with_epigraphdb_mr_eve_mr(
    ent_ids: List[str], config: Config, verbose: bool, **kwargs,
) -> List[str]:
    logger.info(f"Begin filter MR_EVE_MR, {len(ent_ids)=}")
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    # MAYBE: this needs to be fetched from an cached ent list,
    # ideally in web backend api, rather than from the graph itself
    query = """
    MATCH
      (n:Gwas)-[r:MR_EVE_MR]-(m:Gwas)
    WHERE
      n._id IN {id_list}
    RETURN DISTINCT
      n._id AS ent_id
    LIMIT
      {limit}
    """.format(
        id_list=str(ent_ids), limit=len(ent_ids)
    )
    payload = {"query": query}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    results = set([_["ent_id"] for _ in r.json()["results"]])
    ent_ids = list(set(ent_ids).intersection(results))
    if verbose:
        logger.info(f"Done filter, {len(ent_ids)=}")
    return ent_ids


def exist_with_epigraphdb_undirectional_assoc(
    ent_ids: List[str], config: Config, verbose: bool, **kwargs,
) -> List[str]:
    logger.info(f"Begin filter undirectional assoc, {len(ent_ids)=}")
    url = "{url}/cypher".format(url=config.epigraphdb_api_url)
    # MAYBE: this needs to be fetched from an cached ent list,
    # ideally in web backend api, rather than from the graph itself
    query = """
    MATCH
      (n:Gwas)-[r:MR_EVE_MR|PRS|GEN_COR]-(m:Gwas)
    WHERE
      n._id IN {id_list}
    RETURN DISTINCT
      n._id AS ent_id
    LIMIT
      {limit}
    """.format(
        id_list=str(ent_ids), limit=len(ent_ids)
    )
    payload = {"query": query}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    results = set([_["ent_id"] for _ in r.json()["results"]])
    ent_ids = list(set(ent_ids).intersection(results))
    if verbose:
        logger.info(f"Done filter, {len(ent_ids)=}")
    return ent_ids
