"""Pydantic models for link operations."""

from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl
    slug: str | None = None


class LinkResponse(BaseModel):
    slug: str
    url: str
    short_url: str
