"""
预算控制和预警模块单元测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.models.budget import BudgetConfig, BudgetWarning, BudgetAlert
from app.services.budget_service import BudgetService


class TestBudgetConfigModel:
    """预算配置模型测试"""

    @pytest.fixture
    def test_budget_config(self):
        """创建测试预算配置"""
        return BudgetConfig(
            id=1,
            campaign_id=1,
            total_budget=Decimal("5000.00"),
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0,
            is_auto_stop=True,
            is_warning_enabled=True
        )

    def test_budget_config_creation(self, test_budget_config):
        """测试预算配置创建"""
        assert test_budget_config.campaign_id == 1
        assert test_budget_config.total_budget == Decimal("5000.00")
        assert test_budget_config.daily_budget == Decimal("100.00")
        assert test_budget_config.warning_threshold == 80.0
        assert test_budget_config.stop_threshold == 100.0

    def test_calculate_daily_usage_rate(self, test_budget_config):
        """测试计算日预算使用率"""
        daily_spend = Decimal("80.00")
        usage_rate = test_budget_config.calculate_daily_usage_rate(daily_spend)

        assert usage_rate == 80.0

    def test_calculate_total_usage_rate(self, test_budget_config):
        """测试计算总预算使用率"""
        total_spend = Decimal("2500.00")
        usage_rate = test_budget_config.calculate_total_usage_rate(total_spend)

        assert usage_rate == 50.0

    def test_is_warning_threshold_reached(self, test_budget_config):
        """测试是否达到预警阈值"""
        daily_spend = Decimal("85.00")
        is_reached = test_budget_config.is_warning_reached(daily_spend)

        assert is_reached is True

    def test_is_stop_threshold_reached(self, test_budget_config):
        """测试是否达到停止阈值"""
        daily_spend = Decimal("100.00")
        is_reached = test_budget_config.is_stop_reached(daily_spend)

        assert is_reached is True

    def test_is_below_threshold(self, test_budget_config):
        """测试是否低于阈值"""
        daily_spend = Decimal("70.00")
        is_below = test_budget_config.is_below_warning_threshold(daily_spend)

        assert is_below is True

    def test_auto_stop_enabled(self, test_budget_config):
        """测试自动停止是否启用"""
        assert test_budget_config.is_auto_stop is True

    def test_warning_enabled(self, test_budget_config):
        """测试预警是否启用"""
        assert test_budget_config.is_warning_enabled is True


class TestBudgetWarningModel:
    """预算预警模型测试"""

    @pytest.fixture
    def test_warning(self):
        """创建测试预算预警"""
        return BudgetWarning(
            id=1,
            campaign_id=1,
            budget_config_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("85.00"),
            threshold=Decimal("80.00"),
            severity="WARNING",
            message="日预算即将耗尽",
            is_resolved=False
        )

    def test_warning_creation(self, test_warning):
        """测试预算预警创建"""
        assert test_warning.campaign_id == 1
        assert test_warning.warning_type == "DAILY_BUDGET"
        assert test_warning.current_spend == Decimal("85.00")
        assert test_warning.severity == "WARNING"
        assert test_warning.is_resolved is False

    def test_warning_resolve(self, test_warning):
        """测试解决预警"""
        test_warning.is_resolved = True
        test_warning.resolved_at = datetime.now()

        assert test_warning.is_resolved is True
        assert test_warning.resolved_at is not None

    def test_warning_severity_levels(self):
        """测试预警严重级别"""
        warning_info = BudgetWarning(
            campaign_id=1,
            budget_config_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("85.00"),
            threshold=Decimal("80.00"),
            severity="INFO"
        )

        warning_warning = BudgetWarning(
            campaign_id=1,
            budget_config_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("95.00"),
            threshold=Decimal("80.00"),
            severity="WARNING"
        )

        warning_critical = BudgetWarning(
            campaign_id=1,
            budget_config_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("100.00"),
            threshold=Decimal("80.00"),
            severity="CRITICAL"
        )

        assert warning_info.severity == "INFO"
        assert warning_warning.severity == "WARNING"
        assert warning_critical.severity == "CRITICAL"


class TestBudgetAlertModel:
    """预算告警模型测试"""

    @pytest.fixture
    def test_alert(self):
        """创建测试预算告警"""
        return BudgetAlert(
            id=1,
            campaign_id=1,
            alert_type="BUDGET_EXCEEDED",
            current_spend=Decimal("105.00"),
            budget=Decimal("100.00"),
            severity="CRITICAL",
            message="预算已超支",
            status="UNREAD"
        )

    def test_alert_creation(self, test_alert):
        """测试预算告警创建"""
        assert test_alert.campaign_id == 1
        assert test_alert.alert_type == "BUDGET_EXCEEDED"
        assert test_alert.current_spend == Decimal("105.00")
        assert test_alert.severity == "CRITICAL"
        assert test_alert.status == "UNREAD"

    def test_alert_mark_as_read(self, test_alert):
        """测试标记告警为已读"""
        test_alert.status = "READ"
        test_alert.read_at = datetime.now()

        assert test_alert.status == "READ"
        assert test_alert.read_at is not None

    def test_alert_dismiss(self, test_alert):
        """测试忽略告警"""
        test_alert.status = "DISMISSED"
        test_alert.dismissed_at = datetime.now()

        assert test_alert.status == "DISMISSED"
        assert test_alert.dismissed_at is not None


class TestBudgetService:
    """预算服务测试"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock 数据库会话"""
        return MagicMock()

    @pytest.fixture
    def budget_service(self, mock_db_session):
        """创建预算服务实例"""
        return BudgetService(mock_db_session)

    @pytest.fixture
    def test_budget_config(self):
        """测试预算配置"""
        return BudgetConfig(
            id=1,
            campaign_id=1,
            total_budget=Decimal("5000.00"),
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0,
            is_auto_stop=True,
            is_warning_enabled=True
        )

    def test_create_budget_config(self, budget_service, test_budget_config):
        """测试创建预算配置"""
        result = budget_service.create_budget_config(test_budget_config)
        assert result is not None

    def test_update_budget_config(self, budget_service, mock_db_session):
        """测试更新预算配置"""
        mock_config = MagicMock(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00")
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_config

        budget_service.update_budget_config(
            config_id=1,
            daily_budget=Decimal("150.00")
        )

        assert mock_config.daily_budget == Decimal("150.00")

    def test_check_budget_warning(self, budget_service):
        """测试检查预算预警"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            is_warning_enabled=True
        )

        current_spend = Decimal("85.00")

        warning = budget_service.check_budget_warning(config, current_spend)

        assert warning is not None
        assert warning.warning_type == "DAILY_BUDGET"

    def test_check_budget_stop(self, budget_service):
        """测试检查预算停止"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            stop_threshold=100.0,
            is_auto_stop=True
        )

        current_spend = Decimal("100.00")

        should_stop = budget_service.should_stop_campaign(config, current_spend)

        assert should_stop is True

    def test_create_warning_record(self, budget_service):
        """测试创建预警记录"""
        warning = BudgetWarning(
            campaign_id=1,
            budget_config_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("85.00"),
            threshold=Decimal("80.00"),
            severity="WARNING",
            message="日预算即将耗尽"
        )

        result = budget_service.create_warning(warning)

        assert result is not None

    def test_get_active_warnings(self, budget_service, mock_db_session):
        """测试获取活跃预警"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            MagicMock(campaign_id=1, is_resolved=False),
            MagicMock(campaign_id=2, is_resolved=False)
        ]

        warnings = budget_service.get_active_warnings()

        assert len(warnings) == 2

    def test_resolve_warning(self, budget_service, mock_db_session):
        """测试解决预警"""
        mock_warning = MagicMock(
            id=1,
            is_resolved=False
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_warning

        budget_service.resolve_warning(warning_id=1)

        assert mock_warning.is_resolved is True
        assert mock_warning.resolved_at is not None

    def test_get_budget_usage(self, budget_service, mock_db_session):
        """测试获取预算使用情况"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = MagicMock(
            total_spend=Decimal("2500.00"),
            daily_spend=Decimal("85.00")
        )

        usage = budget_service.get_budget_usage(campaign_id=1)

        assert usage["total_spend"] == Decimal("2500.00")
        assert usage["daily_spend"] == Decimal("85.00")


class TestBudgetMonitoring:
    """预算监控测试"""

    def test_real_time_budget_monitoring(self):
        """测试实时预算监控"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        with patch.object(service, 'get_budget_usage') as mock_usage:
            mock_usage.return_value = {
                "total_spend": Decimal("2500.00"),
                "daily_spend": Decimal("85.00")
            }

            with patch.object(service, 'check_budget_warning') as mock_warning:
                mock_warning.return_value = MagicMock()

                service.monitor_budget(campaign_id=1)

                assert mock_usage.called
                assert mock_warning.called

    def test_batch_monitor_budget(self):
        """测试批量监控预算"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        campaign_ids = [1, 2, 3, 4, 5]

        with patch.object(service, 'monitor_budget') as mock_monitor:
            service.batch_monitor_budgets(campaign_ids)

            assert mock_monitor.call_count == 5


class TestBudgetControl:
    """预算控制测试"""

    def test_auto_stop_campaign(self):
        """测试自动停止广告计划"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        with patch.object(service, '_stop_campaign_on_platform') as mock_stop:
            mock_stop.return_value = True

            result = service.auto_stop_campaign(campaign_id=1)

            assert result is True

    def test_auto_pause_campaign(self):
        """测试自动暂停广告计划"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        with patch.object(service, '_pause_campaign_on_platform') as mock_pause:
            mock_pause.return_value = True

            result = service.auto_pause_campaign(campaign_id=1)

            assert result is True

    def test_reduce_bid_amount(self):
        """测试降低出价"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        with patch.object(service, '_update_bid_on_platform') as mock_update:
            mock_update.return_value = True

            result = service.reduce_bid_amount(
                campaign_id=1,
                new_bid=Decimal("1.20")
            )

            assert result is True


class TestBudgetAlerts:
    """预算告警测试"""

    def test_send_budget_warning_notification(self):
        """测试发送预算预警通知"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        warning = BudgetWarning(
            campaign_id=1,
            warning_type="DAILY_BUDGET",
            current_spend=Decimal("85.00"),
            threshold=Decimal("80.00"),
            severity="WARNING",
            message="日预算即将耗尽"
        )

        with patch.object(service, '_send_notification') as mock_notify:
            mock_notify.return_value = True

            result = service.send_warning_notification(warning)

            assert result is True

    def test_send_budget_exceeded_alert(self):
        """测试发送预算超支告警"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        alert = BudgetAlert(
            campaign_id=1,
            alert_type="BUDGET_EXCEEDED",
            current_spend=Decimal("105.00"),
            budget=Decimal("100.00"),
            severity="CRITICAL",
            message="预算已超支"
        )

        with patch.object(service, '_send_notification') as mock_notify:
            mock_notify.return_value = True

            result = service.send_alert_notification(alert)

            assert result is True

    def test_batch_send_notifications(self):
        """测试批量发送通知"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        warnings = [
            BudgetWarning(
                campaign_id=1,
                warning_type="DAILY_BUDGET",
                current_spend=Decimal("85.00"),
                threshold=Decimal("80.00"),
                severity="WARNING",
                message="日预算即将耗尽"
            )
            for _ in range(5)
        ]

        with patch.object(service, '_send_notification') as mock_notify:
            mock_notify.return_value = True

            results = service.batch_send_notifications(warnings)

            assert len(results) == 5
            assert all(results)


class TestBudgetForecast:
    """预算预测测试"""

    def test_predict_daily_spend(self):
        """测试预测日消耗"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        # 模拟历史数据
        historical_spend = [
            Decimal("80.00"),
            Decimal("90.00"),
            Decimal("85.00"),
            Decimal("95.00"),
            Decimal("88.00")
        ]

        predicted_spend = service.predict_daily_spend(historical_spend)

        # 简单平均预测
        expected = sum(historical_spend) / len(historical_spend)

        assert abs(predicted_spend - expected) < Decimal("1.00")

    def test_predict_total_spend(self):
        """测试预测总消耗"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        daily_spend = Decimal("88.00")
        remaining_days = 10

        predicted_total = service.predict_total_spend(
            daily_spend,
            remaining_days
        )

        assert predicted_total == Decimal("880.00")

    def test_estimate_budget_exhaustion_date(self):
        """测试估算预算耗尽日期"""
        from app.services.budget_service import BudgetService

        service = BudgetService(MagicMock())

        remaining_budget = Decimal("500.00")
        daily_spend = Decimal("50.00")

        days_until_exhaustion = service.estimate_days_until_exhaustion(
            remaining_budget,
            daily_spend
        )

        assert days_until_exhaustion == 10


class TestBudgetScenarios:
    """预算场景测试"""

    def test_scenario_normal_usage(self):
        """测试正常使用场景"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0
        )

        # 消耗 70%，正常
        current_spend = Decimal("70.00")

        usage_rate = config.calculate_daily_usage_rate(current_spend)

        assert usage_rate == 70.0
        assert config.is_below_warning_threshold(current_spend) is True

    def test_scenario_warning_level(self):
        """测试预警级别场景"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0
        )

        # 消耗 85%，触发预警
        current_spend = Decimal("85.00")

        usage_rate = config.calculate_daily_usage_rate(current_spend)

        assert usage_rate == 85.0
        assert config.is_warning_reached(current_spend) is True
        assert config.is_stop_reached(current_spend) is False

    def test_scenario_critical_level(self):
        """测试危急级别场景"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0,
            is_auto_stop=True
        )

        # 消耗 100%，触发停止
        current_spend = Decimal("100.00")

        usage_rate = config.calculate_daily_usage_rate(current_spend)

        assert usage_rate == 100.0
        assert config.is_stop_reached(current_spend) is True

    def test_scenario_over_budget(self):
        """测试超预算场景"""
        config = BudgetConfig(
            id=1,
            campaign_id=1,
            daily_budget=Decimal("100.00"),
            warning_threshold=80.0,
            stop_threshold=100.0
        )

        # 消耗 110%，超预算
        current_spend = Decimal("110.00")

        usage_rate = config.calculate_daily_usage_rate(current_spend)

        assert usage_rate == 110.0
        assert config.is_warning_reached(current_spend) is True
        assert config.is_stop_reached(current_spend) is True
