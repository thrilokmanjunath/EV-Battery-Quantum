import json
import functools
import redis.asyncio as redis
from typing import Any, Callable

# Create Redis connection
redis_client = redis.from_url("redis://redis:6379/0", decode_responses=True)

def cache_response(ttl: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a cache key based on the function name and arguments
            key_parts = [func.__name__]
            
            def get_cacheable_str(val):
                type_name = type(val).__name__
                if type_name in ("BackgroundTasks", "Request", "Response", "Session"):
                    return None
                if hasattr(val, "model_dump_json"):
                    return val.model_dump_json()
                if hasattr(val, "dict") and callable(getattr(val, "dict")):
                    import json
                    try:
                        return json.dumps(val.dict(), sort_keys=True)
                    except Exception:
                        pass
                if isinstance(val, dict):
                    import json
                    try:
                        return json.dumps(val, sort_keys=True)
                    except Exception:
                        pass
                return str(val)

            for arg in args:
                s = get_cacheable_str(arg)
                if s is not None:
                    key_parts.append(s)
            for k, v in sorted(kwargs.items()):
                s = get_cacheable_str(v)
                if s is not None:
                    key_parts.append(f"{k}={s}")
                    
            cache_key = ":".join(key_parts)
            
            # Try to get the cached response
            try:
                cached_value = await redis_client.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)
            except Exception as e:
                # If Redis is down, just fall back to the function
                pass
            
            # Call the function if not cached
            # If the route is async, await it; else call it
            import asyncio
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = await asyncio.to_thread(func, *args, **kwargs)
            
            # Cache the result
            try:
                await redis_client.set(cache_key, json.dumps(result), ex=ttl)
            except Exception as e:
                pass
            
            return result
        return wrapper
    return decorator
