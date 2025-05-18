from pydantic import BaseModel

from schemas.film import Film, FilmCreate, FilmUpdate, FilmUpdatePartial


class FilmCatalogStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, new_film_in: FilmCreate) -> Film:
        new_film = Film(**new_film_in.model_dump(), rating=0)
        self.slug_to_film[new_film.slug] = new_film
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def updade(self, film: Film, film_update: FilmUpdate) -> Film:
        for field_name, value in film_update:
            setattr(film, field_name, value)
        return film

    def update_partial(
        self, film: Film, film_update_partial: FilmUpdatePartial
    ) -> Film:
        for field_name, value in film_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(film, field_name, value)
        return film


storage = FilmCatalogStorage()
storage.create(
    FilmCreate(
        slug="the-shawshank-redemption",
        name="The Shawshank Redemption",
        description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        year=1994,
    )
)
storage.create(
    FilmCreate(
        slug="the-godfather",
        name="The Godfather",
        description="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        year=1972,
    )
)
storage.create(
    FilmCreate(
        slug="the-dark-knight",
        name="The Dark Knight",
        description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one that he can't control.",
        year=2008,
    )
)
