"""LinkCtl server — FastAPI application factory."""

import time

from fastapi import FastAPI

_start_time: float = time.monotonic()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="LinkCtl", version="0.1.0")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "version": app.version,
            "uptime_seconds": round(time.monotonic() - _start_time, 2),
        }

    return app


app = create_app()
