from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ping():
    r = client.get("/ping")
    assert r.json() is True
