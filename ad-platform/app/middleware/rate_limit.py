"""
限流中间件
"""
import time
from typing import Callable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.redis import get_redis
from app.core.settings import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """基于 Redis 的限流中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.redis = get_redis()
        self.limit_times = settings.RATE_LIMIT_TIMES
        self.limit_seconds = settings.RATE_LIMIT_SECONDS

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""

        # 如果未启用限流，直接放行
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # 获取客户端标识（IP 或用户 ID）
        client_id = self._get_client_id(request)

        # 限流检查
        if not await self._check_rate_limit(client_id):
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {self.limit_times} requests per {self.limit_seconds} seconds",
            )

        # 处理请求
        response = await call_next(request)

        # 添加限流响应头
        remaining = await self._get_remaining_requests(client_id)
        response.headers["X-RateLimit-Limit"] = str(self.limit_times)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(
            int(time.time()) + self._get_ttl(client_id)
        )

        return response

    def _get_client_id(self, request: Request) -> str:
        """获取客户端标识"""

        # 优先使用用户 ID
        if hasattr(request.state, "user_id") and request.state.user_id:
            return f"user:{request.state.user_id}"

        # 其次使用 IP
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    async def _check_rate_limit(self, client_id: str) -> bool:
        """检查是否超过限流"""

        key = f"rate_limit:{client_id}"
        pipe = self.redis.pipeline()

        try:
            # 获取当前计数
            current = self.redis.get(key)

            if current is None:
                # 首次请求，设置计数和过期时间
                pipe.setex(key, self.limit_seconds, 1)
                pipe.execute()
                return True

            # 检查是否超过限制
            count = int(current)
            if count >= self.limit_times:
                return False

            # 增加计数
            pipe.incr(key)
            pipe.execute()
            return True

        except Exception as e:
            # Redis 异常，降级放行
            print(f"Rate limit check failed: {e}")
            return True

    async def _get_remaining_requests(self, client_id: str) -> int:
        """获取剩余请求次数"""

        key = f"rate_limit:{client_id}"
        try:
            current = self.redis.get(key)
            if current is None:
                return self.limit_times
            return max(0, self.limit_times - int(current))
        except Exception:
            return self.limit_times

    def _get_ttl(self, client_id: str) -> int:
        """获取过期时间"""

        key = f"rate_limit:{client_id}"
        try:
            ttl = self.redis.ttl(key)
            return max(0, ttl)
        except Exception:
            return self.limit_seconds


# 兼容旧代码的导出
rate_limit_middleware = RateLimitMiddleware
