#!/usr/bin/env python3
"""Redis Data storage module"""

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """Decorator to track the number of calls made to a method."""
    @wraps(method)
    def track_calls(self, *args, **kwargs) -> Any:
        """Increment call count and invoke the method."""
        if isinstance(self.cache, redis.Redis):
            self.cache.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return track_calls


def call_history(method: Callable) -> Callable:
    """Decorator to track the call history of a method."""
    @wraps(method)
    def track_history(self, *args, **kwargs) -> Any:
        """Store input/output details and invoke the method."""
        in_key = f"{method.__qualname__}:inputs"
        out_key = f"{method.__qualname__}:outputs"
        if isinstance(self.cache, redis.Redis):
            self.cache.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self.cache, redis.Redis):
            self.cache.rpush(out_key, output)
        return output
    return track_history


def replay(fn: Callable) -> None:
    """Replay call history of a method."""
    if not (fn and hasattr(fn, "__self__")):
        return
    redis_store = getattr(fn.__self__, "cache", None)
    if not isinstance(redis_store, redis.Redis):
        return
    method_name = fn.__qualname__
    in_key = f"{method_name}:inputs"
    out_key = f"{method_name}:outputs"
    method_calls = int(redis_store.get(method_name) or 0)
    print(f"{method_name} was called {method_calls} times:")
    method_inputs = redis_store.lrange(in_key, 0, -1)
    method_outputs = redis_store.lrange(out_key, 0, -1)
    for method_input, method_output in zip(method_inputs, method_outputs):
        print(f"{method_name}(*{method_input.decode('utf-8')}) -> {method_output}")


class Cache:
    """Represents an object for storing data in a Redis data storage."""
    def __init__(self) -> None:
        """Initialize a Cache instance."""
        self.cache = redis.Redis()
        self.cache.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a value in a Redis data storage and return the key."""
        data_key = str(uuid.uuid4())
        self.cache.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve a value from a Redis data storage."""
        data = self.cache.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """Retrieve a string value from a Redis data storage."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve an integer value from a Redis data storage."""
        return self.get(key, int)
