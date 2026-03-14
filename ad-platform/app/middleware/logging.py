"""
请求日志中间件
"""

import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        # 记录请求开始时间
        start_time = time.time()

        # 获取请求 ID
        request_id = request.headers.get("X-Request-ID", "")

        # 记录请求信息
        logger.info(
            json.dumps(
                {
                    "event": "request_started",
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "path": request.url.path,
                    "query_params": str(request.query_params),
                    "client": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent"),
                }
            )
        )

        # 处理请求
        try:
            response = await call_next(request)
        except Exception as e:
            # 记录异常
            logger.error(
                json.dumps(
                    {
                        "event": "request_error",
                        "request_id": request_id,
                        "method": request.method,
                        "url": str(request.url),
                        "error": str(e),
                        "error_type": type(e).__name__,
                    }
                )
            )
            raise

        # 计算响应时间
        process_time = (time.time() - start_time) * 1000  # 毫秒

        # 记录响应信息
        logger.info(
            json.dumps(
                {
                    "event": "request_completed",
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time, 2),
                }
            )
        )

        # 添加响应头
        response.headers["X-Process-Time"] = str(round(process_time, 2))
        response.headers["X-Request-ID"] = request_id

        return response


# 兼容旧代码的导出
request_logging_middleware = LoggingMiddleware
