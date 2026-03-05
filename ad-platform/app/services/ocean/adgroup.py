"""
巨量引擎广告组 (AdGroup) 服务
"""
import json
from typing import Dict, Any, List, Optional
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class AdGroupService:
    """广告组服务"""

    CREATE_URL = "/2/adgroup/create/"
    UPDATE_URL = "/2/adgroup/update/"
    GET_URL = "/2/adgroup/get/"
    DELETE_URL = "/2/adgroup/delete/"
    UPDATE_STATUS_URL = "/2/adgroup/update/status/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def create(
        self,
        advertiser_id: str,
        campaign_id: int,
        adgroup_name: str,
        start_time: str,
        end_time: str,
        promote_mode: int = 1,
        budget_mode: int = 1,
        budget: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        创建广告组

        Args:
            advertiser_id: 广告主 ID
            campaign_id: 计划 ID
            adgroup_name: 广告组名称
            start_time: 开始时间
            end_time: 结束时间
            promote_mode: 推广模式
            budget_mode: 预算模式
            budget: 预算（单位：分）
            **kwargs: 定向条件等参数

        Returns:
            创建结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "campaign_id": campaign_id,
            "adgroup_name": adgroup_name,
            "promote_mode": promote_mode,
            "budget_mode": budget_mode,
            "start_time": start_time,
            "end_time": end_time,
            **kwargs
        }

        if budget is not None:
            data["budget"] = budget

        result = self.client.post_json(self.CREATE_URL, json_data={"adgroup_data": data})
        return {
            "adgroup_id": result.get("adgroup_id"),
            "advertiser_id": result.get("advertiser_id"),
        }

    def get(
        self,
        advertiser_id: str,
        campaign_id: Optional[int] = None,
        adgroup_ids: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        获取广告组列表

        Args:
            advertiser_id: 广告主 ID
            campaign_id: 计划 ID（可选）
            adgroup_ids: 广告组 ID 列表（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            广告组列表
        """
        params = {
            "advertiser_id": advertiser_id,
            "page": page,
            "page_size": page_size,
        }

        filtering = {}
        if campaign_id:
            filtering["campaign_ids"] = [campaign_id]
        if adgroup_ids:
            filtering["adgroup_ids"] = adgroup_ids

        if filtering:
            params["filtering"] = json.dumps(filtering)

        result = self.client.get(self.GET_URL, params=params)
        return {
            "list": result.get("list", []),
            "page_info": result.get("page_info", {}),
        }

    def update(
        self,
        advertiser_id: str,
        adgroup_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        更新广告组

        Args:
            advertiser_id: 广告主 ID
            adgroup_id: 广告组 ID
            **kwargs: 要更新的字段

        Returns:
            更新结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "adgroup_id": adgroup_id,
            **kwargs
        }
        self.client.post_json(self.UPDATE_URL, json_data={"adgroup_data": data})
        return {"success": True}

    def update_status(
        self,
        advertiser_id: str,
        adgroup_id: int,
        opt_status: str = "enable"
    ) -> Dict[str, Any]:
        """
        更新广告组状态

        Args:
            advertiser_id: 广告主 ID
            adgroup_id: 广告组 ID
            opt_status: 操作状态

        Returns:
            操作结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "adgroup_ids": [adgroup_id],
            "opt_status": opt_status,
        }
        self.client.post_json(self.UPDATE_STATUS_URL, json_data={"adgroup_data": data})
        return {"success": True}

    def delete(
        self,
        advertiser_id: str,
        adgroup_id: int
    ) -> Dict[str, Any]:
        """
        删除广告组

        Args:
            advertiser_id: 广告主 ID
            adgroup_id: 广告组 ID

        Returns:
            删除结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "adgroup_ids": [adgroup_id],
        }
        self.client.post_json(self.DELETE_URL, json_data={"adgroup_data": data})
        return {"success": True}
