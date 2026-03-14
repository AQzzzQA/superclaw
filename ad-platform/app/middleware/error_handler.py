"""
统一错误处理中间件
"""

import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.response import APIResponse
from app.core.exceptions import BaseAPIException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """统一错误处理中间件"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except StarletteHTTPException as exc:
            logger.error(
                f"HTTP Exception: {exc.status_code} - {exc.detail} - {request.url}"
            )
            response = APIResponse.error(code=exc.status_code, message=str(exc.detail))
            return JSONResponse(
                status_code=exc.status_code, content=response.model_dump()
            )
        except RequestValidationError as exc:
            logger.error(f"Validation Exception: {exc.errors()} - {request.url}")
            response = APIResponse.error(
                code=422, message="Validation failed", data=exc.errors()
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=response.model_dump(),
            )
        except BaseAPIException as exc:
            logger.error(f"API Exception: {exc.code} - {exc.message} - {request.url}")
            response = APIResponse.error(
                code=exc.code, message=exc.message, data=exc.data
            )
            return JSONResponse(status_code=exc.code, content=response.model_dump())
        except Exception as exc:
            logger.exception(f"Unhandled Exception: {exc} - {request.url}")
            response = APIResponse.internal_error(message="Internal server error")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=response.model_dump(),
            )


# 兼容旧代码的导出
error_handler = ErrorHandlerMiddleware
