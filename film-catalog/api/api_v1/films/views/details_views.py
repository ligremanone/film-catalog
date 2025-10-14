from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film, FilmRead, FilmUpdate, FilmUpdatePartial
from storage.films.crud import storage

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
) -> Film:
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_film(
    film: FilmBySlug,
) -> None:
    storage.delete(film)


@router.put(
    "/",
)
async def update_film_detail(
    film: FilmBySlug,
    film_update: FilmUpdate,
) -> Film:
    return storage.update(film, film_update)


@router.patch(
    "/",
)
async def update_film_partial(
    film: FilmBySlug,
    film_update_partial: FilmUpdatePartial,
) -> Film:
    return storage.update_partial(
        film,
        film_update_partial,
    )


@router.post(
    "/transfer/",
)
async def transfer_film(
    # film: FilmBySlug,
) -> dict[str, str]:
    return {"message": "work in progress"}
