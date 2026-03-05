from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Conversion(Base):
    """转化表"""
    __tablename__ = 'conversions'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    advertiser_id = Column(String(64), index=True)

    click_id = Column(String(128), index=True)
    conversion_type = Column(String(64), index=True)
    conversion_time = Column(String(50), index=True)
    value = Column(Float, default=0)

    status = Column(String(20), default='success')

    created_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f'<Conversion(id={self.id}, click_id={self.click_id}, type={self.conversion_type})>'
