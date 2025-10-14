import logging

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.film import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmUpdatePartial,
)
from storage.films.exceptions import FilmAlreadyExistsError

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.films_db,
    decode_responses=True,
)


class FilmCatalogStorage(BaseModel):
    films_hash_name: str

    def get(self) -> list[Film]:
        data = redis.hvals(name=self.films_hash_name)
        return [Film.model_validate_json(value) for value in data]

    def get_by_slug(self, slug: str) -> Film | None:
        data = redis.hget(name=self.films_hash_name, key=slug)
        if data:
            return Film.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(redis.hexists(name=self.films_hash_name, key=slug))

    def save_film(self, new_film: Film) -> None:
        redis.hset(
            name=self.films_hash_name,
            key=new_film.slug,
            value=new_film.model_dump_json(),
        )

    def clear(self) -> None:
        redis.delete(self.films_hash_name)

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
            self.films_hash_name,
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
        self,
        film: Film,
        film_update_partial: FilmUpdatePartial,
    ) -> Film:
        for field_name, value in film_update_partial.model_dump(
            exclude_unset=True,
        ).items():
            setattr(film, field_name, value)
        self.save_film(film)
        return film


storage = FilmCatalogStorage(films_hash_name=settings.redis.names.films_hash_name)
