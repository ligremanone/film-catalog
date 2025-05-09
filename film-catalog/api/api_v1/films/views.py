from typing import Annotated

from fastapi import Depends, APIRouter, status
from api.api_v1.films.crud import FILMS
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
    return FILMS


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
    return Film(
        **new_film.model_dump(),
        rating=0,
    )
