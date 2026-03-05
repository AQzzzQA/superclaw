"""
异步任务 API
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
from app.tasks.conversion import batch_upload_conversion_task
from app.tasks.report import generate_daily_report_task, batch_generate_reports_task
from app.tasks.export import export_report_task, batch_export_task

router = APIRouter()


# 转化回传任务
@router.post("/tasks/conversion/upload")
async def upload_conversion(conversion_data: Dict[str, Any]):
    """
    上传转化（异步）

    Args:
        conversion_data: 转化数据
            {
                "click_id": "string",
                "conversion_type": "string",
                "conversion_time": "string",
                "value": 0.0
            }
    """
    # 验证数据
    required_fields = ["click_id", "conversion_type", "conversion_time"]
    for field in required_fields:
        if field not in conversion_data:
            raise BadRequestException(f"缺少必需字段: {field}")

    # 提交异步任务
    task = upload_conversion_task.apply_async(args=[conversion_data])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
        },
        message="转化上传任务已提交"
    )


@router.post("/tasks/conversion/batch-upload")
async def batch_upload_conversion(conversions: List[Dict[str, Any]]):
    """
    批量上传转化（异步）

    Args:
        conversions: 转化数据列表
    """
    if not conversions:
        raise BadRequestException("数据不能为空")

    # 提交异步任务
    task = batch_upload_conversion_task.apply_async(args=[conversions])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
            "total": len(conversions),
        },
        message=f"批量上传任务已提交，共 {len(conversions)} 条"
    )


# 报表生成任务
@router.post("/tasks/report/generate")
async def generate_report(
    date: str = Query(..., description="日期 YYYY-MM-DD"),
    advertiser_id: int = Query(..., description="广告主 ID"),
):
    """
    生成日报表（异步）

    Args:
        date: 日期 YYYY-MM-DD
        advertiser_id: 广告主 ID
    """
    # 提交异步任务
    task = generate_daily_report_task.apply_async(args=[date, advertiser_id])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
        },
        message="报表生成任务已提交"
    )


@router.post("/tasks/report/batch-generate")
async def batch_generate_reports(
    dates: List[str] = Query(..., description="日期列表 YYYY-MM-DD"),
    advertiser_ids: List[int] = Query(..., description="广告主 ID 列表"),
):
    """
    批量生成报表（异步）

    Args:
        dates: 日期列表
        advertiser_ids: 广告主 ID 列表
    """
    if not dates or not advertiser_ids:
        raise BadRequestException("日期或广告主 ID 不能为空")

    # 提交异步任务
    task = batch_generate_reports_task.apply_async(args=[dates, advertiser_ids])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
            "total": len(dates) * len(advertiser_ids),
        },
        message=f"批量生成任务已提交，共 {len(dates) * len(advertiser_ids)} 个"
    )


# 数据导出任务
@router.post("/tasks/export/report")
async def export_report(
    data: List[Dict[str, Any]],
    format: str = Query("xlsx", description="导出格式: xlsx | csv"),
):
    """
    导出报表（异步）

    Args:
        data: 报表数据
        format: 导出格式
    """
    if not data:
        raise BadRequestException("数据不能为空")

    if format not in ["xlsx", "csv"]:
        raise BadRequestException("格式错误，支持 xlsx 或 csv")

    # 提交异步任务
    task = export_report_task.apply_async(args=[data, format])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
        },
        message="导出任务已提交"
    )


@router.post("/tasks/export/batch")
async def batch_export(tasks: List[Dict[str, Any]]):
    """
    批量导出（异步）

    Args:
        tasks: 导出任务列表
            [
                {"data": [...], "format": "xlsx"},
                {"data": [...], "format": "csv"},
            ]
    """
    if not tasks:
        raise BadRequestException("任务不能为空")

    # 提交异步任务
    task = batch_export_task.apply_async(args=[tasks])

    return APIResponse.success(
        data={
            "task_id": task.id,
            "status": "pending",
            "total": len(tasks),
        },
        message=f"批量导出任务已提交，共 {len(tasks)} 个"
    )


# 任务状态查询
@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """
    查询任务状态

    Args:
        task_id: 任务 ID
    """
    from app.core.celery_app import celery_app

    # 获取任务结果
    task_result = celery_app.AsyncResult(task_id)

    return APIResponse.success(
        data={
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result if task_result.ready() else None,
        }
    )
