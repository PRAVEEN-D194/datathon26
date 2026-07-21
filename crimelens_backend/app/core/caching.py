import json
from typing import Optional
from app.core.config import settings

class CacheManager:
    """
    Redis cache manager with fallback local dictionary caching to guarantee 
    instant hackathon execution in any offline environment.
    """
    def __init__(self):
        self._local_cache = {}
        self._redis = None
        
        if settings.REDIS_URL:
            try:
                import redis
                self._redis = redis.from_url(settings.REDIS_URL)
            except Exception:
                pass

    def get(self, key: str) -> Optional[dict]:
        if self._redis:
            try:
                val = self._redis.get(key)
                if val:
                    return json.loads(val)
            except Exception:
                pass
        return self._local_cache.get(key)

    def set(self, key: str, value: dict, expire: int = 3600):
        if self._redis:
            try:
                self._redis.setex(key, expire, json.dumps(value))
                return
            except Exception:
                pass
        self._local_cache[key] = value

    def delete(self, key: str):
        if self._redis:
            try:
                self._redis.delete(key)
                return
            except Exception:
                pass
        if key in self._local_cache:
            del self._local_cache[key]

cache = CacheManager()
