from .instances import cache


def from_cache(key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            cached = cache.get(key)
            if cached:
                return cached
            else:
                result = func(*args, **kwargs)
                cache.set(key, result)
                return result

        return wrapper
