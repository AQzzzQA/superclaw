"""
批量操作 API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.response import APIResponse
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


class BatchUpdateStatusRequest(BaseModel):
    """批量更新状态请求"""
    ids: List[int]
    status: str  # enable | disable


class BatchUpdateRequest(BaseModel):
    """批量更新请求"""
    ids: List[int]
    data: dict


# 模拟数据库（实际应从数据库读取）
campaigns_db = []
adgroups_db = []
creatives_db = []


# 广告计划批量操作
@router.post("/campaign/batch-update-status")
async def batch_update_campaign_status(req: BatchUpdateStatusRequest):
    """批量更新广告计划状态"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if req.status not in ["enable", "disable"]:
        raise BadRequestException("status 必须为 enable 或 disable")

    updated_count = 0
    for campaign_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count,
            "status": req.status
        },
        message=f"成功更新 {updated_count} 个广告计划状态"
    )


@router.post("/campaign/batch-update")
async def batch_update_campaigns(req: BatchUpdateRequest):
    """批量更新广告计划"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if not req.data:
        raise BadRequestException("data 不能为空")

    updated_count = 0
    for campaign_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count
        },
        message=f"成功更新 {updated_count} 个广告计划"
    )


# 广告组批量操作
@router.post("/adgroup/batch-update-status")
async def batch_update_adgroup_status(req: BatchUpdateStatusRequest):
    """批量更新广告组状态"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if req.status not in ["enable", "disable"]:
        raise BadRequestException("status 必须为 enable 或 disable")

    updated_count = 0
    for adgroup_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count,
            "status": req.status
        },
        message=f"成功更新 {updated_count} 个广告组状态"
    )


@router.post("/adgroup/batch-update")
async def batch_update_adgroups(req: BatchUpdateRequest):
    """批量更新广告组"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if not req.data:
        raise BadRequestException("data 不能为空")

    updated_count = 0
    for adgroup_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count
        },
        message=f"成功更新 {updated_count} 个广告组"
    )


# 创意批量操作
@router.post("/creative/batch-update-status")
async def batch_update_creative_status(req: BatchUpdateStatusRequest):
    """批量更新创意状态"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if req.status not in ["enable", "disable"]:
        raise BadRequestException("status 必须为 enable 或 disable")

    updated_count = 0
    for creative_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count,
            "status": req.status
        },
        message=f"成功更新 {updated_count} 个创意状态"
    )


@router.post("/creative/batch-update")
async def batch_update_creatives(req: BatchUpdateRequest):
    """批量更新创意"""
    if not req.ids:
        raise BadRequestException("ids 不能为空")

    if not req.data:
        raise BadRequestException("data 不能为空")

    updated_count = 0
    for creative_id in req.ids:
        # 实际应调用 service 层
        updated_count += 1

    return APIResponse.success(
        data={
            "updated_count": updated_count
        },
        message=f"成功更新 {updated_count} 个创意"
    )
