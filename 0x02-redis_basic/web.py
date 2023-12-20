#!/usr/bin/env python3
"""
    page content with cache and count
"""
from functools import wraps
import redis
import requests
from typing import Callable
r = redis.Redis()


def url_counter(method: Callable) -> Callable:
    '''count link access'''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''wrapper for caching site content and counting access'''
        html = r.get(f'cache:{url}')
        r.incr(f'count:{url}')
        if html:
            return html.decode('utf-8')
        html = method(url)
        r.setex(f'cache:{url}', 10, html)
        return html
    return wrapper


@url_counter
def get_page(url: str) -> str:
    '''
    return html content and count page visit times
    page vists are exipred after 10 secs
    '''
    x = requests.get(url)
    return x.text
