import logging

from pydantic import BaseModel
from redis import Redis

from core import config
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


class FilmError(Exception):
    """
    Base exception class for film related errors
    """


class FilmAlreadyExistsError(FilmError):
    """
    Raised when a film with the same slug already exists
    """


class FilmCatalogStorage(BaseModel):
    def get(self) -> list[Film]:
        data = redis.hvals(name=config.REDIS_FILMS_HASH_NAME)
        return [Film.model_validate_json(value) for value in data]

    def get_by_slug(self, slug: str) -> Film | None:
        data = redis.hget(name=config.REDIS_FILMS_HASH_NAME, key=slug)
        if data:
            return Film.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(redis.hexists(name=config.REDIS_FILMS_HASH_NAME, key=slug))

    @staticmethod
    def save_film(new_film: Film) -> None:
        redis.hset(
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

    def create_or_raise_if_exists(self, new_film_in: FilmCreate) -> Film:
        if not self.exists(new_film_in.slug):
            return self.create(new_film_in)
        raise FilmAlreadyExistsError(new_film_in.slug)

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
        self, film: Film, film_update_partial: FilmUpdatePartial,
    ) -> Film:
        for field_name, value in film_update_partial.model_dump(
            exclude_unset=True,
        ).items():
            setattr(film, field_name, value)
        self.save_film(film)
        return film


storage = FilmCatalogStorage()
