"""
报表生成和导出集成测试
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
from fastapi import status


class TestReportQuery:
    """报表查询测试"""

    def test_query_campaign_report(self, client, auth_headers, test_campaign):
        """测试查询广告计划报表"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "campaign_id" in data
        assert "metrics" in data

    def test_query_account_report(self, client, auth_headers, test_media_account):
        """测试查询账户报表"""
        response = client.get(
            f"/api/v1/reports/account/{test_media_account.account_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "account_id" in data

    def test_query_daily_report(self, client, auth_headers):
        """测试查询日报表"""
        response = client.get(
            f"/api/v1/reports/daily?date={datetime.now().date()}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_query_report_by_date_range(self, client, auth_headers):
        """测试按日期范围查询报表"""
        start_date = (datetime.now() - timedelta(days=7)).date()
        end_date = datetime.now().date()

        response = client.get(
            f"/api/v1/reports/daily?start_date={start_date}&end_date={end_date}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_query_hourly_report(self, client, auth_headers, test_campaign):
        """测试查询小时报表"""
        response = client.get(
            f"/api/v1/reports/hourly/{test_campaign.campaign_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_query_report_with_filters(self, client, auth_headers):
        """测试使用过滤器查询报表"""
        response = client.get(
            "/api/v1/reports/daily?channel_code=DOUYIN&status=RUNNING",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportAggregation:
    """报表聚合测试"""

    def test_aggregate_by_campaign(self, client, auth_headers):
        """测试按广告计划聚合"""
        response = client.get(
            "/api/v1/reports/aggregate?by=campaign",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "aggregations" in data

    def test_aggregate_by_account(self, client, auth_headers):
        """测试按账户聚合"""
        response = client.get(
            "/api/v1/reports/aggregate?by=account",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_aggregate_by_channel(self, client, auth_headers):
        """测试按渠道聚合"""
        response = client.get(
            "/api/v1/reports/aggregate?by=channel",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_aggregate_metrics(self, client, auth_headers):
        """测试聚合指标"""
        response = client.get(
            "/api/v1/reports/aggregate?by=campaign&metrics=impression,click,cost,conversion",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_aggregate_with_date_range(self, client, auth_headers):
        """测试按日期范围聚合"""
        start_date = (datetime.now() - timedelta(days=7)).date()
        end_date = datetime.now().date()

        response = client.get(
            f"/api/v1/reports/aggregate?by=campaign&start_date={start_date}&end_date={end_date}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportExport:
    """报表导出测试"""

    def test_export_to_excel(self, client, auth_headers):
        """测试导出为 Excel"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "excel",
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                },
                "filters": {
                    "channel_code": "DOUYIN"
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def test_export_to_csv(self, client, auth_headers):
        """测试导出为 CSV"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "csv",
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert "text/csv" in response.headers["content-type"]

    def test_export_to_pdf(self, client, auth_headers):
        """测试导出为 PDF"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "pdf",
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                },
                "template": "standard"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert "application/pdf" in response.headers["content-type"]

    def test_export_custom_fields(self, client, auth_headers):
        """测试导出自定义字段"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "excel",
                "fields": [
                    "campaign_id",
                    "campaign_name",
                    "impression",
                    "click",
                    "ctr",
                    "cost",
                    "cpc",
                    "conversion",
                    "roi"
                ],
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_export_large_dataset(self, client, auth_headers):
        """测试导出大数据集"""
        response = client.post(
            "/api/v1/reports/export",
            json={
                "format": "excel",
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=90)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            },
            headers=auth_headers
        )

        # 应该返回异步任务 ID
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "task_id" in data

    def test_export_download(self, client, auth_headers):
        """测试下载导出文件"""
        # 假设有一个导出任务 ID
        task_id = "export_task_123"

        response = client.get(
            f"/api/v1/reports/export/download/{task_id}",
            headers=auth_headers
        )

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]


class TestReportMetrics:
    """报表指标测试"""

    def test_calculate_ctr(self, client, auth_headers, test_campaign):
        """测试计算点击率"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/metrics",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "ctr" in data

    def test_calculate_cpc(self, client, auth_headers, test_campaign):
        """测试计算点击成本"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/metrics",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "cpc" in data

    def test_calculate_cvr(self, client, auth_headers, test_campaign):
        """测试计算转化率"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/metrics",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "cvr" in data

    def test_calculate_roi(self, client, auth_headers, test_campaign):
        """测试计算投资回报率"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/metrics",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "roi" in data

    def test_calculate_all_metrics(self, client, auth_headers, test_campaign):
        """测试计算所有指标"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/metrics?all=true",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        expected_metrics = [
            "impression", "click", "ctr", "cost", "cpm",
            "cpc", "conversion", "cvr", "cpa", "roi"
        ]
        for metric in expected_metrics:
            assert metric in data


class TestReportComparison:
    """报表对比测试"""

    def test_compare_periods(self, client, auth_headers):
        """测试对比不同时期"""
        current_start = (datetime.now() - timedelta(days=7)).date()
        current_end = datetime.now().date()
        previous_start = (datetime.now() - timedelta(days=14)).date()
        previous_end = (datetime.now() - timedelta(days=8)).date()

        response = client.post(
            "/api/v1/reports/compare",
            json={
                "current_period": {
                    "start_date": current_start.isoformat(),
                    "end_date": current_end.isoformat()
                },
                "previous_period": {
                    "start_date": previous_start.isoformat(),
                    "end_date": previous_end.isoformat()
                },
                "dimensions": ["campaign"]
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "comparison" in data

    def test_compare_campaigns(self, client, auth_headers):
        """测试对比不同广告计划"""
        response = client.post(
            "/api/v1/reports/compare",
            json={
                "campaign_ids": [1, 2, 3],
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_compare_channels(self, client, auth_headers):
        """测试对比不同渠道"""
        response = client.post(
            "/api/v1/reports/compare",
            json={
                "channel_codes": ["DOUYIN", "KUAISHOU", "WECHAT"],
                "date_range": {
                    "start_date": (datetime.now() - timedelta(days=7)).date().isoformat(),
                    "end_date": datetime.now().date().isoformat()
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportTrends:
    """报表趋势测试"""

    def test_get_trend_data(self, client, auth_headers, test_campaign):
        """测试获取趋势数据"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/trend",
            params={
                "period": "7d",
                "metrics": "impression,click,cost"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "trend" in data
        assert "growth_rate" in data

    def test_get_trend_yoy(self, client, auth_headers, test_campaign):
        """测试获取同比趋势"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/trend?comparison=yoy",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_trend_mom(self, client, auth_headers, test_campaign):
        """测试获取环比趋势"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/trend?comparison=mom",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportTemplates:
    """报表模板测试"""

    def test_create_report_template(self, client, auth_headers):
        """测试创建报表模板"""
        response = client.post(
            "/api/v1/reports/templates",
            json={
                "template_name": "标准报表",
                "fields": [
                    "campaign_id",
                    "campaign_name",
                    "impression",
                    "click",
                    "cost",
                    "roi"
                ],
                "filters": {
                    "channel_code": "DOUYIN"
                },
                "sort_by": "cost",
                "sort_order": "desc"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_report_templates(self, client, auth_headers):
        """测试获取报表模板列表"""
        response = client.get(
            "/api/v1/reports/templates",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "items" in data

    def test_apply_report_template(self, client, auth_headers):
        """测试应用报表模板"""
        template_id = 1

        response = client.post(
            f"/api/v1/reports/templates/{template_id}/apply",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_delete_report_template(self, client, auth_headers):
        """测试删除报表模板"""
        template_id = 1

        response = client.delete(
            f"/api/v1/reports/templates/{template_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportVisualization:
    """报表可视化测试"""

    def test_get_chart_data(self, client, auth_headers, test_campaign):
        """测试获取图表数据"""
        response = client.get(
            f"/api/v1/reports/campaign/{test_campaign.campaign_id}/chart",
            params={
                "chart_type": "line",
                "x_axis": "date",
                "y_axis": "cost"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "chart_config" in data
        assert "data_points" in data

    def test_get_pie_chart_data(self, client, auth_headers):
        """测试获取饼图数据"""
        response = client.get(
            "/api/v1/reports/chart",
            params={
                "chart_type": "pie",
                "dimension": "channel",
                "metric": "cost"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_bar_chart_data(self, client, auth_headers):
        """测试获取柱状图数据"""
        response = client.get(
            "/api/v1/reports/chart",
            params={
                "chart_type": "bar",
                "dimension": "campaign",
                "metric": "impression",
                "limit": 10
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportSharing:
    """报表分享测试"""

    def test_generate_share_link(self, client, auth_headers):
        """测试生成分享链接"""
        response = client.post(
            "/api/v1/reports/share",
            json={
                "report_type": "campaign",
                "report_id": 1,
                "expires_in": 7  # 7天后过期
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert "share_link" in data
        assert "share_token" in data

    def test_access_shared_report(self, client):
        """测试访问分享的报表"""
        share_token = "test_share_token"

        response = client.get(
            f"/api/v1/reports/shared/{share_token}"
        )

        # 可能成功或 404（如果 token 无效）
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_revoke_share_link(self, client, auth_headers):
        """测试撤销分享链接"""
        share_id = 1

        response = client.delete(
            f"/api/v1/reports/share/{share_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK


class TestReportAutomation:
    """报表自动化测试"""

    def test_create_scheduled_report(self, client, auth_headers):
        """测试创建定时报表"""
        response = client.post(
            "/api/v1/reports/schedules",
            json={
                "schedule_name": "日报",
                "report_type": "daily",
                "schedule": "0 9 * * *",  # 每天9点
                "recipients": ["user1@example.com", "user2@example.com"],
                "format": "excel",
                "filters": {
                    "channel_code": "DOUYIN"
                }
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_scheduled_reports(self, client, auth_headers):
        """测试获取定时报表列表"""
        response = client.get(
            "/api/v1/reports/schedules",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_scheduled_report(self, client, auth_headers):
        """测试更新定时报表"""
        schedule_id = 1

        response = client.patch(
            f"/api/v1/reports/schedules/{schedule_id}",
            json={
                "schedule": "0 10 * * *"  # 改为每天10点
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_delete_scheduled_report(self, client, auth_headers):
        """测试删除定时报表"""
        schedule_id = 1

        response = client.delete(
            f"/api/v1/reports/schedules/{schedule_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK

    def test_run_scheduled_report_manually(self, client, auth_headers):
        """测试手动运行定时报表"""
        schedule_id = 1

        response = client.post(
            f"/api/v1/reports/schedules/{schedule_id}/run",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
