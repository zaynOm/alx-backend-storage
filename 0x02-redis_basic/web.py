#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""The module-level Redis instance.
"""


def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data."""

    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function for caching the output."""
        redis_store.incr(f"count:{url}")
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return requests.get(url).text


# #!/usr/bin/env python3
# "Implementing an expiring web cache and tracker"
#
# import redis
# import requests
# from functools import wraps
# from typing import Callable
#
#
# def cache_page(f: Callable) -> Callable:
#     "Cache the page for 10 sec and track number of calls"
#
#     @wraps(f)
#     def wrapper(url):
#         "wrapper func"
#         with redis.Redis() as r:
#             cache_key = f"cache:{url}"
#             count_key = f"count:{url}"
#
#             r.incr(count_key)
#             cached_page = r.get(cache_key)
#             if cached_page:
#                 return cached_page.decode("utf-8")
#             res = f(url)
#             r.setex(cache_key, 10, res)
#             r.set(count_key, 1)
#
#             return res
#
#     return wrapper
#
#
# @cache_page
# def get_page(url: str) -> str:
#     "obtain the HTML content of a page"
#     return requests.get(url).text
