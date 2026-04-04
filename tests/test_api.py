from unittest.mock import AsyncMock, patch

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


def test_process_email():
    mock_result = {
        "final_response": "Thank you for reaching out. We'd be happy to help with your refund.",
        "category": "refund_request",
        "sentiment": "neutral",
        "status": "sent",
        "requires_followup": False,
        "followup_reason": None,
        "conversation_id": "test-conv-abc123",
    }
    with patch("src.api.router.email_agent_graph.ainvoke", new=AsyncMock(return_value=mock_result)):
        response = client.post(
            "/api/v1/email/process",
            json={
                "from_email": "customer@example.com",
                "subject": "Request a refund",
                "body": "Hi, I would like to request a refund for my recent purchase.",
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "refund_request"
    assert data["sentiment"] == "neutral"
    assert data["status"] == "sent"
    assert data["reply_body"] == "Thank you for reaching out. We'd be happy to help with your refund."
    assert data["requires_followup"] is False
