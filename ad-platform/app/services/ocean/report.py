"""
巨量引擎数据报表服务
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class ReportService:
    """数据报表服务"""

    REPORT_URL = "/3/report/ad/get/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def get_daily_report(
        self,
        advertiser_id: str,
        start_date: str,
        end_date: str,
        campaign_ids: Optional[List[int]] = None,
        adgroup_ids: Optional[List[int]] = None,
        creative_ids: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        获取日报表数据

        Args:
            advertiser_id: 广告主 ID
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            campaign_ids: 计划 ID 列表（可选）
            adgroup_ids: 广告组 ID 列表（可选）
            creative_ids: 创意 ID 列表（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            日报表数据
        """
        params = {
            "advertiser_id": advertiser_id,
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
            "data_level": "campaign_adgroup_creative",  # 数据粒度
            "metrics": '["cost","show","click","ctr","cpm","cpc","convert"]',
        }

        # 添加过滤条件
        filtering = {}
        if campaign_ids:
            filtering["campaign_ids"] = campaign_ids
        if adgroup_ids:
            filtering["adgroup_ids"] = adgroup_ids
        if creative_ids:
            filtering["creative_ids"] = creative_ids

        if filtering:
            params["filtering"] = json.dumps(filtering)

        result = self.client.get(self.REPORT_URL, params=params)

        return {
            "list": result.get("list", []),
            "page_info": result.get("page_info", {}),
        }
