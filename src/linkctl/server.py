"""LinkCtl server — FastAPI application factory."""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("linkctl")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    state = {"start_time": time.monotonic()}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        state["start_time"] = time.monotonic()
        logger.info("LinkCtl server started")
        yield
        logger.info("LinkCtl server shutting down")

    app = FastAPI(title="LinkCtl", version="0.1.0", lifespan=lifespan)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"status_code": exc.status_code, "detail": exc.detail}},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": {"status_code": 500, "detail": "Internal server error"}},
        )

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "version": app.version,
            "uptime_seconds": round(time.monotonic() - state["start_time"], 2),
        }

    return app


app = create_app()
