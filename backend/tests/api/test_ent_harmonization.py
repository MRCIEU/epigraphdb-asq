import pytest
from common_processing import ent_harmonization
from common_processing.types import ent_types
from pydantic import create_model_from_typeddict
from starlette.testclient import TestClient

from app.main import app
from app.settings import config


class TestOntologyEnts:
    CLAIM_ENT = "obesity"
    CLAIM_ENT_ID = "http://www.ebi.ac.uk/efo/EFO_0001073"
    OntologyEntModel = create_model_from_typeddict(
        ent_types.OntologyEnt  # type: ignore
    )

    def _common(self, candidates, ents) -> bool:
        print(candidates)
        assert len(candidates) > 0
        for _ in candidates:
            assert self.OntologyEntModel(**_)
            print(ents)
            assert len(ents) > 0
        for _ in ents:
            assert self.OntologyEntModel(**_)
        return True

    def test_processing(self):
        ent_harmonizer = ent_harmonization.OntologyEntHarmonizer(config=config)
        assert ent_harmonizer.harmonize(
            ent_id=self.CLAIM_ENT_ID,
            ent_term=self.CLAIM_ENT,
        )
        candidates = ent_harmonizer.candidates
        ents = ent_harmonizer.ents
        assert self._common(candidates=candidates, ents=ents)

    def test_api(self):
        payload = {
            "ent_id": self.CLAIM_ENT_ID,
            "ent_term": self.CLAIM_ENT,
        }
        with TestClient(app) as client:
            r = client.post("/ent_harmonization/ontology_ents", json=payload)
        assert r.ok


class TestTraitEnts:
    QUERY_ENTS = [
        {
            "ent_id": "http://www.ebi.ac.uk/efo/EFO_0000270",
            "ent_term": "asthma",
        },
    ]
    PRED_TERMS = ["CAUSES", "ASSOCIATED_WITH"]

    @pytest.mark.parametrize("pred_term", PRED_TERMS)
    def test_processing(self, pred_term):
        phenotype_ent_harmonizer = ent_harmonization.PhenotypeEntHarmonizer(
            config=config
        )
        assert phenotype_ent_harmonizer.harmonize(
            ontology_ents=self.QUERY_ENTS,
            pred_term=pred_term,
        )
        ents_df = phenotype_ent_harmonizer.ents_df
        ents = phenotype_ent_harmonizer.ents
        assert len(ents) > 0
        assert len(ents_df) > 0

    @pytest.mark.parametrize("pred_term", PRED_TERMS)
    def test_api(self, pred_term):
        payload = {"ents": self.QUERY_ENTS, "pred_term": pred_term}
        with TestClient(app) as client:
            r = client.post("/ent_harmonization/trait_ents", json=payload)
        assert r.ok
        results = r.json()
        assert len(results["ents"]) > 0
        assert len(results["detail_data"]) > 0


class TestUmlsEnts:
    QUERY_ENT = {
        "ent_id": "C0004096",
        "ent_term": "Asthma",
    }
    ONTOLOGY_ENTS = [
        {
            "ent_id": "http://www.ebi.ac.uk/efo/EFO_0000270",
            "ent_term": "asthma",
        }
    ]

    def test_processing(self):
        litterm_ent_harmonizer = ent_harmonization.UmlsEntHarmonizer(
            config=config
        )
        assert litterm_ent_harmonizer.harmonize(
            umls_ent=self.QUERY_ENT,
            ontology_ents=self.ONTOLOGY_ENTS,
        )
        ents_df = litterm_ent_harmonizer.ents_df
        assert len(ents_df) > 0
        ents = litterm_ent_harmonizer.ents
        assert len(ents) > 0

    def test_api(self):
        payload = {
            "query_umls_ent": self.QUERY_ENT,
            "ontology_ents": self.ONTOLOGY_ENTS,
        }
        with TestClient(app) as client:
            r = client.post("/ent_harmonization/umls_ents", json=payload)
        assert r.ok
        results = r.json()
        assert len(results["ents"]) > 0
        assert len(results["detail_data"]) > 0
