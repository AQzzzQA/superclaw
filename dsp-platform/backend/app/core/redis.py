"""
Redis Configuration and Management
"""

import redis
from typing import Optional, Any
import json

from app.core.config import settings

# Create Redis connection pool
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
    decode_responses=True
)

# Redis client
redis_client = redis.Redis(connection_pool=redis_pool)


def check_redis_connection() -> bool:
    """Check if Redis connection is healthy"""
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False


def set_cache(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set a value in Redis cache
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (optional)
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if ttl:
            return redis_client.setex(key, ttl, json.dumps(value, ensure_ascii=False))
        else:
            return redis_client.set(key, json.dumps(value, ensure_ascii=False))
    except Exception as e:
        print(f"Redis set error: {e}")
        return False


def get_cache(key: str) -> Optional[Any]:
    """
    Get a value from Redis cache
    Args:
        key: Cache key
    Returns:
        Deserialized value or None if not found
    """
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Redis get error: {e}")
        return None


def delete_cache(key: str) -> bool:
    """
    Delete a value from Redis cache
    Args:
        key: Cache key
    Returns:
        bool: True if key was deleted, False otherwise
    """
    try:
        return redis_client.delete(key) > 0
    except Exception as e:
        print(f"Redis delete error: {e}")
        return False


def exists_cache(key: str) -> bool:
    """
    Check if a key exists in Redis cache
    Args:
        key: Cache key
    Returns:
        bool: True if key exists, False otherwise
    """
    try:
        return redis_client.exists(key) > 0
    except Exception as e:
        print(f"Redis exists error: {e}")
        return False


def set_hash(key: str, mapping: dict) -> bool:
    """
    Set a hash in Redis
    Args:
        key: Hash key
        mapping: Dictionary of field-value pairs
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        redis_client.hset(key, mapping=mapping)
        return True
    except Exception as e:
        print(f"Redis hset error: {e}")
        return False


def get_hash(key: str, field: Optional[str] = None) -> Any:
    """
    Get a hash or specific field from Redis
    Args:
        key: Hash key
        field: Optional specific field to retrieve
    Returns:
        Hash value or field value
    """
    try:
        if field:
            return redis_client.hget(key, field)
        else:
            return redis_client.hgetall(key)
    except Exception as e:
        print(f"Redis hget error: {e}")
        return None


def increment(key: str, amount: int = 1) -> int:
    """
    Increment a counter in Redis
    Args:
        key: Counter key
        amount: Amount to increment by (default: 1)
    Returns:
        int: New value
    """
    try:
        return redis_client.incr(key, amount)
    except Exception as e:
        print(f"Redis incr error: {e}")
        return 0
