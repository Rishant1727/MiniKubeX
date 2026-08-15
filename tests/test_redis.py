from cache.redis_client import (
    set_value,
    get_value,
    delete_value
)


def test_redis_operations():

    set_value(
        "test-key",
        "hello"
    )

    result = get_value(
        "test-key"
    )

    assert result == "hello"

    delete_value(
        "test-key"
    )

    assert get_value(
        "test-key"
    ) is None