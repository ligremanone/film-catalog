from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "Rustam")
    redis.set("number", "24")
    redis.set("cat_name", "Barsik")
    print(redis.get("name"))
    print(
        [
            redis.get("number"),
            redis.get("cat_name"),
        ],
    )


if __name__ == "__main__":
    main()
