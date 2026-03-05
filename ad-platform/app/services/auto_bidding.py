"""
自动出价算法
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AutoBiddingAlgorithm:
    """自动出价算法"""

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化自动出价算法

        Args:
            config: 配置参数
        """
        self.config = config or {
            "min_bid": 0.1,  # 最低出价
            "max_bid": 100.0,  # 最高出价
            "budget_limit": 10000.0,  # 预算限制
            "target_roi": 2.0,  # 目标 ROI
            "learning_period": 7,  # 学习周期（天）
        }

    def calculate_bid(
        self,
        campaign_id: int,
        historical_data: List[Dict],
        current_budget: float,
        current_cost: float,
    ) -> float:
        """
        计算最优出价

        Args:
            campaign_id: 广告计划 ID
            historical_data: 历史数据
            current_budget: 当前预算
            current_cost: 当前消耗

        Returns:
            float: 最优出价
        """
        try:
            logger.info(f"计算广告计划 {campaign_id} 的最优出价")

            # 数据不足，使用默认出价
            if len(historical_data) < self.config["learning_period"]:
                logger.warning(f"历史数据不足，使用默认出价")
                return self.config["min_bid"] * 2

            # 计算当前 ROI
            current_roi = self._calculate_roi(historical_data)

            # 计算趋势
            trend = self._calculate_trend(historical_data)

            # 计算剩余预算
            remaining_budget = current_budget - current_cost

            # 根据策略计算出价
            if current_roi >= self.config["target_roi"]:
                # ROI 达标，增加出价
                bid = self._increase_bid(historical_data, trend, remaining_budget)
            elif current_roi >= self.config["target_roi"] * 0.8:
                # ROI 接近目标，维持出价
                bid = self._maintain_bid(historical_data, trend)
            else:
                # ROI 未达标，降低出价
                bid = self._decrease_bid(historical_data, trend, remaining_budget)

            # 限制出价范围
            bid = max(self.config["min_bid"], min(self.config["max_bid"], bid))

            logger.info(f"广告计划 {campaign_id} 最优出价: {bid}")
            return bid

        except Exception as e:
            logger.error(f"计算出价失败: {str(e)}")
            return self.config["min_bid"]

    def _calculate_roi(self, historical_data: List[Dict]) -> float:
        """计算 ROI"""
        total_cost = sum(d.get("cost", 0) for d in historical_data)
        total_revenue = sum(d.get("revenue", 0) for d in historical_data)

        if total_cost == 0:
            return 0.0

        return total_revenue / total_cost

    def _calculate_trend(self, historical_data: List[Dict]) -> str:
        """计算趋势"""
        if len(historical_data) < 3:
            return "stable"

        # 获取最近 3 天的数据
        recent_data = historical_data[-3:]
        rois = [self._calculate_roi([d]) for d in [[d] for d in recent_data]]

        if rois[-1] > rois[-2] > rois[-3]:
            return "up"
        elif rois[-1] < rois[-2] < rois[-3]:
            return "down"
        else:
            return "stable"

    def _increase_bid(
        self, historical_data: List[Dict], trend: str, remaining_budget: float
    ) -> float:
        """增加出价"""
        avg_bid = sum(d.get("bid", self.config["min_bid"]) for d in historical_data) / len(
            historical_data
        )

        # 根据趋势调整增加幅度
        if trend == "up":
            increase_ratio = 1.2  # 上涨趋势，增加 20%
        elif trend == "down":
            increase_ratio = 1.1  # 下跌趋势，增加 10%
        else:
            increase_ratio = 1.15  # 稳定趋势，增加 15%

        new_bid = avg_bid * increase_ratio

        # 检查剩余预算
        if remaining_budget < new_bid * 100:
            new_bid = new_bid * 0.8  # 预算不足，降低出价

        return new_bid

    def _maintain_bid(self, historical_data: List[Dict], trend: str) -> float:
        """维持出价"""
        avg_bid = sum(d.get("bid", self.config["min_bid"]) for d in historical_data) / len(
            historical_data
        )

        # 根据趋势微调
        if trend == "up":
            return avg_bid * 1.05
        elif trend == "down":
            return avg_bid * 0.95
        else:
            return avg_bid

    def _decrease_bid(
        self, historical_data: List[Dict], trend: str, remaining_budget: float
    ) -> float:
        """降低出价"""
        avg_bid = sum(d.get("bid", self.config["min_bid"]) for d in historical_data) / len(
            historical_data
        )

        # 根据趋势调整降低幅度
        if trend == "up":
            decrease_ratio = 0.9  # 上涨趋势，降低 10%
        elif trend == "down":
            decrease_ratio = 0.8  # 下跌趋势，降低 20%
        else:
            decrease_ratio = 0.85  # 稳定趋势，降低 15%

        new_bid = avg_bid * decrease_ratio

        # 检查剩余预算
        if remaining_budget < new_bid * 100:
            new_bid = new_bid * 0.7  # 预算不足，进一步降低出价

        return max(self.config["min_bid"], new_bid)


class AutoBiddingService:
    """自动出价服务"""

    def __init__(self):
        self.algorithm = AutoBiddingAlgorithm()

    def update_campaign_bid(
        self,
        campaign_id: int,
        historical_data: List[Dict],
        current_budget: float,
        current_cost: float,
    ) -> Dict[str, Any]:
        """
        更新广告计划出价

        Args:
            campaign_id: 广告计划 ID
            historical_data: 历史数据
            current_budget: 当前预算
            current_cost: 当前消耗

        Returns:
            dict: 更新结果
        """
        try:
            # 计算最优出价
            optimal_bid = self.algorithm.calculate_bid(
                campaign_id, historical_data, current_budget, current_cost
            )

            # 模拟更新出价到巨量引擎
            # 实际应调用巨量引擎 API
            logger.info(f"更新广告计划 {campaign_id} 出价为: {optimal_bid}")

            return {
                "campaign_id": campaign_id,
                "optimal_bid": optimal_bid,
                "status": "success",
                "message": "出价更新成功",
            }

        except Exception as e:
            logger.error(f"更新出价失败: {str(e)}")
            return {
                "campaign_id": campaign_id,
                "status": "error",
                "message": str(e),
            }

    def batch_update_bids(
        self, campaigns: List[Dict]
    ) -> Dict[str, Any]:
        """
        批量更新出价

        Args:
            campaigns: 广告计划列表
                [
                    {
                        "campaign_id": 1,
                        "historical_data": [...],
                        "current_budget": 10000,
                        "current_cost": 5000,
                    },
                    ...
                ]

        Returns:
            dict: 批量更新结果
        """
        results = {
            "total": len(campaigns),
            "success": 0,
            "failed": 0,
            "errors": [],
        }

        for campaign in campaigns:
            try:
                result = self.update_campaign_bid(
                    campaign["campaign_id"],
                    campaign["historical_data"],
                    campaign["current_budget"],
                    campaign["current_cost"],
                )

                if result["status"] == "success":
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        {
                            "campaign_id": campaign["campaign_id"],
                            "error": result.get("message", "未知错误"),
                        }
                    )

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {"campaign_id": campaign["campaign_id"], "error": str(e)}
                )

        return results
