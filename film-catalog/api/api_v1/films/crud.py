import json
from pathlib import Path

from pydantic import BaseModel

from core.config import DB_PATH
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmUpdatePartial,
)


class FilmCatalogStorage(BaseModel):
    slug_to_film: dict[str, Film] = {}

    def save_data(self):
        with open(
            DB_PATH,
            "w+",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.model_dump(),
                file,
                indent=4,
                ensure_ascii=False,
            )

    @classmethod
    def from_data(cls) -> "FilmCatalogStorage":
        if not Path(DB_PATH).exists():
            return FilmCatalogStorage()
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            return cls.model_validate(data)

    def get(self) -> list[Film]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_film.get(slug)

    def create(self, new_film_in: FilmCreate) -> Film:
        new_film = Film(**new_film_in.model_dump(), rating=0)
        self.slug_to_film[new_film.slug] = new_film
        self.save_data()
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.save_data()
        self.slug_to_film.pop(slug, None)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(self, film: Film, film_update: FilmUpdate) -> Film:
        for field_name, value in film_update:
            setattr(film, field_name, value)
        self.save_data()
        return film

    def update_partial(
        self, film: Film, film_update_partial: FilmUpdatePartial
    ) -> Film:
        for field_name, value in film_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(film, field_name, value)
        self.save_data()
        return film


try:
    storage = FilmCatalogStorage().from_data()
except ValueError:
    storage = FilmCatalogStorage()
    storage.save_data()
