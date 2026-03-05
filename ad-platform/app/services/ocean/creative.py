"""
巨量引擎创意 (Creative) 服务
"""
import json
from typing import Dict, Any, List, Optional
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class CreativeService:
    """创意服务"""

    CREATE_URL = "/2/creative/create/"
    UPDATE_URL = "/2/creative/update/"
    GET_URL = "/2/creative/get/"
    DELETE_URL = "/2/creative/delete/"
    UPDATE_STATUS_URL = "/2/creative/update/status/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def create(
        self,
        advertiser_id: str,
        adgroup_id: int,
        creative_name: str,
        creative_type: int,
        creative_material_mode: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        创建创意

        Args:
            advertiser_id: 广告主 ID
            adgroup_id: 广告组 ID
            creative_name: 创意名称
            creative_type: 创意类型
            creative_material_mode: 创意素材模式
            **kwargs: 素材内容等参数

        Returns:
            创建结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "adgroup_id": adgroup_id,
            "creative_name": creative_name,
            "creative_type": creative_type,
            "creative_material_mode": creative_material_mode,
            **kwargs
        }

        result = self.client.post_json(self.CREATE_URL, json_data={"creative_data": data})
        return {
            "creative_id": result.get("creative_id"),
            "advertiser_id": result.get("advertiser_id"),
        }

    def get(
        self,
        advertiser_id: str,
        adgroup_id: Optional[int] = None,
        creative_ids: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, Any]:
        """
        获取创意列表

        Args:
            advertiser_id: 广告主 ID
            adgroup_id: 广告组 ID（可选）
            creative_ids: 创意 ID 列表（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            创意列表
        """
        params = {
            "advertiser_id": advertiser_id,
            "page": page,
            "page_size": page_size,
        }

        filtering = {}
        if adgroup_id:
            filtering["adgroup_ids"] = [adgroup_id]
        if creative_ids:
            filtering["creative_ids"] = creative_ids

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
        creative_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        更新创意

        Args:
            advertiser_id: 广告主 ID
            creative_id: 创意 ID
            **kwargs: 要更新的字段

        Returns:
            更新结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "creative_id": creative_id,
            **kwargs
        }
        self.client.post_json(self.UPDATE_URL, json_data={"creative_data": data})
        return {"success": True}

    def update_status(
        self,
        advertiser_id: str,
        creative_id: int,
        opt_status: str = "enable"
    ) -> Dict[str, Any]:
        """
        更新创意状态

        Args:
            advertiser_id: 广告主 ID
            creative_id: 创意 ID
            opt_status: 操作状态

        Returns:
            操作结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "creative_ids": [creative_id],
            "opt_status": opt_status,
        }
        self.client.post_json(self.UPDATE_STATUS_URL, json_data={"creative_data": data})
        return {"success": True}

    def delete(
        self,
        advertiser_id: str,
        creative_id: int
    ) -> Dict[str, Any]:
        """
        删除创意

        Args:
            advertiser_id: 广告主 ID
            creative_id: 创意 ID

        Returns:
            删除结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "creative_ids": [creative_id],
        }
        self.client.post_json(self.DELETE_URL, json_data={"creative_data": data})
        return {"success": True}
