"""LinkCtl server — stub for workflow-pipeline E2E testing."""

from fastapi import FastAPI

app = FastAPI(title="LinkCtl", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
