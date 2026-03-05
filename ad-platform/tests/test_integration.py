"""
集成测试 - Phase 1 + Phase 2 + Phase 3
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCampaignWorkflow:
    """广告计划工作流集成测试"""

    def test_campaign_full_workflow(self):
        """测试广告计划完整工作流"""
        # 1. 创建广告计划
        response = client.post(
            "/api/v1/campaign/create",
            json={
                "campaignName": "测试计划",
                "objectiveType": "产品推广",
                "budget": 1000,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200

        # 2. 更新广告计划状态
        response = client.post(
            "/api/v1/campaign/update-status",
            json={
                "campaignId": 1,
                "status": "enable",
            },
        )
        assert response.status_code == 200

        # 3. 查询广告计划列表
        response = client.get("/api/v1/campaign/list")
        assert response.status_code == 200


class TestBatchOperations:
    """批量操作集成测试"""

    def test_batch_campaign_operations(self):
        """测试广告计划批量操作"""
        # 1. 批量更新状态
        response = client.post(
            "/api/v1/campaign/batch-update-status",
            json={
                "ids": [1, 2, 3],
                "status": "enable",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "updated_count" in data["data"]

        # 2. 批量更新
        response = client.post(
            "/api/v1/campaign/batch-update",
            json={
                "ids": [1, 2, 3],
                "data": {"objectiveType": "应用推广"},
            },
        )
        assert response.status_code == 200


class TestConversionWorkflow:
    """转化回传工作流集成测试"""

    def test_conversion_async_workflow(self):
        """测试转化回传异步工作流"""
        # 1. 上传转化（异步）
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
        task_id = data["data"]["task_id"]

        # 2. 查询任务状态
        response = client.get(f"/api/v1/tasks/{task_id}/status")
        assert response.status_code == 200


class TestAutoBiddingWorkflow:
    """自动出价工作流集成测试"""

    def test_auto_bidding_workflow(self):
        """测试自动出价工作流"""
        # 1. 创建广告计划
        response = client.post(
            "/api/v1/campaign/create",
            json={
                "campaignName": "自动出价测试",
                "objectiveType": "产品推广",
                "budget": 10000,
            },
        )
        assert response.status_code == 200

        # 2. 更新自动出价
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
                ],
                "current_budget": 10000,
                "current_cost": 5000,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "optimal_bid" in data["data"]


class TestABTestWorkflow:
    """A/B 测试工作流集成测试"""

    def test_ab_test_full_workflow(self):
        """测试 A/B 测试完整工作流"""
        # 1. 创建 A/B 测试
        response = client.post(
            "/api/v1/ab-test/create",
            json={
                "name": "测试出价策略",
                "test_type": "bid",
                "variants": [
                    {"name": "变体 A", "config": {"bid": 1.5}},
                    {"name": "变体 B", "config": {"bid": 2.0}},
                ],
                "duration_days": 7,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        test_id = data["data"]["test_id"]

        # 2. 启动 A/B 测试
        response = client.post(f"/api/v1/ab-test/{test_id}/start")
        assert response.status_code == 200

        # 3. 分析 A/B 测试
        response = client.post(f"/api/v1/ab-test/{test_id}/analyze")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


class TestAttributionWorkflow:
    """归因工作流集成测试"""

    def test_attribution_workflow(self):
        """测试归因工作流"""
        # 1. 归因转化
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

        # 2. 比较归因模型
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


class TestUserManagementWorkflow:
    """用户管理工作流集成测试"""

    def test_user_role_workflow(self):
        """测试用户角色工作流"""
        # 1. 创建用户
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

        # 2. 创建角色
        response = client.post(
            "/api/v1/roles",
            json={
                "name": "editor",
                "description": "编辑角色",
                "permissions": [
                    "campaign:read",
                    "campaign:write",
                ],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        role_id = data["data"]["id"]

        # 3. 分配角色
        response = client.post(f"/api/v1/users/1/roles", json={"role_id": role_id})
        assert response.status_code == 200


class TestExportWorkflow:
    """数据导出工作流集成测试"""

    def test_export_workflow(self):
        """测试数据导出工作流"""
        # 1. 导出报表（同步）
        response = client.get(
            "/api/v1/report/export",
            params={
                "start_date": "2026-02-27",
                "end_date": "2026-02-28",
                "format": "xlsx",
            },
        )
        assert response.status_code == 200

        # 2. 导出报表（异步）
        response = client.post(
            "/api/v1/tasks/export/report",
            json=[
                {
                    "date": "2026-02-27",
                    "cost": 10000,
                    "show": 50000,
                    "click": 1000,
                },
            ],
            params={"format": "xlsx"},
        )
        assert response.status_code == 200
