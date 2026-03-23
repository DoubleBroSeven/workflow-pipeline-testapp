"""Tests for the app factory and server setup."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from linkctl.server import create_app


def test_create_app_returns_fastapi_instance():
    app = create_app()
    assert isinstance(app, FastAPI)


def test_create_app_has_title():
    app = create_app()
    assert app.title == "LinkCtl"


def test_create_app_has_version():
    app = create_app()
    assert app.version == "0.1.0"


def test_app_responds_to_requests():
    app = create_app()
    client = TestClient(app)
    # Root endpoint should return something (even if just 404 for now)
    # The app should at minimum not crash on a request
    response = client.get("/health")
    assert response.status_code == 200
