from datetime import datetime, timedelta
"""
实时监控与预警业务逻辑服务
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.monitoring import AlertRule, AlertEvent, RealtimeMetrics
from app.schemas.monitoring import (
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertEventCreate,
)
from app.core.exceptions import ValidationError, NotFoundError


class AlertRuleService:
    """预警规则服务"""

    @staticmethod
    def create(db: Session, obj_in: AlertRuleCreate, tenant_id: int) -> AlertRule:
        """创建预警规则"""
        try:
            db_obj = AlertRule(
                tenant_id=tenant_id,
                **obj_in.dict()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建预警规则失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[AlertRule]:
        """获取单个预警规则"""
        return db.query(AlertRule).filter(
            and_(AlertRule.id == id, AlertRule.tenant_id == tenant_id)
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AlertRule]:
        """获取预警规则列表"""
        query = db.query(AlertRule).filter(
            AlertRule.tenant_id == tenant_id
        )
        if campaign_id:
            query = query.filter(AlertRule.campaign_id == campaign_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: AlertRule,
        obj_in: AlertRuleUpdate
    ) -> AlertRule:
        """更新预警规则"""
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新预警规则失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除预警规则"""
        db_obj = AlertRuleService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("预警规则不存在")
        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除预警规则失败: {str(e)}")

    @staticmethod
    def trigger_alert(db: Session, rule: AlertRule, current_value: float) -> AlertEvent:
        """触发预警"""
        try:
            # 根据规则类型和阈值判断是否触发
            is_triggered = False
            if rule.rule_type == 'cost_alert':
                is_triggered = current_value >= rule.threshold
            elif rule.rule_type == 'performance_alert':
                is_triggered = current_value <= rule.threshold  # 性能下降
            elif rule.rule_type == 'anomaly_detection':
                # 异常检测逻辑（简化版）
                is_triggered = abs(current_value - rule.threshold) > rule.threshold * 0.5

            if is_triggered:
                # 创建预警事件
                alert_event = AlertEvent(
                    tenant_id=rule.tenant_id,
                    campaign_id=rule.campaign_id,
                    rule_id=rule.id,
                    alert_type=rule.rule_type,
                    alert_message=f"{rule.name} 触发：当前值 {current_value}，阈值 {rule.threshold}",
                    current_value=current_value,
                    threshold_value=rule.threshold,
                    severity="high",
                )
                db.add(alert_event)

                # 更新规则触发计数和时间
                rule.last_triggered_at = datetime.now()
                rule.trigger_count += 1

                db.commit()
                return alert_event

            return None
        except Exception as e:
            db.rollback()
            raise ValidationError(f"触发预警失败: {str(e)}")


class AlertEventService:
    """预警事件服务"""

    @staticmethod
    def create(db: Session, obj_in: AlertEventCreate, tenant_id: int) -> AlertEvent:
        """创建预警事件"""
        try:
            db_obj = AlertEvent(
                tenant_id=tenant_id,
                **obj_in.dict()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建预警事件失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[AlertEvent]:
        """获取单个预警事件"""
        return db.query(AlertEvent).filter(
            and_(AlertEvent.id == id, AlertEvent.tenant_id == tenant_id)
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        rule_id: Optional[int] = None,
        is_resolved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AlertEvent]:
        """获取预警事件列表"""
        query = db.query(AlertEvent).filter(AlertEvent.tenant_id == tenant_id)

        if campaign_id:
            query = query.filter(AlertEvent.campaign_id == campaign_id)
        if rule_id:
            query = query.filter(AlertEvent.rule_id == rule_id)
        if is_resolved is not None:
            query = query.filter(AlertEvent.is_resolved == is_resolved)

        return query.order_by(AlertEvent.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def resolve(db: Session, id: int, tenant_id: int, resolved_by: int) -> bool:
        """解决预警事件"""
        db_obj = AlertEventService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("预警事件不存在")
        try:
            db_obj.is_resolved = True
            db_obj.resolved_at = datetime.now()
            db_obj.resolved_by = resolved_by
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"解决预警事件失败: {str(e)}")


class RealtimeMetricsService:
    """实时数据服务"""

    @staticmethod
    def create_or_update(db: Session, data: Dict[str, Any]) -> RealtimeMetrics:
        """创建或更新实时数据"""
        try:
            # 检查是否存在同一时间的数据
            existing = db.query(RealtimeMetrics).filter(
                and_(
                    RealtimeMetrics.campaign_id == data['campaign_id'],
                    RealtimeMetrics.metric_time == data['metric_time']
                )
            ).first()

            if existing:
                # 更新
                for key, value in data.items():
                    if key != 'campaign_id':
                        setattr(existing, key, value)
                db.commit()
                db.refresh(existing)
                return existing
            else:
                # 创建
                db_obj = RealtimeMetrics(**data)
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
                return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新实时数据失败: {str(e)}")

    @staticmethod
    def get_metrics(
        db: Session,
        tenant_id: int,
        campaign_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> List[RealtimeMetrics]:
        """获取实时数据"""
        return db.query(RealtimeMetrics).filter(
            and_(
                RealtimeMetrics.tenant_id == tenant_id,
                RealtimeMetrics.campaign_id == campaign_id,
                RealtimeMetrics.metric_time >= start_time,
                RealtimeMetrics.metric_time <= end_time,
            )
        ).order_by(RealtimeMetrics.metric_time.desc()).all()

    @staticmethod
    def get_aggregated_metrics(
        db: Session,
        tenant_id: int,
        campaign_ids: List[int],
        start_time: datetime,
        end_time: datetime,
    ) -> Dict[str, Any]:
        """获取聚合指标"""
        from sqlalchemy import func

        query = db.query(RealtimeMetrics).filter(
            and_(
                RealtimeMetrics.tenant_id == tenant_id,
                RealtimeMetrics.campaign_id.in_(campaign_ids),
                RealtimeMetrics.metric_time >= start_time,
                RealtimeMetrics.metric_time <= end_time,
            )
        )

        total_show = query.with_entities(func.sum(RealtimeMetrics.show_count)).scalar() or 0
        total_click = query.with_entities(func.sum(RealtimeMetrics.click_count)).scalar() or 0
        total_convert = query.with_entities(func.sum(RealtimeMetrics.convert_count)).scalar() or 0
        total_cost = query.with_entities(func.sum(RealtimeMetrics.cost)).scalar() or 0.0

        return {
            'total_show': total_show,
            'total_click': total_click,
            'total_convert': total_convert,
            'total_cost': total_cost,
            'avg_ctr': (total_click / total_show * 100) if total_show > 0 else 0,
            'avg_cvr': (total_convert / total_click * 100) if total_click > 0 else 0,
        }
