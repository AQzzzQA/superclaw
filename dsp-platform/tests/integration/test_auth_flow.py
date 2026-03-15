"""
媒体账户授权流程集成测试
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from fastapi import status


class TestOAuthAuthorizationFlow:
    """OAuth 授权流程测试"""

    def test_oauth_redirect_to_platform(self, client, test_user, test_media_channel):
        """测试重定向到媒体平台授权页"""
        response = client.get(
            f"/api/v1/accounts/oauth/authorize?channel_code={test_media_channel.channel_code}",
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        # 应该返回授权 URL
        assert response.status_code == status.HTTP_200_OK
        assert "oauth_url" in response.json()

    def test_oauth_callback_success(self, client, test_user, test_media_channel):
        """测试 OAuth 回调成功"""
        with patch('app.services.account_service.AccountService._exchange_code_for_token') as mock_exchange:
            mock_exchange.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 2592000
            }

            response = client.post(
                f"/api/v1/accounts/oauth/callback?channel_code={test_media_channel.channel_code}",
                json={
                    "code": "test_code",
                    "state": "test_state"
                },
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["code"] == 0

    def test_oauth_callback_invalid_code(self, client, test_user, test_media_channel):
        """测试 OAuth 回调失败（无效 code）"""
        with patch('app.services.account_service.AccountService._exchange_code_for_token') as mock_exchange:
            mock_exchange.side_effect = Exception("Invalid code")

            response = client.post(
                f"/api/v1/accounts/oauth/callback?channel_code={test_media_channel.channel_code}",
                json={
                    "code": "invalid_code",
                    "state": "test_state"
                },
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_oauth_callback_missing_code(self, client, test_user, test_media_channel):
        """测试 OAuth 回调失败（缺少 code）"""
        response = client.post(
            f"/api/v1/accounts/oauth/callback?channel_code={test_media_channel.channel_code}",
            json={
                "state": "test_state"
            },
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestTokenRefresh:
    """令牌刷新测试"""

    def test_refresh_token_success(self, client, test_user, test_media_account):
        """测试刷新令牌成功"""
        with patch('app.services.account_service.AccountService._refresh_token_from_platform') as mock_refresh:
            mock_refresh.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 2592000
            }

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/refresh-token",
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["code"] == 0

    def test_refresh_token_expired(self, client, test_user, test_media_account):
        """测试刷新令牌失败（令牌已过期）"""
        with patch('app.services.account_service.AccountService._refresh_token_from_platform') as mock_refresh:
            mock_refresh.side_effect = Exception("Token expired")

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/refresh-token",
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestAuthorizationRevocation:
    """授权撤销测试"""

    def test_revoke_authorization_success(self, client, test_user, test_media_account):
        """测试撤销授权成功"""
        with patch('app.services.account_service.AccountService._revoke_token_from_platform') as mock_revoke:
            mock_revoke.return_value = True

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/revoke",
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["code"] == 0

    def test_revoke_authorization_already_revoked(self, client, test_user, test_media_account):
        """测试撤销授权失败（已撤销）"""
        test_media_account.is_authorized = False

        response = client.post(
            f"/api/v1/accounts/{test_media_account.account_id}/revoke",
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestAccountSynchronization:
    """账户信息同步测试"""

    def test_sync_account_info_success(self, client, test_user, test_media_account):
        """测试同步账户信息成功"""
        with patch('app.services.account_service.AccountService._fetch_account_from_platform') as mock_fetch:
            mock_fetch.return_value = {
                "account_id": "test_account_001",
                "account_name": "更新后的名称",
                "balance": 15000.00
            }

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/sync",
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["code"] == 0

    def test_sync_account_info_api_failure(self, client, test_user, test_media_account):
        """测试同步账户信息失败（API 错误）"""
        with patch('app.services.account_service.AccountService._fetch_account_from_platform') as mock_fetch:
            mock_fetch.side_effect = Exception("API error")

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/sync",
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_batch_sync_accounts(self, client, test_user):
        """测试批量同步账户"""
        with patch('app.services.account_service.AccountService.sync_account_info') as mock_sync:
            mock_sync.return_value = True

            response = client.post(
                "/api/v1/accounts/batch-sync",
                json={
                    "account_ids": ["account_001", "account_002", "account_003"]
                },
                headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
            )

            assert response.status_code == status.HTTP_200_OK
            assert mock_sync.call_count == 3

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestAccountHealthCheck:
    """账户健康检查测试"""

    def test_check_account_health(self, client, test_user, test_media_account):
        """测试检查账户健康度"""
        response = client.get(
            f"/api/v1/accounts/{test_media_account.account_id}/health",
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "health_score" in data
        assert "is_healthy" in data

    def test_check_account_health_low_balance(self, client, test_user, test_media_account, db_session):
        """测试检查账户健康度（余额不足）"""
        test_media_account.balance = 100.00
        db_session.commit()

        response = client.get(
            f"/api/v1/accounts/{test_media_account.account_id}/health",
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["health_score"] < 80

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestAuthorizationPermissions:
    """授权权限测试"""

    def test_get_own_accounts(self, client, test_user, test_media_account):
        """测试获取自己的账户"""
        response = client.get(
            "/api/v1/accounts",
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK
        accounts = response.json()["data"]["items"]
        assert len(accounts) > 0

    def test_get_other_accounts_forbidden(self, client, test_user, test_media_account):
        """测试获取其他账户（无权限）"""
        # 创建另一个用户
        from app.core.security import get_password_hash
        from app.models.user import User

        other_user = User(
            username="otheruser",
            email="other@example.com",
            hashed_password=get_password_hash("otherpass"),
            is_active=True
        )
        db_session = client.app.dependency_overrides[app.core.database.get_db]()
        db_session.add(other_user)
        db_session.commit()

        # 用另一个用户的 token
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "otheruser",
                "password": "otherpass"
            }
        )
        token = response.json()["access_token"]

        # 尝试访问第一个用户的账户
        response = client.get(
            f"/api/v1/accounts/{test_media_account.account_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]


class TestMultiChannelAuthorization:
    """多渠道授权测试"""

    def test_authorize_douyin_account(self, client, test_user):
        """测试授权抖音账户"""
        response = client.post(
            "/api/v1/accounts/oauth/authorize",
            json={
                "channel_code": "DOUYIN",
                "redirect_uri": "http://example.com/callback"
            },
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "oauth_url" in response.json()["data"]

    def test_authorize_kuaishou_account(self, client, test_user):
        """测试授权快手账户"""
        response = client.post(
            "/api/v1/accounts/oauth/authorize",
            json={
                "channel_code": "KUAISHOU",
                "redirect_uri": "http://example.com/callback"
            },
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_authorize_wechat_account(self, client, test_user):
        """测试授权微信账户"""
        response = client.post(
            "/api/v1/accounts/oauth/authorize",
            json={
                "channel_code": "WECHAT",
                "redirect_uri": "http://example.com/callback"
            },
            headers={"Authorization": f"Bearer {self._get_token(client, test_user)}"}
        )

        assert response.status_code == status.HTTP_200_OK

    def _get_token(self, client, test_user):
        """获取测试 token"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        return response.json()["access_token"]
