from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Creative(Base):
    """创意表"""

    __tablename__ = "creatives"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    advertiser_id = Column(String(64), index=True)

    creative_id = Column(String(64), index=True)
    creative_name = Column(String(200))
    creative_type = Column(Integer, default=1)

    image_url = Column(Text)
    title = Column(String(200))
    description = Column(Text)

    status = Column(Integer, default=1)

    created_at = Column(String(50), default="Asia/Shanghai")
    updated_at = Column(String(50), default="Asia/Shanghai")

    def __repr__(self):
        return f"<Creative(id={self.id}, creative_id={self.creative_id})>"
