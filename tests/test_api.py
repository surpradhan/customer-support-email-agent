from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_followups_empty():
    response = client.get("/api/v1/followups")
    assert response.status_code == 200
    assert response.json()["followups"] == []


def test_followup_not_found():
    response = client.get("/api/v1/followups/nonexistent-id")
    assert response.status_code == 404
