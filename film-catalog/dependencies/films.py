from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from starlette import status

from schemas.film import Film
from storage.films import FilmCatalogStorage


def get_films_storage(request: Request) -> FilmCatalogStorage | Any:  # noqa: ANN401
    return request.app.state.films_storage


GetFilmsStorage = Annotated[FilmCatalogStorage, Depends(get_films_storage)]


async def prefetch_film(
    slug: str,
    storage: GetFilmsStorage,
) -> Film:
    film = storage.get_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug!r} slug not found",
    )


FilmBySlug = Annotated[Film, Depends(prefetch_film)]
