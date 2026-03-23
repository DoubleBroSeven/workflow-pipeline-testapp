"""Tests for creating shortened links (E2-001)."""

import pytest
from fastapi.testclient import TestClient

from linkctl.server import create_app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c


def test_create_link_returns_201(client):
    response = client.post("/links", json={"url": "https://example.com"})
    assert response.status_code == 201


def test_create_link_returns_slug(client):
    response = client.post("/links", json={"url": "https://example.com"})
    data = response.json()
    assert "slug" in data
    assert len(data["slug"]) >= 4


def test_create_link_returns_short_url(client):
    response = client.post("/links", json={"url": "https://example.com"})
    data = response.json()
    assert "short_url" in data
    assert data["slug"] in data["short_url"]


def test_create_link_stores_original_url(client):
    response = client.post("/links", json={"url": "https://example.com/page"})
    data = response.json()
    assert data["url"] == "https://example.com/page"


def test_create_link_with_custom_slug(client):
    response = client.post("/links", json={"url": "https://example.com", "slug": "my-link"})
    data = response.json()
    assert data["slug"] == "my-link"


def test_create_link_rejects_missing_url(client):
    response = client.post("/links", json={})
    assert response.status_code == 422


def test_create_link_rejects_invalid_url(client):
    response = client.post("/links", json={"url": "not-a-url"})
    assert response.status_code == 422
