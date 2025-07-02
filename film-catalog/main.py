import logging

from fastapi import FastAPI, Request

from api import router as api_router
from app_lifespan import lifespan
from core.config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
)
app = FastAPI(
    name="Film Catalog",
    title="Film Catalog",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.get("/")
async def read_root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": "Welcome to film catalog",
        "docs": str(docs_url),
    }
