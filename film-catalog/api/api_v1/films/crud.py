import json
from json import JSONDecodeError
from pathlib import Path
import logging
from pydantic import BaseModel
from redis import Redis

from core import config
from core.config import DB_PATH
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmUpdatePartial,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmCatalogStorage(BaseModel):
    def get(self) -> list[Film]:
        data = redis.hvals(name=config.REDIS_FILMS_HASH_NAME)
        return [Film.model_validate_json(value) for value in data]

    def get_by_slug(self, slug: str) -> Film | None:
        data = redis.hget(name=config.REDIS_FILMS_HASH_NAME, key=slug)
        if data:
            return Film.model_validate_json(data)
        return None

    @staticmethod
    def save_film(new_film: Film):
        return redis.hset(
            name=config.REDIS_FILMS_HASH_NAME,
            key=new_film.slug,
            value=new_film.model_dump_json(),
        )

    def create(self, new_film_in: FilmCreate) -> Film:
        new_film = Film(**new_film_in.model_dump(), rating=0)
        self.save_film(new_film)
        log.info(
            "Film %r created",
            new_film.name,
        )
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_FILMS_HASH_NAME,
            slug,
        )

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(self, film: Film, film_update: FilmUpdate) -> Film:
        for field_name, value in film_update:
            setattr(film, field_name, value)
        self.save_film(film)
        return film

    def update_partial(
        self, film: Film, film_update_partial: FilmUpdatePartial
    ) -> Film:
        for field_name, value in film_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(film, field_name, value)
        self.save_film(film)
        return film


storage = FilmCatalogStorage()
