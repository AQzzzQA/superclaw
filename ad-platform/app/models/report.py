from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class DailyReport(Base):
    """日报表"""
    __tablename__ = 'daily_reports'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    advertiser_id = Column(String(64), index=True)
    report_date = Column(String(50), index=True)

    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0)

    ctr = Column(Float, default=0)
    cvr = Column(Float, default=0)

    created_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f'<DailyReport(id={self.id}, date={self.report_date}, cost={self.cost})>'
