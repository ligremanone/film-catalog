from typing import Annotated

from fastapi import APIRouter, Depends, status, BackgroundTasks

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film, FilmUpdate, FilmUpdatePartial, FilmRead

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film with 'slug' slug not found",
                    },
                },
            },
        },
    },
)

FilmBySlug = Annotated[Film, Depends(prefetch_film)]


@router.get(
    "/",
    response_model=FilmRead,
)
async def get_film_by_slug(
    film: FilmBySlug,
):
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_film(
    film: FilmBySlug,
):
    storage.delete(film)


@router.put(
    "/",
    response_model=Film,
)
async def update_film_detail(
    film: FilmBySlug,
    film_update: FilmUpdate,
) -> Film:
    return storage.update(film, film_update)


@router.patch(
    "/",
    response_model=Film,
)
async def update_film_partial(
    film: FilmBySlug,
    film_update_partial: FilmUpdatePartial,
) -> Film:
    return storage.update_partial(
        film,
        film_update_partial,
    )
