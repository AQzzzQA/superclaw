from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)

    username = Column(String(100), unique=True, index=True)
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)

    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(String(50), default="Asia/Shanghai")
    updated_at = Column(String(50), default="Asia/Shanghai")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
