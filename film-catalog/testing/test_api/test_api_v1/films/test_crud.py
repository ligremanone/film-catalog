from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.films.crud import FilmAlreadyExistsError, storage
from schemas.film import Film, FilmCreate, FilmUpdate, FilmUpdatePartial
from testing.conftest import build_film_create_random_slug, create_film_random_slug


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = create_film_random_slug()

    def tearDown(self) -> None:
        storage.delete(self.film)

    def test_update(self) -> None:
        film_update = FilmUpdate(
            **self.film.model_dump(),
        )
        source_description = self.film.description
        film_update.description = "new description"
        updated_film = storage.update(self.film, film_update)
        self.assertNotEqual(
            source_description,
            updated_film.description,
        )
        self.assertEqual(
            film_update,
            FilmUpdate(**updated_film.model_dump()),
        )

    def test_update_partial(self) -> None:
        film_partial_update = FilmUpdatePartial(
            description="new description for partial update",
        )
        source_description = self.film.description
        updated_film = storage.update_partial(self.film, film_partial_update)
        self.assertNotEqual(
            source_description,
            updated_film.description,
        )
        self.assertEqual(
            film_partial_update.description,
            updated_film.description,
        )


class FilmStorageGetTestCase(TestCase):
    FILMS_COUNT = 5
    films: ClassVar[list[Film]] = []

    @classmethod
    def setUpClass(cls) -> None:
        storage.clear()
        cls.films = [create_film_random_slug() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete(film)

    def test_get_list(self) -> None:
        films = storage.get()
        expected_slugs = {f.slug for f in self.films}
        slugs = {f.slug for f in films}
        self.assertEqual(
            expected_slugs,
            slugs,
        )

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(
                slug=film.slug,
                msg=f"Validate can get slug {film.slug!r}",
            ):
                db_film = storage.get_by_slug(film.slug)
                self.assertEqual(
                    film,
                    db_film,
                )


def test_create_or_raise_if_exists(film: Film) -> None:
    film_create = FilmCreate(**film.model_dump())
    with pytest.raises(
        FilmAlreadyExistsError,
        match=film_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(film_create)
    assert exc_info.value.args[0] == film_create.slug


def test_create_twice() -> None:
    film_create = build_film_create_random_slug()
    storage.create_or_raise_if_exists(film_create)
    with pytest.raises(
        FilmAlreadyExistsError,
        match=film_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(film_create)
    assert exc_info.value.args[0] == film_create.slug
