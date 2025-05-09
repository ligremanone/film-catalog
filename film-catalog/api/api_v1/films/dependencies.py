from fastapi import HTTPException, status

from api.api_v1.films.crud import FILMS
from schemas.film import Film


async def prefetch_film(slug: str) -> Film:
    film: Film | None = next(
        (film for film in FILMS if film.slug == slug),
        None,
    )
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug!r} slug not found",
    )
