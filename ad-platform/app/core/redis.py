"""
Redis 连接配置
"""

import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


def get_redis():
    """获取 Redis 客户端"""
    return redis_client
