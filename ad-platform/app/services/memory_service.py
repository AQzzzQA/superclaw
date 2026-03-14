"""
Ad Platform Memory Service

集成 OpenViking Memory Plugin，为广告平台提供记忆存储和检索功能。
支持用户偏好存储、项目历史记录、广告策略优化等场景。
"""

import asyncio
import json
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from openviking_memory_plugin import OpenVikingMemoryPlugin


class MemoryService:
    """
    记忆服务 - 集成 OpenViking
    """

    def __init__(
        self, server_url: str = "http://localhost:1933", api_key: Optional[str] = None
    ):
        """
        初始化记忆服务

        Args:
            server_url: OpenViking 服务器地址
            api_key: API 密钥（可选）
        """
        self.plugin = OpenVikingMemoryPlugin(server_url=server_url, api_key=api_key)
        self.cache = {}

    # ========== 用户相关记忆 ==========

    async def store_user_preference(
        self,
        user_id: str,
        campaign_type: str,
        preference: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        存储用户偏好

        Args:
            user_id: 用户ID
            campaign_type: 广告计划类型
            preference: 偏好设置
            metadata: 额外元数据

        Returns:
            存储结果
        """
        key = f"user_{user_id}_preference_{campaign_type}"
        value = {
            "user_id": user_id,
            "campaign_type": campaign_type,
            "preference": preference,
            "created_at": datetime.now().isoformat(),
        }

        if metadata:
            value.update(metadata)

        return await self.plugin.store(
            key, value, {"type": "user_preference", "user_id": user_id}, "L1"
        )

    async def get_user_preferences(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户所有偏好

        Args:
            user_id: 用户ID

        Returns:
            用户偏好列表
        """
        query = f"user_{user_id}_preference"
        return await self.plugin.search_memory(query, max_results=20)

    async def get_campaign_preferences(
        self, user_id: str, campaign_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取特定类型的用户偏好

        Args:
            user_id: 用户ID
            campaign_type: 广告计划类型

        Returns:
            偏好数据
        """
        key = f"user_{user_id}_preference_{campaign_type}"
        return await self.plugin.get_memory(key)

    # ========== 广告活动相关记忆 ==========

    async def store_campaign_history(
        self,
        campaign_id: str,
        data: Dict[str, Any],
        result: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        存储广告活动历史记录

        Args:
            campaign_id: 广告计划ID
            data: 活动创建时的数据
            result: 活动执行结果
            metadata: 额外元数据

        Returns:
            存储结果
        """
        key = (
            f"campaign_history_{campaign_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        value = {
            "campaign_id": campaign_id,
            "creation_data": data,
            "execution_result": result,
            "created_at": datetime.now().isoformat(),
            "result_summary": self._generate_result_summary(result),
        }

        if metadata:
            value.update(metadata)

        return await self.plugin.store(
            key, value, {"type": "campaign_history", "campaign_id": campaign_id}, "L1"
        )

    async def get_campaign_histories(
        self, campaign_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取广告计划的历史记录

        Args:
            campaign_id: 广告计划ID
            limit: 最大记录数

        Returns:
            历史记录列表
        """
        query = f"campaign_history_{campaign_id}"
        return await self.plugin.search_memory(query, max_results=limit)

    async def get_optimization_suggestions(
        self, user_id: str, campaign_type: str
    ) -> List[Dict[str, Any]]:
        """
        基于历史数据生成优化建议

        Args:
            user_id: 用户ID
            campaign_type: 广告计划类型

        Returns:
            优化建议列表
        """
        # 获取用户历史偏好
        preferences = await self.get_user_preferences(user_id)

        # 获取该类型的历史记录
        query = f"campaign_history_{campaign_type}"
        histories = await self.plugin.search_memory(query, max_results=20)

        # 生成优化建议
        suggestions = []

        if preferences and histories:
            # 分析偏好和执行结果的关系
            for pref in preferences:
                for history in histories:
                    # 这里可以加入更复杂的分析逻辑
                    suggestion = {
                        "type": "optimization",
                        "based_on": f"user_preference_{pref.get('campaign_type', '')}_history",
                        "suggestion": f"根据用户偏好 {pref.get('preference', {})} 和历史数据，建议优化策略",
                        "confidence": 0.8,
                        "created_at": datetime.now().isoformat(),
                    }
                    suggestions.append(suggestion)

        return suggestions

    # ========== 智能推荐记忆 ==========

    async def store_ad_strategy(
        self,
        strategy_id: str,
        strategy_data: Dict[str, Any],
        performance_metrics: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        存储广告策略

        Args:
            strategy_id: 策略ID
            strategy_data: 策略数据
            performance_metrics: 性能指标
            metadata: 额外元数据

        Returns:
            存储结果
        """
        key = f"ad_strategy_{strategy_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        value = {
            "strategy_id": strategy_id,
            "strategy_data": strategy_data,
            "performance_metrics": performance_metrics,
            "created_at": datetime.now().isoformat(),
            "effectiveness_score": self._calculate_effectiveness(performance_metrics),
        }

        if metadata:
            value.update(metadata)

        return await self.plugin.store(
            key, value, {"type": "ad_strategy", "strategy_id": strategy_id}, "L0"
        )

    async def get_similar_strategies(
        self, strategy_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        查找相似策略

        Args:
            strategy_data: 策略数据

        Returns:
            相似策略列表
        """
        # 转换策略数据为搜索查询
        campaign_type = strategy_data.get("campaign_type", "")
        budget = strategy_data.get("budget", 0)
        target_audience = strategy_data.get("target_audience", "")

        query = f"ad_strategy_{campaign_type}_{budget}_{target_audience}"
        return await self.plugin.search_memory(query, max_results=10)

    # ========== 批量处理接口 ==========

    async def store_user_session(
        self, user_id: str, session_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        存储用户会话数据

        Args:
            user_id: 用户ID
            session_data: 会话数据

        Returns:
            存储结果
        """
        key = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        value = {
            "user_id": user_id,
            "session_data": session_data,
            "created_at": datetime.now().isoformat(),
        }

        return await self.plugin.store(
            key, value, {"type": "user_session", "user_id": user_id}, "L1"
        )

    async def load_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        加载用户上下文

        Args:
            user_id: 用户ID

        Returns:
            用户上下文
        """
        # 获取用户偏好
        preferences = await self.get_user_preferences(user_id)

        # 获取最近的会话
        session_query = f"session_{user_id}"
        recent_sessions = await self.plugin.search_memory(session_query, max_results=5)

        return {
            "user_id": user_id,
            "preferences": preferences,
            "recent_sessions": recent_sessions,
            "created_at": datetime.now().isoformat(),
        }

    # ========== 工具方法 ==========

    def _generate_result_summary(self, result: Dict[str, Any]) -> str:
        """
        生成结果摘要

        Args:
            result: 执行结果

        Returns:
            摘要文本
        """
        clicks = result.get("clicks", 0)
        impressions = result.get("impressions", 0)
        spend = result.get("spend", 0)

        if impressions > 0:
            ctr = (clicks / impressions) * 100
        else:
            ctr = 0

        if spend > 0:
            cpc = spend / clicks if clicks > 0 else 0
        else:
            cpc = 0

        return f"CTR: {ctr:.2f}%, CPC: {cpc:.2f}, Clicks: {clicks}, Impressions: {impressions}"

    def _calculate_effectiveness(self, metrics: Dict[str, Any]) -> float:
        """
        计算策略有效评分

        Args:
            metrics: 性能指标

        Returns:
            有效评分 (0-1)
        """
        ctr = metrics.get("ctr", 0)
        roas = metrics.get("roas", 0)
        conversion_rate = metrics.get("conversion_rate", 0)

        # 简单的加权评分
        effectiveness = (ctr * 0.3 + roas * 0.4 + conversion_rate * 0.3) / 100
        return min(max(effectiveness, 0), 1)  # 确保在 0-1 范围内


# 全局实例
memory_service = MemoryService()
