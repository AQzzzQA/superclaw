"""
后端单元测试
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()


def test_health_check():
    """测试健康检查"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "data" in data


def test_batch_update_campaign_status():
    """测试批量更新广告计划状态"""
    response = client.post(
        "/api/v1/campaign/batch-update-status",
        json={
            "ids": [1, 2, 3],
            "status": "enable"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "updated_count" in data["data"]


def test_batch_update_campaign_status_empty_ids():
    """测试批量更新空 ID 列表"""
    response = client.post(
        "/api/v1/campaign/batch-update-status",
        json={
            "ids": [],
            "status": "enable"
        }
    )
    assert response.status_code == 400


def test_batch_update_campaign_status_invalid_status():
    """测试批量更新无效状态"""
    response = client.post(
        "/api/v1/campaign/batch-update-status",
        json={
            "ids": [1, 2, 3],
            "status": "invalid"
        }
    )
    assert response.status_code == 400
