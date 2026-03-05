"""
广告计划 (Campaign) API
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.services.ocean import get_ocean_client, CampaignService

router = APIRouter(prefix="/campaign", tags=["Campaign"])


# ========== 数据模型 ==========

class CampaignCreateRequest(BaseModel):
    """创建广告计划请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    campaign_name: str = Field(..., description="计划名称")
    budget_mode: int = Field(1, description="预算模式：1-日预算，2-总预算")
    budget: Optional[int] = Field(None, description="预算（分）")
    start_time: str = Field(..., description="开始时间（ISO 8601）")
    end_time: str = Field(..., description="结束时间（ISO 8601）")
    objectives: List[str] = Field(default_factory=list, description="推广目标列表")


class CampaignUpdateRequest(BaseModel):
    """更新广告计划请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    campaign_id: int = Field(..., description="计划 ID")
    campaign_name: Optional[str] = Field(None, description="计划名称")
    budget: Optional[int] = Field(None, description="预算（分）")


class CampaignStatusRequest(BaseModel):
    """更新广告计划状态请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    campaign_id: int = Field(..., description="计划 ID")
    opt_status: str = Field("enable", description="操作状态：enable-启用，disable-停用")


class CampaignDeleteRequest(BaseModel):
    """删除广告计划请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    campaign_id: int = Field(..., description="计划 ID")


# ========== 路由 ==========

@router.post("/create")
def create_campaign(request: CampaignCreateRequest):
    """
    创建广告计划
    """
    try:
        client = get_ocean_client()  # 需要传入 access_token，这里暂时略过
        service = CampaignService(client)

        result = service.create(
            advertiser_id=request.advertiser_id,
            campaign_name=request.campaign_name,
            budget_mode=request.budget_mode,
            budget=request.budget,
            start_time=request.start_time,
            end_time=request.end_time,
            objectives=request.objectives,
        )

        return {
            "code": 0,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
def get_campaign_list(
    advertiser_id: str = Query(..., description="广告主 ID"),
    campaign_ids: Optional[str] = Query(None, description="计划 ID 列表，逗号分隔"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """
    获取广告计划列表
    """
    try:
        client = get_ocean_client()
        service = CampaignService(client)

        campaign_id_list = None
        if campaign_ids:
            campaign_id_list = [int(x.strip()) for x in campaign_ids.split(",")]

        result = service.get(
            advertiser_id=advertiser_id,
            campaign_ids=campaign_id_list,
            page=page,
            page_size=page_size,
        )

        return {
            "code": 0,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update")
def update_campaign(request: CampaignUpdateRequest):
    """
    更新广告计划
    """
    try:
        client = get_ocean_client()
        service = CampaignService(client)

        update_data = {}
        if request.campaign_name:
            update_data["campaign_name"] = request.campaign_name
        if request.budget is not None:
            update_data["budget"] = request.budget

        if not update_data:
            raise ValueError("没有要更新的字段")

        service.update(
            advertiser_id=request.advertiser_id,
            campaign_id=request.campaign_id,
            **update_data
        )

        return {
            "code": 0,
            "message": "success",
            "data": {"success": True}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-status")
def update_campaign_status(request: CampaignStatusRequest):
    """
    更新广告计划状态
    """
    try:
        client = get_ocean_client()
        service = CampaignService(client)

        service.update_status(
            advertiser_id=request.advertiser_id,
            campaign_id=request.campaign_id,
            opt_status=request.opt_status,
        )

        return {
            "code": 0,
            "message": "success",
            "data": {"success": True}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/delete")
def delete_campaign(request: CampaignDeleteRequest):
    """
    删除广告计划
    """
    try:
        client = get_ocean_client()
        service = CampaignService(client)

        service.delete(
            advertiser_id=request.advertiser_id,
            campaign_id=request.campaign_id,
        )

        return {
            "code": 0,
            "message": "success",
            "data": {"success": True}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
