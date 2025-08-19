import logging
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = f"{BASE_DIR}//db.json"
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_LEVEL: int = logging.INFO

REDIS_HOST: str = getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(getenv("REDIS_PORT", "0")) or 6379
REDIS_DB: int = 0

REDIS_DB_TOKENS = 1
REDIS_DB_SET_NAME = "tokens"

REDIS_DB_USERS = 2

REDIS_DB_FILMS = 3

REDIS_FILMS_HASH_NAME = "films"

DESCRIPTION_MAX_LENGTH = 200
