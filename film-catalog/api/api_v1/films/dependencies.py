import logging
from typing import Annotated

from fastapi import HTTPException, status, BackgroundTasks, Request, Query

from api.api_v1.films.crud import storage
from core.config import API_TOKENS
from schemas.film import Film

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


async def prefetch_film(slug: str) -> Film:
    film = storage.get_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug!r} slug not found",
    )


def save_storage_data(
    background_tasks: BackgroundTasks,
    request: Request,
):
    yield
    if request.method not in UNSAFE_METHODS:
        return
    log.info("Add background task to save data")
    background_tasks.add_task(storage.save_data)


def check_api_token(api_token: Annotated[str, Query]):
    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )
