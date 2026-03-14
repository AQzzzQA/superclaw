"""
数据报表 API
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ocean_account import OceanAccount
from app.models.report import DailyReport
from app.models.tenant import Tenant
from app.services.ocean import get_ocean_client, ReportService

router = APIRouter(prefix="/report", tags=["Report"])


# ========== 数据模型 ==========


class ReportQueryRequest(BaseModel):
    """报表查询请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    start_date: str = Field(..., description="开始日期（YYYY-MM-DD）")
    end_date: str = Field(..., description="结束日期（YYYY-MM-DD）")
    campaign_ids: Optional[str] = Field(None, description="计划 ID 列表，逗号分隔")
    adgroup_ids: Optional[str] = Field(None, description="广告组 ID 列表，逗号分隔")


# ========== 路由 ==========


@router.post("/daily")
def get_daily_report(
    request: ReportQueryRequest,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    获取日报表数据
    """
    try:
        # 获取账户 access_token
        account = (
            db.query(OceanAccount)
            .filter(
                OceanAccount.advertiser_id == request.advertiser_id,
                OceanAccount.tenant_id == current_user.tenant_id,
            )
            .first()
        )

        if not account:
            raise HTTPException(status_code=404, detail="账户不存在")

        # 调用巨量 API
        client = get_ocean_client(account.access_token)
        service = ReportService(client)

        # 解析 ID 列表
        campaign_ids = None
        adgroup_ids = None

        if request.campaign_ids:
            campaign_ids = [int(x.strip()) for x in request.campaign_ids.split(",")]
        if request.adgroup_ids:
            adgroup_ids = [int(x.strip()) for x in request.adgroup_ids.split(",")]

        result = service.get_daily_report(
            advertiser_id=request.advertiser_id,
            start_date=request.start_date,
            end_date=request.end_date,
            campaign_ids=campaign_ids,
            adgroup_ids=adgroup_ids,
            page=page,
            page_size=page_size,
        )

        # 存入数据库（可选，用于历史记录）
        for item in result.get("list", []):
            existing_report = (
                db.query(DailyReport)
                .filter(
                    DailyReport.tenant_id == current_user.tenant_id,
                    DailyReport.advertiser_id == request.advertiser_id,
                    DailyReport.stat_date
                    == datetime.strptime(item["stat_date"], "%Y-%m-%d").date(),
                    DailyReport.campaign_id == item.get("campaign_id"),
                    DailyReport.adgroup_id == item.get("adgroup_id"),
                    DailyReport.creative_id == item.get("creative_id"),
                )
                .first()
            )

            if existing_report:
                # 更新
                existing_report.cost = item.get("cost", 0)
                existing_report.show = item.get("show", 0)
                existing_report.click = item.get("click", 0)
                existing_report.ctr = item.get("ctr", 0)
                existing_report.cpm = item.get("cpm", 0)
                existing_report.cpc = item.get("cpc", 0)
                existing_report.convert = item.get("convert", 0)
                existing_report.updated_at = datetime.now()
            else:
                # 新增
                report = DailyReport(
                    tenant_id=current_user.tenant_id,
                    advertiser_id=request.advertiser_id,
                    stat_date=datetime.strptime(item["stat_date"], "%Y-%m-%d").date(),
                    campaign_id=item.get("campaign_id"),
                    adgroup_id=item.get("adgroup_id"),
                    creative_id=item.get("creative_id"),
                    cost=item.get("cost", 0),
                    show=item.get("show", 0),
                    click=item.get("click", 0),
                    ctr=item.get("ctr", 0),
                    cpm=item.get("cpm", 0),
                    cpc=item.get("cpc", 0),
                    convert=item.get("convert", 0),
                )
                db.add(report)

        db.commit()

        return {"code": 0, "message": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
def get_report_history(
    advertiser_id: str = Query(..., description="广告主 ID"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    获取历史报表数据（从本地数据库）
    """
    query = db.query(DailyReport).filter(
        DailyReport.tenant_id == current_user.tenant_id,
        DailyReport.advertiser_id == advertiser_id,
    )

    if start_date:
        query = query.filter(
            DailyReport.stat_date >= datetime.strptime(start_date, "%Y-%m-%d").date()
        )
    if end_date:
        query = query.filter(
            DailyReport.stat_date <= datetime.strptime(end_date, "%Y-%m-%d").date()
        )

    query = query.order_by(DailyReport.stat_date.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "code": 0,
        "message": "success",
        "data": {
            "list": [
                {
                    "stat_date": item.stat_date.isoformat(),
                    "cost": item.cost,
                    "show": item.show,
                    "click": item.click,
                    "ctr": float(item.ctr) if item.ctr else 0,
                    "cpm": item.cpm,
                    "cpc": item.cpc,
                    "convert": item.convert,
                }
                for item in items
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    }
