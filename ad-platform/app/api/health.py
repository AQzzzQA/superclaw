"""
健康检查 API
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.response import APIResponse
from app.core.settings import settings
from app.core.redis import get_redis
from app.core.database import engine

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查"""
    redis_status = "ok"
    db_status = "ok"

    # 检查 Redis
    try:
        redis = get_redis()
        redis.ping()
    except Exception:
        redis_status = "error"

    # 检查数据库
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception:
        db_status = "error"

    response = APIResponse.success(
        data={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "healthy",
            "redis": redis_status,
            "database": db_status,
        }
    )

    return JSONResponse(content=response.model_dump())


@router.get("/metrics")
async def metrics():
    """Prometheus metrics"""
    # 这里可以返回 Prometheus 格式的指标
    metrics_data = """
# HELP app_up 应用运行状态
# TYPE app_up gauge
app_up 1

# HELP app_requests_total 总请求数
# TYPE app_requests_total counter
app_requests_total 0
    """

    return JSONResponse(content={"metrics": metrics_data.strip()})
