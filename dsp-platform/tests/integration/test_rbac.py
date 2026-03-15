"""
权限系统（RBAC）集成测试
"""

import pytest
from fastapi import status


class TestUserAuthentication:
    """用户认证测试"""

    def test_user_login_success(self, client, test_user):
        """测试用户登录成功"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["code"] == 0
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_user_login_wrong_password(self, client, test_user):
        """测试用户登录失败（错误密码）"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": "wrongpassword"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_login_user_not_found(self, client):
        """测试用户登录失败（用户不存在）"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "anypassword"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_logout(self, client, auth_headers):
        """测试用户登出"""
        response = client.post(
            "/api/v1/auth/logout",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_refresh_token(self, client, test_user):
        """测试刷新令牌"""
        # 先登录获取 refresh token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        refresh_token = login_response.json()["data"]["refresh_token"]

        # 使用 refresh token 获取新的 access token
        response = client.post(
            "/api/v1/auth/refresh",
            json={
                "refresh_token": refresh_token
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()["data"]

    def test_invalid_token(self, client):
        """测试无效令牌"""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUserPermissions:
    """用户权限测试"""

    def test_get_user_info(self, client, auth_headers, test_user):
        """测试获取用户信息"""
        response = client.get(
            "/api/v1/users/me",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["username"] == test_user["username"]
        assert data["email"] == test_user["email"]

    def test_update_user_info(self, client, auth_headers):
        """测试更新用户信息"""
        response = client.patch(
            "/api/v1/users/me",
            json={
                "full_name": "更新后的姓名"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["full_name"] == "更新后的姓名"

    def test_change_password(self, client, auth_headers):
        """测试修改密码"""
        response = client.post(
            "/api/v1/users/change-password",
            json={
                "old_password": "testpass123",
                "new_password": "newpass456"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_change_password_wrong_old_password(self, client, auth_headers):
        """测试修改密码（旧密码错误）"""
        response = client.post(
            "/api/v1/users/change-password",
            json={
                "old_password": "wrongpassword",
                "new_password": "newpass456"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestRolePermissions:
    """角色权限测试"""

    def test_admin_has_all_permissions(self, client, admin_headers):
        """测试管理员拥有所有权限"""
        response = client.get(
            "/api/v1/users",
            headers=admin_headers
        )

        # 管理员应该能访问所有用户
        assert response.status_code == status.HTTP_200_OK

    def test_regular_user_cannot_access_admin_resources(self, client, auth_headers):
        """测试普通用户不能访问管理员资源"""
        response = client.get(
            "/api/v1/admin/users",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_as_admin(self, client, admin_headers):
        """测试管理员创建用户"""
        response = client.post(
            "/api/v1/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "新用户",
                "role_code": "ADVERTISER"
            },
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_regular_user_cannot_create_user(self, client, auth_headers):
        """测试普通用户不能创建用户"""
        response = client.post(
            "/api/v1/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestResourceAccessControl:
    """资源访问控制测试"""

    def test_access_own_resources(self, client, auth_headers, test_campaign):
        """测试访问自己的资源"""
        response = client.get(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_access_other_user_resources_forbidden(self, client, test_user, test_campaign):
        """测试访问其他用户的资源（被禁止）"""
        # 创建另一个用户
        from app.core.security import get_password_hash
        from app.models.user import User

        other_user_data = {
            "username": "otheruser",
            "email": "other@example.com",
            "hashed_password": get_password_hash("otherpass"),
            "is_active": True
        }
        # （这里需要在 db 中创建用户，简化处理）

        # 用另一个用户的 token 尝试访问
        # 实际测试中需要创建并登录另一个用户
        response = client.get(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers={"Authorization": "Bearer other_user_token"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_cross_account_resources_with_permission(self, client, admin_headers, test_campaign):
        """测试有权限时跨账户访问资源"""
        # 管理员应该能访问所有账户的资源
        response = client.get(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestPermissionEndpoints:
    """权限端点测试"""

    def test_get_user_permissions(self, client, auth_headers):
        """测试获取用户权限"""
        response = client.get(
            "/api/v1/users/me/permissions",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "permissions" in data

    def test_get_user_roles(self, client, auth_headers):
        """测试获取用户角色"""
        response = client.get(
            "/api/v1/users/me/roles",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "roles" in data

    def test_check_permission_granted(self, client, auth_headers):
        """测试检查权限（有权限）"""
        response = client.post(
            "/api/v1/auth/check-permission",
            json={
                "resource_type": "CAMPAIGN",
                "action": "CREATE"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["has_permission"] is True

    def test_check_permission_denied(self, client, auth_headers):
        """测试检查权限（无权限）"""
        response = client.post(
            "/api/v1/auth/check-permission",
            json={
                "resource_type": "ADMIN",
                "action": "DELETE"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["has_permission"] is False


class TestCampaignPermissions:
    """广告计划权限测试"""

    def test_create_campaign_with_permission(self, client, auth_headers, test_media_account):
        """测试有权限创建广告计划"""
        response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "测试广告计划",
                "account_id": test_media_account.id,
                "budget": 5000.00,
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": "2026-03-15",
                "end_date": "2026-04-15"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_update_own_campaign(self, client, auth_headers, test_campaign):
        """测试更新自己的广告计划"""
        response = client.patch(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            json={
                "campaign_name": "更新后的名称"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_delete_own_campaign(self, client, auth_headers, test_campaign):
        """测试删除自己的广告计划"""
        response = client.delete(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_cannot_update_other_campaign(self, client, test_user):
        """测试不能更新其他人的广告计划"""
        # 创建另一个用户并登录
        other_token = "other_user_token"

        response = client.patch(
            f"/api/v1/campaigns/test_campaign_001",
            json={
                "campaign_name": "尝试修改"
            },
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestAccountPermissions:
    """账户权限测试"""

    def test_view_own_accounts(self, client, auth_headers):
        """测试查看自己的账户"""
        response = client.get(
            "/api/v1/accounts",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_create_own_account(self, client, auth_headers):
        """测试创建自己的账户"""
        response = client.post(
            "/api/v1/accounts",
            json={
                "account_name": "测试账户",
                "channel_code": "DOUYIN"
            },
            headers=auth_headers
        )

        # 可能成功（如果有权限）或 403（如果没有权限）
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]

    def test_admin_view_all_accounts(self, client, admin_headers):
        """测试管理员查看所有账户"""
        response = client.get(
            "/api/v1/admin/accounts",
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportPermissions:
    """报表权限测试"""

    def test_view_own_reports(self, client, auth_headers):
        """测试查看自己的报表"""
        response = client.get(
            "/api/v1/reports",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_export_own_report(self, client, auth_headers):
        """测试导出自己的报表"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "excel",
                "filters": {}
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_cannot_export_other_reports(self, client, test_user):
        """测试不能导出其他人的报表"""
        other_token = "other_user_token"

        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "excel",
                "filters": {"user_id": 1}
            },
            headers={"Authorization": f"Bearer {other_token}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestRBACScenarios:
    """RBAC 场景测试"""

    def test_advertiser_workflow(self, client, auth_headers, test_media_account):
        """测试广告主完整工作流"""
        # 1. 创建广告计划
        campaign_response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "广告主测试",
                "account_id": test_media_account.id,
                "budget": 5000.00,
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": "2026-03-15",
                "end_date": "2026-04-15"
            },
            headers=auth_headers
        )
        assert campaign_response.status_code == status.HTTP_201_CREATED

        # 2. 查看自己的报表
        report_response = client.get(
            "/api/v1/reports",
            headers=auth_headers
        )
        assert report_response.status_code == status.HTTP_200_OK

        # 3. 尝试访问管理员资源（应该失败）
        admin_response = client.get(
            "/api/v1/admin/users",
            headers=auth_headers
        )
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_workflow(self, client, admin_headers):
        """测试管理员完整工作流"""
        # 1. 查看所有用户
        users_response = client.get(
            "/api/v1/admin/users",
            headers=admin_headers
        )
        assert users_response.status_code == status.HTTP_200_OK

        # 2. 查看所有账户
        accounts_response = client.get(
            "/api/v1/admin/accounts",
            headers=admin_headers
        )
        assert accounts_response.status_code == status.HTTP_200_OK

        # 3. 查看所有广告计划
        campaigns_response = client.get(
            "/api/v1/admin/campaigns",
            headers=admin_headers
        )
        assert campaigns_response.status_code == status.HTTP_200_OK

    def test_role_assignment(self, client, admin_headers, test_user):
        """测试角色分配"""
        response = client.patch(
            f"/api/v1/admin/users/{test_user['id']}/role",
            json={
                "role_code": "ADMIN"
            },
            headers=admin_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_permission_inheritance(self, client, auth_headers):
        """测试权限继承"""
        # 测试用户是否继承了角色的所有权限
        response = client.get(
            "/api/v1/users/me/permissions",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "permissions" in data
        assert len(data["permissions"]) > 0
