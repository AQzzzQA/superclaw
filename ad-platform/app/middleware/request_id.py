"""
请求 ID 中间件
"""
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestIDMiddleware(BaseHTTPMiddleware):
    """请求 ID 中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""

        # 获取或生成请求 ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        # 添加到请求状态
        request.state.request_id = request_id

        # 处理请求
        response = await call_next(request)

        # 添加响应头
        response.headers["X-Request-ID"] = request_id

        return response


# 兼容旧代码的导出
request_id_middleware = RequestIDMiddleware
