#!/usr/bin/env python3
"""
redis Cache
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
import uuid


def count_calls(method: Callable) -> Callable:
    '''count calls'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        '''
        count call wrapper
        increase count by 1
        '''
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''save input and outputs'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        '''
        call history wrapper
        '''
        self._redis.rpush(f'{key}:inputs', str(args))
        output = str(method(self, *args, **kwds))
        self._redis.rpush(f'{key}:outputs', output)
        return output
    return wrapper


def replay(method: Callable):
    '''
    replay method usage
    '''
    re = redis.Redis()
    name = method.__qualname__
    inputs = re.lrange(f'{name}:inputs', 0, -1)
    outputs = re.lrange(f'{name}:outputs', 0, -1)
    count = int(re.get(name))
    print(f'{name} was called {count} times')
    for i in zip(inputs, outputs):
        print(f'{name}(*{i[0].decode("utf-8")}) -> {i[1].decode("utf-8")}')


class Cache:
    '''Cache class to store data using redis'''

    def __init__(self):
        '''
        initialize redis client instance
        and flush db
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''store given data into redis with random uuid as the key'''
        uid = str(uuid.uuid4())
        self._redis.set(uid, data)
        return uid

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        '''get stored data using key and convert data type if prompted'''
        new_key = self._redis.get(key)
        if fn:
            new_key = fn(new_key)
        return new_key

    def get_str(self, key: str) -> str:
        '''convert to str'''
        new_key = self._redis.get(key)
        return new_key.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''convert to int'''
        new_key = self._redis.get(key)
        try:
            return int(new_key)
        except ValueError:
            return 0
