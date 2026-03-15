"""
媒体账户管理模块单元测试
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.models.account import MediaAccount, MediaChannel
from app.services.account_service import AccountService


class TestMediaChannelModel:
    """媒体渠道模型测试"""

    @pytest.fixture
    def test_channel(self):
        """创建测试媒体渠道"""
        return MediaChannel(
            channel_code="DOUYIN",
            channel_name="抖音",
            channel_type="VIDEO",
            oauth_url="https://open.douyin.com/oauth",
            api_endpoint="https://open.douyin.com/api",
            is_active=True
        )

    def test_channel_creation(self, test_channel):
        """测试渠道创建"""
        assert test_channel.channel_code == "DOUYIN"
        assert test_channel.channel_name == "抖音"
        assert test_channel.channel_type == "VIDEO"
        assert test_channel.is_active is True

    def test_channel_oauth_url(self, test_channel):
        """测试 OAuth URL"""
        assert test_channel.oauth_url.startswith("https://")
        assert "/oauth" in test_channel.oauth_url

    def test_channel_api_endpoint(self, test_channel):
        """测试 API 端点"""
        assert test_channel.api_endpoint.startswith("https://")
        assert "/api" in test_channel.api_endpoint

    def test_channel_deactivate(self, test_channel):
        """测试渠道停用"""
        test_channel.is_active = False
        assert test_channel.is_active is False


class TestMediaAccountModel:
    """媒体账户模型测试"""

    @pytest.fixture
    def test_account(self):
        """创建测试媒体账户"""
        return MediaAccount(
            account_id="test_account_001",
            account_name="测试广告账户",
            channel_code="DOUYIN",
            owner_id=1,
            balance=10000.00,
            status="ACTIVE",
            auth_token="test_token_123",
            refresh_token="test_refresh_token_123",
            token_expires_at=datetime.now() + timedelta(days=30),
            is_authorized=True
        )

    def test_account_creation(self, test_account):
        """测试账户创建"""
        assert test_account.account_id == "test_account_001"
        assert test_account.account_name == "测试广告账户"
        assert test_account.channel_code == "DOUYIN"
        assert test_account.balance == 10000.00
        assert test_account.status == "ACTIVE"
        assert test_account.is_authorized is True

    def test_account_token_expiring_soon(self, test_account):
        """测试令牌即将过期"""
        # 设置令牌 5 天后过期
        test_account.token_expires_at = datetime.now() + timedelta(days=5)
        assert test_account.is_token_expiring() is True

    def test_account_token_not_expiring_soon(self, test_account):
        """测试令牌未即将过期"""
        # 设置令牌 25 天后过期
        test_account.token_expires_at = datetime.now() + timedelta(days=25)
        assert test_account.is_token_expiring() is False

    def test_account_token_expired(self, test_account):
        """测试令牌已过期"""
        test_account.token_expires_at = datetime.now() - timedelta(days=1)
        assert test_account.is_token_expired() is True

    def test_account_balance_sufficient(self, test_account):
        """测试账户余额充足"""
        assert test_account.has_sufficient_balance(5000.00) is True
        assert test_account.has_sufficient_balance(10000.00) is True
        assert test_account.has_sufficient_balance(10001.00) is False

    def test_account_deduct_balance(self, test_account):
        """测试扣减账户余额"""
        initial_balance = test_account.balance
        test_account.deduct_balance(1000.00)
        assert test_account.balance == initial_balance - 1000.00

    def test_account_status_check(self, test_account):
        """测试账户状态检查"""
        assert test_account.is_active() is True
        assert test_account.is_authorized is True

    def test_account_health_score(self, test_account):
        """测试账户健康度计算"""
        # 账户活跃且授权，余额充足，健康度高
        test_account.status = "ACTIVE"
        test_account.is_authorized = True
        test_account.balance = 5000.00

        score = test_account.calculate_health_score()
        assert score >= 80


class TestAccountService:
    """账户服务测试"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock 数据库会话"""
        return MagicMock()

    @pytest.fixture
    def account_service(self, mock_db_session):
        """创建账户服务实例"""
        return AccountService(mock_db_session)

    @pytest.fixture
    def test_account(self):
        """测试账户对象"""
        return MediaAccount(
            id=1,
            account_id="test_account_001",
            account_name="测试账户",
            channel_code="DOUYIN",
            owner_id=1,
            balance=10000.00,
            status="ACTIVE",
            auth_token="test_token",
            refresh_token="test_refresh_token",
            token_expires_at=datetime.now() + timedelta(days=30),
            is_authorized=True
        )

    def test_create_account_success(self, account_service, test_account):
        """测试创建账户成功"""
        account_service.create_account(test_account)
        assert account_service.db_session.add.called

    def test_update_account_info(self, account_service, mock_db_session):
        """测试更新账户信息"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = MagicMock(
            id=1,
            account_id="test_account_001",
            account_name="旧名称"
        )

        account_service.update_account_info(
            account_id="test_account_001",
            account_name="新名称"
        )

        assert mock_db_session.commit.called

    def test_refresh_token_success(self, account_service, test_account):
        """测试刷新令牌成功"""
        with patch.object(account_service, '_refresh_token_from_platform') as mock_refresh:
            mock_refresh.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 2592000
            }

            result = account_service.refresh_token(test_account)

            assert result["access_token"] == "new_access_token"
            assert result["refresh_token"] == "new_refresh_token"

    def test_refresh_token_failure(self, account_service, test_account):
        """测试刷新令牌失败"""
        with patch.object(account_service, '_refresh_token_from_platform') as mock_refresh:
            mock_refresh.side_effect = Exception("Token refresh failed")

            with pytest.raises(Exception):
                account_service.refresh_token(test_account)

    def test_sync_account_info(self, account_service, mock_db_session):
        """测试同步账户信息"""
        mock_account = MagicMock()
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_account

        with patch.object(account_service, '_fetch_account_from_platform') as mock_fetch:
            mock_fetch.return_value = {
                "account_id": "test_account_001",
                "account_name": "更新后的名称",
                "balance": 15000.00
            }

            account_service.sync_account_info("test_account_001")

            assert mock_account.account_name == "更新后的名称"
            assert mock_account.balance == 15000.00

    def test_check_account_permission(self, account_service):
        """测试检查账户权限"""
        user = MagicMock(id=1)
        account = MagicMock(id=1, owner_id=1)

        with patch.object(account_service, 'has_account_permission') as mock_check:
            mock_check.return_value = True

            result = account_service.check_account_permission(user, account)
            assert result is True

    def test_get_accounts_by_owner(self, account_service, mock_db_session):
        """测试按所有者获取账户列表"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            MagicMock(account_id="account_001"),
            MagicMock(account_id="account_002")
        ]

        accounts = account_service.get_accounts_by_owner(user_id=1)

        assert len(accounts) == 2
        assert accounts[0].account_id == "account_001"

    def test_deactivate_account(self, account_service, mock_db_session):
        """测试停用账户"""
        mock_account = MagicMock(id=1, status="ACTIVE")
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_account

        account_service.deactivate_account("test_account_001")

        assert mock_account.status == "INACTIVE"
        assert mock_db_session.commit.called


class TestOAuthFlow:
    """OAuth 授权流程测试"""

    def test_generate_oauth_url(self):
        """测试生成 OAuth URL"""
        from app.services.account_service import AccountService

        channel = MediaChannel(
            channel_code="DOUYIN",
            oauth_url="https://open.douyin.com/oauth/authorize",
            app_id="test_app_id"
        )

        service = AccountService(MagicMock())
        oauth_url = service.generate_oauth_url(channel, redirect_uri="http://example.com/callback")

        assert "https://open.douyin.com/oauth/authorize" in oauth_url
        assert "redirect_uri" in oauth_url
        assert "app_id" in oauth_url

    def test_handle_oauth_callback_success(self):
        """测试处理 OAuth 回调成功"""
        from app.services.account_service import AccountService

        service = AccountService(MagicMock())

        with patch.object(service, '_exchange_code_for_token') as mock_exchange:
            mock_exchange.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 2592000
            }

            result = service.handle_oauth_callback(
                code="test_code",
                state="test_state",
                user_id=1
            )

            assert result["access_token"] == "test_access_token"

    def test_handle_oauth_callback_invalid_code(self):
        """测试处理 OAuth 回调失败（无效 code）"""
        from app.services.account_service import AccountService

        service = AccountService(MagicMock())

        with patch.object(service, '_exchange_code_for_token') as mock_exchange:
            mock_exchange.side_effect = Exception("Invalid code")

            with pytest.raises(Exception):
                service.handle_oauth_callback(
                    code="invalid_code",
                    state="test_state",
                    user_id=1
                )

    def test_revoke_authorization_success(self):
        """测试撤销授权成功"""
        from app.services.account_service import AccountService

        service = AccountService(MagicMock())
        account = MagicMock(
            account_id="test_account_001",
            is_authorized=True
        )

        with patch.object(service, '_revoke_token_from_platform') as mock_revoke:
            mock_revoke.return_value = True

            service.revoke_authorization(account)

            assert account.is_authorized is False
            assert account.auth_token is None


class TestAccountHealth:
    """账户健康度测试"""

    @pytest.fixture
    def test_account(self):
        """测试账户"""
        return MediaAccount(
            id=1,
            account_id="test_account_001",
            account_name="测试账户",
            channel_code="DOUYIN",
            owner_id=1,
            balance=10000.00,
            status="ACTIVE",
            is_authorized=True
        )

    def test_healthy_account(self, test_account):
        """测试健康账户"""
        test_account.status = "ACTIVE"
        test_account.is_authorized = True
        test_account.balance = 5000.00

        score = test_account.calculate_health_score()
        assert score >= 90

    def test_unhealthy_account_low_balance(self, test_account):
        """测试不健康账户（余额不足）"""
        test_account.status = "ACTIVE"
        test_account.is_authorized = True
        test_account.balance = 100.00

        score = test_account.calculate_health_score()
        assert score < 80

    def test_unhealthy_account_unauthorized(self, test_account):
        """测试不健康账户（未授权）"""
        test_account.status = "ACTIVE"
        test_account.is_authorized = False
        test_account.balance = 5000.00

        score = test_account.calculate_health_score()
        assert score < 80

    def test_unhealthy_account_inactive(self, test_account):
        """测试不健康账户（状态不活跃）"""
        test_account.status = "INACTIVE"
        test_account.is_authorized = True
        test_account.balance = 5000.00

        score = test_account.calculate_health_score()
        assert score < 80
