"""
Celery任务定义
"""
from .worker import celery_app


@celery_app.task
def process_bid_request(request_id: str):
    """处理竞价请求"""
    return {"request_id": request_id, "status": "processed"}


@celery_app.task
def generate_report(report_type: str, date: str):
    """生成报表"""
    return {"report_type": report_type, "date": date, "status": "generated"}
