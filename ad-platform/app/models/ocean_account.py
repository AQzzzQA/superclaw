from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class OceanAccount(Base):
    """巨量账户"""
    __tablename__ = 'ocean_accounts'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)

    advertiser_id = Column(String(64), index=True)
    account_name = Column(String(200))
    account_type = Column(String(50))

    access_token = Column(Text)
    expires_at = Column(String(50))

    status = Column(String(20), default='active')
    is_authorized = Column(Boolean, default=False)

    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f"<OceanAccount(id={self.id}, advertiser_id={self.advertiser_id})>"
