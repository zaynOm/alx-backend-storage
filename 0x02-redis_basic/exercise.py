#!/usr/bin/env python3
"Writing strings to Redis"

from functools import wraps
from typing import Callable, Optional, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    "Incrementing values"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        "keep track of func calls"
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


class Cache:
    "Create redis cache"

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        "Srores the input data in Redis"
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        "Retrive stored data"
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        "Retrive stored string"
        return self.get(key, str)

    def get_int(self, key: int) -> int:
        "Retrive stored integer"
        return self.get(key, int)
