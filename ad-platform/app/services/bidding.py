from datetime import datetime, timedelta
"""
出价策略优化业务逻辑服务
"""
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.bidding import BiddingStrategy, BiddingRule
from app.schemas.bidding import (
    BiddingStrategyCreate,
    BiddingStrategyUpdate,
    BiddingRuleCreate,
    BiddingRuleUpdate,
)
from app.core.exceptions import ValidationError, NotFoundError


class BiddingStrategyService:
    """出价策略服务"""

    @staticmethod
    def create(db: Session, obj_in: BiddingStrategyCreate, tenant_id: int) -> BiddingStrategy:
        """创建出价策略"""
        try:
            db_obj = BiddingStrategy(
                tenant_id=tenant_id,
                **obj_in.dict(),
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建出价策略失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[BiddingStrategy]:
        """获取单个出价策略"""
        return db.query(BiddingStrategy).filter(
            and_(
                BiddingStrategy.id == id,
                BiddingStrategy.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        is_enabled: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[BiddingStrategy]:
        """获取出价策略列表"""
        query = db.query(BiddingStrategy).filter(
            BiddingStrategy.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(BiddingStrategy.campaign_id == campaign_id)
        if is_enabled is not None:
            query = query.filter(BiddingStrategy.is_enabled == is_enabled)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: BiddingStrategy,
        obj_in: BiddingStrategyUpdate
    ) -> BiddingStrategy:
        """更新出价策略"""
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新出价策略失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除出价策略"""
        db_obj = BiddingStrategyService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("出价策略不存在")
        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除出价策略失败: {str(e)}")

    @staticmethod
    def activate(db: Session, id: int, tenant_id: int) -> BiddingStrategy:
        """激活策略"""
        db_obj = BiddingStrategyService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("出价策略不存在")
        try:
            # 停用该计划的其他策略
            db.query(BiddingStrategy).filter(
                and_(
                    BiddingStrategy.campaign_id == db_obj.campaign_id,
                    BiddingStrategy.id != id,
                    BiddingStrategy.tenant_id == tenant_id
                )
            ).update({
                'is_enabled': False,
                'deactivated_at': datetime.now()
            })

            # 激活当前策略
            db_obj.is_enabled = True
            db_obj.activated_at = datetime.now()
            db_obj.deactivated_at = None

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"激活策略失败: {str(e)}")

    @staticmethod
    def deactivate(db: Session, id: int, tenant_id: int) -> BiddingStrategy:
        """停用策略"""
        db_obj = BiddingStrategyService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("出价策略不存在")
        try:
            db_obj.is_enabled = False
            db_obj.deactivated_at = datetime.now()

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"停用策略失败: {str(e)}")

    @staticmethod
    def calculate_bid(
        strategy: BiddingStrategy,
        historical_data: Dict[str, Any]
    ) -> float:
        """计算最优出价"""
        min_bid = strategy.min_bid
        max_bid = strategy.max_bid

        # 简化版出价算法
        # 实际应该使用机器学习模型
        if strategy.strategy_type == 'ocpa':
            # oCPA: 优化转化成本
            target_cpa = strategy.target_cpa or 50.0
            if historical_data.get('avg_cpa'):
                # 基于历史数据调整出价
                adjustment = (target_cpa / historical_data['avg_cpa']) * strategy.bid_adjustment_factor
                bid = adjustment * historical_data.get('avg_cpc', 2.0)
            else:
                bid = min_bid + (max_bid - min_bid) * 0.5

        elif strategy.strategy_type == 'ocpc':
            # oCPC: 优化点击成本
            target_cpc = strategy.target_cpc or 2.0
            if historical_data.get('avg_cpc'):
                adjustment = (target_cpc / historical_data['avg_cpc']) * strategy.bid_adjustment_factor
                bid = adjustment * target_cpc
            else:
                bid = min_bid + (max_bid - min_bid) * 0.5

        elif strategy.strategy_type == 'roas':
            # ROAS: 优化投资回报率
            target_roas = strategy.target_roas or 3.0
            if historical_data.get('avg_roas'):
                adjustment = (target_roas / historical_data['avg_roas']) * strategy.bid_adjustment_factor
                bid = adjustment * historical_data.get('avg_cpc', 2.0)
            else:
                bid = min_bid + (max_bid - min_bid) * 0.5

        else:
            bid = (min_bid + max_bid) / 2

        # 确保出价在范围内
        return max(min(bid, max_bid), min_bid)

    @staticmethod
    def update_performance_metrics(
        db: Session,
        strategy_id: int,
        metrics: Dict[str, Any]
    ) -> BiddingStrategy:
        """更新策略效果指标"""
        strategy = db.query(BiddingStrategy).filter(BiddingStrategy.id == strategy_id).first()
        if not strategy:
            raise NotFoundError("策略不存在")

        try:
            strategy.total_impressions += metrics.get('impressions', 0)
            strategy.total_clicks += metrics.get('clicks', 0)
            strategy.total_conversions += metrics.get('conversions', 0)
            strategy.total_cost += metrics.get('cost', 0.0)

            # 计算平均值
            if strategy.total_clicks > 0:
                strategy.avg_cpc = strategy.total_cost / strategy.total_clicks
            if strategy.total_conversions > 0:
                strategy.avg_cpa = strategy.total_cost / strategy.total_conversions
                strategy.avg_roas = (metrics.get('conversion_value', 0) / strategy.total_cost) if strategy.total_cost > 0 else None

            db.commit()
            db.refresh(strategy)
            return strategy
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新效果指标失败: {str(e)}")


class BiddingRuleService:
    """出价规则服务"""

    @staticmethod
    def create(db: Session, obj_in: BiddingRuleCreate, tenant_id: int) -> BiddingRule:
        """创建出价规则"""
        try:
            # 将 conditions 转换为 JSON 字符串
            conditions_json = json.dumps(obj_in.conditions, ensure_ascii=False)

            db_obj = BiddingRule(
                tenant_id=tenant_id,
                strategy_id=obj_in.strategy_id,
                rule_name=obj_in.rule_name,
                rule_type=obj_in.rule_type,
                adjustment_type=obj_in.adjustment_type,
                adjustment_value=obj_in.adjustment_value,
                conditions=conditions_json,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建出价规则失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[BiddingRule]:
        """获取单个出价规则"""
        return db.query(BiddingRule).filter(
            and_(
                BiddingRule.id == id,
                BiddingRule.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        strategy_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[BiddingRule]:
        """获取出价规则列表"""
        query = db.query(BiddingRule).filter(
            BiddingRule.tenant_id == tenant_id
        )

        if strategy_id:
            query = query.filter(BiddingRule.strategy_id == strategy_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: BiddingRule,
        obj_in: BiddingRuleUpdate
    ) -> BiddingRule:
        """更新出价规则"""
        try:
            update_data = obj_in.dict(exclude_unset=True)

            # 如果更新了 conditions，转换为 JSON
            if 'conditions' in update_data:
                update_data['conditions'] = json.dumps(update_data['conditions'], ensure_ascii=False)

            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新出价规则失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除出价规则"""
        db_obj = BiddingRuleService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("出价规则不存在")
        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除出价规则失败: {str(e)}")
