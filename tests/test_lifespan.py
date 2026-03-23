"""Tests for graceful shutdown via FastAPI lifespan."""

import logging

from fastapi.testclient import TestClient

from linkctl.server import create_app


def test_app_starts_and_shuts_down_cleanly():
    """The app should start and shut down without errors via lifespan."""
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
    # If we get here without exception, shutdown was clean


def test_health_reports_uptime_after_startup():
    """After startup, uptime should be a non-negative number."""
    app = create_app()
    with TestClient(app) as client:
        data = client.get("/health").json()
        assert data["uptime_seconds"] >= 0


def test_lifespan_logs_startup(caplog):
    """Lifespan should log on startup."""
    app = create_app()
    with caplog.at_level(logging.INFO, logger="linkctl"):
        with TestClient(app):
            pass
    assert any("started" in record.message.lower() for record in caplog.records)


def test_lifespan_logs_shutdown(caplog):
    """Lifespan should log on shutdown."""
    app = create_app()
    with caplog.at_level(logging.INFO, logger="linkctl"):
        with TestClient(app):
            pass
    assert any("shutting down" in record.message.lower() for record in caplog.records)
