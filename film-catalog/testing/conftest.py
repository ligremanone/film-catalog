import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from pydantic import AnyHttpUrl

from schemas.film import Film, FilmCreate
from storage.films.crud import storage


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
    url: AnyHttpUrl,
    description: str = "Some description",
    name: str = "Some Film",
) -> FilmCreate:
    return FilmCreate(
        slug=slug,
        name=name,
        description=description,
        year=2025,
        url=url,
    )


def build_film_create_random_slug(
    description: str = "Some description",
    name: str = "Some Film",
    url: AnyHttpUrl = "https://example.com",
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
        url=url,
    )


def create_film(
    slug: str,
    description: str = "Some description",
    name: str = "Some Film",
    url: AnyHttpUrl = "https://example.com",
) -> Film:
    new_film_in = build_film_create(
        slug,
        description=description,
        name=name,
        url=url,
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
