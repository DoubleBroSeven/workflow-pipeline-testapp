"""Tests for the health endpoint."""

from fastapi.testclient import TestClient

from linkctl.server import create_app

client = TestClient(create_app())


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_includes_status():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_includes_version():
    response = client.get("/health")
    data = response.json()
    assert data["version"] == "0.1.0"


def test_health_includes_uptime_seconds():
    response = client.get("/health")
    data = response.json()
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0
