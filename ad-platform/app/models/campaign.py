from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Campaign(Base):
    """广告计划"""
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)

    campaign_id = Column(Integer, index=True)
    campaign_name = Column(String(200))
    objective_type = Column(String(50))
    budget = Column(Float)
    status = Column(String(20), default='enable')

    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f"<Campaign(id={self.id}, campaign_id={self.campaign_id}, name={self.campaign_name})>"
