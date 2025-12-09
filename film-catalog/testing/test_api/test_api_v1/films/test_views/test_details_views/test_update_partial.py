from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.film import Film
from storage.films.crud import storage
from testing.conftest import create_film_random_slug

pytestmark = pytest.mark.apitest
DESCRIPTION_MAX_LENGTH = 200


class TestUpdatePartial:
    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[Film]:
        film = create_film_random_slug(
            description=request.param,
        )
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description",
        [
            pytest.param(
                "a description",
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                "",
                "new description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "",
                id="max-description-to-no-description",
            ),
            pytest.param(
                "",
                "a" * DESCRIPTION_MAX_LENGTH,
                id="no-description-to-max-description",
            ),
        ],
        indirect=[
            "film",
        ],
    )
    def test_update_film_partial(
        self,
        film: Film,
        auth_client: TestClient,
        new_description: str,
    ) -> None:
        url = app.url_path_for(
            "update_film_partial",
            slug=film.slug,
        )
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = storage.get_by_slug(film.slug)
        assert film_db
        assert film_db.description == new_description
