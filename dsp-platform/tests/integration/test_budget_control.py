"""
预算控制和预警逻辑集成测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch
from fastapi import status


class TestBudgetConfiguration:
    """预算配置测试"""

    def test_create_budget_config(self, client, auth_headers, test_campaign):
        """测试创建预算配置"""
        response = client.post(
            "/api/v1/budget/config",
            json={
                "campaign_id": test_campaign.id,
                "total_budget": 5000.00,
                "daily_budget": 100.00,
                "warning_threshold": 80.0,
                "stop_threshold": 100.0,
                "is_auto_stop": True,
                "is_warning_enabled": True
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["total_budget"] == 5000.00
        assert data["daily_budget"] == 100.00

    def test_create_budget_config_invalid_threshold(self, client, auth_headers, test_campaign):
        """测试创建预算配置（无效阈值）"""
        response = client.post(
            "/api/v1/budget/config",
            json={
                "campaign_id": test_campaign.id,
                "total_budget": 5000.00,
                "daily_budget": 100.00,
                "warning_threshold": 120.0,  # 大于停止阈值
                "stop_threshold": 100.0
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_budget_config(self, client, auth_headers, test_budget_config):
        """测试更新预算配置"""
        response = client.patch(
            f"/api/v1/budget/config/{test_budget_config.id}",
            json={
                "daily_budget": 150.00,
                "warning_threshold": 75.0
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["daily_budget"] == 150.00
        assert data["warning_threshold"] == 75.0

    def test_get_budget_config(self, client, auth_headers, test_budget_config):
        """测试获取预算配置"""
        response = client.get(
            f"/api/v1/budget/config/{test_budget_config.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["campaign_id"] == test_budget_config.campaign_id

    def test_delete_budget_config(self, client, auth_headers, test_budget_config):
        """测试删除预算配置"""
        response = client.delete(
            f"/api/v1/budget/config/{test_budget_config.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestBudgetMonitoring:
    """预算监控测试"""

    def test_monitor_daily_budget(self, client, auth_headers, test_budget_config):
        """测试监控日预算"""
        response = client.get(
            f"/api/v1/budget/monitor/{test_budget_config.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "daily_usage_rate" in data
        assert "total_usage_rate" in data

    def test_monitor_total_budget(self, client, auth_headers, test_budget_config):
        """测试监控总预算"""
        response = client.get(
            f"/api/v1/budget/monitor/{test_budget_config.campaign_id}?type=total",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "total_spend" in data
        assert "remaining_budget" in data

    def test_get_budget_usage_report(self, client, auth_headers, test_budget_config):
        """测试获取预算使用报告"""
        response = client.get(
            f"/api/v1/budget/report/{test_budget_config.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "daily_spend" in data
        assert "total_spend" in data
        assert "usage_rate" in data

    def test_batch_monitor_budgets(self, client, auth_headers):
        """测试批量监控预算"""
        campaign_ids = [1, 2, 3, 4, 5]

        response = client.post(
            "/api/v1/budget/batch-monitor",
            json={"campaign_ids": campaign_ids},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data) > 0


class TestBudgetWarning:
    """预算预警测试"""

    def test_warning_threshold_reached(self, client, auth_headers, test_budget_config):
        """测试达到预警阈值"""
        # 模拟消耗达到 85%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("85.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["warning_triggered"] is True

    def test_warning_threshold_not_reached(self, client, auth_headers, test_budget_config):
        """测试未达到预警阈值"""
        # 模拟消耗只有 70%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("70.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["warning_triggered"] is False

    def test_get_active_warnings(self, client, auth_headers):
        """测试获取活跃预警"""
        response = client.get(
            "/api/v1/budget/warnings?status=active",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_resolve_warning(self, client, auth_headers, test_budget_warning):
        """测试解决预警"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/resolve",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["is_resolved"] is True

    def test_get_warning_history(self, client, auth_headers, test_budget_config):
        """测试获取预警历史"""
        response = client.get(
            f"/api/v1/budget/warnings/history?campaign_id={test_budget_config.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data


class TestBudgetControl:
    """预算控制测试"""

    def test_auto_stop_campaign(self, client, auth_headers, test_budget_config):
        """测试自动停止广告计划"""
        # 模拟消耗达到 100%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("100.00")

            response = client.post(
                f"/api/v1/budget/auto-stop/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["stopped"] is True

    def test_auto_pause_campaign(self, client, auth_headers, test_budget_config):
        """测试自动暂停广告计划"""
        response = client.post(
            f"/api/v1/budget/auto-pause/{test_budget_config.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_reduce_bid_amount(self, client, auth_headers, test_budget_config):
        """测试降低出价"""
        response = client.post(
            f"/api/v1/budget/reduce-bid/{test_budget_config.campaign_id}",
            json={
                "new_bid_amount": 1.20
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_enable_auto_stop(self, client, auth_headers, test_budget_config):
        """测试启用自动停止"""
        response = client.patch(
            f"/api/v1/budget/config/{test_budget_config.id}",
            json={
                "is_auto_stop": True
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["is_auto_stop"] is True

    def test_disable_auto_stop(self, client, auth_headers, test_budget_config):
        """测试禁用自动停止"""
        response = client.patch(
            f"/api/v1/budget/config/{test_budget_config.id}",
            json={
                "is_auto_stop": False
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["is_auto_stop"] is False


class TestBudgetAlerts:
    """预算告警测试"""

    def test_send_budget_warning_notification(self, client, auth_headers, test_budget_warning):
        """测试发送预算预警通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_budget_exceeded_alert(self, client, auth_headers, test_budget_config):
        """测试发送预算超支告警"""
        # 模拟消耗超过预算
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("105.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK

    def test_get_alerts(self, client, auth_headers):
        """测试获取告警列表"""
        response = client.get(
            "/api/v1/budget/alerts",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_mark_alert_as_read(self, client, auth_headers):
        """测试标记告警为已读"""
        # 假设有一个告警 ID
        alert_id = 1

        response = client.post(
            f"/api/v1/budget/alerts/{alert_id}/read",
            headers=auth_headers
        )

        # 可能返回 200 或 404（如果告警不存在）
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_dismiss_alert(self, client, auth_headers):
        """测试忽略告警"""
        alert_id = 1

        response = client.post(
            f"/api/v1/budget/alerts/{alert_id}/dismiss",
            headers=auth_headers
        )

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


class TestBudgetScenarios:
    """预算场景测试"""

    def test_scenario_normal_usage(self, client, auth_headers, test_budget_config):
        """测试正常使用场景"""
        # 消耗 70%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("70.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["usage_rate"] == 70.0
            assert data["warning_triggered"] is False

    def test_scenario_warning_level(self, client, auth_headers, test_budget_config):
        """测试预警级别场景"""
        # 消耗 85%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("85.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["usage_rate"] == 85.0
            assert data["warning_triggered"] is True
            assert data["stop_triggered"] is False

    def test_scenario_critical_level(self, client, auth_headers, test_budget_config):
        """测试危急级别场景"""
        # 消耗 100%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("100.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["usage_rate"] == 100.0
            assert data["stop_triggered"] is True

    def test_scenario_over_budget(self, client, auth_headers, test_budget_config):
        """测试超预算场景"""
        # 消耗 110%
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("110.00")

            response = client.post(
                f"/api/v1/budget/check/{test_budget_config.campaign_id}",
                headers=auth_headers
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()["data"]
            assert data["usage_rate"] == 110.0
            assert data["stop_triggered"] is True


class TestBudgetForecast:
    """预算预测测试"""

    def test_predict_daily_spend(self, client, auth_headers, test_budget_config):
        """测试预测日消耗"""
        response = client.get(
            f"/api/v1/budget/forecast/{test_budget_config.campaign_id}?metric=daily",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "predicted_spend" in data

    def test_predict_total_spend(self, client, auth_headers, test_budget_config):
        """测试预测总消耗"""
        response = client.get(
            f"/api/v1/budget/forecast/{test_budget_config.campaign_id}?metric=total",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "predicted_total_spend" in data

    def test_estimate_exhaustion_date(self, client, auth_headers, test_budget_config):
        """测试估算预算耗尽日期"""
        response = client.get(
            f"/api/v1/budget/forecast/{test_budget_config.campaign_id}?metric=exhaustion_date",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "estimated_exhaustion_date" in data
        assert "days_until_exhaustion" in data


class TestBudgetNotifications:
    """预算通知测试"""

    def test_send_email_notification(self, client, auth_headers, test_budget_warning):
        """测试发送邮件通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            json={
                "channels": ["email"]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_wechat_notification(self, client, auth_headers, test_budget_warning):
        """测试发送微信通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            json={
                "channels": ["wechat"]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_dingtalk_notification(self, client, auth_headers, test_budget_warning):
        """测试发送钉钉通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            json={
                "channels": ["dingtalk"]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_multi_channel_notification(self, client, auth_headers, test_budget_warning):
        """测试发送多渠道通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            json={
                "channels": ["email", "wechat", "dingtalk"]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_send_notification_with_custom_message(self, client, auth_headers, test_budget_warning):
        """测试发送自定义消息通知"""
        response = client.post(
            f"/api/v1/budget/warnings/{test_budget_warning.id}/notify",
            json={
                "channels": ["email"],
                "custom_message": "您的广告计划预算即将耗尽，请及时处理"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestBudgetIntegration:
    """预算集成测试"""

    def test_full_budget_control_workflow(self, client, auth_headers, test_campaign, test_budget_config):
        """测试完整预算控制工作流"""
        # 1. 创建预算配置
        config_response = client.post(
            "/api/v1/budget/config",
            json={
                "campaign_id": test_campaign.id,
                "total_budget": 5000.00,
                "daily_budget": 100.00,
                "warning_threshold": 80.0,
                "stop_threshold": 100.0,
                "is_auto_stop": True,
                "is_warning_enabled": True
            },
            headers=auth_headers
        )
        assert config_response.status_code == status.HTTP_201_CREATED

        # 2. 监控预算使用
        monitor_response = client.get(
            f"/api/v1/budget/monitor/{test_campaign.id}",
            headers=auth_headers
        )
        assert monitor_response.status_code == status.HTTP_200_OK

        # 3. 模拟消耗达到预警阈值
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("85.00")

            check_response = client.post(
                f"/api/v1/budget/check/{test_campaign.id}",
                headers=auth_headers
            )
            assert check_response.status_code == status.HTTP_200_OK
            assert check_response.json()["data"]["warning_triggered"] is True

        # 4. 发送预警通知
        warnings_response = client.get(
            "/api/v1/budget/warnings?status=active",
            headers=auth_headers
        )
        assert warnings_response.status_code == status.HTTP_200_OK

        # 5. 模拟消耗达到停止阈值
        with patch('app.services.budget_service.BudgetService.get_current_spend') as mock_spend:
            mock_spend.return_value = Decimal("100.00")

            check_response = client.post(
                f"/api/v1/budget/check/{test_campaign.id}",
                headers=auth_headers
            )
            assert check_response.status_code == status.HTTP_200_OK
            assert check_response.json()["data"]["stop_triggered"] is True

        # 6. 自动停止广告计划
        stop_response = client.post(
            f"/api/v1/budget/auto-stop/{test_campaign.id}",
            headers=auth_headers
        )
        assert stop_response.status_code == status.HTTP_200_OK
