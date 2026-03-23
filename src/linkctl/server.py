"""LinkCtl server — FastAPI application factory."""

import logging
import secrets
import sqlite3
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from linkctl.db import get_connection, init_db
from linkctl.models import LinkCreate, LinkResponse

logger = logging.getLogger("linkctl")


def create_app(db_path: Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    state: dict = {"start_time": time.monotonic(), "db": None}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        state["start_time"] = time.monotonic()
        conn = get_connection(db_path or Path(":memory:"))
        init_db(conn)
        state["db"] = conn
        logger.info("LinkCtl server started")
        yield
        if state["db"]:
            state["db"].close()
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

    @app.post("/links", status_code=201, response_model=LinkResponse)
    def create_link(link: LinkCreate, request: Request):
        db: sqlite3.Connection = state["db"]
        slug = link.slug or secrets.token_urlsafe(6)
        url_str = str(link.url)
        try:
            db.execute("INSERT INTO links (slug, url) VALUES (?, ?)", (slug, url_str))
            db.commit()
        except sqlite3.IntegrityError:
            raise StarletteHTTPException(status_code=409, detail=f"Slug '{slug}' already exists")
        base_url = str(request.base_url).rstrip("/")
        return LinkResponse(slug=slug, url=url_str, short_url=f"{base_url}/{slug}")

    return app


app = create_app()
