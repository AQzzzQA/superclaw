"""
记忆服务测试
测试 OpenViking Memory Plugin 的集成功能
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from app.services.memory_service import MemoryService


class TestMemoryService:
    """记忆服务测试类"""
    
    @pytest.fixture
    def memory_service(self):
        """创建记忆服务实例"""
        with patch('app.services.memory_plugin.OpenVikingMemoryPlugin') as mock_plugin:
            mock_plugin.return_value = MagicMock()
            service = MemoryService()
            service.plugin = mock_plugin.return_value
            return service
    
    @pytest.mark.asyncio
    async def test_store_user_preference(self, memory_service):
        """测试存储用户偏好"""
        mock_result = {"success": True, "memory_id": "test123"}
        memory_service.plugin.store = AsyncMock(return_value=mock_result)
        
        preference = {"budget": 10000, "target_audience": "年轻人"}
        result = await memory_service.store_user_preference(
            user_id="user123",
            campaign_type="brand",
            preference=preference,
            metadata={"source": "test"}
        )
        
        # 验证调用
        memory_service.plugin.store.assert_called_once()
        call_args = memory_service.plugin.store.call_args
        
        # 验证参数
        assert call_args[1]['key'].startswith('user_user123_preference_brand')
        assert call_args[1]['value']['user_id'] == 'user123'
        assert call_args[1]['value']['campaign_type'] == 'brand'
        assert call_args[1]['value']['preference'] == preference
        assert call_args[1]['metadata']['type'] == 'user_preference'
        assert call_args[1]['layer'] == 'L1'
        
        assert result == mock_result
    
    @pytest.mark.asyncio
    async def test_get_user_preferences(self, memory_service):
        """测试获取用户偏好"""
        mock_preferences = [
            {"key": "user_user123_preference_brand", "value": {"preference": {}}},
            {"key": "user_user123_performance", "value": {"preference": {}}}
        ]
        memory_service.plugin.search_memory = AsyncMock(return_value=mock_preferences)
        
        result = await memory_service.get_user_preferences("user123")
        
        # 验证调用
        memory_service.plugin.search_memory.assert_called_once_with(
            "user_user123_preference", max_results=20
        )
        
        assert result == mock_preferences
    
    @pytest.mark.asyncio
    async def test_store_campaign_history(self, memory_service):
        """测试存储广告计划历史记录"""
        mock_result = {"success": True, "memory_id": "history123"}
        memory_service.plugin.store = AsyncMock(return_value=mock_result)
        
        campaign_data = {"name": "春季活动", "budget": 50000}
        execution_result = {"clicks": 1000, "impressions": 50000, "spend": 10000}
        
        result = await memory_service.store_campaign_history(
            campaign_id="camp123",
            data=campaign_data,
            result=execution_result,
            metadata={"source": "api"}
        )
        
        # 验证调用
        memory_service.plugin.store.assert_called_once()
        call_args = memory_service.plugin.store.call_args
        
        # 验证参数
        assert call_args[1]['key'].startswith('campaign_history_camp123_')
        assert call_args[1]['value']['campaign_id'] == 'camp123'
        assert call_args[1]['value']['creation_data'] == campaign_data
        assert call_args[1]['value']['execution_result'] == execution_result
        assert 'result_summary' in call_args[1]['value']
        
        assert result == mock_result
    
    @pytest.mark.asyncio
    async def test_get_campaign_histories(self, memory_service):
        """测试获取广告计划历史记录"""
        mock_histories = [
            {"key": "campaign_history_camp123_20240301", "value": {}},
            {"key": "campaign_history_camp123_20240228", "value": {}}
        ]
        memory_service.plugin.search_memory = AsyncMock(return_value=mock_histories)
        
        result = await memory_service.get_campaign_histories("camp123", limit=5)
        
        # 验证调用
        memory_service.plugin.search_memory.assert_called_once_with(
            "campaign_history_camp123", max_results=5
        )
        
        assert result == mock_histories
    
    @pytest.mark.asyncio
    async def test_get_optimization_suggestions(self, memory_service):
        """测试获取优化建议"""
        mock_preferences = [{"key": "pref1", "value": {"campaign_type": "brand"}}]
        mock_histories = [{"key": "hist1", "value": {"campaign_type": "brand"}}]
        
        memory_service.get_user_preferences = AsyncMock(return_value=mock_preferences)
        memory_service.plugin.search_memory = AsyncMock(return_value=mock_histories)
        
        result = await memory_service.get_optimization_suggestions("user123", "brand")
        
        # 验证建议生成
        assert len(result) > 0
        assert all('type' in item for item in result)
        assert all('based_on' in item for item in result)
        assert all('suggestion' in item for item in result)
        assert all('confidence' in item for item in result)
        assert all('created_at' in item for item in result)
    
    @pytest.mark.asyncio
    async def test_store_ad_strategy(self, memory_service):
        """测试存储广告策略"""
        mock_result = {"success": True, "memory_id": "strategy123"}
        memory_service.plugin.store = AsyncMock(return_value=mock_result)
        
        strategy_data = {"name": "高性能策略", "type": "performance"}
        performance_metrics = {"ctr": 2.5, "roas": 3.0}
        
        result = await memory_service.store_ad_strategy(
            strategy_id="strategy123",
            strategy_data=strategy_data,
            performance_metrics=performance_metrics,
            metadata={"test": True}
        )
        
        # 验证调用
        memory_service.plugin.store.assert_called_once()
        call_args = memory_service.plugin.store.call_args
        
        # 验证参数
        assert call_args[1]['key'].startswith('ad_strategy_strategy123_')
        assert call_args[1]['value']['strategy_id'] == 'strategy123'
        assert call_args[1]['value']['strategy_data'] == strategy_data
        assert call_args[1]['value']['performance_metrics'] == performance_metrics
        assert 'effectiveness_score' in call_args[1]['value']
        assert call_args[1]['metadata']['type'] == 'ad_strategy'
        
        assert result == mock_result
    
    @pytest.mark.asyncio
    async def test_get_similar_strategies(self, memory_service):
        """测试获取相似策略"""
        mock_strategies = [
            {"key": "strategy1", "value": {"campaign_type": "brand"}},
            {"key": "strategy2", "value": {"campaign_type": "brand"}}
        ]
        memory_service.plugin.search_memory = AsyncMock(return_value=mock_strategies)
        
        strategy_data = {"campaign_type": "brand", "budget": 10000}
        result = await memory_service.get_similar_strategies(strategy_data)
        
        # 验证调用
        expected_query = "ad_strategy_brand_10000_"
        memory_service.plugin.search_memory.assert_called_once()
        call_args = memory_service.plugin.search_memory.call_args
        assert call_args[1]['query'].startswith(expected_query)
        assert call_args[1]['max_results'] == 10
        
        assert result == mock_strategies
    
    @pytest.mark.asyncio
    async def test_store_user_session(self, memory_service):
        """测试存储用户会话"""
        mock_result = {"success": True, "memory_id": "session123"}
        memory_service.plugin.store = AsyncMock(return_value=mock_result)
        
        session_data = {"page": "campaign_list", "action": "filter"}
        result = await memory_service.store_user_session("user123", session_data)
        
        # 验证调用
        memory_service.plugin.store.assert_called_once()
        call_args = memory_service.plugin.store.call_args
        
        # 验证参数
        assert call_args[1]['key'].startswith('session_user123_')
        assert call_args[1]['value']['user_id'] == 'user123'
        assert call_args[1]['value']['session_data'] == session_data
        assert call_args[1]['metadata']['type'] == 'user_session'
        
        assert result == mock_result
    
    @pytest.mark.asyncio
    async def test_load_user_context(self, memory_service):
        """测试加载用户上下文"""
        mock_preferences = [{"key": "pref1", "value": {}}]
        mock_sessions = [{"key": "session1", "value": {}}]
        
        memory_service.get_user_preferences = AsyncMock(return_value=mock_preferences)
        memory_service.plugin.search_memory = AsyncMock(return_value=mock_sessions)
        
        result = await memory_service.load_user_context("user123")
        
        # 验证结果
        assert result['user_id'] == 'user123'
        assert result['preferences'] == mock_preferences
        assert result['recent_sessions'] == mock_sessions
        assert 'created_at' in result
        
        # 验证调用
        memory_service.get_user_preferences.assert_called_once_with("user123")
        memory_service.plugin.search_memory.assert_called_once_with(
            "session_user123", max_results=5
        )
    
    def test_generate_result_summary(self, memory_service):
        """测试结果摘要生成"""
        result = {
            "clicks": 1000,
            "impressions": 50000,
            "spend": 10000
        }
        
        summary = memory_service._generate_result_summary(result)
        
        # 验证摘要内容
        assert "CTR:" in summary
        assert "CPC:" in summary
        assert "Clicks: 1000" in summary
        assert "Impressions: 50000" in summary
    
    def test_calculate_effectiveness(self, memory_service):
        """测试有效评分计算"""
        metrics = {
            "ctr": 2.5,  # 2.5%
            "roas": 3.0,  # 3.0x
            "conversion_rate": 1.2  # 1.2%
        }
        
        effectiveness = memory_service._calculate_effectiveness(metrics)
        
        # 验证评分在 0-1 范围内
        assert 0 <= effectiveness <= 1
        assert effectiveness > 0
    
    def test_calculate_effectiveness_zero_metrics(self, memory_service):
        """测试零指标的有效评分"""
        metrics = {
            "ctr": 0,
            "roas": 0,
            "conversion_rate": 0
        }
        
        effectiveness = memory_service._calculate_effectiveness(metrics)
        
        # 验证评分为 0
        assert effectiveness == 0