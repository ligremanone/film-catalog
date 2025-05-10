from typing import Annotated

from fastapi import Depends, APIRouter, status
from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film, FilmCreate

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get(
    "/",
    response_model=list[Film],
)
async def get_all_films():
    return storage.get()


@router.get("/{slug}")
async def get_film_by_slug(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
async def create_film(
    new_film: FilmCreate,
):
    return storage.create(new_film)
