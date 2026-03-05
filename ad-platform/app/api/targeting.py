"""
定向投放 API 接口
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.response import success_response, error_response
from app.models.user import User
from app.schemas.targeting import (
    # 人群定向
    AudienceTargetingCreate,
    AudienceTargetingUpdate,
    AudienceTargetingResponse,
    # 设备定向
    DeviceTargetingCreate,
    DeviceTargetingUpdate,
    DeviceTargetingResponse,
    # 地域定向
    GeoTargetingCreate,
    GeoTargetingUpdate,
    GeoTargetingResponse,
    # 时间定向
    TimeTargetingCreate,
    TimeTargetingUpdate,
    TimeTargetingResponse,
    # 环境定向
    EnvironmentTargetingCreate,
    EnvironmentTargetingUpdate,
    EnvironmentTargetingResponse
)
from app.services.targeting import (
    AudienceTargetingService,
    DeviceTargetingService,
    GeoTargetingService,
    TimeTargetingService,
    EnvironmentTargetingService
)

router = APIRouter(prefix="/targeting", tags=["定向投放"])


# ============================================================================
# 人群定向 API
# ============================================================================

@router.get("/audience", response_model=List[AudienceTargetingResponse])
def get_audience_targetings(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取人群定向列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    targetings = AudienceTargetingService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit
    )
    return targetings


@router.get("/audience/{targeting_id}", response_model=AudienceTargetingResponse)
def get_audience_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个人群定向

    - **targeting_id**: 定向ID
    """
    targeting = AudienceTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="人群定向不存在")
    return targeting


@router.post("/audience", response_model=AudienceTargetingResponse)
def create_audience_targeting(
    obj_in: AudienceTargetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建人群定向

    - **targeting_type**: 定向类型
    - **targeting_value**: 定向值（JSON格式）
    - **is_include**: 包含或排除
    - **campaign_id**: 广告计划ID
    """
    try:
        targeting = AudienceTargetingService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id
        )
        return targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/audience/{targeting_id}", response_model=AudienceTargetingResponse)
def update_audience_targeting(
    targeting_id: int,
    obj_in: AudienceTargetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新人群定向

    - **targeting_id**: 定向ID
    - **obj_in**: 更新数据
    """
    targeting = AudienceTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="人群定向不存在")

    try:
        # 解析 JSON 字符串返回给前端
        updated_targeting = AudienceTargetingService.update(
            db=db,
            db_obj=targeting,
            obj_in=obj_in
        )
        return updated_targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/audience/{targeting_id}")
def delete_audience_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除人群定向

    - **targeting_id**: 定向ID
    """
    try:
        AudienceTargetingService.delete(
            db=db,
            id=targeting_id,
            tenant_id=current_user.tenant_id
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 设备定向 API
# ============================================================================

@router.get("/device", response_model=List[DeviceTargetingResponse])
def get_device_targetings(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取设备定向列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    targetings = DeviceTargetingService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit
    )
    return targetings


@router.get("/device/{targeting_id}", response_model=DeviceTargetingResponse)
def get_device_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个设备定向

    - **targeting_id**: 定向ID
    """
    targeting = DeviceTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="设备定向不存在")
    return targeting


@router.post("/device", response_model=DeviceTargetingResponse)
def create_device_targeting(
    obj_in: DeviceTargetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建设备定向

    - **os_type**: 操作系统
    - **os_version_min**: 最低版本
    - **os_version_max**: 最高版本
    - **device_brand**: 设备品牌
    - **device_model**: 设备型号
    - **device_type**: 设备类型
    - **network_type**: 网络类型
    - **campaign_id**: 广告计划ID
    """
    try:
        targeting = DeviceTargetingService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id
        )
        return targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/device/{targeting_id}", response_model=DeviceTargetingResponse)
def update_device_targeting(
    targeting_id: int,
    obj_in: DeviceTargetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新设备定向

    - **targeting_id**: 定向ID
    - **obj_in**: 更新数据
    """
    targeting = DeviceTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="设备定向不存在")

    try:
        updated_targeting = DeviceTargetingService.update(
            db=db,
            db_obj=targeting,
            obj_in=obj_in
        )
        return updated_targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/device/{targeting_id}")
def delete_device_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除设备定向

    - **targeting_id**: 定向ID
    """
    try:
        DeviceTargetingService.delete(
            db=db,
            id=targeting_id,
            tenant_id=current_user.tenant_id
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 地域定向 API
# ============================================================================

@router.get("/geo", response_model=List[GeoTargetingResponse])
def get_geo_targetings(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取地域定向列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    targetings = GeoTargetingService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit
    )
    return targetings


@router.get("/geo/{targeting_id}", response_model=GeoTargetingResponse)
def get_geo_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个地域定向

    - **targeting_id**: 定向ID
    """
    targeting = GeoTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="地域定向不存在")
    return targeting


@router.post("/geo", response_model=GeoTargetingResponse)
def create_geo_targeting(
    obj_in: GeoTargetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建地域定向

    - **targeting_type**: 地域类型
    - **geo_level**: 地域级别
    - **geo_list**: 地域列表
    - **is_exclude**: 是否排除模式
    - **latitude**: 纬度（LBS定向使用）
    - **longitude**: 经度（LBS定向使用）
    - **radius**: 半径（LBS定向使用）
    - **campaign_id**: 广告计划ID
    """
    try:
        targeting = GeoTargetingService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id
        )
        return targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/geo/{targeting_id}", response_model=GeoTargetingResponse)
def update_geo_targeting(
    targeting_id: int,
    obj_in: GeoTargetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新地域定向

    - **targeting_id**: 定向ID
    - **obj_in**: 更新数据
    """
    targeting = GeoTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="地域定向不存在")

    try:
        updated_targeting = GeoTargetingService.update(
            db=db,
            db_obj=targeting,
            obj_in=obj_in
        )
        return updated_targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/geo/{targeting_id}")
def delete_geo_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除地域定向

    - **targeting_id**: 定向ID
    """
    try:
        GeoTargetingService.delete(
            db=db,
            id=targeting_id,
            tenant_id=current_user.tenant_id
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 时间定向 API
# ============================================================================

@router.get("/time", response_model=List[TimeTargetingResponse])
def get_time_targetings(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取时间定向列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    targetings = TimeTargetingService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit
    )
    return targetings


@router.get("/time/{targeting_id}", response_model=TimeTargetingResponse)
def get_time_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个时间定向

    - **targeting_id**: 定向ID
    """
    targeting = TimeTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="时间定向不存在")
    return targeting


@router.post("/time", response_model=TimeTargetingResponse)
def create_time_targeting(
    obj_in: TimeTargetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建时间定向

    - **targeting_type**: 时间类型
    - **time_config**: 时间配置（JSON格式）
    - **timezone**: 时区
    - **campaign_id**: 广告计划ID
    """
    try:
        targeting = TimeTargetingService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id
        )
        return targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/time/{targeting_id}", response_model=TimeTargetingResponse)
def update_time_targeting(
    targeting_id: int,
    obj_in: TimeTargetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新时间定向

    - **targeting_id**: 定向ID
    - **obj_in**: 更新数据
    """
    targeting = TimeTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="时间定向不存在")

    try:
        updated_targeting = TimeTargetingService.update(
            db=db,
            db_obj=targeting,
            obj_in=obj_in
        )
        return updated_targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/time/{targeting_id}")
def delete_time_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除时间定向

    - **targeting_id**: 定向ID
    """
    try:
        TimeTargetingService.delete(
            db=db,
            id=targeting_id,
            tenant_id=current_user.tenant_id
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 环境定向 API
# ============================================================================

@router.get("/environment", response_model=List[EnvironmentTargetingResponse])
def get_environment_targetings(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取环境定向列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    targetings = EnvironmentTargetingService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit
    )
    return targetings


@router.get("/environment/{targeting_id}", response_model=EnvironmentTargetingResponse)
def get_environment_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个环境定向

    - **targeting_id**: 定向ID
    """
    targeting = EnvironmentTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="环境定向不存在")
    return targeting


@router.post("/environment", response_model=EnvironmentTargetingResponse)
def create_environment_targeting(
    obj_in: EnvironmentTargetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建环境定向

    - **network_type**: 网络类型
    - **carrier**: 运营商
    - **app_environment**: App环境
    - **device_price**: 设备价格区间
    - **campaign_id**: 广告计划ID
    """
    try:
        targeting = EnvironmentTargetingService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id
        )
        return targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/environment/{targeting_id}", response_model=EnvironmentTargetingResponse)
def update_environment_targeting(
    targeting_id: int,
    obj_in: EnvironmentTargetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新环境定向

    - **targeting_id**: 定向ID
    - **obj_in**: 更新数据
    """
    targeting = EnvironmentTargetingService.get(
        db=db,
        id=targeting_id,
        tenant_id=current_user.tenant_id
    )
    if not targeting:
        return error_response(code=404, message="环境定向不存在")

    try:
        updated_targeting = EnvironmentTargetingService.update(
            db=db,
            db_obj=targeting,
            obj_in=obj_in
        )
        return updated_targeting
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/environment/{targeting_id}")
def delete_environment_targeting(
    targeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除环境定向

    - **targeting_id**: 定向ID
    """
    try:
        EnvironmentTargetingService.delete(
            db=db,
            id=targeting_id,
            tenant_id=current_user.tenant_id
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))
