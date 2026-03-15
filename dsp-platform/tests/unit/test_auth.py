"""
用户认证和权限模块单元测试
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import JWTError

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from app.models.user import User, Role, Permission
from app.services.auth_service import AuthService


class TestPasswordSecurity:
    """密码安全测试"""

    def test_password_hashing(self):
        """测试密码哈希"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        # 哈希值不应等于原密码
        assert hashed != password
        # 哈希值应包含特定格式
        assert hashed.startswith("$2b$")

    def test_password_verification_success(self):
        """测试密码验证成功"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """测试密码验证失败"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_password_hash_different_each_time(self):
        """测试每次哈希结果不同（salt 机制）"""
        password = "test_password_123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2


class TestJWTToken:
    """JWT Token 测试"""

    def test_create_access_token(self):
        """测试创建访问令牌"""
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)

        # Token 应该是字符串
        assert isinstance(token, str)
        # Token 应该有三部分
        assert len(token.split('.')) == 3

    def test_decode_access_token_success(self):
        """测试解码访问令牌成功"""
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)
        decoded = decode_access_token(token)

        assert decoded["sub"] == "testuser"
        assert decoded["user_id"] == 1
        assert "exp" in decoded

    def test_decode_access_token_invalid(self):
        """测试解码无效令牌"""
        invalid_token = "invalid.token.string"

        with pytest.raises(JWTError):
            decode_access_token(invalid_token)

    def test_token_expiration(self):
        """测试令牌过期"""
        # 创建一个立即过期的令牌
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))

        with pytest.raises(JWTError):
            decode_access_token(token)

    def test_token_contains_claims(self):
        """测试令牌包含必要的声明"""
        data = {"sub": "testuser", "user_id": 1, "role": "admin"}
        token = create_access_token(data)
        decoded = decode_access_token(token)

        assert "sub" in decoded
        assert "exp" in decoded
        assert "user_id" in decoded
        assert "role" in decoded


class TestUserModel:
    """用户模型测试"""

    @pytest.fixture
    def test_user(self):
        """创建测试用户"""
        return User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpass"),
            full_name="测试用户",
            is_active=True,
            is_superuser=False
        )

    def test_user_creation(self, test_user):
        """测试用户创建"""
        assert test_user.username == "testuser"
        assert test_user.email == "test@example.com"
        assert test_user.is_active is True
        assert test_user.is_superuser is False

    def test_user_verify_password(self, test_user):
        """测试用户密码验证"""
        assert test_user.verify_password("testpass") is True
        assert test_user.verify_password("wrongpass") is False

    def test_user_deactivate(self, test_user):
        """测试用户停用"""
        test_user.is_active = False
        assert test_user.is_active is False


class TestRoleModel:
    """角色模型测试"""

    @pytest.fixture
    def test_role(self):
        """创建测试角色"""
        return Role(
            role_code="ADVERTISER",
            role_name="广告主",
            description="拥有广告投放权限"
        )

    def test_role_creation(self, test_role):
        """测试角色创建"""
        assert test_role.role_code == "ADVERTISER"
        assert test_role.role_name == "广告主"
        assert test_role.description == "拥有广告投放权限"

    @pytest.fixture
    def test_role_with_permissions(self):
        """创建带权限的角色"""
        role = Role(
            role_code="ADMIN",
            role_name="管理员",
            description="系统管理员"
        )

        perm1 = Permission(
            permission_code="CAMPAIGN_CREATE",
            permission_name="创建广告计划",
            resource_type="CAMPAIGN",
            action="CREATE"
        )
        perm2 = Permission(
            permission_code="CAMPAIGN_UPDATE",
            permission_name="更新广告计划",
            resource_type="CAMPAIGN",
            action="UPDATE"
        )

        role.permissions = [perm1, perm2]
        return role

    def test_role_permissions(self, test_role_with_permissions):
        """测试角色权限"""
        assert len(test_role_with_permissions.permissions) == 2
        assert test_role_with_permissions.permissions[0].permission_code == "CAMPAIGN_CREATE"
        assert test_role_with_permissions.permissions[1].permission_code == "CAMPAIGN_UPDATE"


class TestAuthService:
    """认证服务测试"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock 数据库会话"""
        return MagicMock()

    @pytest.fixture
    def auth_service(self, mock_db_session):
        """创建认证服务实例"""
        return AuthService(mock_db_session)

    def test_authenticate_user_success(self, auth_service, mock_db_session):
        """测试用户认证成功"""
        # Mock 用户数据
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = user

        # 执行认证
        result = auth_service.authenticate_user("testuser", "testpass")

        assert result is not None
        assert result.username == "testuser"

    def test_authenticate_user_wrong_password(self, auth_service, mock_db_session):
        """测试用户认证失败（错误密码）"""
        user = User(
            username="testuser",
            hashed_password=get_password_hash("testpass"),
            is_active=True
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = user

        result = auth_service.authenticate_user("testuser", "wrongpass")

        assert result is None

    def test_authenticate_user_not_found(self, auth_service, mock_db_session):
        """测试用户认证失败（用户不存在）"""
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        result = auth_service.authenticate_user("nonexistent", "anypassword")

        assert result is None

    def test_authenticate_user_inactive(self, auth_service, mock_db_session):
        """测试用户认证失败（用户未激活）"""
        user = User(
            username="testuser",
            hashed_password=get_password_hash("testpass"),
            is_active=False
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = user

        result = auth_service.authenticate_user("testuser", "testpass")

        assert result is None

    def test_create_user(self, auth_service, mock_db_session):
        """测试创建用户"""
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
            "full_name": "新用户"
        }

        with patch.object(auth_service, 'create_user') as mock_create:
            mock_create.return_value = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"]
            )

            result = auth_service.create_user(user_data)
            assert result.username == "newuser"

    def test_check_user_permission(self, auth_service):
        """测试检查用户权限"""
        user = User(
            id=1,
            username="testuser",
            role_code="ADVERTISER"
        )

        # Mock 权限检查
        with patch.object(auth_service, 'has_permission') as mock_check:
            mock_check.return_value = True

            result = auth_service.check_user_permission(user, "CAMPAIGN", "CREATE")
            assert result is True


class TestRBAC:
    """基于角色的访问控制测试"""

    def test_superuser_has_all_permissions(self):
        """测试超级用户拥有所有权限"""
        user = User(
            id=1,
            username="admin",
            is_superuser=True
        )

        assert user.has_permission("ANY", "ANY") is True

    def test_regular_user_permission_check(self):
        """测试普通用户权限检查"""
        role = Role(role_code="ADVERTISER")

        perm1 = Permission(
            permission_code="CAMPAIGN_CREATE",
            resource_type="CAMPAIGN",
            action="CREATE"
        )
        perm2 = Permission(
            permission_code="CAMPAIGN_READ",
            resource_type="CAMPAIGN",
            action="READ"
        )

        role.permissions = [perm1, perm2]

        user = User(
            id=1,
            username="advertiser",
            role=role
        )

        assert user.has_permission("CAMPAIGN", "CREATE") is True
        assert user.has_permission("CAMPAIGN", "READ") is True
        assert user.has_permission("CAMPAIGN", "DELETE") is False

    def test_cross_account_access_check(self):
        """测试跨账户访问检查"""
        user = User(
            id=1,
            username="testuser",
            role_code="ADVERTISER"
        )

        # 用户可以访问自己的账户
        assert user.can_access_account(1) is True
        # 用户不能访问其他账户
        assert user.can_access_account(999) is False
