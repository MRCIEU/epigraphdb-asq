import json
from pathlib import Path

import pandas as pd
from common_processing import scores
from starlette.testclient import TestClient

from app.main import app

test_data_dir = Path(__file__).parent.parent / "test_data" / "test-scores"
assert test_data_dir.exists()

with (test_data_dir / "assoc-evidence.json").open() as f:
    assoc_evidence = json.load(f)
    assoc_evidence_df = pd.DataFrame(assoc_evidence)

with (test_data_dir / "triple-evidence.json").open() as f:
    triple_evidence = json.load(f)
    triple_evidence_df = pd.DataFrame(triple_evidence)

with (test_data_dir / "ontology-object-ents.json").open() as f:
    ontology_object_ents = json.load(f)
    ontology_object_ents_df = pd.DataFrame(ontology_object_ents)

with (test_data_dir / "ontology-subject-ents.json").open() as f:
    ontology_subject_ents = json.load(f)
    ontology_subject_ents_df = pd.DataFrame(ontology_subject_ents)

with (test_data_dir / "trait-object-ents.json").open() as f:
    trait_object_ents = json.load(f)
    trait_object_ents_df = pd.DataFrame(trait_object_ents)

with (test_data_dir / "trait-subject-ents.json").open() as f:
    trait_subject_ents = json.load(f)
    trait_subject_ents_df = pd.DataFrame(trait_subject_ents)

with (test_data_dir / "umls-subject-ents.json").open() as f:
    umls_subject_ents = json.load(f)
    umls_subject_ents_df = pd.DataFrame(umls_subject_ents)

with (test_data_dir / "umls-object-ents.json").open() as f:
    umls_object_ents = json.load(f)
    umls_object_ents_df = pd.DataFrame(umls_object_ents)


class TestAssocScores:
    QUERY_SUBJECT_TERM = "Obesity"
    QUERY_OBJECT_TERM = "Asthma"

    def test_processing(self):
        res = scores.make_assoc_scores(
            assoc_evidence=assoc_evidence_df,
            query_subject_term=self.QUERY_SUBJECT_TERM,
            query_object_term=self.QUERY_OBJECT_TERM,
            ontology_subject_mapping=ontology_subject_ents_df,
            ontology_object_mapping=ontology_object_ents_df,
            trait_subject_mapping=trait_subject_ents_df,
            trait_object_mapping=trait_object_ents_df,
        )
        assert len(res)

    def test_api(self):
        payload = {
            "assoc_evidence": assoc_evidence,
            "query_subject_term": self.QUERY_SUBJECT_TERM,
            "query_object_term": self.QUERY_OBJECT_TERM,
            "ontology_subject_mapping": ontology_subject_ents,
            "ontology_object_mapping": ontology_object_ents,
            "trait_subject_mapping": trait_subject_ents,
            "trait_object_mapping": trait_object_ents,
        }
        url = "/scores/assoc"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        assert len(r.json()) > 0
        assert len(r.json()["data"]) > 0


class TestTripleScores:
    QUERY_SUBJECT_TERM = "Obesity"
    QUERY_OBJECT_TERM = "Asthma"

    def test_processing(self):
        res = scores.make_triple_scores(
            triple_evidence=triple_evidence_df,
            query_subject_term=self.QUERY_SUBJECT_TERM,
            query_object_term=self.QUERY_OBJECT_TERM,
            ontology_subject_mapping=ontology_subject_ents_df,
            ontology_object_mapping=ontology_object_ents_df,
            umls_subject_mapping=umls_subject_ents_df,
            umls_object_mapping=umls_object_ents_df,
        )
        assert len(res)

    def test_api(self):
        payload = {
            "triple_evidence": triple_evidence,
            "query_subject_term": self.QUERY_SUBJECT_TERM,
            "query_object_term": self.QUERY_OBJECT_TERM,
            "ontology_subject_mapping": ontology_subject_ents,
            "ontology_object_mapping": ontology_object_ents,
            "umls_subject_mapping": umls_subject_ents,
            "umls_object_mapping": umls_object_ents,
        }
        url = "/scores/triples"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        assert len(r.json()) > 0
        assert len(r.json()["data"]) > 0
