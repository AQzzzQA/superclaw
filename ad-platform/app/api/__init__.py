"""
API 路由模块
"""
from . import (
    oauth, campaign, adgroup, creative,
    auth, account, tenant, report, conversion, health,
    targeting  # 新增
)

__all__ = [
    "oauth",
    "campaign",
    "adgroup",
    "creative",
    "auth",
    "account",
    "tenant",
    "report",
    "conversion",
    "health",
    "targeting",  # 新增
    "monitoring",  # 新增
]
