from pprint import pprint

import requests

from app.settings import config


def test_semrep():
    text = "modafinil is a novel stimulant that is effective in the treatment of narcolepsy"
    url = config.semrep_api_url
    r = requests.post(
        url=url,
        data=text.encode("utf-8"),
        headers={"Content-Type": "text/plain"},
    )
    r.raise_for_status()
    res = r.content.decode().split("\n")
    pprint(res)
    assert len(res) > 0


def test_melodi_presto():
    lit_id = "21782230"
    url = "{url}/sentence/".format(url=config.melodi_presto_api_url)
    payload = {"pmid": lit_id}
    r = requests.post(url, json=payload)
    results = r.json()["data"]
    pprint(results)
    assert r.ok
