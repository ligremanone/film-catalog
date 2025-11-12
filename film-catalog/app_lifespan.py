from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.films import FilmCatalogStorage


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    app.state.films_storage = FilmCatalogStorage(
        films_hash_name=settings.redis.names.films_hash_name,
    )
    yield
