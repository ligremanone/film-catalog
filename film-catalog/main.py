from fastapi import FastAPI, HTTPException, status, Depends
from schemas.film import Film
from typing import Annotated

app = FastAPI(name="Film Catalog")

FILMS = [
    Film(
        id=1,
        name="The Shawshank Redemption",
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        year=1994,
        rating=9.3,
    ),
    Film(
        id=2,
        name="The Godfather",
        description="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        year=1972,
        rating=9.2,
    ),
    Film(
        id=3,
        name="The Dark Knight",
        description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one that he can't control.",
        year=2008,
        rating=9.0,
    ),
]


@app.get(
    "/films/",
    response_model=list[Film],
)
async def get_all_films():
    return FILMS


async def prefetch_film(movie_id: int) -> Film:
    film: Film | None = next(
        (film for film in FILMS if film.id == movie_id),
        None,
    )
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film not found",
    )


@app.get("/films/{movie_id}")
async def get_film_by_id(
    film: Annotated[
        Film,
        Depends(prefetch_film),
    ],
):
    return film
