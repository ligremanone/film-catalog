from fastapi import HTTPException, status

from api.api_v1.films.crud import storage
from schemas.film import Film


async def prefetch_film(slug: str) -> Film:
    film = storage.get_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug!r} slug not found",
    )
