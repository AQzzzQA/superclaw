from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 数据库
from app.core.database import engine, Base, SessionLocal

# 中间件
from app.middleware.error_handler import error_handler
from app.middleware.logging import request_logging_middleware
from app.middleware.request_id import request_id_middleware
from app.middleware.rate_limit import rate_limit_middleware

# API 路由
from app.api import (
    oauth, campaign, adgroup, creative,
    auth, account, tenant, report, conversion, health,
    batch, auto_bidding, ab_test, attribution,
    users, roles, logs, config, report_v2,
    targeting, monitoring,  # bidding 临时禁用（schemas 有语法错误）
)

# 创建应用
app = FastAPI(title="广告平台管理系统", version="2.0")

# CORS 中间件（使用 FastAPI 自带）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 错误处理中间件
app.add_middleware(error_handler)

# 其他中间件
app.middleware("/api")
app.middleware(request_logging_middleware)
app.middleware(request_id_middleware)
app.middleware(rate_limit_middleware)

# 数据库会话
@asynccontextmanager
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建表
@app.on_event("startup")
async def on_startup():
    print("Starting up database connection...")
    from app.core.database import Base
    from app import models  # 导入所有模型以创建表
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# 路由注册
app.include_router(oauth.router, prefix="/api/v1", tags=["OAuth"])
app.include_router(campaign.router, prefix="/api/v1", tags=["广告计划"])
app.include_router(adgroup.router, prefix="/api/v1", tags=["广告组"])
app.include_router(creative.router, prefix="/api/v1", tags=["创意"])
app.include_router(report.router, prefix="/api/v1", tags=["数据报表"])
app.include_router(conversion.router, prefix="/api/v1", tags=["转化追踪"])
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])

app.include_router(batch.router, prefix="/api/v1", tags=["批量操作"])
# app.include_router(export.router, prefix="/api/v1", tags=["数据导出"])  # 临时禁用（缺少 pandas）
# app.include_router(batch_conversion.router, prefix="/api/v1", tags=["批量转化"])  # 临时禁用（缺少 pandas）
# app.include_router(async_tasks.router, prefix="/api/v1", tags=["异步任务"])  # 临时禁用（缺少 celery）

app.include_router(auto_bidding.router, prefix="/api/v1", tags=["自动出价"])
app.include_router(ab_test.router, prefix="/api/v1", tags=["A/B 测试"])
app.include_router(attribution.router, prefix="/api/v1", tags=["归因模型"])
app.include_router(users.router, prefix="/api/v1", tags=["用户管理"])
app.include_router(roles.router, prefix="/api/v1", tags=["角色管理"])
app.include_router(logs.router, prefix="/api/v1", tags=['操作日志'])
app.include_router(config.router, prefix="/api/v1", tags=['系统配置'])

app.include_router(report_v2.router, prefix="/api/v2", tags=['报表 V2'])
# app.include_router(conversion_v2.router, prefix="/api/v2", tags=['转化 V2'])  # 临时禁用（缺少 celery）

app.include_router(targeting.router, prefix="/api/v1", tags=['定向投放'])
app.include_router(monitoring.router, prefix="/api/v1", tags=['实时监控'])
# app.include_router(bidding.router, prefix="/api/v1", tags=['出价策略'])  # 临时禁用（schemas 有语法错误）

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "2.0",
        "components": {
            "api": "ok",
            "database": "ok",
            "redis": "pending",
        }
    }
