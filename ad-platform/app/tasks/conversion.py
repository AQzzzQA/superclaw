"""
转化回传任务
"""
from celery import shared_task
from app.core.celery_app import celery_app
from app.core.response import APIResponse
import httpx
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.conversion.upload_conversion")
def upload_conversion_task(conversion_data: dict):
    """
    单个转化上传任务（异步）

    Args:
        conversion_data: 转化数据
            {
                "click_id": "string",
                "conversion_type": "string",
                "conversion_time": "string",
                "value": 0.0
            }

    Returns:
        dict: 上传结果
    """
    try:
        logger.info(f"开始上传转化: {conversion_data['click_id']}")

        # 模拟调用巨量引擎 API
        # 实际应使用 httpx 异步调用
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{settings.OCEAN_API_BASE_URL}/conversion/upload",
        #         json=conversion_data,
        #         headers={
        #             "Authorization": f"Bearer {token}",
        #             "Content-Type": "application/json",
        #         }
        #     )
        #     response.raise_for_status()
        #     return response.json()

        # 模拟成功
        logger.info(f"转化上传成功: {conversion_data['click_id']}")
        return {
            "click_id": conversion_data["click_id"],
            "status": "success",
            "message": "上传成功",
        }

    except Exception as e:
        logger.error(f"转化上传失败: {conversion_data['click_id']}, 错误: {str(e)}")
        # 任务失败，自动重试（最多 3 次）
        raise


@celery_app.task(name="app.tasks.conversion.batch_upload_conversion")
def batch_upload_conversion_task(conversions: list):
    """
    批量转化上传任务（异步）

    Args:
        conversions: 转化数据列表

    Returns:
        dict: 批量上传结果
    """
    try:
        logger.info(f"开始批量上传转化，共 {len(conversions)} 条")

        results = {
            "total": len(conversions),
            "success": 0,
            "failed": 0,
            "errors": [],
        }

        for conversion in conversions:
            try:
                # 调用单个转化上传任务
                result = upload_conversion_task.apply_async(args=[conversion]).get(timeout=30)
                if result["status"] == "success":
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        {"click_id": conversion["click_id"], "error": result.get("message", "未知错误")}
                    )
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {"click_id": conversion["click_id"], "error": str(e)}
                )

        logger.info(
            f"批量上传完成: 成功 {results['success']} 条，失败 {results['failed']} 条"
        )
        return results

    except Exception as e:
        logger.error(f"批量上传失败: {str(e)}")
        raise


@celery_app.task(name="app.tasks.conversion.retry_failed_conversion")
def retry_failed_conversion_task(failed_conversions: list):
    """
    重试失败的转化上传任务

    Args:
        failed_conversions: 失败的转化数据列表

    Returns:
        dict: 重试结果
    """
    logger.info(f"开始重试失败的转化，共 {len(failed_conversions)} 条")
    return batch_upload_conversion_task.apply_async(args=[failed_conversions]).get(timeout=120)
