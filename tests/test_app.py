from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "devops-lab"


def test_metrics():
    client.get("/health")

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "devops_lab_http_requests_total" in response.text
    assert 'path="/health"' in response.text
    assert "devops_lab_http_request_duration_seconds" in response.text
