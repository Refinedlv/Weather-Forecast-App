import os
import json
from typing import Optional

class CacheManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def get_cached_data(self, key: str) -> Optional[dict]:
        path = self._get_cache_path(key)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return None

    def cache_data(self, key: str, data: dict):
        path = self._get_cache_path(key)
        with open(path, "w") as f:
            json.dump(data, f)

    def clear_cache(self, key: Optional[str] = None):
        if key:
            path = self._get_cache_path(key)
            if os.path.exists(path):
                os.remove(path)
        else:
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))
