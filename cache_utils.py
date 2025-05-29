from functools import lru_cache, wraps
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional, Tuple
import hashlib
import json

class TimedLRUCache:
    def __init__(self, maxsize: int = 128, ttl: int = 1800):  # 1800 seconds = 30 minutes
        self.cache = {}
        self.maxsize = maxsize
        self.ttl = ttl

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a unique cache key based on function name and arguments."""
        # Convert args and kwargs to a stable string representation
        key_parts = [func_name]
        if args:
            key_parts.extend([str(arg) for arg in args])
        if kwargs:
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        
        # Create a hash of the key parts
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate a unique key for this function call
            key = self._generate_key(func.__name__, args, kwargs)
            
            # Check if the result is in cache and not expired
            if key in self.cache:
                result, timestamp = self.cache[key]
                if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                    return result
                else:
                    # Remove expired cache entry
                    del self.cache[key]
            
            # Get fresh result
            result = func(*args, **kwargs)
            
            # Store in cache with timestamp
            if len(self.cache) >= self.maxsize:
                # Remove oldest entry if cache is full
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                del self.cache[oldest_key]
            
            self.cache[key] = (result, datetime.now())
            return result
        
        return wrapper

# Create separate cache instances for different types of data
coordinates_cache = TimedLRUCache(maxsize=100, ttl=1800)  # Cache for coordinates
weather_cache = TimedLRUCache(maxsize=100, ttl=1800)      # Cache for weather data
forecast_cache = TimedLRUCache(maxsize=100, ttl=1800)     # Cache for forecast data 