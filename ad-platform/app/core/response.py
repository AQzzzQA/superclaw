"""
统一响应格式
"""

from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel
import time

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""

    code: int = 200
    message: str = "success"
    data: Optional[T] = None
    timestamp: int = int(time.time())

    @classmethod
    def success(cls, data: Any = None, message: str = "success") -> "APIResponse":
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(
        cls, code: int = 500, message: str = "error", data: Any = None
    ) -> "APIResponse":
        """错误响应"""
        return cls(code=code, message=message, data=data)

    @classmethod
    def created(cls, data: Any = None, message: str = "created") -> "APIResponse":
        """创建成功"""
        return cls(code=201, message=message, data=data)

    @classmethod
    def not_found(cls, message: str = "not found") -> "APIResponse":
        """未找到"""
        return cls(code=404, message=message)

    @classmethod
    def bad_request(cls, message: str = "bad request") -> "APIResponse":
        """请求错误"""
        return cls(code=400, message=message)

    @classmethod
    def unauthorized(cls, message: str = "unauthorized") -> "APIResponse":
        """未授权"""
        return cls(code=401, message=message)

    @classmethod
    def forbidden(cls, message: str = "forbidden") -> "APIResponse":
        """禁止访问"""
        return cls(code=403, message=message)

    @classmethod
    def internal_error(cls, message: str = "internal server error") -> "APIResponse":
        """服务器内部错误"""
        return cls(code=500, message=message)


# 兼容旧代码的导出
success_response = APIResponse.success
error_response = APIResponse.error
