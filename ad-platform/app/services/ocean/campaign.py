"""
巨量引擎广告计划 (Campaign) 服务
"""
import json
from typing import Dict, Any, List, Optional
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class CampaignService:
    """广告计划服务"""

    CREATE_URL = "/2/campaign/create/"
    UPDATE_URL = "/2/campaign/update/"
    GET_URL = "/2/campaign/get/"
    DELETE_URL = "/2/campaign/delete/"
    UPDATE_STATUS_URL = "/2/campaign/update/status/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def create(
        self,
        advertiser_id: str,
        campaign_name: str,
        start_time: str,
        end_time: str,
        budget_mode: int = 1,
        budget: Optional[int] = None,
        objectives: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        创建广告计划

        Args:
            advertiser_id: 广告主 ID
            campaign_name: 计划名称
            start_time: 开始时间（ISO 8601）
            end_time: 结束时间（ISO 8601）
            budget_mode: 预算模式（1-日预算，2-总预算）
            budget: 预算（单位：分）
            objectives: 推广目标列表
            **kwargs: 其他参数

        Returns:
            创建结果
        """
        if objectives is None:
            objectives = ["LIFESPAN_PROMOTION"]

        data = {
            "advertiser_id": advertiser_id,
            "campaign_name": campaign_name,
            "budget_mode": budget_mode,
            "start_time": start_time,
            "end_time": end_time,
            "objective_type": objectives[0],
            **kwargs
        }

        if budget is not None:
            data["budget"] = budget

        result = self.client.post_json(self.CREATE_URL, json_data={"campaign_data": data})
        return {
            "campaign_id": result.get("campaign_id"),
            "advertiser_id": result.get("advertiser_id"),
        }

    def get(
        self,
        advertiser_id: str,
        campaign_ids: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        获取广告计划列表

        Args:
            advertiser_id: 广告主 ID
            campaign_ids: 计划 ID 列表（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            广告计划列表
        """
        params = {
            "advertiser_id": advertiser_id,
            "page": page,
            "page_size": page_size,
        }

        if campaign_ids:
            params["filtering"] = json.dumps({
                "campaign_ids": campaign_ids,
            })

        result = self.client.get(self.GET_URL, params=params)
        return {
            "list": result.get("list", []),
            "page_info": result.get("page_info", {}),
        }

    def update(
        self,
        advertiser_id: str,
        campaign_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        更新广告计划

        Args:
            advertiser_id: 广告主 ID
            campaign_id: 计划 ID
            **kwargs: 要更新的字段

        Returns:
            更新结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "campaign_id": campaign_id,
            **kwargs
        }
        self.client.post_json(self.UPDATE_URL, json_data={"campaign_data": data})
        return {"success": True}

    def update_status(
        self,
        advertiser_id: str,
        campaign_id: int,
        opt_status: str = "enable"
    ) -> Dict[str, Any]:
        """
        更新广告计划状态

        Args:
            advertiser_id: 广告主 ID
            campaign_id: 计划 ID
            opt_status: 操作状态（enable-启用，disable-停用）

        Returns:
            操作结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "campaign_ids": [campaign_id],
            "opt_status": opt_status,
        }
        self.client.post_json(self.UPDATE_STATUS_URL, json_data={"campaign_data": data})
        return {"success": True}

    def delete(
        self,
        advertiser_id: str,
        campaign_id: int
    ) -> Dict[str, Any]:
        """
        删除广告计划

        Args:
            advertiser_id: 广告主 ID
            campaign_id: 计划 ID

        Returns:
            删除结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "campaign_ids": [campaign_id],
        }
        self.client.post_json(self.DELETE_URL, json_data={"campaign_data": data})
        return {"success": True}
