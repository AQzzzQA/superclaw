"""
实时监控与预警数据验证 Schema
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime

# 预警规则相关 Schema


class AlertRuleBase(BaseModel):
    """预警规则基础 Schema"""

    name: str = Field(default=None, description="预警规则名称")
    rule_type: Literal["cost_alert", "performance_alert", "anomaly_detection"] = Field(
        ..., description="预警类型"
    )
    threshold: float = Field(default=None, description="阈值")
    period: Literal["hourly", "daily", "weekly"] = Field(
        default=None, description="周期"
    )
    action: Literal["pause_campaign", "send_notification", "both"] = Field(
        ..., description="触发动作"
    )
    is_enabled: bool = Field(True, description="是否启用")


class AlertRuleCreate(AlertRuleBase):
    """创建预警规则 Schema"""

    campaign_id: Optional[int] = Field(None, description="广告计划ID（空表示全局）")


class AlertRuleUpdate(BaseModel):
    """更新预警规则 Schema"""

    name: Optional[str] = None
    threshold: Optional[float] = None
    period: Optional[Literal["hourly", "daily", "weekly"]] = None
    action: Optional[Literal["pause_campaign", "send_notification", "both"]] = None
    is_enabled: Optional[bool] = None


class AlertRuleResponse(AlertRuleBase):
    """预警规则响应 Schema"""

    id: int
    campaign_id: Optional[int]
    tenant_id: int
    created_at: datetime
    updated_at: datetime
    last_triggered_at: Optional[datetime]

    class Config:
        orm_mode = True


# 预警事件相关 Schema


class AlertEventBase(BaseModel):
    """预警事件基础 Schema"""

    rule_id: int = Field(default=None, description="预警规则ID")
    campaign_id: int = Field(default=None, description="广告计划ID")
    alert_type: str = Field(default=None, description="预警类型")
    alert_message: str = Field(default=None, description="预警消息")
    current_value: float = Field(default=None, description="当前值")
    threshold_value: float = Field(default=None, description="阈值")
    severity: Literal["low", "medium", "high", "critical"] = Field(
        default=None, description="严重程度"
    )
    is_resolved: bool = Field(False, description="是否已解决")


class AlertEventCreate(AlertEventBase):
    """创建预警事件 Schema"""

    pass


class AlertEventResponse(AlertEventBase):
    """预警事件响应 Schema"""

    id: int
    tenant_id: int
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True


# 实时数据相关 Schema


class RealtimeMetric(BaseModel):
    """实时数据指标"""

    campaign_id: int
    campaign_name: str
    show_count: int = Field(default=None, description="曝光量")
    click_count: int = Field(default=None, description="点击量")
    convert_count: int = Field(default=None, description="转化量")
    cost: float = Field(default=None, description="消耗")
    ctr: float = Field(default=None, description="点击率")
    cvr: float = Field(default=None, description="转化率")
    roi: Optional[float] = Field(None, description="ROI")


class RealtimeDataResponse(BaseModel):
    """实时数据响应"""

    metrics: List[RealtimeMetric]
    summary: Dict[str, Any]
    last_updated: datetime
