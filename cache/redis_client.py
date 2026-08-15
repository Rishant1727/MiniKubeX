import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def set_value(
    key: str,
    value: str,
    expiration: int | None = None
):

    redis_client.set(
        key,
        value,
        ex=expiration
    )


def get_value(
    key: str
):

    return redis_client.get(key)


def delete_value(
    key: str
):

    redis_client.delete(key)