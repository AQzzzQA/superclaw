"""
出价策略优化数据模型
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Text,
    JSON,
    BigInteger,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class BiddingStrategy(Base):
    """出价策略模型"""

    __tablename__ = "bidding_strategies"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id"), nullable=False, index=True
    )

    # 策略配置
    name = Column(String(200), nullable=False, index=True, comment="策略名称")
    strategy_type = Column(
        String(50), nullable=False, comment="策略类型：ocpa, ocpc, roas"
    )
    target_cpa = Column(Float, nullable=True, comment="目标转化成本")
    target_cpc = Column(Float, nullable=True, comment="目标点击成本")
    target_roas = Column(Float, nullable=True, comment="目标ROI")
    min_bid = Column(Float, nullable=False, comment="最低出价")
    max_bid = Column(Float, nullable=False, comment="最高出价")
    learning_period = Column(Integer, default=7, comment="学习周期（天）")

    # 配置参数
    bid_adjustment_factor = Column(Float, default=1.0, comment="出价调整系数")
    confidence_level = Column(Float, default=0.95, comment="置信度")
    is_enabled = Column(Boolean, default=True, comment="是否启用")

    # 效果统计
    total_impressions = Column(Integer, default=0, comment="总曝光")
    total_clicks = Column(Integer, default=0, comment="总点击")
    total_conversions = Column(Integer, default=0, comment="总转化")
    total_cost = Column(Float, default=0.0, comment="总消耗")
    avg_cpa = Column(Float, nullable=True, comment="平均转化成本")
    avg_cpc = Column(Float, nullable=True, comment="平均点击成本")
    avg_roas = Column(Float, nullable=True, comment="平均ROI")

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )
    activated_at = Column(DateTime, nullable=True, comment="激活时间")
    deactivated_at = Column(DateTime, nullable=True, comment="停用时间")

    # 关系
    campaign = relationship("Campaign", back_populates="bidding_strategies")
    bidding_rules = relationship("BiddingRule", back_populates="strategy")

    def __repr__(self):
        return f"<BiddingStrategy(id={self.id}, name={self.name}, type={self.strategy_type})>"


class BiddingRule(Base):
    """出价规则模型"""

    __tablename__ = "bidding_rules"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    strategy_id = Column(
        Integer, ForeignKey("bidding_strategies.id"), nullable=False, index=True
    )

    # 规则配置
    rule_name = Column(String(200), nullable=False, comment="规则名称")
    rule_type = Column(String(50), nullable=False, comment="规则类型")
    adjustment_type = Column(String(20), nullable=False, comment="调整类型")
    adjustment_value = Column(Float, nullable=False, comment="调整值")
    conditions = Column(JSON, nullable=False, comment="触发条件")
    is_enabled = Column(Boolean, default=True, comment="是否启用")

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    # 关系
    strategy = relationship("BiddingStrategy", back_populates="bidding_rules")

    def __repr__(self):
        return (
            f"<BiddingRule(id={self.id}, name={self.rule_name}, type={self.rule_type})>"
        )
