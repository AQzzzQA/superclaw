"""
出价策略优化 API 接口
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.response import success_response, error_response
from app.models.user import User
from app.schemas.bidding import (
    BiddingStrategyCreate,
    BiddingStrategyUpdate,
    BiddingStrategyResponse,
    StrategyPerformanceMetrics,
    BiddingRuleCreate,
    BiddingRuleUpdate,
    BiddingRuleResponse,
)
from app.services.bidding import (
    BiddingStrategyService,
    BiddingRuleService,
)

router = APIRouter(prefix="/bidding", tags=["出价策略"])


# ============================================================================
# 出价策略 API
# ============================================================================

@router.get("/strategies", response_model=List[BiddingStrategyResponse])
def get_bidding_strategies(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    is_enabled: Optional[bool] = Query(None, description="是否启用"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取出价策略列表

    - **campaign_id**: 广告计划ID（可选）
    - **is_enabled**: 是否启用（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    strategies = BiddingStrategyService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        is_enabled=is_enabled,
        skip=skip,
        limit=limit,
    )
    return strategies


@router.get("/strategies/{strategy_id}", response_model=BiddingStrategyResponse)
def get_bidding_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个出价策略

    - **strategy_id**: 策略ID
    """
    strategy = BiddingStrategyService.get(
        db=db,
        id=strategy_id,
        tenant_id=current_user.tenant_id,
    )
    if not strategy:
        return error_response(code=404, message="出价策略不存在")
    return strategy


@router.post("/strategies", response_model=BiddingStrategyResponse)
def create_bidding_strategy(
    obj_in: BiddingStrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建出价策略

    - **name**: 策略名称
    - **strategy_type**: 策略类型
    - **target_cpa**: 目标转化成本
    - **target_cpc**: 目标点击成本
    - **target_roas**: 目标ROI
    - **min_bid**: 最低出价
    - **max_bid**: 最高出价
    - **learning_period**: 学习周期
    - **is_enabled**: 是否启用
    - **campaign_id**: 广告计划ID
    """
    try:
        strategy = BiddingStrategyService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id,
        )
        return strategy
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/strategies/{strategy_id}", response_model=BiddingStrategyResponse)
def update_bidding_strategy(
    strategy_id: int,
    obj_in: BiddingStrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新出价策略

    - **strategy_id**: 策略ID
    - **obj_in**: 更新数据
    """
    strategy = BiddingStrategyService.get(
        db=db,
        id=strategy_id,
        tenant_id=current_user.tenant_id,
    )
    if not strategy:
        return error_response(code=404, message="出价策略不存在")

    try:
        updated_strategy = BiddingStrategyService.update(
            db=db,
            db_obj=strategy,
            obj_in=obj_in,
        )
        return updated_strategy
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/strategies/{strategy_id}")
def delete_bidding_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除出价策略

    - **strategy_id**: 策略ID
    """
    try:
        BiddingStrategyService.delete(
            db=db,
            id=strategy_id,
            tenant_id=current_user.tenant_id,
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.post("/strategies/{strategy_id}/activate")
def activate_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    激活策略

    - **strategy_id**: 策略ID
    """
    try:
        strategy = BiddingStrategyService.activate(
            db=db,
            id=strategy_id,
            tenant_id=current_user.tenant_id,
        )
        return success_response(message="策略激活成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.post("/strategies/{strategy_id}/deactivate")
def deactivate_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    停用策略

    - **strategy_id**: 策略ID
    """
    try:
        BiddingStrategyService.deactivate(
            db=db,
            id=strategy_id,
            tenant_id=current_user.tenant_id,
        )
        return success_response(message="策略停用成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.get("/strategies/{strategy_id}/performance")
def get_strategy_performance(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取策略效果

    - **strategy_id**: 策略ID
    """
    strategy = BiddingStrategyService.get(
        db=db,
        id=strategy_id,
        tenant_id=current_user.tenant_id,
    )
    if not strategy:
        return error_response(code=404, message="出价策略不存在")

    # 模拟效果数据
    performance = StrategyPerformanceMetrics(
        strategy_id=strategy_id,
        total_impressions=strategy.total_impressions,
        total_clicks=strategy.total_clicks,
        total_conversions=strategy.total_conversions,
        total_cost=strategy.total_cost,
        actual_cpa=strategy.avg_cpa or 0,
        actual_cpc=strategy.avg_cpc or 0,
        actual_roas=strategy.avg_roas or 0,
        ctr=(strategy.total_clicks / strategy.total_impressions * 100) if strategy.total_impressions > 0 else 0,
        cvr=(strategy.total_conversions / strategy.total_clicks * 100) if strategy.total_clicks > 0 else 0,
    )

    return performance


# ============================================================================
# 出价规则 API
# ============================================================================

@router.get("/rules", response_model=List[BiddingRuleResponse])
def get_bidding_rules(
    strategy_id: Optional[int] = Query(None, description="策略ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取出价规则列表

    - **strategy_id**: 策略ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    rules = BiddingRuleService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        strategy_id=strategy_id,
        skip=skip,
        limit=limit,
    )
    return rules


@router.post("/rules", response_model=BiddingRuleResponse)
def create_bidding_rule(
    obj_in: BiddingRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建出价规则

    - **strategy_id**: 策略ID
    - **rule_name**: 规则名称
    - **rule_type**: 规则类型
    - **adjustment_type**: 调整类型
    - **adjustment_value**: 调整值
    - **conditions**: 触发条件（JSON格式）
    """
    try:
        rule = BiddingRuleService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id,
        )
        return rule
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/rules/{rule_id}", response_model=BiddingRuleResponse)
def update_bidding_rule(
    rule_id: int,
    obj_in: BiddingRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新出价规则

    - **rule_id**: 规则ID
    - **obj_in**: 更新数据
    """
    rule = BiddingRuleService.get(
        db=db,
        id=rule_id,
        tenant_id=current_user.tenant_id,
    )
    if not rule:
        return error_response(code=404, message="出价规则不存在")

    try:
        updated_rule = BiddingRuleService.update(
            db=db,
            db_obj=rule,
            obj_in=obj_in,
        )
        return updated_rule
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/rules/{rule_id}")
def delete_bidding_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除出价规则

    - **rule_id**: 规则ID
    """
    try:
        BiddingRuleService.delete(
            db=db,
            id=rule_id,
            tenant_id=current_user.tenant_id,
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))
