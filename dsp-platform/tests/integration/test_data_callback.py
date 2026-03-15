"""
实时数据回传接口集成测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
from fastapi import status


class TestDataReception:
    """数据接收测试"""

    def test_receive_campaign_data(self, client, test_media_account, test_campaign):
        """测试接收广告计划数据"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500,
                    "cost": 150.00,
                    "conversion": 20,
                    "timestamp": datetime.now().isoformat()
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["code"] == 0

    def test_receive_adgroup_data(self, client, test_media_account, test_adgroup):
        """测试接收广告组数据"""
        response = client.post(
            "/api/v1/data/adgroup",
            json={
                "account_id": test_media_account.id,
                "adgroup_id": test_adgroup.id,
                "data": {
                    "impression": 5000,
                    "click": 250,
                    "cost": 75.00,
                    "conversion": 10,
                    "timestamp": datetime.now().isoformat()
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK

    def test_receive_creative_data(self, client, test_media_account, test_creative):
        """测试接收创意数据"""
        response = client.post(
            "/api/v1/data/creative",
            json={
                "account_id": test_media_account.id,
                "creative_id": test_creative.id,
                "data": {
                    "impression": 2000,
                    "click": 100,
                    "cost": 30.00,
                    "conversion": 5,
                    "timestamp": datetime.now().isoformat()
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK

    def test_receive_batch_data(self, client, test_media_account):
        """测试接收批量数据"""
        batch_data = [
            {
                "campaign_id": 1,
                "impression": 10000,
                "click": 500,
                "cost": 150.00,
                "conversion": 20
            },
            {
                "campaign_id": 2,
                "impression": 8000,
                "click": 400,
                "cost": 120.00,
                "conversion": 15
            }
        ]

        response = client.post(
            "/api/v1/data/batch",
            json={
                "account_id": test_media_account.id,
                "data_list": batch_data,
                "timestamp": datetime.now().isoformat()
            }
        )

        assert response.status_code == status.HTTP_200_OK

    def test_receive_data_invalid_signature(self, client, test_media_account, test_campaign):
        """测试接收数据（无效签名）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500
                },
                "signature": "invalid_signature"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_receive_data_missing_required_fields(self, client, test_media_account):
        """测试接收数据（缺少必填字段）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": 1,
                "data": {
                    "impression": 10000
                    # 缺少 click, cost 等必填字段
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_receive_data_invalid_format(self, client, test_media_account):
        """测试接收数据（格式错误）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": "not_a_number",  # 应该是数字
                "data": {
                    "impression": 10000,
                    "click": 500
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDataValidation:
    """数据验证测试"""

    def test_validate_positive_values(self, client, test_media_account, test_campaign):
        """测试验证正数（成功）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,  # 正数
                    "click": 500,  # 正数
                    "cost": 150.00,  # 正数
                    "conversion": 20  # 正数
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK

    def test_validate_negative_values(self, client, test_media_account, test_campaign):
        """测试验证负数（失败）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": -10000,  # 负数
                    "click": 500
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_click_not_greater_than_impression(self, client, test_media_account, test_campaign):
        """验证点击数不应大于曝光数"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 100,
                    "click": 200  # 大于曝光数
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_conversion_not_greater_than_click(self, client, test_media_account, test_campaign):
        """验证转化数不应大于点击数"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500,
                    "conversion": 600  # 大于点击数
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_timestamp_future(self, client, test_media_account, test_campaign):
        """验证时间戳不应是未来时间"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500
                },
                "timestamp": (datetime.now() + timedelta(hours=1)).isoformat(),
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDataProcessing:
    """数据处理测试"""

    def test_process_data_to_database(self, client, test_media_account, test_campaign):
        """测试处理数据并写入数据库"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500,
                    "cost": 150.00,
                    "conversion": 20,
                    "timestamp": datetime.now().isoformat()
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK

        # 验证数据已写入数据库
        # 这里可以通过查询数据库来验证

    def test_calculate_metrics(self, client, test_media_account, test_campaign):
        """测试计算指标（CTR, CPC, CVR 等）"""
        response = client.post(
            "/api/v1/data/campaign",
            json={
                "account_id": test_media_account.id,
                "campaign_id": test_campaign.id,
                "data": {
                    "impression": 10000,
                    "click": 500,
                    "cost": 150.00,
                    "conversion": 20,
                    "timestamp": datetime.now().isoformat()
                },
                "signature": "test_signature"
            }
        )

        assert response.status_code == status.HTTP_200_OK

        # 验证指标计算正确
        # CTR = 500/10000*100 = 5%
        # CPC = 150/500 = 0.30
        # CVR = 20/500*100 = 4%

    def test_aggregate_hourly_data(self, client, test_media_account, test_campaign):
        """测试聚合小时数据"""
        # 发送多个小时的数据
        for i in range(5):
            response = client.post(
                "/api/v1/data/campaign",
                json={
                    "account_id": test_media_account.id,
                    "campaign_id": test_campaign.id,
                    "data": {
                        "impression": 1000 * (i + 1),
                        "click": 50 * (i + 1),
                        "cost": 15.00 * (i + 1),
                        "conversion": 2 * (i + 1),
                        "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
                    },
                    "signature": "test_signature"
                }
            )
            assert response.status_code == status.HTTP_200_OK

        # 验证小时数据聚合

    def test_aggregate_daily_data(self, client, test_media_account, test_campaign):
        """测试聚合日数据"""
        # 发送一天的数据
        for i in range(24):
            response = client.post(
                "/api/v1/data/campaign",
                json={
                    "account_id": test_media_account.id,
                    "campaign_id": test_campaign.id,
                    "data": {
                        "impression": 500,
                        "click": 25,
                        "cost": 7.50,
                        "conversion": 1,
                        "timestamp": (datetime.now().replace(hour=i, minute=0, second=0)).isoformat()
                    },
                    "signature": "test_signature"
                }
            )
            assert response.status_code == status.HTTP_200_OK

        # 验证日数据聚合
        # 总曝光: 500 * 24 = 12000
        # 总点击: 25 * 24 = 600


class TestDataSync:
    """数据同步测试"""

    def test_sync_from_media_platform(self, client, test_media_account):
        """测试从媒体平台同步数据"""
        with patch('app.services.data_service.DataService._fetch_data_from_platform') as mock_fetch:
            mock_fetch.return_value = {
                "impression": 10000,
                "click": 500,
                "cost": 150.00,
                "conversion": 20
            }

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/sync",
                json={
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            )

            assert response.status_code == status.HTTP_200_OK

    def test_sync_realtime_data(self, client, test_media_account):
        """测试同步实时数据"""
        with patch('app.services.data_service.DataService._fetch_realtime_data') as mock_fetch:
            mock_fetch.return_value = {
                "impression": 1000,
                "click": 50,
                "cost": 15.00,
                "conversion": 2
            }

            response = client.post(
                f"/api/v1/accounts/{test_media_account.account_id}/sync-realtime"
            )

            assert response.status_code == status.HTTP_200_OK

    def test_batch_sync_accounts(self, client):
        """测试批量同步账户数据"""
        with patch('app.services.data_service.DataService.sync_account_data') as mock_sync:
            mock_sync.return_value = True

            response = client.post(
                "/api/v1/data/batch-sync",
                json={
                    "account_ids": ["account_001", "account_002", "account_003"],
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            )

            assert response.status_code == status.HTTP_200_OK
            assert mock_sync.call_count == 3


class TestRateLimiting:
    """速率限制测试"""

    def test_rate_limit_exceeded(self, client, test_media_account, test_campaign):
        """测试速率限制（超过限制）"""
        # 模拟发送大量请求超过速率限制
        for i in range(100):  # 假设限制是每分钟 60 次
            response = client.post(
                "/api/v1/data/campaign",
                json={
                    "account_id": test_media_account.id,
                    "campaign_id": test_campaign.id,
                    "data": {
                        "impression": 100,
                        "click": 5
                    },
                    "signature": "test_signature"
                }
            )

            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                # 达到速率限制
                return True

        pytest.fail("Should have hit rate limit")


class TestDataDeduplication:
    """数据去重测试"""

    def test_duplicate_data_handling(self, client, test_media_account, test_campaign):
        """测试重复数据处理"""
        data = {
            "account_id": test_media_account.id,
            "campaign_id": test_campaign.id,
            "data": {
                "impression": 10000,
                "click": 500,
                "cost": 150.00,
                "conversion": 20,
                "timestamp": datetime.now().isoformat()
            },
            "signature": "test_signature"
        }

        # 第一次发送
        response1 = client.post("/api/v1/data/campaign", json=data)
        assert response1.status_code == status.HTTP_200_OK

        # 第二次发送相同数据（应该被去重）
        response2 = client.post("/api/v1/data/campaign", json=data)
        assert response2.status_code == status.HTTP_200_OK

        # 验证只有一条记录被写入数据库

    def test_deduplication_by_timestamp(self, client, test_media_account, test_campaign):
        """测试按时间戳去重"""
        timestamp = datetime.now().isoformat()

        # 发送相同时间戳的数据
        for i in range(3):
            response = client.post(
                "/api/v1/data/campaign",
                json={
                    "account_id": test_media_account.id,
                    "campaign_id": test_campaign.id,
                    "data": {
                        "impression": 10000,
                        "click": 500
                    },
                    "timestamp": timestamp,
                    "signature": "test_signature"
                }
            )
            assert response.status_code == status.HTTP_200_OK

        # 验证只有一条记录
