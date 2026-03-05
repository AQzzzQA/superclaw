"""
定向投放数据验证 Schema
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# 人群定向相关 Schema

class AudienceTargetingBase(BaseModel):
    """人群定向基础 Schema"""
    targeting_type: str = Field(default=None, description="定向类型：interest, behavior, custom")
    targeting_value: Dict[str, Any] = Field(default=None, description="定向值，JSON格式")
    is_include: bool = Field(True, description="包含或排除")

    @validator('targeting_type')
    def validate_targeting_type(cls, v):
        valid_types = ['interest', 'behavior', 'custom']
        if v not in valid_types:
            raise ValueError(f"定向类型必须是: {', '.join(valid_types)}")
        return v


class AudienceTargetingCreate(AudienceTargetingBase):
    """创建人群定向 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class AudienceTargetingUpdate(AudienceTargetingBase):
    """更新人群定向 Schema"""
    pass


class AudienceTargetingResponse(AudienceTargetingBase):
    """人群定向响应 Schema"""
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 设备定向相关 Schema

class DeviceTargetingBase(BaseModel):
    """设备定向基础 Schema"""
    os_type: Optional[str] = Field(None, description="操作系统")
    os_version_min: Optional[str] = Field(None, description="最低版本")
    os_version_max: Optional[str] = Field(None, description="最高版本")
    device_brand: Optional[str] = Field(None, description="设备品牌")
    device_model: Optional[str] = Field(None, description="设备型号")
    device_type: Optional[str] = Field(None, description="设备类型")
    network_type: Optional[str] = Field(None, description="网络类型")

    @validator('os_type')
    def validate_os_type(cls, v):
        if v and v not in ['iOS', 'Android', 'All']:
            raise ValueError("操作系统必须是: iOS, Android, All")
        return v

    @validator('device_type')
    def validate_device_type(cls, v):
        if v and v not in ['phone', 'tablet', 'all']:
            raise ValueError("设备类型必须是: phone, tablet, all")
        return v

    @validator('network_type')
    def validate_network_type(cls, v):
        if v and v not in ['WiFi', '4G', '5G', 'All']:
            raise ValueError("网络类型必须是: WiFi, 4G, 5G, All")
        return v


class DeviceTargetingCreate(DeviceTargetingBase):
    """创建设备定向 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class DeviceTargetingUpdate(DeviceTargetingBase):
    """更新设备定向 Schema"""
    pass


class DeviceTargetingResponse(DeviceTargetingBase):
    """设备定向响应 Schema"""
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 地域定向相关 Schema

class GeoTargetingBase(BaseModel):
    """地域定向基础 Schema"""
    targeting_type: str = Field(default=None, description="地域类型：province, city, district, business_area, lbs")
    geo_level: int = Field(default=None, description="地域级别：1=省，2=市，3=区，4=商圈，5=LBS")
    geo_list: List[str] = Field(default=None, description="地域列表")
    is_exclude: bool = Field(False, description="是否排除模式")
    latitude: Optional[str] = Field(None, description="纬度（LBS定向使用）")
    longitude: Optional[str] = Field(None, description="经度（LBS定向使用）")
    radius: Optional[int] = Field(None, description="半径（米）")

    @validator('geo_level')
    def validate_geo_level(cls, v):
        if v < 1 or v > 5:
            raise ValueError("地域级别必须是: 1-5")
        return v

    @validator('targeting_type')
    def validate_targeting_type(cls, v):
        valid_types = ['province', 'city', 'district', 'business_area', 'lbs']
        if v not in valid_types:
            raise ValueError(f"地域类型必须是: {', '.join(valid_types)}")
        return v


class GeoTargetingCreate(GeoTargetingBase):
    """创建地域定向 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class GeoTargetingUpdate(GeoTargetingBase):
    """更新地域定向 Schema"""
    pass


class GeoTargetingResponse(GeoTargetingBase):
    """地域定向响应 Schema"""
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 时间定向相关 Schema

class TimeTargetingBase(BaseModel):
    """时间定向基础 Schema"""
    targeting_type: str = Field(default=None, description="时间类型：hour, day, week, custom")
    time_config: Dict[str, Any] = Field(default=None, description="时间配置，JSON格式")
    timezone: str = Field('Asia/Shanghai', description="时区")

    @validator('targeting_type')
    def validate_targeting_type(cls, v):
        valid_types = ['hour', 'day', 'week', 'custom']
        if v not in valid_types:
            raise ValueError(f"时间类型必须是: {', '.join(valid_types)}")
        return v


class TimeTargetingCreate(TimeTargetingBase):
    """创建时间定向 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class TimeTargetingUpdate(TimeTargetingBase):
    """更新时间定向 Schema"""
    pass


class TimeTargetingResponse(TimeTargetingBase):
    """时间定向响应 Schema"""
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 环境定向相关 Schema

class EnvironmentTargetingBase(BaseModel):
    """环境定向基础 Schema"""
    network_type: Optional[str] = Field(None, description="网络类型")
    carrier: Optional[str] = Field(None, description="运营商")
    app_environment: Optional[str] = Field(None, description="App环境")
    device_price: Optional[Dict[str, int]] = Field(None, description="设备价格区间")

    @validator('network_type')
    def validate_network_type(cls, v):
        if v and v not in ['WiFi', '4G', '5G', 'All']:
            raise ValueError("网络类型必须是: WiFi, 4G, 5G, All")
        return v

    @validator('carrier')
    def validate_carrier(cls, v):
        if v and v not in ['移动', '联通', '电信']:
            raise ValueError("运营商必须是: 移动, 联通, 电信")
        return v

    @validator('app_environment')
    def validate_app_environment(cls, v):
        if v and v not in ['production', 'test', 'all']:
            raise ValueError("App环境必须是: production, test, all")
        return v


class EnvironmentTargetingCreate(EnvironmentTargetingBase):
    """创建环境定向 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class EnvironmentTargetingUpdate(EnvironmentTargetingBase):
    """更新环境定向 Schema"""
    pass


class EnvironmentTargetingResponse(EnvironmentTargetingBase):
    """环境定向响应 Schema"""
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
