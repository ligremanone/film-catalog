from redis import Redis

from core.config import settings
from services.auth.tokens_helper import AbstractTokenHelper


class RedisTokenHelper(AbstractTokenHelper):

    def __init__(self, host: str, port: int, db: int, tokens_set_name: str) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set_name

    def token_exists(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                self.tokens_set,
                token,
            ),
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(
            self.tokens_set,
            token,
        )

    def get_tokens(self) -> list[str]:
        return list(self.redis.smembers(self.tokens_set))

    def delete_token(
        self,
        token: str,
    ) -> None:
        self.redis.srem(
            self.tokens_set,
            token,
        )


redis_tokens = RedisTokenHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.tokens_db,
    tokens_set_name=settings.redis.names.tokens_set_name,
)
