"""
定向投放数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class AudienceTargeting(Base):
    """人群定向模型"""
    __tablename__ = 'audience_targeting'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 定向配置
    targeting_type = Column(String(50), nullable=False, comment='定向类型：interest, behavior, custom')
    targeting_value = Column(Text, nullable=False, comment='定向值，JSON格式')
    is_include = Column(Boolean, default=True, comment='包含或排除：True=包含，False=排除')

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    campaign = relationship("Campaign", back_populates="audience_targetings")

    def __repr__(self):
        return f"<AudienceTargeting(id={self.id}, campaign_id={self.campaign_id}, type={self.targeting_type})>"


class DeviceTargeting(Base):
    """设备定向模型"""
    __tablename__ = 'device_targeting'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 操作系统
    os_type = Column(String(50), nullable=True, comment='操作系统：iOS, Android, All')
    os_version_min = Column(String(50), nullable=True, comment='最低版本')
    os_version_max = Column(String(50), nullable=True, comment='最高版本')

    # 设备信息
    device_brand = Column(String(100), nullable=True, comment='设备品牌')
    device_model = Column(String(100), nullable=True, comment='设备型号')
    device_type = Column(String(50), nullable=True, comment='设备类型：phone, tablet, all')

    # 网络类型
    network_type = Column(String(50), nullable=True, comment='网络类型：WiFi, 4G, 5G, All')

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    campaign = relationship("Campaign", back_populates="device_targetings")

    def __repr__(self):
        return f"<DeviceTargeting(id={self.id}, campaign_id={self.campaign_id}, os={self.os_type})>"


class GeoTargeting(Base):
    """地域定向模型"""
    __tablename__ = 'geo_targeting'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 定向类型
    targeting_type = Column(String(50), nullable=False, comment='地域类型：province, city, district, business_area, lbs')
    geo_level = Column(Integer, nullable=False, comment='地域级别：1=省，2=市，3=区，4=商圈，5=LBS')

    # 地域列表
    geo_list = Column(Text, nullable=False, comment='地域列表，JSON格式')
    is_exclude = Column(Boolean, default=False, comment='是否排除模式')

    # LBS 定向
    latitude = Column(String(50), nullable=True, comment='纬度')
    longitude = Column(String(50), nullable=True, comment='经度')
    radius = Column(Integer, nullable=True, comment='半径（米）')

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    campaign = relationship("Campaign", back_populates="geo_targetings")

    def __repr__(self):
        return f"<GeoTargeting(id={self.id}, campaign_id={self.campaign_id}, type={self.targeting_type})>"


class TimeTargeting(Base):
    """时间定向模型"""
    __tablename__ = 'time_targeting'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 定向类型
    targeting_type = Column(String(50), nullable=False, comment='时间类型：hour, day, week, custom')

    # 时间配置
    time_config = Column(Text, nullable=False, comment='时间配置，JSON格式')

    # 时区
    timezone = Column(String(50), default='Asia/Shanghai', comment='时区')

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    campaign = relationship("Campaign", back_populates="time_targetings")

    def __repr__(self):
        return f"<TimeTargeting(id={self.id}, campaign_id={self.campaign_id}, type={self.targeting_type})>"


class EnvironmentTargeting(Base):
    """环境定向模型"""
    __tablename__ = 'environment_targeting'

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 网络定向
    network_type = Column(String(50), nullable=True, comment='网络类型：WiFi, 4G, 5G, All')

    # 运营商
    carrier = Column(String(100), nullable=True, comment='运营商：移动, 联通, 电信')

    # App 环境
    app_environment = Column(String(50), nullable=True, comment='App环境：production, test, all')

    # 设备价格
    device_price = Column(JSON, nullable=True, comment='设备价格区间')

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关系
    campaign = relationship("Campaign", back_populates="environment_targetings")

    def __repr__(self):
        return f"<EnvironmentTargeting(id={self.id}, campaign_id={self.campaign_id}, network={self.network_type})>"
