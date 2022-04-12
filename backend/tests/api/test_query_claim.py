from pprint import pprint

from common_processing import claim_parsing
from starlette.testclient import TestClient

from app.main import app
from app.settings import config


class TestTextParser:
    CLAIM_TEXT = """\
There is a major epidemic of obesity, and many obese patients suffer with respiratory symptoms and disease. The overall impact of obesity on lung function is multifactorial, related to mechanical and inflammatory aspects of obesity. Areas covered: Obesity causes substantial changes to the mechanics of the lungs and chest wall, and these mechanical changes cause asthma and asthma-like symptoms such as dyspnea, wheeze, and airway hyperresponsiveness. Excess adiposity is also associated with increased production of inflammatory cytokines and immune cells that may also lead to disease. This article reviews the literature addressing the relationship between obesity and lung function, and studies addressing how the mechanical and inflammatory effects of obesity might lead to changes in lung mechanics and pulmonary function in obese adults and children. Expert commentary: Obesity has significant effects on respiratory function, which contribute significantly to the burden of respiratory disease. These mechanical effects are not readily quantified with conventional pulmonary function testing and measurement of body mass index. Changes in mediators produced by adipose tissue likely also contribute to altered lung function, though as of yet this is poorly understood.
"""

    def test_processing(self):
        claim_text = self.CLAIM_TEXT
        claim_parser = claim_parsing.ClaimParser(config=config)
        claim_parser.parse_claim(claim_text=claim_text)
        triple_df = claim_parser.triple_df
        triple_items = claim_parser.triple_items
        invalid_triple_items = claim_parser.invalid_triple_items
        print(triple_df)
        pprint(triple_items)
        pprint(invalid_triple_items)
        assert len(triple_df) > 0
        assert len(triple_items) > 0

    def test_api(self):
        payload = {"claim_text": self.CLAIM_TEXT}
        with TestClient(app) as client:
            r = client.post("/claim_parsing/parse", json=payload)
        assert r.ok


class TestInvalidTripleText:
    CLAIM_TEXT = "There is a major epidemic of obesity, and many obese patients suffer with respiratory symptoms and disease."

    def test_processing(self):
        claim_text = self.CLAIM_TEXT
        claim_parser = claim_parsing.ClaimParser(config=config)
        claim_parser.parse_claim(claim_text=claim_text)
        triple_df = claim_parser.triple_df
        triple_items = claim_parser.triple_items
        invalid_triple_items = claim_parser.invalid_triple_items
        print(triple_df)
        pprint(triple_items)
        pprint(invalid_triple_items)
        assert len(triple_df) == 0
        assert len(triple_items) == 0
        assert len(invalid_triple_items) > 0

    def test_api(self):
        payload = {"claim_text": self.CLAIM_TEXT}
        with TestClient(app) as client:
            r = client.post("/claim_parsing/parse", json=payload)
        assert r.ok


class TestBullshitText:
    CLAIM_TEXT = "A quick brown fox jumps over the lazy dog."

    def test_processing(self):
        claim_text = self.CLAIM_TEXT
        claim_parser = claim_parsing.ClaimParser(config=config)
        claim_parser.parse_claim(claim_text=claim_text)
        triple_df = claim_parser.triple_df
        triple_items = claim_parser.triple_items
        invalid_triple_items = claim_parser.invalid_triple_items
        print(triple_df)
        pprint(triple_items)
        pprint(invalid_triple_items)
        assert len(triple_df) == 0
        assert len(triple_items) == 0
        assert len(invalid_triple_items) == 0

    def test_api(self):
        payload = {"claim_text": self.CLAIM_TEXT}
        with TestClient(app) as client:
            r = client.post("/claim_parsing/parse", json=payload)
        assert r.ok
