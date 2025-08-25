import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


DESCRIPTION_MAX_LENGTH = 200


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisNamesConfig(BaseModel):
    tokens_set_name: str = "tokens"
    films_hash_name: str = "films"


class RedisDBConfig(BaseModel):
    db: int = 0
    tokens_db: int = 1
    users_db: int = 2
    films_db: int = 3


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDBConfig = RedisDBConfig()
    names: RedisNamesConfig = RedisNamesConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
