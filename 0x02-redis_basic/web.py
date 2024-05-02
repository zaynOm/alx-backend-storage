#!/usr/bin/env python3
"Implementing an expiring web cache and tracker"

from functools import wraps
import redis
import requests


def cache_page(f):
    "Cache the page for 10 sec and track number of calls"

    @wraps(f)
    def wrapper(*args, **kwds):
        with redis.Redis() as r:
            cache_key = "cache: {args[0]}"
            count_key = f"count:{args[0]}"

            cached_page = r.get(cache_key)
            if cached_page:
                res = cached_page.decode("utf-8")
            else:
                res = f(*args, **kwds)
                r.setex(cache_key, 10, res)

            r.incr(count_key)

            return res

    return wrapper


@cache_page
def get_page(url: str) -> str:
    "obtain the HTML content of a page"
    res = requests.get(url)
    return res.text
