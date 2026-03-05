"""
巨量引擎转化回传服务
"""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class ConversionService:
    """转化回传服务"""

    CONVERT_URL = "/2/conversion/upload/"
    CONVERT_QUERY_URL = "/2/conversion/query/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def upload_conversion(
        self,
        advertiser_id: str,
        conversions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        上传转化数据

        Args:
            advertiser_id: 广告主 ID
            conversions: 转化数据列表

        Returns:
            上传结果
        """
        data = {
            "advertiser_id": advertiser_id,
            "conversion_data": conversions,
        }

        result = self.client.post_json(self.CONVERT_URL, json_data={"conversion_data": data})

        return {
            "success": result.get("success", False),
            "conversion_id_list": result.get("conversion_id_list", []),
        }

    def query_conversion(
        self,
        advertiser_id: str,
        start_date: str,
        end_date: str,
        page: int = 1,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        查询转化数据

        Args:
            advertiser_id: 广告主 ID
            start_date: 开始日期
            end_date: 结束日期
            page: 页码
            page_size: 每页数量

        Returns:
            转化数据列表
        """
        params = {
            "advertiser_id": advertiser_id,
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
        }

        result = self.client.get(self.CONVERT_QUERY_URL, params=params)

        return {
            "list": result.get("list", []),
            "page_info": result.get("page_info", {}),
        }
