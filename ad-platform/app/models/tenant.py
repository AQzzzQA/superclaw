from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), index=True)
    company_code = Column(String(50), unique=True)
    email = Column(String(255))
    phone = Column(String(20))
    balance = Column(String, default='0')
    status = Column(String(20), default='active')
    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')
    def __repr__(self):
        return f'<Tenant(id={self.id}, name={self.company_name})>'
