
"""
系统配置模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = 'system_configs'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    key = Column(String(200), nullable=False, unique=True, index=True)
    value = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False)

    # 时间戳
    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f"<SystemConfig(id={self.id}, key={self.key}, tenant_id={self.tenant_id})>"
