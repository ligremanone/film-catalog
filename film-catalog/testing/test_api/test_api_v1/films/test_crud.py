import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate, FilmUpdate, FilmUpdatePartial

if getenv("TESTING") != "1":
    msg = "Environment not ready for testing"
    raise OSError(msg)


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = self.create_film()

    def tearDown(self) -> None:
        storage.delete(self.film)

    def create_film(self) -> Film:
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
