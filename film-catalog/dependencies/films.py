from typing import Annotated

from fastapi import Depends, Request

from storage.films import FilmCatalogStorage


def get_films_storage(request: Request) -> FilmCatalogStorage:
    return request.app.state.films_storage


GetFilmsStorage = Annotated[FilmCatalogStorage, Depends(get_films_storage)]
