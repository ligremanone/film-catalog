import secrets

from redis import Redis
from core import config
from abc import ABC, abstractmethod


class AbstractTokenHelper(ABC):
    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        pass

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        pass

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(16)

    def generate_and_save_token(
        self,
        token: str,
    ) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


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
            )
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(
            self.tokens_set,
            token,
        )


redis_tokens = RedisTokenHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_DB_SET_NAME,
)
