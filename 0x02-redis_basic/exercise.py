#!/usr/bin/env python3
"Writing strings to Redis"

from typing import Union
import redis
import uuid


class Cache:
    "Create redis cache"

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        "Srores the input data in Redis"
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
