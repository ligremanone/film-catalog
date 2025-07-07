from unittest import TestCase

from schemas.film import Film, FilmCreate, FilmUpdate, FilmUpdatePartial


class FilmCreateTestCase(TestCase):
    def test_film_can_be_created_from_create_schema(self) -> None:
        film_in = FilmCreate(
            slug="some-slug",
            name="Some Film",
            year=2022,
            description="Some description",
        )
        film = Film(
            **film_in.model_dump(),
            rating=0,
        )
        self.assertEqual(film_in.slug, film.slug)
        self.assertEqual(film_in.name, film.name)
        self.assertEqual(film_in.year, film.year)
        self.assertEqual(film_in.description, film.description)

    def test_film_create_accepts_different_name(self) -> None:
        names = [
            "Some Film",
            "AB" * 50,
            "New Film",
        ]
        for name in names:
            with self.subTest(name=name, msg=f"test-name-{name}"):
                film_create = FilmCreate(
                    slug="some-slug",
                    name=name,
                    year=2022,
                    description="Some description",
                )
                self.assertEqual(
                    name,
                    film_create.name,
                )

    def test_film_create_accepts_different_year(self) -> None:
        years = [
            2022,
            2023,
            2024,
        ]
        for year in years:
            with self.subTest(year=year, msg=f"test-year-{year}"):
                film_create = FilmCreate(
                    slug="some-slug",
                    name="Some Film",
                    year=year,
                    description="Some description",
                )
                self.assertEqual(
                    year,
                    film_create.year,
                )


class FilmUpdateTestCase(TestCase):
    def test_film_can_be_updated_from_update_schema(self) -> None:
        film_in = FilmUpdate(
            name="Some Film",
            year=2022,
            description="Some description",
        )
        film = Film(
            **film_in.model_dump(),
            slug="some-slug",
            rating=0,
        )
        self.assertEqual(film_in.name, film.name)
        self.assertEqual(film_in.year, film.year)
        self.assertEqual(film_in.description, film.description)


class FilmUpdatePartialTestCase(TestCase):
    def test_film_can_be_updated_from_update_partial_schema(self) -> None:
        film = FilmCreate(
            slug="some-slug",
            name="Some Film",
            year=2022,
            description="Some description",
        )
        film_in = FilmUpdatePartial(
            description="New description",
        )
        new_film = Film(
            slug=film.slug,
            name=film.name if not film_in.name else film_in.name,
            year=film.year if not film_in.year else film_in.year,
            description=(
                film.description if not film_in.description else film_in.description
            ),
            rating=0,
        )
        self.assertEqual(
            film.name,
            new_film.name,
        )
        self.assertEqual(film.year, new_film.year)
        self.assertEqual(film_in.description, new_film.description)
