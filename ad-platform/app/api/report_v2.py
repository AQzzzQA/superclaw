"""
数据报表 API - 整合数据库
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, date
from app.core.response import APIResponse
from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.report import DailyReport
from app.models.conversion import Conversion
from app.models.ocean_account import OceanAccount
from app.models.user import User
from sqlalchemy import desc, func, and_, or_

router = APIRouter(prefix="/report", tags=["Report"])


# ========== 数据模型 ==========


class ReportQuery(BaseModel):
    """报表查询"""

    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    advertiser_id: Optional[str] = Field(None, description="广告主 ID")
    campaign_id: Optional[int] = Field(None, description="计划 ID")
    adgroup_id: Optional[int] = Field(None, description="广告组 ID")


class ConversionUploadRequest(BaseModel):
    """转化数据上传"""

    advertiser_id: str = Field(..., description="广告主 ID")
    conversions: List[dict] = Field(..., description="转化数据")


class ConversionQueryRequest(BaseModel):
    """转化查询"""

    advertiser_id: str = Field(..., description="广告主 ID")
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    conversion_type: Optional[str] = Field(None, description="转化类型")


# ========== 路由 ==========


@router.get("/daily")
async def get_daily_report(
    start_date: str = Query(..., description="开始日期"),
    end_date: str = Query(..., description="结束日期"),
    advertiser_id: Optional[str] = Query(None, description="广告主 ID"),
    campaign_id: Optional[int] = Query(None, description="计划 ID"),
    adgroup_id: Optional[int] = Query(None, description="广告组 ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取日报表数据"""
    try:
        # 构建查询
        query = db.query(DailyReport).filter(
            DailyReport.tenant_id == current_user.tenant_id
        )

        if advertiser_id:
            query = query.filter(DailyReport.advertiser_id == advertiser_id)
        if campaign_id:
            query = query.filter(DailyReport.campaign_id == campaign_id)
        if adgroup_id:
            query = query.filter(DailyReport.adgroup_id == adgroup_id)
        if start_date:
            query = query.filter(
                DailyReport.stat_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            query = query.filter(
                DailyReport.stat_date <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        # 排序
        query = query.order_by(DailyReport.stat_date.desc())

        # 分页
        total = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()

        # 序列化
        data = [
            {
                "id": r.id,
                "date": r.stat_date.strftime("%Y-%m-%d"),
                "advertiser_id": r.advertiser_id,
                "campaign_id": r.campaign_id,
                "adgroup_id": r.adgroup_id,
                "creative_id": r.creative_id,
                "cost": r.cost,
                "show": r.show,
                "click": r.click,
                "ctr": float(r.ctr) if r.ctr else 0,
                "cpm": r.cpm,
                "cpc": r.cpc,
                "convert": r.convert,
            }
            for r in results
        ]

        return APIResponse.success(
            data={"total": total, "page": page, "page_size": page_size, "results": data}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend")
async def get_trend_report(
    start_date: str = Query(..., description="开始日期"),
    end_date: str = Query(..., description="结束日期"),
    advertiser_id: str = Query(..., description="广告主 ID"),
    campaign_id: Optional[int] = Query(None, description="计划 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取趋势报表"""
    try:
        # 获取数据
        reports = db.query(DailyReport).filter(
            dailyReport.tenant_id == current_user.tenant_id,
            dailyReport.advertiser_id == advertiser_id,
        )

        if campaign_id:
            reports = reports.filter(DailyReport.campaign_id == campaign_id)

        if start_date:
            reports = reports.filter(
                DailyReport.stat_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            reports = reports.filter(
                DailyReport.stat_date <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        # 按日期分组汇总
        trend_data = {}
        for r in reports:
            date_key = r.stat_date.strftime("%Y-%m-%d")
            if date_key not in trend_data:
                trend_data[date_key] = {
                    "date": date_key,
                    "cost": 0,
                    "show": 0,
                    "click": 0,
                    "convert": 0,
                }

            trend_data[date_key]["cost"] += r.cost or 0
            trend_data[date_key]["show"] += r.show or 0
            trend_data[date_key]["click"] += r.click or 0
            trend_data[date_key]["convert"] += r.convert or 0

        # 排序
        sorted_data = sorted(trend_data.values(), key=lambda x: x["date"])

        return APIResponse.success(data=sorted_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_report(
    start_date: str = Query(..., description="开始日期"),
    end_date: str = Query(..., description="结束日期"),
    format: str = Query("xlsx", description="导出格式: xlsx | csv"),
    advertiser_id: str = Query(..., description="广告主 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """导出报表数据"""
    try:
        # 获取数据
        reports = db.query(DailyReport).filter(
            dailyReport.tenant_id == current_user.tenant_id,
            dailyReport.advertiser_id == advertiser_id,
        )

        if start_date:
            reports = reports.filter(
                DailyReport.stat_date
                >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        if end_date:
            reports = reports.filter(
                DailyReport.stat_date <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )

        reports = reports.order_by(DailyReport.stat_date.desc()).all()

        # 准备数据
        data = [
            {
                "date": r.stat_date.strftime("%Y-%m-%d"),
                "广告主": r.advertiser_id,
                "计划": r.campaign_id,
                "曝光": r.show,
                "点击": r.click,
                "CTR": f"{float(r.ctr):.2f}%" if r.ctr else "0%",
                "转化": r.convert,
                "消耗": r.cost,
                "CPM": r.cpm,
                "CPC": r.cpc,
                "CPA": (
                    f"{(r.cost / (r.convert or 1)):.2f}"
                    if r.convert and r.cost
                    else "0.00"
                ),
            }
            for r in reports
        ]

        # 异步导出
        from app.api.async_tasks import export_report_task

        task = export_report_task.apply_async(args=[data, format])

        return APIResponse.success(
            data={
                "task_id": task.id,
                "status": "pending",
                "message": f"导出任务已提交（{format.upper()}）",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_report_history(
    advertiser_id: str = Query(..., description="广告主 ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取历史报表"""
    try:
        # 获取账户
        account = (
            db.query(OceanAccount)
            .filter(
                OceanAccount.advertiser_id == advertiser_id,
                OceanAccount.tenant_id == current_user.tenant_id,
            )
            .first()
        )

        if not account:
            raise HTTPException(status_code=404, detail="账户不存在")

        # 获取报表数据
        reports = (
            db.query(DailyReport)
            .filter(DailyReport.advertiser_id == advertiser_id)
            .order_by(DailyReport.stat_date.desc())
            .all()
        )

        # 分页
        total = len(reports)
        results = reports.offset((page - 1) * page_size).limit(page_size).all()

        return APIResponse.success(
            data={
                "total": total,
                "page": page,
                "page_size": page_size,
                "results": [
                    {
                        "id": r.id,
                        "date": r.stat_date.strftime("%Y-%m-%d"),
                        "cost": r.cost,
                        "show": r.show,
                        "click": r.click,
                        "ctr": float(r.ctr) if r.ctr else 0,
                        "convert": r.convert,
                    }
                    for r in results
                ],
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
