"""
后端单元测试 - Phase 2 和 Phase 3
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ==================== 异步任务测试 ====================
def test_upload_conversion_async():
    """测试异步上传转化"""
    response = client.post(
        "/api/v1/tasks/conversion/upload",
        json={
            "click_id": "test_001",
            "conversion_type": "purchase",
            "conversion_time": "2026-02-27 10:00:00",
            "value": 100.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "task_id" in data["data"]


def test_batch_upload_conversion_async():
    """测试异步批量上传转化"""
    response = client.post(
        "/api/v1/tasks/conversion/batch-upload",
        json=[
            {
                "click_id": "test_001",
                "conversion_type": "purchase",
                "conversion_time": "2026-02-27 10:00:00",
                "value": 100.0,
            },
            {
                "click_id": "test_002",
                "conversion_type": "purchase",
                "conversion_time": "2026-02-27 10:00:00",
                "value": 200.0,
            },
        ],
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "task_id" in data["data"]


def test_get_task_status():
    """测试查询任务状态"""
    response = client.get("/api/v1/tasks/test-task-id/status")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


# ==================== 自动出价测试 ====================
def test_update_auto_bidding():
    """测试更新自动出价"""
    response = client.post(
        "/api/v1/auto-bidding/update",
        json={
            "campaign_id": 1,
            "historical_data": [
                {
                    "date": "2026-02-27",
                    "cost": 10000,
                    "revenue": 20000,
                    "bid": 1.5,
                },
                {
                    "date": "2026-02-26",
                    "cost": 12000,
                    "revenue": 24000,
                    "bid": 1.6,
                },
            ],
            "current_budget": 10000,
            "current_cost": 5000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "optimal_bid" in data["data"]


def test_batch_update_auto_bidding():
    """测试批量更新自动出价"""
    response = client.post(
        "/api/v1/auto-bidding/batch-update",
        json={
            "campaigns": [
                {
                    "campaign_id": 1,
                    "historical_data": [
                        {
                            "date": "2026-02-27",
                            "cost": 10000,
                            "revenue": 20000,
                            "bid": 1.5,
                        },
                    ],
                    "current_budget": 10000,
                    "current_cost": 5000,
                },
                {
                    "campaign_id": 2,
                    "historical_data": [
                        {
                            "date": "2026-02-27",
                            "cost": 15000,
                            "revenue": 30000,
                            "bid": 2.0,
                        },
                    ],
                    "current_budget": 15000,
                    "current_cost": 7500,
                },
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


# ==================== A/B 测试测试 ====================
def test_create_ab_test():
    """测试创建 A/B 测试"""
    response = client.post(
        "/api/v1/ab-test/create",
        json={
            "name": "测试出价策略",
            "description": "测试不同出价策略的效果",
            "test_type": "bid",
            "variants": [
                {
                    "name": "变体 A",
                    "config": {"bid": 1.5},
                },
                {
                    "name": "变体 B",
                    "config": {"bid": 2.0},
                },
            ],
            "duration_days": 7,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "test_id" in data["data"]


def test_start_ab_test():
    """测试启动 A/B 测试"""
    response = client.post("/api/v1/ab-test/test-001/start")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_analyze_ab_test():
    """测试分析 A/B 测试"""
    response = client.post("/api/v1/ab-test/test-001/analyze")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "winner" in data["data"]


# ==================== 归因模型测试 ====================
def test_attribute_conversion():
    """测试归因转化"""
    response = client.post(
        "/api/v1/attribution/attribute",
        json={
            "conversion": {
                "conversion_id": "conv_001",
                "conversion_time": "2026-02-27 10:00:00",
                "value": 100.0,
            },
            "touchpoints": [
                {
                    "touchpoint_id": "tp_001",
                    "channel": "search",
                    "timestamp": "2026-02-27 09:00:00",
                    "cost": 50.0,
                },
                {
                    "touchpoint_id": "tp_002",
                    "channel": "social",
                    "timestamp": "2026-02-27 09:30:00",
                    "cost": 50.0,
                },
            ],
            "model": "time_decay",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "attribution" in data["data"]


def test_compare_attribution_models():
    """测试比较归因模型"""
    response = client.post(
        "/api/v1/attribution/compare",
        json={
            "conversion": {
                "conversion_id": "conv_001",
                "conversion_time": "2026-02-27 10:00:00",
                "value": 100.0,
            },
            "touchpoints": [
                {
                    "touchpoint_id": "tp_001",
                    "channel": "search",
                    "timestamp": "2026-02-27 09:00:00",
                    "cost": 50.0,
                },
                {
                    "touchpoint_id": "tp_002",
                    "channel": "social",
                    "timestamp": "2026-02-27 09:30:00",
                    "cost": 50.0,
                },
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "models" in data["data"]


# ==================== 用户管理测试 ====================
def test_create_user():
    """测试创建用户"""
    response = client.post(
        "/api/v1/users",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "full_name": "测试用户",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_list_users():
    """测试获取用户列表"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "users" in data["data"]


def test_get_user():
    """测试获取用户详情"""
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_update_user():
    """测试更新用户"""
    response = client.put(
        "/api/v1/users/1",
        json={
            "full_name": "管理员用户",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


# ==================== 角色权限管理测试 ====================
def test_create_role():
    """测试创建角色"""
    response = client.post(
        "/api/v1/roles",
        json={
            "name": "editor",
            "description": "编辑角色",
            "permissions": [
                "campaign:read",
                "campaign:write",
                "report:read",
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_list_roles():
    """测试获取角色列表"""
    response = client.get("/api/v1/roles")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "roles" in data["data"]


def test_assign_role():
    """测试分配角色"""
    response = client.post("/api/v1/users/1/roles", json={"role_id": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


# ==================== 操作日志测试 ====================
def test_list_logs():
    """测试获取操作日志"""
    response = client.get("/api/v1/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "logs" in data["data"]


# ==================== 系统配置测试 ====================
def test_get_config():
    """测试获取系统配置"""
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_get_config_section():
    """测试获取配置节"""
    response = client.get("/api/v1/config/app")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200


def test_update_config_section():
    """测试更新配置节"""
    response = client.put(
        "/api/v1/config/features",
        json={
            "auto_bidding": {
                "enabled": True,
                "default_model": "roi",
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
