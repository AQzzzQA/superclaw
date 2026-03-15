"""
广告投放管理模块单元测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.models.campaign import Campaign, AdGroup, Creative
from app.services.campaign_service import CampaignService


class TestCampaignModel:
    """广告计划模型测试"""

    @pytest.fixture
    def test_campaign(self):
        """创建测试广告计划"""
        return Campaign(
            id=1,
            campaign_id="test_campaign_001",
            campaign_name="测试广告计划",
            account_id=1,
            owner_id=1,
            budget=5000.00,
            budget_type="DAILY",
            bid_type="CPC",
            bid_amount=Decimal("1.50"),
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30)).date(),
            status="RUNNING"
        )

    def test_campaign_creation(self, test_campaign):
        """测试广告计划创建"""
        assert test_campaign.campaign_id == "test_campaign_001"
        assert test_campaign.campaign_name == "测试广告计划"
        assert test_campaign.budget == 5000.00
        assert test_campaign.bid_type == "CPC"
        assert test_campaign.status == "RUNNING"

    def test_campaign_is_running(self, test_campaign):
        """测试广告计划是否运行中"""
        test_campaign.status = "RUNNING"
        assert test_campaign.is_running() is True

        test_campaign.status = "PAUSED"
        assert test_campaign.is_running() is False

    def test_campaign_is_active_period(self, test_campaign):
        """测试广告计划是否在活跃期"""
        today = datetime.now().date()
        test_campaign.start_date = today - timedelta(days=10)
        test_campaign.end_date = today + timedelta(days=20)

        assert test_campaign.is_in_active_period() is True

    def test_campaign_is_not_active_period(self, test_campaign):
        """测试广告计划不在活跃期"""
        # 已过期
        test_campaign.start_date = datetime.now().date() - timedelta(days=40)
        test_campaign.end_date = datetime.now().date() - timedelta(days=10)

        assert test_campaign.is_in_active_period() is False

    def test_campaign_budget_check(self, test_campaign):
        """测试预算检查"""
        # 日预算 100，当前消耗 80
        test_campaign.budget = 100.00
        test_campaign.daily_spend = 80.00

        assert test_campaign.has_remaining_budget() is True
        assert test_campaign.get_remaining_budget() == 20.00

    def test_campaign_budget_exceeded(self, test_campaign):
        """测试预算超支"""
        test_campaign.budget = 100.00
        test_campaign.daily_spend = 120.00

        assert test_campaign.has_remaining_budget() is False
        assert test_campaign.get_remaining_budget() == -20.00

    def test_campaign_transition_to_paused(self, test_campaign):
        """测试广告计划状态转换（暂停）"""
        test_campaign.status = "RUNNING"
        test_campaign.pause()

        assert test_campaign.status == "PAUSED"

    def test_campaign_transition_to_running(self, test_campaign):
        """测试广告计划状态转换（运行）"""
        test_campaign.status = "PAUSED"
        test_campaign.start()

        assert test_campaign.status == "RUNNING"

    def test_campaign_invalid_bid_amount(self):
        """测试无效出价金额"""
        with pytest.raises(ValueError):
            Campaign(
                campaign_id="test",
                campaign_name="测试",
                account_id=1,
                owner_id=1,
                budget=5000.00,
                bid_type="CPC",
                bid_amount=Decimal("0"),  # 无效出价
                start_date=datetime.now().date(),
                end_date=(datetime.now() + timedelta(days=30)).date()
            )


class TestAdGroupModel:
    """广告组模型测试"""

    @pytest.fixture
    def test_adgroup(self):
        """创建测试广告组"""
        return AdGroup(
            id=1,
            adgroup_id="test_adgroup_001",
            adgroup_name="测试广告组",
            campaign_id=1,
            account_id=1,
            owner_id=1,
            budget=1000.00,
            bid_type="CPC",
            bid_amount=Decimal("1.50"),
            targeting='{"age": ["18-24", "25-30"], "gender": ["MALE"]}',
            status="RUNNING"
        )

    def test_adgroup_creation(self, test_adgroup):
        """测试广告组创建"""
        assert test_adgroup.adgroup_id == "test_adgroup_001"
        assert test_adgroup.adgroup_name == "测试广告组"
        assert test_adgroup.campaign_id == 1
        assert test_adgroup.budget == 1000.00
        assert test_adgroup.status == "RUNNING"

    def test_adgroup_targeting_parsing(self, test_adgroup):
        """测试定向条件解析"""
        targeting = test_adgroup.get_targeting()

        assert targeting["age"] == ["18-24", "25-30"]
        assert targeting["gender"] == ["MALE"]

    def test_adgroup_bid_amount_validation(self, test_adgroup):
        """测试出价金额验证"""
        # 有效出价
        test_adgroup.bid_amount = Decimal("1.50")
        assert test_adgroup.is_valid_bid_amount() is True

        # 无效出价（负数）
        test_adgroup.bid_amount = Decimal("-1.00")
        assert test_adgroup.is_valid_bid_amount() is False

    def test_adgroup_status_transition(self, test_adgroup):
        """测试广告组状态转换"""
        test_adgroup.status = "RUNNING"
        test_adgroup.pause()
        assert test_adgroup.status == "PAUSED"

        test_adgroup.start()
        assert test_adgroup.status == "RUNNING"

    def test_adgroup_budget_usage(self, test_adgroup):
        """测试广告组预算使用"""
        test_adgroup.budget = 1000.00
        test_adgroup.spend = 750.00

        usage_rate = test_adgroup.get_budget_usage_rate()
        assert usage_rate == 0.75  # 75%

    def test_adgroup_is_over_budget(self, test_adgroup):
        """测试广告组是否超预算"""
        test_adgroup.budget = 1000.00
        test_adgroup.spend = 1100.00

        assert test_adgroup.is_over_budget() is True


class TestCreativeModel:
    """广告创意模型测试"""

    @pytest.fixture
    def test_creative(self):
        """创建测试创意"""
        return Creative(
            id=1,
            creative_id="test_creative_001",
            creative_name="测试创意",
            adgroup_id=1,
            account_id=1,
            campaign_id=1,
            creative_type="IMAGE",
            material_url="https://example.com/image.jpg",
            material_type="IMAGE",
            title="测试标题",
            description="测试描述",
            landing_url="https://example.com/landing",
            display_url="example.com",
            button_text="立即购买",
            audit_status=1,
            status=1
        )

    def test_creative_creation(self, test_creative):
        """测试创意创建"""
        assert test_creative.creative_id == "test_creative_001"
        assert test_creative.creative_type == "IMAGE"
        assert test_creative.title == "测试标题"
        assert test_creative.audit_status == 1
        assert test_creative.status == 1

    def test_creative_is_approved(self, test_creative):
        """测试创意是否审核通过"""
        test_creative.audit_status = 1  # 审核通过
        assert test_creative.is_approved() is True

        test_creative.audit_status = 2  # 审核拒绝
        assert test_creative.is_approved() is False

    def test_creative_is_active(self, test_creative):
        """测试创意是否激活"""
        test_creative.status = 1  # 投放中
        assert test_creative.is_active() is True

        test_creative.status = 2  # 暂停
        assert test_creative.is_active() is False

    def test_creative_material_validation(self, test_creative):
        """测试素材验证"""
        # 有效 URL
        test_creative.material_url = "https://example.com/image.jpg"
        assert test_creative.is_valid_material() is True

        # 无效 URL
        test_creative.material_url = "invalid-url"
        assert test_creative.is_valid_material() is False

    def test_creative_landing_page_validation(self, test_creative):
        """测试落地页验证"""
        # 有效 URL
        test_creative.landing_url = "https://example.com/landing"
        assert test_creative.is_valid_landing_page() is True

        # 无效 URL
        test_creative.landing_url = "not-a-url"
        assert test_creative.is_valid_landing_page() is False


class TestCampaignService:
    """广告服务测试"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock 数据库会话"""
        return MagicMock()

    @pytest.fixture
    def campaign_service(self, mock_db_session):
        """创建广告服务实例"""
        return CampaignService(mock_db_session)

    @pytest.fixture
    def test_campaign(self):
        """测试广告计划"""
        return Campaign(
            id=1,
            campaign_id="test_campaign_001",
            campaign_name="测试计划",
            account_id=1,
            owner_id=1,
            budget=5000.00,
            bid_type="CPC",
            bid_amount=Decimal("1.50"),
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30)).date(),
            status="RUNNING"
        )

    def test_create_campaign_success(self, campaign_service, test_campaign):
        """测试创建广告计划成功"""
        result = campaign_service.create_campaign(test_campaign)
        assert result is not None
        assert campaign_service.db_session.add.called

    def test_create_campaign_validation_error(self, campaign_service):
        """测试创建广告计划（验证错误）"""
        invalid_campaign = Campaign(
            campaign_id="test",
            campaign_name="测试",
            account_id=1,
            owner_id=1,
            budget=0.00,  # 无效预算
            bid_type="CPC",
            bid_amount=Decimal("1.50"),
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30)).date()
        )

        with pytest.raises(ValueError):
            campaign_service.create_campaign(invalid_campaign)

    def test_update_campaign_budget(self, campaign_service, mock_db_session):
        """测试更新广告计划预算"""
        mock_campaign = MagicMock(
            id=1,
            campaign_id="test",
            budget=1000.00
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_service.update_campaign_budget(
            campaign_id="test",
            new_budget=2000.00
        )

        assert mock_campaign.budget == 2000.00

    def test_pause_campaign(self, campaign_service, mock_db_session):
        """测试暂停广告计划"""
        mock_campaign = MagicMock(
            id=1,
            campaign_id="test",
            status="RUNNING"
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_service.pause_campaign("test")

        assert mock_campaign.status == "PAUSED"

    def test_start_campaign(self, campaign_service, mock_db_session):
        """测试启动广告计划"""
        mock_campaign = MagicMock(
            id=1,
            campaign_id="test",
            status="PAUSED"
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_service.start_campaign("test")

        assert mock_campaign.status == "RUNNING"

    def test_create_adgroup(self, campaign_service, mock_db_session):
        """测试创建广告组"""
        adgroup = AdGroup(
            adgroup_id="test_adgroup",
            adgroup_name="测试组",
            campaign_id=1,
            account_id=1,
            owner_id=1,
            budget=1000.00,
            bid_type="CPC",
            bid_amount=Decimal("1.50"),
            status="RUNNING"
        )

        result = campaign_service.create_adgroup(adgroup)
        assert result is not None

    def test_create_creative(self, campaign_service, mock_db_session):
        """测试创建创意"""
        creative = Creative(
            creative_id="test_creative",
            creative_name="测试创意",
            adgroup_id=1,
            account_id=1,
            campaign_id=1,
            creative_type="IMAGE",
            material_url="https://example.com/image.jpg",
            title="测试标题",
            audit_status=0,
            status=1
        )

        result = campaign_service.create_creative(creative)
        assert result is not None

    def test_batch_create_campaigns(self, campaign_service):
        """测试批量创建广告计划"""
        campaigns = [
            Campaign(
                campaign_id=f"campaign_{i}",
                campaign_name=f"计划{i}",
                account_id=1,
                owner_id=1,
                budget=1000.00,
                bid_type="CPC",
                bid_amount=Decimal("1.50"),
                start_date=datetime.now().date(),
                end_date=(datetime.now() + timedelta(days=30)).date()
            )
            for i in range(1, 6)
        ]

        result = campaign_service.batch_create_campaigns(campaigns)
        assert len(result) == 5

    def test_get_campaigns_by_owner(self, campaign_service, mock_db_session):
        """测试按所有者获取广告计划"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            MagicMock(campaign_id="campaign_001"),
            MagicMock(campaign_id="campaign_002")
        ]

        campaigns = campaign_service.get_campaigns_by_owner(user_id=1)

        assert len(campaigns) == 2

    def test_delete_campaign(self, campaign_service, mock_db_session):
        """测试删除广告计划"""
        mock_campaign = MagicMock(
            id=1,
            campaign_id="test",
            status="DELETED"
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_campaign

        campaign_service.delete_campaign("test")

        assert mock_campaign.status == "DELETED"


class TestBidStrategy:
    """出价策略测试"""

    def test_cpc_bid_calculation(self):
        """测试 CPC 出价计算"""
        bid_amount = Decimal("1.50")

        # 基础 CPC 出价
        assert bid_amount > 0
        assert bid_amount >= Decimal("0.01")

    def test_cpm_bid_calculation(self):
        """测试 CPM 出价计算"""
        bid_amount = Decimal("15.00")

        # 基础 CPM 出价
        assert bid_amount > 0
        assert bid_amount >= Decimal("1.00")

    def test_oCPM_bid_calculation(self):
        """测试 oCPM 出价计算"""
        target_cpa = Decimal("10.00")
        estimated_cvr = Decimal("0.02")

        # oCPM = target_cpa * estimated_cvr * 1000
        ocpm = target_cpa * estimated_cvr * Decimal("1000")

        assert ocpm == Decimal("200.00")

    def test_smart_bid_adjustment(self):
        """测试智能出价调整"""
        base_bid = Decimal("1.50")
        ctr_factor = Decimal("1.2")  # CTR 高于平均水平
        competition_factor = Decimal("0.9")  # 竞争较低

        adjusted_bid = base_bid * ctr_factor * competition_factor

        assert adjusted_bid == Decimal("1.62")
