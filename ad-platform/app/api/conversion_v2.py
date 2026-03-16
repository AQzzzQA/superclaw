"""
转化回传 API v2 - 整合数据库
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Query
from pydantic import BaseModel, Field
from datetime import datetime
from app.core.response import APIResponse
from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.conversion import Conversion
from app.models.ocean_account import OceanAccount
from app.models.user import User
from app.tasks.conversion import batch_upload_conversion_task

router = APIRouter(prefix="/conversion", tags=["Conversion"])


class ConversionItem(BaseModel):
    """转化项"""

    click_id: str = Field(..., description="点击 ID")
    conversion_type: str = Field(..., description="转化类型")
    conversion_time: str = Field(..., description="转化时间（ISO 格式）")
    value: float = Field(0.0, description="转化价值")


class ConversionUploadRequest(BaseModel):
    """上传转化请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    conversions: List[ConversionItem] = Field(..., description="转化数据列表")


class ConversionQueryRequest(BaseModel):
    """转化查询请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    end_date: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    conversion_type: Optional[str] = Field(None, description="转化类型")


@router.post("/upload")
async def upload_conversion(
    request: ConversionUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """上传转化数据（同步）"""
    try:
        # 获取账户
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

        # 构造转化数据
        conversions_data = []
        for conv in request.conversions:
            conversions_data.append(
                {
                    "click_id": conv.click_id,
                    "conversion_type": conv.conversion_type,
                    "conversion_time": int(
                        datetime.fromisoformat(conv.conversion_time).timestamp()
                    ),
                    "value": conv.value,
                }
            )

        # 保存到数据库
        count = 0
        for conv_data in conversions_data:
            conversion = Conversion(
                tenant_id=current_user.tenant_id,
                advertiser_id=request.advertiser_id,
                **conv_data,
            )
            db.add(conversion)
            count += 1

        db.commit()

        return APIResponse.success(
            data={"total": count, "success": count, "failed": 0},
            message=f"成功保存 {count} 条转化数据",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-upload")
async def batch_upload_conversion(
    request: ConversionUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """批量上传转化（同步）"""
    try:
        # 获取账户
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

        # 构造转化数据
        conversions_data = []
        for conv in request.conversions:
            conversions_data.append(
                {
                    "click_id": conv.click_id,
                    "conversion_type": conv.conversion_type,
                    "conversion_time": int(
                        datetime.fromisoformat(conv.conversion_time).timestamp()
                    ),
                    "value": conv.value,
                }
            )

        # 保存到数据库
        success = 0
        for conv_data in conversions_data:
            try:
                conversion = Conversion(
                    tenant_id=current_user.tenant_id,
                    advertiser_id=request.advertiser_id,
                    **conv_data,
                )
                db.add(conversion)
                success += 1
            except Exception as e:
                pass

        db.commit()

        failed = len(conversions_data) - success

        return APIResponse.success(
            data={
                "total": len(conversions_data),
                "success": success,
                "failed": failed,
            },
            message=f"上传完成：成功 {success} 条，失败 {failed} 条",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-upload-async")
async def batch_upload_conversion_async(
    request: ConversionUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """批量上传转化（异步）"""
    try:
        # 获取账户
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

        # 构造转化数据
        conversions_data = []
        for conv in request.conversions:
            conversions_data.append(
                {
                    "click_id": conv.click_id,
                    "conversion_type": conv.conversion_type,
                    "conversion_time": int(
                        datetime.fromisoformat(conv.conversion_time).timestamp()
                    ),
                    "value": conv.value,
                }
            )

        # 提交异步任务
        task = batch_upload_conversion_task.apply_async(args=[conversions_data])

        return APIResponse.success(
            data={
                "task_id": task.id,
                "status": "pending",
                "total": len(conversions_data),
            },
            message=f"批量上传任务已提交，共 {len(conversions_data)} 条",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query")
async def query_conversions(
    advertiser_id: str = Query(..., description="广告主 ID"),
    start_date: str = Query(..., description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="结束日期 (YYYY-MM-DD)"),
    conversion_type: Optional[str] = Query(None, description="转化类型"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询转化数据"""
    try:
        # 构建查询
        query = db.query(Conversion).filter(
            Conversion.tenant_id == current_user.tenant_id,
            Conversion.advertiser_id == advertiser_id,
        )

        if start_date:
            query = query.filter(
                Conversion.conversion_time
                >= datetime.strptime(start_date, "%Y-%m-%d").timestamp()
            )
        if end_date:
            query = query.filter(
                Conversion.conversion_time
                <= datetime.strptime(end_date, "%Y-%m-%d").timestamp()
            )
        if conversion_type:
            query = query.filter(Conversion.conversion_type == conversion_type)

        # 排序
        query = query.order_by(Conversion.conversion_time.desc())

        # 分页
        total = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()

        # 序列化
        data = [
            {
                "id": c.id,
                "click_id": c.click_id,
                "conversion_type": c.conversion_type,
                "conversion_time": datetime.fromtimestamp(
                    c.conversion_time
                ).isoformat(),
                "value": c.value,
            }
            for c in results
        ]

        return APIResponse.success(
            data={"total": total, "page": page, "page_size": page_size, "results": data}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_conversion_stats(
    advertiser_id: str = Query(..., description="广告主 ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取转化统计"""
    try:
        # 获取所有转化
        conversions = (
            db.query(Conversion)
            .filter(
                Conversion.tenant_id == current_user.tenant_id,
                Conversion.advertiser_id == advertiser_id,
            )
            .all()
        )

        if not conversions:
            return APIResponse.success(data={"total": 0, "by_type": {}})

        # 按类型统计
        by_type = {}
        for conv in conversions:
            if conv.conversion_type not in by_type:
                by_type[conv.conversion_type] = 0
            by_type[conv.conversion_type] += 1

        # 总计
        total = len(conversions)
        total_value = sum(c.value or 0 for c in conversions)

        return APIResponse.success(
            data={"total": total, "total_value": total_value, "by_type": by_type}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
