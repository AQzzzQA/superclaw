"""
广告计划/组/创意 CRUD 集成测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch
from fastapi import status


class TestCampaignCRUD:
    """广告计划 CRUD 测试"""

    def test_create_campaign_success(self, client, auth_headers, test_media_account):
        """测试创建广告计划成功"""
        response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "测试广告计划",
                "account_id": test_media_account.id,
                "budget": 5000.00,
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": (datetime.now()).isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["campaign_name"] == "测试广告计划"
        assert data["budget"] == 5000.00

    def test_create_campaign_missing_required_field(self, client, auth_headers):
        """测试创建广告计划（缺少必填字段）"""
        response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "测试广告计划",
                "account_id": 1
                # 缺少 budget, bid_type 等必填字段
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_campaign_invalid_budget(self, client, auth_headers, test_media_account):
        """测试创建广告计划（无效预算）"""
        response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "测试广告计划",
                "account_id": test_media_account.id,
                "budget": -100.00,  # 负预算
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": (datetime.now()).isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_campaign_by_id(self, client, auth_headers, test_campaign):
        """测试根据 ID 获取广告计划"""
        response = client.get(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["campaign_id"] == test_campaign.campaign_id

    def test_get_campaign_list(self, client, auth_headers, test_campaign):
        """测试获取广告计划列表"""
        response = client.get(
            "/api/v1/campaigns",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data
        assert len(data["items"]) > 0

    def test_update_campaign_budget(self, client, auth_headers, test_campaign):
        """测试更新广告计划预算"""
        response = client.patch(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            json={
                "budget": 6000.00
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["budget"] == 6000.00

    def test_pause_campaign(self, client, auth_headers, test_campaign):
        """测试暂停广告计划"""
        response = client.post(
            f"/api/v1/campaigns/{test_campaign.campaign_id}/pause",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["status"] == "PAUSED"

    def test_start_campaign(self, client, auth_headers, test_campaign):
        """测试启动广告计划"""
        # 先暂停
        client.post(
            f"/api/v1/campaigns/{test_campaign.campaign_id}/pause",
            headers=auth_headers
        )

        # 再启动
        response = client.post(
            f"/api/v1/campaigns/{test_campaign.campaign_id}/start",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["status"] == "RUNNING"

    def test_delete_campaign(self, client, auth_headers, test_campaign):
        """测试删除广告计划"""
        response = client.delete(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_batch_create_campaigns(self, client, auth_headers, test_media_account):
        """测试批量创建广告计划"""
        campaigns = [
            {
                "campaign_name": f"批量测试计划{i}",
                "account_id": test_media_account.id,
                "budget": 1000.00,
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": (datetime.now()).isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat()
            }
            for i in range(1, 6)
        ]

        response = client.post(
            "/api/v1/campaigns/batch",
            json={"campaigns": campaigns},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["created"]) == 5


class TestAdGroupCRUD:
    """广告组 CRUD 测试"""

    def test_create_adgroup_success(self, client, auth_headers, test_campaign):
        """测试创建广告组成功"""
        response = client.post(
            "/api/v1/adgroups",
            json={
                "adgroup_name": "测试广告组",
                "campaign_id": test_campaign.id,
                "account_id": test_campaign.account_id,
                "budget": 1000.00,
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "targeting": {
                    "age": ["18-24", "25-30"],
                    "gender": ["MALE"],
                    "location": ["北京", "上海"]
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["adgroup_name"] == "测试广告组"

    def test_create_adgroup_invalid_targeting(self, client, auth_headers, test_campaign):
        """测试创建广告组（无效定向）"""
        response = client.post(
            "/api/v1/adgroups",
            json={
                "adgroup_name": "测试广告组",
                "campaign_id": test_campaign.id,
                "account_id": test_campaign.account_id,
                "budget": 1000.00,
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "targeting": {
                    "age": "18-24"  # 应该是数组
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_adgroup_by_id(self, client, auth_headers, test_adgroup):
        """测试根据 ID 获取广告组"""
        response = client.get(
            f"/api/v1/adgroups/{test_adgroup.adgroup_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["adgroup_id"] == test_adgroup.adgroup_id

    def test_get_adgroups_by_campaign(self, client, auth_headers, test_campaign, test_adgroup):
        """测试获取广告计划下的广告组列表"""
        response = client.get(
            f"/api/v1/campaigns/{test_campaign.campaign_id}/adgroups",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["items"]) > 0

    def test_update_adgroup_bid(self, client, auth_headers, test_adgroup):
        """测试更新广告组出价"""
        response = client.patch(
            f"/api/v1/adgroups/{test_adgroup.adgroup_id}",
            json={
                "bid_amount": 2.00
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["bid_amount"] == 2.00

    def test_pause_adgroup(self, client, auth_headers, test_adgroup):
        """测试暂停广告组"""
        response = client.post(
            f"/api/v1/adgroups/{test_adgroup.adgroup_id}/pause",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["status"] == "PAUSED"

    def test_delete_adgroup(self, client, auth_headers, test_adgroup):
        """测试删除广告组"""
        response = client.delete(
            f"/api/v1/adgroups/{test_adgroup.adgroup_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestCreativeCRUD:
    """广告创意 CRUD 测试"""

    def test_create_image_creative(self, client, auth_headers, test_adgroup):
        """测试创建图片创意成功"""
        response = client.post(
            "/api/v1/creatives",
            json={
                "creative_name": "测试图片创意",
                "adgroup_id": test_adgroup.id,
                "account_id": test_adgroup.account_id,
                "campaign_id": test_adgroup.campaign_id,
                "creative_type": "IMAGE",
                "material_url": "https://example.com/image.jpg",
                "title": "测试标题",
                "description": "测试描述",
                "landing_url": "https://example.com/landing",
                "display_url": "example.com",
                "button_text": "立即购买"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["creative_type"] == "IMAGE"

    def test_create_video_creative(self, client, auth_headers, test_adgroup):
        """测试创建视频创意成功"""
        response = client.post(
            "/api/v1/creatives",
            json={
                "creative_name": "测试视频创意",
                "adgroup_id": test_adgroup.id,
                "account_id": test_adgroup.account_id,
                "campaign_id": test_adgroup.campaign_id,
                "creative_type": "VIDEO",
                "material_url": "https://example.com/video.mp4",
                "video_duration": 30,
                "title": "测试标题",
                "description": "测试描述",
                "landing_url": "https://example.com/landing",
                "display_url": "example.com"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["creative_type"] == "VIDEO"

    def test_create_creative_invalid_url(self, client, auth_headers, test_adgroup):
        """测试创建创意（无效 URL）"""
        response = client.post(
            "/api/v1/creatives",
            json={
                "creative_name": "测试创意",
                "adgroup_id": test_adgroup.id,
                "account_id": test_adgroup.account_id,
                "campaign_id": test_adgroup.campaign_id,
                "creative_type": "IMAGE",
                "material_url": "not-a-valid-url",
                "title": "测试标题",
                "landing_url": "https://example.com/landing"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_creative_by_id(self, client, auth_headers, test_creative):
        """测试根据 ID 获取创意"""
        response = client.get(
            f"/api/v1/creatives/{test_creative.creative_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["creative_id"] == test_creative.creative_id

    def test_get_creatives_by_adgroup(self, client, auth_headers, test_adgroup, test_creative):
        """测试获取广告组下的创意列表"""
        response = client.get(
            f"/api/v1/adgroups/{test_adgroup.adgroup_id}/creatives",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["items"]) > 0

    def test_update_creative_title(self, client, auth_headers, test_creative):
        """测试更新创意标题"""
        response = client.patch(
            f"/api/v1/creatives/{test_creative.creative_id}",
            json={
                "title": "更新后的标题"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["title"] == "更新后的标题"

    def test_pause_creative(self, client, auth_headers, test_creative):
        """测试暂停创意"""
        response = client.post(
            f"/api/v1/creatives/{test_creative.creative_id}/pause",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["status"] == 2  # 暂停

    def test_delete_creative(self, client, auth_headers, test_creative):
        """测试删除创意"""
        response = client.delete(
            f"/api/v1/creatives/{test_creative.creative_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestBatchOperations:
    """批量操作测试"""

    def test_batch_create_adgroups(self, client, auth_headers, test_campaign):
        """测试批量创建广告组"""
        adgroups = [
            {
                "adgroup_name": f"批量测试组{i}",
                "campaign_id": test_campaign.id,
                "account_id": test_campaign.account_id,
                "budget": 200.00,
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "targeting": {"age": ["18-24"]}
            }
            for i in range(1, 4)
        ]

        response = client.post(
            "/api/v1/adgroups/batch",
            json={"adgroups": adgroups},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["created"]) == 3

    def test_batch_create_creatives(self, client, auth_headers, test_adgroup):
        """测试批量创建创意"""
        creatives = [
            {
                "creative_name": f"批量创意{i}",
                "adgroup_id": test_adgroup.id,
                "account_id": test_adgroup.account_id,
                "campaign_id": test_adgroup.campaign_id,
                "creative_type": "IMAGE",
                "material_url": f"https://example.com/image{i}.jpg",
                "title": f"标题{i}",
                "landing_url": "https://example.com/landing"
            }
            for i in range(1, 4)
        ]

        response = client.post(
            "/api/v1/creatives/batch",
            json={"creatives": creatives},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert len(data["created"]) == 3

    def test_batch_pause_campaigns(self, client, auth_headers, test_campaign, db_session):
        """测试批量暂停广告计划"""
        # 创建多个广告计划
        from app.models.campaign import Campaign

        campaigns = []
        for i in range(1, 4):
            campaign = Campaign(
                campaign_id=f"test_campaign_{i}",
                campaign_name=f"测试计划{i}",
                account_id=test_campaign.account_id,
                owner_id=test_campaign.owner_id,
                budget=1000.00,
                bid_type="CPC",
                bid_amount=Decimal("1.50"),
                start_date=datetime.now().date(),
                end_date=(datetime.now() + timedelta(days=30)).date(),
                status="RUNNING"
            )
            db_session.add(campaign)
            campaigns.append(campaign)

        db_session.commit()

        # 批量暂停
        response = client.post(
            "/api/v1/campaigns/batch-pause",
            json={
                "campaign_ids": [c.campaign_id for c in campaigns]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_batch_update_bid(self, client, auth_headers, test_adgroup, db_session):
        """测试批量更新出价"""
        # 创建多个广告组
        from app.models.campaign import AdGroup

        adgroups = []
        for i in range(1, 4):
            adgroup = AdGroup(
                adgroup_id=f"test_adgroup_{i}",
                adgroup_name=f"测试组{i}",
                campaign_id=test_adgroup.campaign_id,
                account_id=test_adgroup.account_id,
                owner_id=test_adgroup.owner_id,
                budget=200.00,
                bid_type="CPC",
                bid_amount=Decimal("1.50"),
                status="RUNNING"
            )
            db_session.add(adgroup)
            adgroups.append(adgroup)

        db_session.commit()

        # 批量更新出价
        response = client.post(
            "/api/v1/adgroups/batch-update-bid",
            json={
                "adgroup_ids": [ag.adgroup_id for ag in adgroups],
                "new_bid_amount": 2.00
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestStatusTransitions:
    """状态转换测试"""

    def test_campaign_full_lifecycle(self, client, auth_headers, test_media_account):
        """测试广告计划完整生命周期"""
        # 1. 创建
        create_response = client.post(
            "/api/v1/campaigns",
            json={
                "campaign_name": "生命周期测试",
                "account_id": test_media_account.id,
                "budget": 1000.00,
                "budget_type": "DAILY",
                "bid_type": "CPC",
                "bid_amount": 1.50,
                "start_date": (datetime.now()).isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat()
            },
            headers=auth_headers
        )
        campaign_id = create_response.json()["data"]["campaign_id"]

        # 2. 启动
        client.post(f"/api/v1/campaigns/{campaign_id}/start", headers=auth_headers)

        # 3. 暂停
        client.post(f"/api/v1/campaigns/{campaign_id}/pause", headers=auth_headers)

        # 4. 重新启动
        client.post(f"/api/v1/campaigns/{campaign_id}/start", headers=auth_headers)

        # 5. 删除
        response = client.delete(f"/api/v1/campaigns/{campaign_id}", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_status_transition(self, client, auth_headers, test_campaign):
        """测试无效状态转换"""
        # 尝试删除运行中的广告计划（应该失败）
        test_campaign.status = "RUNNING"

        response = client.delete(
            f"/api/v1/campaigns/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
