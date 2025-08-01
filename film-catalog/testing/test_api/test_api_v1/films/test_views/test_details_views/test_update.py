from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.films.crud import storage
from main import app
from schemas.film import Film, FilmUpdate
from testing.conftest import create_film_random_slug


class TestUpdate:
    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[Film]:
        description, title = request.param
        film = create_film_random_slug(
            description=description,
            name=title,
        )
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description, new_title",
        [
            pytest.param(
                (
                    "some description",
                    "some title",
                ),
                "some description",
                "new title",
                id="same-title-and-new-title",
            ),
            pytest.param(
                (
                    "some description",
                    "some title",
                ),
                "new description",
                "new title",
                id="new-title-and-new-title",
            ),
        ],
        indirect=[
            "film",
        ],
    )
    def test_update_film_details(
        self,
        film: Film,
        auth_client: TestClient,
        new_description: str,
        new_title: str,
    ) -> None:
        url = app.url_path_for(
            "update_film_detail",
            slug=film.slug,
        )
        update = FilmUpdate(
            description=new_description,
            name=new_title,
            year=film.year,
        )
        response = auth_client.put(
            url,
            json=update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = storage.get_by_slug(film.slug)
        assert film_db
        new_data = FilmUpdate(**film_db.model_dump())
        assert new_data == update
