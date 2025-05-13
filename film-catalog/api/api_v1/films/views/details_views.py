from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film

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


@router.get("/")
async def get_film_by_slug(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_film(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    storage.delete(film)
