import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.film import Film
from storage.films.crud import storage
from testing.conftest import create_film


@pytest.fixture(
    params=[
        "some-slug",
        "slug",
        pytest.param(
            "abc",
            id="minimal length",
        ),
        pytest.param(
            "qwerty-abc",
            id="maximal length",
        ),
    ],
)
def film(request: SubRequest) -> Film:
    return create_film(request.param)


@pytest.mark.apitest
def test_delete_film(
    auth_client: TestClient,
    film: Film,
) -> None:
    url = app.url_path_for(
        "delete_film",
        slug=film.slug,
    )
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(film.slug)
