"""
Celery Worker配置
"""
from celery import Celery
from ..core.config import settings

# 创建Celery应用
celery_app = Celery(
    "dsp-platform",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.tasks"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟
    task_soft_time_limit=25 * 60,  # 25分钟
)


@celery_app.task
def process_bid_request(request_id: str):
    """处理竞价请求"""
    return {"request_id": request_id, "status": "processed"}


@celery_app.task
def generate_report(report_type: str, date: str):
    """生成报表"""
    return {"report_type": report_type, "date": date, "status": "generated"}
