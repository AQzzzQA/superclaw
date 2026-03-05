"""
自定义异常类
"""
from typing import Any, Optional


class BaseAPIException(Exception):
    """基础 API 异常"""

    def __init__(
        self,
        message: str = "Internal server error",
        code: int = 500,
        data: Any = None,
    ):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)


class UnauthorizedException(BaseAPIException):
    """未授权异常"""

    def __init__(self, message: str = "Unauthorized", data: Any = None):
        super().__init__(message=message, code=401, data=data)


class ForbiddenException(BaseAPIException):
    """禁止访问异常"""

    def __init__(self, message: str = "Forbidden", data: Any = None):
        super().__init__(message=message, code=403, data=data)


class NotFoundException(BaseAPIException):
    """未找到异常"""

    def __init__(self, message: str = "Not found", data: Any = None):
        super().__init__(message=message, code=404, data=data)


class BadRequestException(BaseAPIException):
    """请求错误异常"""

    def __init__(self, message: str = "Bad request", data: Any = None):
        super().__init__(message=message, code=400, data=data)


class ValidationException(BaseAPIException):
    """验证异常"""

    def __init__(self, message: str = "Validation failed", data: Any = None):
        super().__init__(message=message, code=422, data=data)


class RateLimitException(BaseAPIException):
    """限流异常"""

    def __init__(self, message: str = "Rate limit exceeded", data: Any = None):
        super().__init__(message=message, code=429, data=data)


class ExternalAPIException(BaseAPIException):
    """外部 API 异常"""

    def __init__(self, message: str = "External API error", data: Any = None):
        super().__init__(message=message, code=502, data=data)


# 兼容旧代码的导出
ValidationError = ValidationException
NotFoundError = NotFoundException
