"""
实时监控与预警 API 接口
"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.response import success_response, error_response
from app.models.user import User
from app.schemas.monitoring import (
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRuleResponse,
    AlertEventResponse,
    RealtimeDataResponse,
)
from app.services.monitoring import (
    AlertRuleService,
    AlertEventService,
    RealtimeMetricsService,
)

router = APIRouter(prefix="/monitoring", tags=["实时监控"])


# ============================================================================
# 预警规则 API
# ============================================================================

@router.get("/alerts/rules", response_model=List[AlertRuleResponse])
def get_alert_rules(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取预警规则列表

    - **campaign_id**: 广告计划ID（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    rules = AlertRuleService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        skip=skip,
        limit=limit,
    )
    return rules


@router.get("/alerts/rules/{rule_id}", response_model=AlertRuleResponse)
def get_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个预警规则

    - **rule_id**: 规则ID
    """
    rule = AlertRuleService.get(
        db=db,
        id=rule_id,
        tenant_id=current_user.tenant_id,
    )
    if not rule:
        return error_response(code=404, message="预警规则不存在")
    return rule


@router.post("/alerts/rules", response_model=AlertRuleResponse)
def create_alert_rule(
    obj_in: AlertRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建预警规则

    - **name**: 规则名称
    - **rule_type**: 规则类型
    - **threshold**: 阈值
    - **period**: 周期
    - **action**: 触发动作
    - **is_enabled**: 是否启用
    - **campaign_id**: 广告计划ID（可选）
    """
    try:
        rule = AlertRuleService.create(
            db=db,
            obj_in=obj_in,
            tenant_id=current_user.tenant_id,
        )
        return rule
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.put("/alerts/rules/{rule_id}", response_model=AlertRuleResponse)
def update_alert_rule(
    rule_id: int,
    obj_in: AlertRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新预警规则

    - **rule_id**: 规则ID
    - **obj_in**: 更新数据
    """
    rule = AlertRuleService.get(
        db=db,
        id=rule_id,
        tenant_id=current_user.tenant_id,
    )
    if not rule:
        return error_response(code=404, message="预警规则不存在")

    try:
        updated_rule = AlertRuleService.update(
            db=db,
            db_obj=rule,
            obj_in=obj_in,
        )
        return updated_rule
    except Exception as e:
        return error_response(code=400, message=str(e))


@router.delete("/alerts/rules/{rule_id}")
def delete_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除预警规则

    - **rule_id**: 规则ID
    """
    try:
        AlertRuleService.delete(
            db=db,
            id=rule_id,
            tenant_id=current_user.tenant_id,
        )
        return success_response(message="删除成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 预警事件 API
# ============================================================================

@router.get("/alerts/events", response_model=List[AlertEventResponse])
def get_alert_events(
    campaign_id: Optional[int] = Query(None, description="广告计划ID"),
    rule_id: Optional[int] = Query(None, description="规则ID"),
    is_resolved: Optional[bool] = Query(None, description="是否已解决"),
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取预警事件列表

    - **campaign_id**: 广告计划ID（可选）
    - **rule_id**: 规则ID（可选）
    - **is_resolved**: 是否已解决（可选）
    - **skip**: 跳过条数，默认 0
    - **limit**: 返回条数，默认 100，最大 100
    """
    events = AlertEventService.get_multi(
        db=db,
        tenant_id=current_user.tenant_id,
        campaign_id=campaign_id,
        rule_id=rule_id,
        is_resolved=is_resolved,
        skip=skip,
        limit=limit,
    )
    return events


@router.get("/alerts/events/{event_id}", response_model=AlertEventResponse)
def get_alert_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个预警事件

    - **event_id**: 事件ID
    """
    event = AlertEventService.get(
        db=db,
        id=event_id,
        tenant_id=current_user.tenant_id,
    )
    if not event:
        return error_response(code=404, message="预警事件不存在")
    return event


@router.put("/alerts/events/{event_id}/resolve")
def resolve_alert_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    解决预警事件

    - **event_id**: 事件ID
    """
    try:
        AlertEventService.resolve(
            db=db,
            id=event_id,
            tenant_id=current_user.tenant_id,
            resolved_by=current_user.id,
        )
        return success_response(message="解决成功")
    except Exception as e:
        return error_response(code=400, message=str(e))


# ============================================================================
# 实时数据 API
# ============================================================================

@router.get("/realtime", response_model=RealtimeDataResponse)
def get_realtime_data(
    campaign_id: int = Query(..., description="广告计划ID"),
    hours: int = Query(24, ge=1, le=168, description="查询小时数，默认24小时"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取实时数据

    - **campaign_id**: 广告计划ID
    - **hours**: 查询小时数，默认24小时
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    # 获取实时数据（模拟）
    # 实际应该从数据库或缓存中查询
    metrics = [
        {
            'campaign_id': campaign_id,
            'campaign_name': '测试计划',
            'show_count': 1000,
            'click_count': 20,
            'convert_count': 1,
            'cost': 50.0,
            'ctr': 2.0,
            'cvr': 5.0,
            'roi': None,
        }
    ]

    # 计算汇总数据
    summary = {
        'total_show': sum(m['show_count'] for m in metrics),
        'total_click': sum(m['click_count'] for m in metrics),
        'total_convert': sum(m['convert_count'] for m in metrics),
        'total_cost': sum(m['cost'] for m in metrics),
        'avg_ctr': sum(m['ctr'] for m in metrics) / len(metrics) if metrics else 0,
        'avg_cvr': sum(m['cvr'] for m in metrics) / len(metrics) if metrics else 0,
    }

    return {
        'metrics': metrics,
        'summary': summary,
        'last_updated': end_time,
    }


@router.post("/test-alert")
def test_alert(
    rule_type: str = Query(..., description="预警类型"),
    threshold: float = Query(..., description="阈值"),
    current_value: float = Query(..., description="当前值"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    测试预警

    - **rule_type**: 预警类型
    - **threshold**: 阈值
    - **current_value**: 当前值
    """
    # 模拟创建预警规则并触发
    try:
        from app.schemas.monitoring import AlertRuleCreate

        test_rule = AlertRuleCreate(
            name="测试预警",
            rule_type=rule_type,
            threshold=threshold,
            period="hourly",
            action="send_notification",
            is_enabled=True,
        )

        rule = AlertRuleService.create(
            db=db,
            obj_in=test_rule,
            tenant_id=current_user.tenant_id,
        )

        # 触发预警
        alert_event = AlertRuleService.trigger_alert(
            db=db,
            rule=rule,
            current_value=current_value,
        )

        if alert_event:
            return success_response(
                message="预警触发成功",
                data={
                    'alert_id': alert_event.id,
                    'alert_message': alert_event.alert_message,
                }
            )
        else:
            return success_response(message="未达到预警阈值")

    except Exception as e:
        return error_response(code=400, message=str(e))
