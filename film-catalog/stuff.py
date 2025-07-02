from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
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
        ]
    )


if __name__ == "__main__":
    main()
