"""
创意 (Creative) API
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from app.services.ocean import get_ocean_client, CreativeService

router = APIRouter(prefix="/creative", tags=["Creative"])


# ========== 数据模型 ==========


class CreativeCreateRequest(BaseModel):
    """创建创意请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    adgroup_id: int = Field(..., description="广告组 ID")
    creative_name: str = Field(..., description="创意名称")
    creative_type: int = Field(..., description="创意类型")
    creative_material_mode: int = Field(1, description="创意素材模式")


class CreativeUpdateRequest(BaseModel):
    """更新创意请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    creative_id: int = Field(..., description="创意 ID")
    creative_name: Optional[str] = Field(None, description="创意名称")


class CreativeStatusRequest(BaseModel):
    """更新创意状态请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    creative_id: int = Field(..., description="创意 ID")
    opt_status: str = Field("enable", description="操作状态")


class CreativeDeleteRequest(BaseModel):
    """删除创意请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    creative_id: int = Field(..., description="创意 ID")


# ========== 路由 ==========


@router.post("/create")
def create_creative(request: CreativeCreateRequest):
    """
    创建创意
    """
    try:
        client = get_ocean_client()
        service = CreativeService(client)

        result = service.create(
            advertiser_id=request.advertiser_id,
            adgroup_id=request.adgroup_id,
            creative_name=request.creative_name,
            creative_type=request.creative_type,
            creative_material_mode=request.creative_material_mode,
        )

        return {"code": 0, "message": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list")
def get_creative_list(
    advertiser_id: str = Query(..., description="广告主 ID"),
    adgroup_id: Optional[int] = Query(None, description="广告组 ID"),
    creative_ids: Optional[str] = Query(None, description="创意 ID 列表，逗号分隔"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
):
    """
    获取创意列表
    """
    try:
        client = get_ocean_client()
        service = CreativeService(client)

        creative_id_list = None
        if creative_ids:
            creative_id_list = [int(x.strip()) for x in creative_ids.split(",")]

        result = service.get(
            advertiser_id=advertiser_id,
            adgroup_id=adgroup_id,
            creative_ids=creative_id_list,
            page=page,
            page_size=page_size,
        )

        return {"code": 0, "message": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update")
def update_creative(request: CreativeUpdateRequest):
    """
    更新创意
    """
    try:
        client = get_ocean_client()
        service = CreativeService(client)

        update_data = {}
        if request.creative_name:
            update_data["creative_name"] = request.creative_name

        if not update_data:
            raise ValueError("没有要更新的字段")

        service.update(
            advertiser_id=request.advertiser_id,
            creative_id=request.creative_id,
            **update_data
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-status")
def update_creative_status(request: CreativeStatusRequest):
    """
    更新创意状态
    """
    try:
        client = get_ocean_client()
        service = CreativeService(client)

        service.update_status(
            advertiser_id=request.advertiser_id,
            creative_id=request.creative_id,
            opt_status=request.opt_status,
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/delete")
def delete_creative(request: CreativeDeleteRequest):
    """
    删除创意
    """
    try:
        client = get_ocean_client()
        service = CreativeService(client)

        service.delete(
            advertiser_id=request.advertiser_id,
            creative_id=request.creative_id,
        )

        return {"code": 0, "message": "success", "data": {"success": True}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
