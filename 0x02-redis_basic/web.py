#!/usr/bin/env python3
"""
    page content
"""
from functools import wraps
import redis
import requests
r = redis.Redis()


def counter(method):
    '''count link access'''
    @wraps(method)
    def wrapper(url):
        '''wrapper'''
        html = r.get(f'cache:{url}')
        if html:
            return html.decode('utf-8')
        html = method(url)
        r.incr(f'count:{url}')
        r.set(f'cache:{url}', html, ex=10)
        return html
    return wrapper


@counter
def get_page(url: str) -> str:
    '''
    return html content and count page visit times
    page vists are exipred after 10 secs
    '''
    x = requests.get(url)
    return x.text
