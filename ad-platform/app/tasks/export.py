"""
数据导出任务
"""
from celery import shared_task
from app.core.celery_app import celery_app
import pandas as pd
import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.export.export_report")
def export_report_task(data: list, format: str = "xlsx"):
    """
    导出报表任务（异步）

    Args:
        data: 报表数据
        format: 导出格式 xlsx | csv

    Returns:
        dict: 导出结果（包含文件内容）
    """
    try:
        logger.info(f"开始导出报表，格式: {format}")

        # 创建 DataFrame
        df = pd.DataFrame(data)

        # 导出到字节流
        output = io.BytesIO()

        if format == "xlsx":
            df.to_excel(output, index=False, engine="openpyxl")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format == "csv":
            df.to_csv(output, index=False)
            mime_type = "text/csv"
        else:
            raise ValueError(f"不支持的格式: {format}")

        output.seek(0)

        # 生成文件名
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"

        logger.info(f"报表导出成功: {filename}")
        return {
            "filename": filename,
            "mime_type": mime_type,
            "content": output.getvalue().hex(),  # 转换为 hex 存储
            "size": len(output.getvalue()),
        }

    except Exception as e:
        logger.error(f"报表导出失败: {str(e)}")
        raise


@celery_app.task(name="app.tasks.export.export_to_excel")
def export_to_excel_task(data: list, sheet_name: str = "Sheet1"):
    """
    导出到 Excel 任务

    Args:
        data: 数据
        sheet_name: 工作表名称

    Returns:
        dict: 导出结果
    """
    return export_report_task.apply_async(args=[data, "xlsx"]).get(timeout=60)


@celery_app.task(name="app.tasks.export.export_to_csv")
def export_to_csv_task(data: list):
    """
    导出到 CSV 任务

    Args:
        data: 数据

    Returns:
        dict: 导出结果
    """
    return export_report_task.apply_async(args=[data, "csv"]).get(timeout=60)


@celery_app.task(name="app.tasks.export.batch_export")
def batch_export_task(tasks: list):
    """
    批量导出任务

    Args:
        tasks: 导出任务列表
            [
                {"data": [...], "format": "xlsx"},
                {"data": [...], "format": "csv"},
            ]

    Returns:
        dict: 批量导出结果
    """
    try:
        logger.info(f"开始批量导出，共 {len(tasks)} 个任务")

        results = {
            "total": len(tasks),
            "success": 0,
            "failed": 0,
            "files": [],
        }

        for i, task in enumerate(tasks):
            try:
                result = export_report_task.apply_async(args=[task["data"], task["format"]]).get(timeout=60)
                results["success"] += 1
                results["files"].append(result)
            except Exception as e:
                results["failed"] += 1
                logger.error(f"导出失败: 任务 {i}, 错误: {str(e)}")

        logger.info(f"批量导出完成: 成功 {results['success']} 个，失败 {results['failed']} 个")
        return results

    except Exception as e:
        logger.error(f"批量导出失败: {str(e)}")
        raise
