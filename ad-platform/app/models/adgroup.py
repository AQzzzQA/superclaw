from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class AdGroup(Base):
    """广告组"""
    __tablename__ = 'adgroups'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), index=True)

    adgroup_id = Column(String(64), index=True)
    adgroup_name = Column(String(128))
    bid = Column(Float, default=0)
    status = Column(Integer, default=1)

    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f'<AdGroup(id={self.id}, adgroup_id={self.adgroup_id})>'
