from fastapi import APIRouter, status, Depends
from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.film import Film, FilmCreate, FilmRead

router = APIRouter(
    prefix="/films",
    tags=["films"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[FilmRead],
)
async def get_all_films():
    return storage.get()


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
async def create_film(
    new_film: FilmCreate,
):
    return storage.create(new_film)
