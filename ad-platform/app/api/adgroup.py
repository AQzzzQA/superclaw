"""
广告组 (AdGroup) API
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from app.services.ocean import get_ocean_client, AdGroupService

router = APIRouter(prefix="/adgroup", tags=["AdGroup"])


# ========== 数据模型 ==========


class AdGroupCreateRequest(BaseModel):
    """创建广告组请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    campaign_id: int = Field(..., description="计划 ID")
    adgroup_name: str = Field(..., description="广告组名称")
    promote_mode: int = Field(1, description="推广模式")
    budget_mode: int = Field(1, description="预算模式：1-日预算，2-总预算")
    budget: Optional[int] = Field(None, description="预算（分）")
    start_time: str = Field(..., description="开始时间（ISO 8601）")
    end_time: str = Field(..., description="结束时间（ISO 8601）")


class AdGroupUpdateRequest(BaseModel):
    """更新广告组请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    adgroup_id: int = Field(..., description="广告组 ID")
    adgroup_name: Optional[str] = Field(None, description="广告组名称")
    budget: Optional[int] = Field(None, description="预算（分）")


class AdGroupStatusRequest(BaseModel):
    """更新广告组状态请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    adgroup_id: int = Field(..., description="广告组 ID")
    opt_status: str = Field("enable", description="操作状态")


class AdGroupDeleteRequest(BaseModel):
    """删除广告组请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    adgroup_id: int = Field(..., description="广告组 ID")


# ========== 路由 ==========


@router.post("/create")
def create_adgroup(request: AdGroupCreateRequest):
    """
    创建广告组
    """
    try:
        client = get_ocean_client()
        service = AdGroupService(client)

        result = service.create(
            advertiser_id=request.advertiser_id,
            campaign_id=request.campaign_id,
            adgroup_name=request.adgroup_name,
            promote_mode=request.promote_mode,
            budget_mode=request.budget_mode,
            budget=request.budget,
            start_time=request.start_time,
            end_time=request.end_time,
        )

        return {"code": 0, "message": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
def get_adgroup_list(
    advertiser_id: str = Query(..., description="广告主 ID"),
    campaign_id: Optional[int] = Query(None, description="计划 ID"),
    adgroup_ids: Optional[str] = Query(None, description="广告组 ID 列表，逗号分隔"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
):
    """
    获取广告组列表
    """
    try:
        client = get_ocean_client()
        service = AdGroupService(client)

        adgroup_id_list = None
        if adgroup_ids:
            adgroup_id_list = [int(x.strip()) for x in adgroup_ids.split(",")]

        result = service.get(
            advertiser_id=advertiser_id,
            campaign_id=campaign_id,
            adgroup_ids=adgroup_id_list,
            page=page,
            page_size=page_size,
        )

        return {"code": 0, "message": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update")
def update_adgroup(request: AdGroupUpdateRequest):
    """
    更新广告组
    """
    try:
        client = get_ocean_client()
        service = AdGroupService(client)

        update_data = {}
        if request.adgroup_name:
            update_data["adgroup_name"] = request.adgroup_name
        if request.budget is not None:
            update_data["budget"] = request.budget

        if not update_data:
            raise ValueError("没有要更新的字段")

        service.update(
            advertiser_id=request.advertiser_id,
            adgroup_id=request.adgroup_id,
            **update_data
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-status")
def update_adgroup_status(request: AdGroupStatusRequest):
    """
    更新广告组状态
    """
    try:
        client = get_ocean_client()
        service = AdGroupService(client)

        service.update_status(
            advertiser_id=request.advertiser_id,
            adgroup_id=request.adgroup_id,
            opt_status=request.opt_status,
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/delete")
def delete_adgroup(request: AdGroupDeleteRequest):
    """
    删除广告组
    """
    try:
        client = get_ocean_client()
        service = AdGroupService(client)

        service.delete(
            advertiser_id=request.advertiser_id,
            adgroup_id=request.adgroup_id,
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
