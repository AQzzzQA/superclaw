"""
E2E 测试配置
Playwright 配置和全局 fixtures
"""

import pytest
from playwright.sync_api import BrowserContext, Page
import os


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai"
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """创建页面实例"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def base_url():
    """基础 URL 配置"""
    return os.getenv("E2E_BASE_URL", "http://localhost:8000")


@pytest.fixture
def test_credentials():
    """测试账号凭据"""
    return {
        "normal_user": {
            "username": "testuser",
            "password": "testpass123"
        },
        "admin_user": {
            "username": "admin",
            "password": "admin123"
        }
    }


@pytest.fixture
def login_page(page, base_url):
    """登录页面 fixture"""
    page.goto(f"{base_url}/login")
    return page


def pytest_configure(config):
    """Pytest 配置"""
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to run tests (chromium, firefox, webkit)"
    )
    parser.addoption(
        "--slowmo",
        action="store",
        default=0,
        help="Run tests in slow motion"
    )
