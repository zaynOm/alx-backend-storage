#!/usr/bin/python3
""" Redis exercise """
import redis
import requests

r = redis.Redis()


def get_page(url: str) -> str:
    """Get page"""
    page_key = f"page:{url}"
    count_key = f"count:{url}"

    if r.get(page_key):
        r.incr(count_key)
        return r.get(page_key).decode("utf-8")

    response = requests.get(url)
    r.setex(page_key, 10, response.text)
    r.set(count_key, 1)
    return response.text


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
