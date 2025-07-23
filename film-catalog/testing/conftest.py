import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate

if getenv("TESTING") != "1":
    msg = "Environment not ready for testing"
    pytest.exit(msg)


def create_film() -> Film:
    new_film_in = FilmCreate(
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
    return storage.create(new_film_in)


@pytest.fixture()
def film() -> Generator[Film]:
    film = create_film()
    yield film
    storage.delete(film)
