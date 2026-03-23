"""Tests for error middleware — structured error responses."""

from fastapi.testclient import TestClient

from linkctl.server import create_app

client = TestClient(create_app())


def test_404_returns_json_error():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["status_code"] == 404


def test_404_includes_detail():
    response = client.get("/nonexistent")
    data = response.json()
    assert "detail" in data["error"]


def test_unhandled_exception_returns_500():
    """Test that unhandled exceptions return a structured 500 response."""
    app = create_app()

    @app.get("/boom")
    def boom():
        raise RuntimeError("something broke")

    test_client = TestClient(app, raise_server_exceptions=False)
    response = test_client.get("/boom")
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["status_code"] == 500
    assert "detail" in data["error"]
