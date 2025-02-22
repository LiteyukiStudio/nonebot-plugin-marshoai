from ..models import Cache

cache = Cache()


def from_cache(key):
    """
    当缓存中有数据时，直接返回缓存中的数据，否则执行函数并将结果存入缓存
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            cached = cache.get(key)
            if cached:
                return cached
            else:
                result = await func(*args, **kwargs)
                cache.set(key, result)
                return result

        return wrapper

    return decorator


def update_to_cache(key):
    """
    执行函数并将结果存入缓存
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            cache.set(key, result)
            return result

        return wrapper

    return decorator
