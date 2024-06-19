#!/usr/bin/env python3
'''A module for fetching and caching web pages.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def data_cacher(method: Callable) -> Callable:
    '''A decorator function for caching the output of fetched data.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''A wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Fetches the content of a URL and caches the response.
    '''
    return requests.get(url).text