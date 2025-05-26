import json
from json import JSONDecodeError
from pathlib import Path
import logging
from pydantic import BaseModel

from core.config import DB_PATH
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmUpdatePartial,
)

log = logging.getLogger(__name__)


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
        log.info(
            "Saved films to storage file",
        )

    @classmethod
    def from_data(cls) -> "FilmCatalogStorage":
        if not Path(DB_PATH).exists():
            log.info("Data not found")
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
        log.info(
            "Film '%s' created",
            new_film.name,
        )
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_film.pop(slug, None)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(self, film: Film, film_update: FilmUpdate) -> Film:
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

    def init_storage_from_data(self):
        try:
            data = FilmCatalogStorage().from_data()
        except JSONDecodeError:
            self.save_data()
            log.warning("Rewritten films storage file due to JSONDecodeError")
            return
        self.slug_to_film.update(data.slug_to_film)
        log.warning("Loaded films from storage file")


storage = FilmCatalogStorage()
