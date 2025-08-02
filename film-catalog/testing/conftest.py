import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate


@pytest.fixture(
    scope="session",
    autouse=True,
)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        msg = "Environment not ready for testing"
        pytest.exit(msg)


def build_film_create(
    slug: str,
    description: str = "Some description",
    name: str = "Some Film",
) -> FilmCreate:
    return FilmCreate(
        slug=slug,
        name=name,
        description=description,
        year=2025,
    )


def build_film_create_random_slug(
    description: str = "Some description",
    name: str = "Some Film",
) -> FilmCreate:
    return build_film_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description=description,
        name=name,
    )


def create_film(
    slug: str,
    description: str = "Some description",
    name: str = "Some Film",
) -> Film:
    new_film_in = build_film_create(
        slug,
        description=description,
        name=name,
    )
    return storage.create(new_film_in)


def create_film_random_slug(
    description: str = "Some description",
    name: str = "Some Film",
) -> Film:
    new_film_in = build_film_create_random_slug(
        description=description,
        name=name,
    )
    return storage.create(new_film_in)


@pytest.fixture()
def film() -> Generator[Film]:
    film = create_film_random_slug()
    yield film
    storage.delete(film)
