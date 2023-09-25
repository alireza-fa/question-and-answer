from typing import Any

from django.core.cache import cache


def set_cache(key: str, value: Any, timeout: int | None = None) -> None:
    if timeout:
        cache.set(key=key, value=value, timeout=timeout)
        cache.close()
    else:
        cache.set(key=key, value=value, timeout=86400)
        cache.close()


def get_cache(key: str) -> Any:
    value = cache.get(key=key)
    cache.close()
    return value


def incr(key: str) -> None:
    cache.incr(key=key)
    cache.close()
