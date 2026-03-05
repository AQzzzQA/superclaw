"""
转化回传 API
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ocean_account import OceanAccount
from app.services.ocean import get_ocean_client, ConversionService

router = APIRouter(prefix="/conversion", tags=["Conversion"])


# ========== 数据模型 ==========

class ConversionItem(BaseModel):
    """转化项"""
    click_id: str = Field(..., description="点击 ID")
    conversion_time: str = Field(..., description="转化时间（时间戳，毫秒）")
    conversion_type: str = Field(..., description="转化类型")


class ConversionUploadRequest(BaseModel):
    """上传转化请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    conversions: List[ConversionItem] = Field(..., description="转化数据列表")


class ConversionQueryRequest(BaseModel):
    """查询转化请求"""
    advertiser_id: str = Field(..., description="广告主 ID")
    start_date: str = Field(..., description="开始日期（YYYY-MM-DD）")
    end_date: str = Field(..., description="结束日期（YYYY-MM-DD）")


# ========== 路由 ==========

@router.post("/upload")
def upload_conversion(
    request: ConversionUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传转化数据
    """
    try:
        # 获取账户 access_token
        account = db.query(OceanAccount).filter(
            OceanAccount.advertiser_id == request.advertiser_id,
            OceanAccount.tenant_id == current_user.tenant_id
        ).first()

        if not account:
            raise HTTPException(status_code=404, detail="账户不存在")

        # 调用巨量 API
        client = get_ocean_client(account.access_token)
        service = ConversionService(client)

        # 构造转化数据
        conversion_data = []
        for conv in request.conversions:
            conversion_data.append({
                "click_id": conv.click_id,
                "conversion_time": int(datetime.fromisoformat(conv.conversion_time).timestamp() * 1000),
                "conversion_type": conv.conversion_type,
            })

        result = service.upload_conversion(
            advertiser_id=request.advertiser_id,
            conversions=conversion_data
        )

        return {
            "code": 0,
            "message": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/query")
def query_conversion(
    request: ConversionQueryRequest,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查询转化数据
    """
    try:
        # 获取账户 access_token
        account = db.query(OceanAccount).filter(
            OceanAccount.advertiser_id == request.advertiser_id,
            OceanAccount.tenant_id == current_user.tenant_id
        ).first()

        if not account:
            raise HTTPException(status_code=404, detail="账户不存在")

        # 调用巨量 API
        client = get_ocean_client(account.access_token)
        service = ConversionService(client)

        result = service.query_conversion(
            advertiser_id=request.advertiser_id,
            start_date=request.start_date,
            end_date=request.end_date,
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
