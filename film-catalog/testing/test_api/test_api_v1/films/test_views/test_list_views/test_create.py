import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from starlette.testclient import TestClient

from api.api_v1.films.crud import storage
from main import app
from schemas.film import Film, FilmCreate

pytestmark = pytest.mark.apitest


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
    storage.delete_by_slug(film_create.slug)


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


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("ab", "string_too_short"), id="minimal length"),
            pytest.param(("abc-abc-abc", "string_too_long"), id="minimal length"),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
        film: Film,
    ) -> tuple[dict[str, Any], str]:
        data = film.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_film")
        create_data, expected_err_type = movie_create_values
        response = auth_client.post(
            url,
            json=create_data,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        assert response.json()["detail"][0]["type"] == expected_err_type
