"""
出价策略优化数据验证 Schema
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


# 出价策略相关 Schema

class BiddingStrategyBase(BaseModel):
    """出价策略基础 Schema"""
    name: str = Field(default=None, description="策略名称")
    strategy_type: Literal["ocpa", "ocpc", "roas"] = Field(default=None, description="策略类型")
    target_cpa: Optional[float] = Field(None, description="目标转化成本")
    target_cpc: Optional[float] = Field(None, description="目标点击成本")
    target_roas: Optional[float] = Field(None, description="目标ROI")
    min_bid: float = Field(0.10, description="最低出价")
    max_bid: float = Field(10.0, description="最高出价")
    learning_period: int = Field(7, description="学习周期（天）")
    is_enabled: bool = Field(True, description="是否启用")


class BiddingStrategyCreate(BiddingStrategyBase):
    """创建出价策略 Schema"""
    campaign_id: int = Field(default=None, description="广告计划ID")


class BiddingStrategyUpdate(BaseModel):
    """更新出价策略 Schema"""
    name: Optional[str] = None
    target_cpa: Optional[float] = None
    target_cpc: Optional[float] = None
    target_roas: Optional[float] = None
    min_bid: Optional[float] = None
    max_bid: Optional[float] = None
    learning_period: Optional[int] = None
    is_enabled: Optional[bool] = None


class BiddingStrategyResponse(BiddingStrategyBase):
    """出价策略响应 Schema"""
    id: int
    campaign_id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 出价规则相关 Schema

class BiddingRuleBase(BaseModel):
    """出价规则基础 Schema"""
    rule_name: str = Field(default=None, description="规则名称")
    rule_type: Literal["hourly", "daily", "weekly", "custom"] = Field(default=None, description="规则类型")
    adjustment_type: Literal["percentage", "fixed"] = Field(default=None, description="调整类型")
    adjustment_value: float = Field(default=None, description="调整值")
    conditions: Dict[str, Any] = Field(default=None, description="触发条件")
    is_enabled: bool = Field(True, description="是否启用")


class BiddingRuleCreate(BiddingRuleBase):
    """创建出价规则 Schema"""
    strategy_id: int = Field(default=None, description="策略ID")


class BiddingRuleUpdate(BaseModel):
    """更新出价规则 Schema"""
    rule_name: Optional[str] = None
    adjustment_type: Optional[Literal["percentage", "fixed"]] = None
    adjustment_value: Optional[float] = None
    conditions: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None


class BiddingRuleResponse(BiddingRuleBase):
    """出价规则响应 Schema"""
    id: int
    strategy_id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 策略效果相关 Schema

class StrategyPerformanceMetrics(BaseModel):
    """策略效果指标"""
    strategy_id: int
    total_impressions: int = Field(default=None, description="总曝光")
    total_clicks: int = Field(default=None, description="总点击")
    total_conversions: int = Field(default=None, description="总转化")
    total_cost: float = Field(default=None, description="总消耗")
    actual_cpa: float = Field(default=None, description="实际转化成本")
    actual_cpc: float = Field(default=None, description="实际点击成本")
    actual_roas: float = Field(default=None, description="实际ROI")
    ctr: float = Field(default=None, description="点击率")
    cvr: float = Field(default=None, description="转化率")
