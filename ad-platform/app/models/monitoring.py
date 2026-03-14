"""
实时监控与预警数据模型
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


class AlertRule(Base):
    """预警规则模型"""

    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True, index=True)

    # 规则配置
    name = Column(String(200), nullable=False, index=True, comment="预警规则名称")
    rule_type = Column(String(50), nullable=False, comment="预警类型")
    threshold = Column(Float, nullable=False, comment="阈值")
    period = Column(String(20), nullable=False, comment="周期")
    action = Column(String(50), nullable=False, comment="触发动作")
    is_enabled = Column(Boolean, default=True, comment="是否启用")

    # 监控配置
    metric_name = Column(String(100), nullable=True, comment="监控指标名称")
    comparison_operator = Column(String(20), default=">", comment="比较运算符")

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )
    last_triggered_at = Column(DateTime, nullable=True, comment="最后触发时间")
    trigger_count = Column(Integer, default=0, comment="触发次数")

    # 关系
    campaign = relationship("Campaign", back_populates="alert_rules")
    alert_events = relationship("AlertEvent", back_populates="rule")

    def __repr__(self):
        return f"<AlertRule(id={self.id}, name={self.name}, type={self.rule_type})>"


class AlertEvent(Base):
    """预警事件模型"""

    __tablename__ = "alert_events"

    id = Column(BigInteger, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id"), nullable=False, index=True
    )
    rule_id = Column(Integer, ForeignKey("alert_rules.id"), nullable=False, index=True)

    # 预警信息
    alert_type = Column(String(50), nullable=False, comment="预警类型")
    alert_message = Column(Text, nullable=False, comment="预警消息")
    current_value = Column(Float, nullable=False, comment="当前值")
    threshold_value = Column(Float, nullable=False, comment="阈值")
    severity = Column(String(20), nullable=False, comment="严重程度")
    is_resolved = Column(Boolean, default=False, comment="是否已解决")

    # 触发动作记录
    action_taken = Column(JSON, nullable=True, comment="执行的动作")
    action_result = Column(String(500), nullable=True, comment="动作结果")

    # 元数据
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    resolved_at = Column(DateTime, nullable=True, comment="解决时间")
    resolved_by = Column(
        Integer, ForeignKey("users.id"), nullable=True, comment="解决人"
    )

    # 关系
    campaign = relationship("Campaign")
    rule = relationship("AlertRule", back_populates="alert_events")

    def __repr__(self):
        return f"<AlertEvent(id={self.id}, type={self.alert_type}, severity={self.severity})>"


class RealtimeMetrics(Base):
    """实时数据指标模型"""

    __tablename__ = "realtime_metrics"

    id = Column(BigInteger, primary_key=True, index=True)
    campaign_id = Column(
        Integer, ForeignKey("campaigns.id"), nullable=False, index=True
    )
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    # 实时指标
    show_count = Column(Integer, default=0, comment="曝光量")
    click_count = Column(Integer, default=0, comment="点击量")
    convert_count = Column(Integer, default=0, comment="转化量")
    cost = Column(Float, default=0.0, comment="消耗")
    ctr = Column(Float, default=0.0, comment="点击率")
    cvr = Column(Float, default=0.0, comment="转化率")
    roi = Column(Float, nullable=True, comment="ROI")

    # 时间戳
    metric_time = Column(DateTime, nullable=False, index=True, comment="指标时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关系
    campaign = relationship("Campaign")

    def __repr__(self):
        return f"<RealtimeMetrics(id={self.id}, campaign_id={self.campaign_id}, time={self.metric_time})>"
