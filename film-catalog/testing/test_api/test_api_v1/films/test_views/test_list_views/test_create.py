import random
import string

from fastapi import status
from starlette.testclient import TestClient

from main import app
from schemas.film import Film, FilmCreate


def test_create_film(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("create_film")
    film_create = FilmCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        name="Some Film",
        description="Some description",
        year=2025,
    )
    data: dict[str, str] = film_create.model_dump(mode="json")
    response = auth_client.post(
        url,
        json=data,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_data = FilmCreate(**response_data)
    assert received_data == film_create, response_data


def test_create_film_already_exists(auth_client: TestClient, film: Film) -> None:
    url = app.url_path_for("create_film")
    film_create = FilmCreate(**film.model_dump())
    data: dict[str, str] = film_create.model_dump(mode="json")
    response = auth_client.post(
        url,
        json=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    assert (
        response.json().get("detail") == f"Film with slug={film.slug!r} already exists"
    ), response.text
