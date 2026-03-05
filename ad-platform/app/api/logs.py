"""
操作日志 API
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime
from app.core.response import APIResponse
import uuid

router = APIRouter()

# 模拟操作日志数据库
operation_logs_db = []


class LogQuery(BaseModel):
    """日志查询参数"""
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


def add_log(
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
):
    """添加操作日志"""
    log = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "details": details,
        "ip_address": "127.0.0.1",  # 实际应从请求中获取
        "user_agent": "Mozilla/5.0",  # 实际应从请求中获取
        "created_at": datetime.now().isoformat(),
    }

    operation_logs_db.append(log)
    return log


@router.get("/logs")
async def list_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
):
    """获取操作日志列表"""
    logs = operation_logs_db

    # 过滤
    if user_id is not None:
        logs = [log for log in logs if log["user_id"] == user_id]

    if action is not None:
        logs = [log for log in logs if log["action"] == action]

    if resource_type is not None:
        logs = [log for log in logs if log["resource_type"] == resource_type]

    if start_time is not None:
        logs = [log for log in logs if log["created_at"] >= start_time]

    if end_time is not None:
        logs = [log for log in logs if log["created_at"] <= end_time]

    # 按时间倒序
    logs = sorted(logs, key=lambda x: x["created_at"], reverse=True)

    # 分页
    total = len(logs)
    logs = logs[skip : skip + limit]

    return APIResponse.success(
        data={
            "logs": logs,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    )


@router.get("/logs/{log_id}")
async def get_log(log_id: str):
    """获取操作日志详情"""
    log = next((log for log in operation_logs_db if log["id"] == log_id), None)

    if not log:
        raise NotFoundException("日志不存在")

    return APIResponse.success(data=log)
