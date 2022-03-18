from starlette.testclient import TestClient

from app.main import app


def test_efo_ic_scores():
    ent_ids = [
        "http://purl.obolibrary.org/obo/UBERON_0001906",
        "http://purl.obolibrary.org/obo/UBERON_0001062",
        "http://purl.obolibrary.org/obo/UBERON_0001737",
        "http://purl.obolibrary.org/obo/UBERON_0000061",
        "http://purl.obolibrary.org/obo/UBERON_0001465",
        "http://purl.obolibrary.org/obo/UBERON_0002384",
        "http://purl.obolibrary.org/obo/UBERON_0005366",
        "http://purl.obolibrary.org/obo/UBERON_0000358",
    ]
    payload = {"ent_ids": ent_ids}
    with TestClient(app) as client:
        r = client.post("/data/efo_ic_scores", json=payload)
    assert r.ok
    assert len(r.json()) > 0


def test_efo_data_case0():
    ent_ids = [
        "http://www.ebi.ac.uk/efo/EFO_0004340",
        "http://www.ebi.ac.uk/efo/EFO_0004324",
    ]
    query_terms = ["obesity", "overweight"]
    payload = {"ent_ids": ent_ids, "query_terms": query_terms}
    with TestClient(app) as client:
        r = client.post("/data/ontology", json=payload)
    assert r.ok
    assert len(r.json()) > 0


def test_efo_data_case1():
    ent_ids = [
        "http://purl.obolibrary.org/obo/UBERON_0001906",
        "http://purl.obolibrary.org/obo/UBERON_0001062",
        "http://purl.obolibrary.org/obo/UBERON_0001737",
        "http://purl.obolibrary.org/obo/UBERON_0000061",
        "http://purl.obolibrary.org/obo/UBERON_0001465",
        "http://purl.obolibrary.org/obo/UBERON_0002384",
        "http://purl.obolibrary.org/obo/UBERON_0005366",
        "http://purl.obolibrary.org/obo/UBERON_0000358",
    ]
    payload = {"ent_ids": ent_ids}
    with TestClient(app) as client:
        r = client.post("/data/ontology", json=payload)
    assert r.ok
    assert len(r.json()) > 0


def test_data_prompt_literature_term():
    q = "fun"
    with TestClient(app) as client:
        r = client.get("/data/prompt/literature-term", params={"q": q})
    assert r.ok
    assert len(r.json()) > 0


def test_analysis_results():
    with TestClient(app) as client:
        r = client.get("/data/analysis-results")
    assert r.ok
    assert len(r.json()) > 0
