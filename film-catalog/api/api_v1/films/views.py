from typing import Annotated

from fastapi import Depends, APIRouter

from api.api_v1.films.crud import FILMS
from api.api_v1.films.dependencies import prefetch_film
from schemas.film import Film

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


@router.get("/{movie_id}")
async def get_film_by_id(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
