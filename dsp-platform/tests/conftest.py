"""
pytest 配置文件
全局 fixtures 和测试配置
"""

import os
import sys
import asyncio
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from httpx import AsyncClient

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 测试配置
TEST_DB_URL = os.getenv(
    "TEST_DB_URL",
    "sqlite:///./test.db"
)

# ============================================
# 数据库 Fixtures
# ============================================

@pytest.fixture(scope="session")
def engine():
    """创建测试数据库引擎"""
    from app.core.database import Base

    engine = create_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False} if "sqlite" in TEST_DB_URL else {},
        poolclass=StaticPool
    )

    # 创建所有表
    Base.metadata.create_all(bind=engine)

    yield engine

    # 清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """创建数据库会话"""
    from app.core.database import SessionLocal

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ============================================
# FastAPI 客户端 Fixtures
# ============================================

@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """创建 FastAPI 测试客户端"""
    from app.main import app

    # 依赖注入覆盖
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    from app.core.database import get_db
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ============================================
# Async HTTP 客户端 Fixtures
# ============================================

@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """创建异步 HTTP 客户端"""
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ============================================
# 认证 Fixtures
# ============================================

@pytest.fixture
def test_user(db_session) -> dict:
    """创建测试用户"""
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="测试用户",
        is_active=True,
        is_superuser=False
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": "testpass123"
    }


@pytest.fixture
def auth_headers(client, test_user) -> dict:
    """获取认证头"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, db_session) -> dict:
    """获取管理员认证头"""
    from app.models.user import User
    from app.core.security import get_password_hash

    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="管理员",
        is_active=True,
        is_superuser=True
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": admin.username,
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================================
# 媒体账户 Fixtures
# ============================================

@pytest.fixture
def test_media_channel(db_session):
    """创建测试媒体渠道"""
    from app.models.account import MediaChannel

    channel = MediaChannel(
        channel_code="DOUYIN",
        channel_name="抖音",
        channel_type="VIDEO",
        oauth_url="https://open.douyin.com/oauth",
        api_endpoint="https://open.douyin.com/api",
        is_active=True
    )

    db_session.add(channel)
    db_session.commit()
    db_session.refresh(channel)

    return channel


@pytest.fixture
def test_media_account(db_session, test_user, test_media_channel):
    """创建测试媒体账户"""
    from app.models.account import MediaAccount

    account = MediaAccount(
        account_id="test_account_001",
        account_name="测试广告账户",
        channel_code="DOUYIN",
        channel_id=test_media_channel.id,
        owner_id=test_user["id"],
        balance=10000.00,
        status="ACTIVE",
        auth_token="test_token_123456",
        refresh_token="test_refresh_token_123456",
        token_expires_at=datetime.now() + timedelta(days=30),
        is_authorized=True
    )

    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    return account


# ============================================
# 广告投放 Fixtures
# ============================================

@pytest.fixture
def test_campaign(db_session, test_user, test_media_account):
    """创建测试广告计划"""
    from app.models.campaign import Campaign

    campaign = Campaign(
        campaign_id="test_campaign_001",
        campaign_name="测试广告计划",
        account_id=test_media_account.id,
        owner_id=test_user["id"],
        budget=5000.00,
        budget_type="DAILY",
        bid_type="CPC",
        bid_amount=1.50,
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=30)).date(),
        status="RUNNING"
    )

    db_session.add(campaign)
    db_session.commit()
    db_session.refresh(campaign)

    return campaign


@pytest.fixture
def test_adgroup(db_session, test_user, test_campaign):
    """创建测试广告组"""
    from app.models.campaign import AdGroup

    adgroup = AdGroup(
        adgroup_id="test_adgroup_001",
        adgroup_name="测试广告组",
        campaign_id=test_campaign.id,
        account_id=test_campaign.account_id,
        owner_id=test_user["id"],
        budget=1000.00,
        bid_type="CPC",
        bid_amount=1.50,
        targeting='{"age": ["18-24", "25-30"], "gender": ["MALE"]}',
        status="RUNNING"
    )

    db_session.add(adgroup)
    db_session.commit()
    db_session.refresh(adgroup)

    return adgroup


@pytest.fixture
def test_creative(db_session, test_user, test_adgroup):
    """创建测试广告创意"""
    from app.models.campaign import Creative

    creative = Creative(
        creative_id="test_creative_001",
        creative_name="测试创意",
        adgroup_id=test_adgroup.id,
        account_id=test_adgroup.account_id,
        campaign_id=test_adgroup.campaign_id,
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

    db_session.add(creative)
    db_session.commit()
    db_session.refresh(creative)

    return creative


# ============================================
# 数据报表 Fixtures
# ============================================

@pytest.fixture
def test_report_data(db_session, test_media_account, test_campaign):
    """创建测试报表数据"""
    from app.models.report import ReportDaily

    report = ReportDaily(
        account_id=test_media_account.id,
        campaign_id=test_campaign.id,
        report_date=datetime.now().date(),
        impression=10000,
        click=500,
        ctr=0.0500,
        cost=150.00,
        cpm=15.00,
        cpc=0.30,
        conversion=20,
        cvr=0.0400,
        cpa=7.50,
        revenue=300.00,
        roi=2.0000
    )

    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    return report


# ============================================
# 预算风控 Fixtures
# ============================================

@pytest.fixture
def test_budget_config(db_session, test_campaign):
    """创建测试预算配置"""
    from app.models.budget import BudgetConfig

    config = BudgetConfig(
        campaign_id=test_campaign.id,
        total_budget=5000.00,
        daily_budget=100.00,
        warning_threshold=80.0,
        stop_threshold=100.0,
        is_auto_stop=True,
        is_warning_enabled=True
    )

    db_session.add(config)
    db_session.commit()
    db_session.refresh(config)

    return config


@pytest.fixture
def test_budget_warning(db_session, test_campaign, test_budget_config):
    """创建测试预算预警记录"""
    from app.models.budget import BudgetWarning

    warning = BudgetWarning(
        campaign_id=test_campaign.id,
        budget_config_id=test_budget_config.id,
        warning_type="DAILY_BUDGET",
        current_spend=85.00,
        threshold=80.00,
        severity="WARNING",
        message="日预算即将耗尽",
        is_resolved=False
    )

    db_session.add(warning)
    db_session.commit()
    db_session.refresh(warning)

    return warning


# ============================================
# Mock 外部 API
# ============================================

@pytest.fixture
def mock_douyin_api(monkeypatch):
    """Mock 抖音 API"""
    class MockDouyinAPI:
        def __init__(self, access_token):
            self.access_token = access_token

        def get_account_info(self):
            return {
                "account_id": "test_douyin_001",
                "account_name": "抖音测试账户",
                "balance": 5000.00
            }

        def refresh_token(self):
            return {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 2592000
            }

    return MockDouyinAPI


@pytest.fixture
def mock_notification_service(monkeypatch):
    """Mock 通知服务"""
    class MockNotificationService:
        def send_email(self, to, subject, body):
            return True

        def send_wechat(self, user_id, message):
            return True

        def send_dingtalk(self, webhook_url, message):
            return True

    return MockNotificationService


# ============================================
# 测试工具函数
# ============================================

@pytest.fixture
def faker():
    """Faker 数据生成器"""
    from faker import Faker
    return Faker("zh_CN")


@pytest.fixture
def mock_redis():
    """Mock Redis 客户端"""
    import redis
    from unittest.mock import MagicMock

    mock_client = MagicMock(spec=redis.Redis)
    mock_client.get.return_value = None
    mock_client.set.return_value = True
    mock_client.delete.return_value = 1
    mock_client.expire.return_value = True

    return mock_client


# ============================================
# Pytest 钩子
# ============================================

def pytest_configure(config):
    """Pytest 配置钩子"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集行为"""
    # 自动标记慢速测试
    for item in items:
        if "slow" in item.name.lower():
            item.add_marker(pytest.mark.slow)
