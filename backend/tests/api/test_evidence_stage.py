import pytest
from common_processing import (
    assoc_evidence,
    literature_evidence,
    triple_evidence,
)
from starlette.testclient import TestClient

from app.main import app
from app.settings import config

EVIDENCE_TYPE_LIST = ["supporting", "contradictory"]


class TestTripleEvidence:
    subject_ents = [
        {"ent_id": "C0028754", "ent_term": "Obesity"},
        {"ent_id": "C0028756", "ent_term": "Morbid obesity"},
        {"ent_id": "C0267989", "ent_term": "Lifelong obesity"},
        {"ent_id": "C0348956", "ent_term": "Drug-induced obesity"},
        {"ent_id": "C0342940", "ent_term": "Android obesity"},
        {"ent_id": "C2362324", "ent_term": "Pediatric Obesity"},
        {"ent_id": "C0451819", "ent_term": "Simple obesity"},
        {"ent_id": "C0267990", "ent_term": "Adult-onset obesity"},
        {"ent_id": "C1281429", "ent_term": "Exogenous obesity"},
        {"ent_id": "C1281440", "ent_term": "Familial obesity"},
        {"ent_id": "C0857116", "ent_term": "Gross obesity"},
        {"ent_id": "C0242339", "ent_term": "Dyslipidemias"},
        {"ent_id": "C1167682", "ent_term": "Abdominal obesity"},
        {"ent_id": "C1285391", "ent_term": "Obesity associated disorder"},
        {"ent_id": "C0342942", "ent_term": "Generalized obesity"},
        {"ent_id": "C0271885", "ent_term": "Hypothalamic obesity"},
        {"ent_id": "C0267992", "ent_term": "Obesity of endocrine origin"},
        {
            "ent_id": "C1536989",
            "ent_term": "abdominal obesity metabolic syndrome",
        },
        {"ent_id": "C1260894", "ent_term": "Hypertrophic obesity"},
        {"ent_id": "C1532480", "ent_term": "Hyperplastic obesity"},
        {"ent_id": "C0342880", "ent_term": "Polygenic hypercholesterolemia"},
    ]
    object_ents = [
        {"ent_id": "C0004096", "ent_term": "Asthma"},
        {"ent_id": "C0155877", "ent_term": "Allergic asthma"},
        {"ent_id": "C0877430", "ent_term": "Asthma chronic"},
        {"ent_id": "C0264408", "ent_term": "Childhood asthma"},
        {
            "ent_id": "C4041248",
            "ent_term": "Severe persistent allergic asthma",
        },
        {"ent_id": "C0340067", "ent_term": "Drug-induced asthma"},
        {"ent_id": "C0264423", "ent_term": "Occupational asthma"},
        {"ent_id": "C0856716", "ent_term": "Asthma aspirin-sensitive"},
        {"ent_id": "C0582415", "ent_term": "Acute asthma"},
        {"ent_id": "C0348819", "ent_term": "Mixed asthma"},
        {"ent_id": "C1740754", "ent_term": "Intermittent asthma"},
        {"ent_id": "C0004099", "ent_term": "Asthma, Exercise-Induced"},
        {"ent_id": "C1516055", "ent_term": "Asthma Preparation"},
        {"ent_id": "C0238266", "ent_term": "Meat-wrappers' asthma"},
        {"ent_id": "C1319018", "ent_term": "Asthmatic bronchitis"},
        {"ent_id": "C1260881", "ent_term": "Allergic bronchitis"},
        {"ent_id": "C0264348", "ent_term": "Chronic asthmatic bronchitis"},
        {"ent_id": "C0861154", "ent_term": "Allergic rhinoconjunctivitis"},
        {"ent_id": "C0684913", "ent_term": "Chemical-induced asthma"},
        {"ent_id": "C0340073", "ent_term": "Factitious asthma"},
    ]
    pred_term = "CAUSES"

    @pytest.mark.parametrize("evidence_type", EVIDENCE_TYPE_LIST)
    def test_processing(self, evidence_type):
        processor = triple_evidence.TripleEvidenceProcessor(config=config)
        processor.process(
            evidence_type=evidence_type,
            subject_ents=self.subject_ents,
            object_ents=self.object_ents,
            pred_term=self.pred_term,
        )
        df = processor.evidence_df
        assert len(df) > 0

    @pytest.mark.parametrize("evidence_type", EVIDENCE_TYPE_LIST)
    def test_api(self, evidence_type):
        payload = {
            "evidence_type": evidence_type,
            "subject_ents": self.subject_ents,
            "object_ents": self.object_ents,
            "pred_term": self.pred_term,
        }
        url = "/evidence/triples"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        assert len(r.json()) > 0


class TestLiteratureLiteEvidence:
    triple_evidence_items = [
        {
            "triple_id": "C0028754:CAUSES:C0004096",
            "triple_label": "obesity:causes:asthma",
        },
        {
            "triple_id": "C0242339:CAUSES:C0004096",
            "triple_label": "dyslipidemias:causes:asthma",
        },
    ]

    def test_processing(self):
        processor = literature_evidence.LiteratureLiteEvidenceProcessor(
            config=config
        )
        assert processor.process(triples=self.triple_evidence_items)
        evidence_df = processor.evidence_df
        assert evidence_df is not None and len(evidence_df) > 0

    def test_api(self):
        payload = {"triple_items": self.triple_evidence_items}
        url = "/evidence/literature-lite"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        assert len(r.json()) > 0


class TestLiteratureEvidence:
    triple_evidence_items = [
        {
            "triple_id": "C0028754:CAUSES:C0004096",
            "triple_label": "obesity:causes:asthma",
        },
        {
            "triple_id": "C0242339:CAUSES:C0004096",
            "triple_label": "dyslipidemias:causes:asthma",
        },
    ]

    def test_processing(self):
        processor = literature_evidence.LiteratureEvidenceProcessor(
            config=config
        )
        assert processor.process(triples=self.triple_evidence_items)
        evidence_df = processor.evidence_df
        assert evidence_df is not None and len(evidence_df) > 0

    def test_api(self):
        payload = {"triple_items": self.triple_evidence_items}
        url = "/evidence/literature"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        assert len(r.json()) > 0


class TestAssocEvidence:
    SUBJECT_GWAS_ENTS = [
        {"ent_id": "ieu-a-1096", "ent_term": "Childhood obesity"},
        {"ent_id": "ieu-a-93", "ent_term": "Overweight"},
    ]
    OBJECT_GWAS_ENTS = [
        {"ent_id": "ukb-d-J10_ASTHMA", "ent_term": "Asthma"},
        {"ent_id": "ieu-a-44", "ent_term": "Asthma"},
        {
            "ent_id": "ukb-a-447",
            "ent_term": "Blood clot  DVT  bronchitis  emphysema  asthma  rhinitis  "
            + "eczema  allergy diagnosed by doctor: Hayfever  allergic "
            + "rhinitis or eczema",
        },
        {
            "ent_id": "ukb-a-446",
            "ent_term": "Blood clot  DVT  bronchitis  emphysema  asthma  rhinitis  "
            + "eczema  allergy diagnosed by doctor: Asthma",
        },
        {
            "ent_id": "ukb-b-12753",
            "ent_term": "Recent medication for hayfever or allergic rhinitis",
        },
        {
            "ent_id": "ukb-a-444",
            "ent_term": "Blood clot  DVT  bronchitis  emphysema  asthma  rhinitis  "
            + "eczema  allergy diagnosed by doctor: Emphysema/chronic "
            + "bronchitis",
        },
        {
            "ent_id": "ukb-b-17241",
            "ent_term": "Blood clot, DVT, bronchitis, emphysema, asthma, rhinitis, "
            + "eczema, allergy diagnosed by doctor: Hayfever, allergic "
            + "rhinitis or eczema",
        },
        {
            "ent_id": "ukb-b-7178",
            "ent_term": "Doctor diagnosed hayfever or allergic rhinitis",
        },
        {
            "ent_id": "ukb-a-254",
            "ent_term": "Doctor diagnosed hayfever or allergic rhinitis",
        },
    ]
    PARAMS = [
        ("CAUSES", "supporting"),
        ("CAUSES", "contradictory_directional_type1"),
        ("CAUSES", "contradictory_directional_type2"),
        ("CAUSES", "generic_directional"),
        ("ASSOCIATED_WITH", "supporting"),
        ("ASSOCIATED_WITH", "contradictory_undirectional"),
    ]

    @pytest.mark.parametrize("pred_term, evidence_type", PARAMS)
    def test_processing(self, pred_term, evidence_type):
        assoc_evidence_processor = assoc_evidence.AssocEvidenceProcessor(
            config=config
        )

        process_status = assoc_evidence_processor.process(
            evidence_type=evidence_type,
            pred_term=pred_term,
            subject_ents=self.SUBJECT_GWAS_ENTS,
            object_ents=self.OBJECT_GWAS_ENTS,
        )
        df = assoc_evidence_processor.evidence_df
        if evidence_type == "supporting":
            assert process_status
            assert len(df) > 0

    @pytest.mark.parametrize("pred_term, evidence_type", PARAMS)
    def test_api(self, pred_term, evidence_type):
        payload = {
            "subject_ents": self.SUBJECT_GWAS_ENTS,
            "object_ents": self.OBJECT_GWAS_ENTS,
            "pred_term": pred_term,
            "evidence_type": evidence_type,
        }
        url = "/evidence/association"
        with TestClient(app) as client:
            r = client.post(url, json=payload)
        assert r.ok
        if evidence_type == "supporting":
            assert len(r.json()["data"]) > 0
