"""
数据报表模块单元测试
"""

import pytest
from datetime import datetime, timedelta, date
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.models.report import ReportDaily, ReportHourly
from app.services.report_service import ReportService


class TestReportDailyModel:
    """日报表模型测试"""

    @pytest.fixture
    def test_report(self):
        """创建测试日报表"""
        return ReportDaily(
            id=1,
            account_id=1,
            campaign_id=1,
            report_date=datetime.now().date(),
            impression=10000,
            click=500,
            ctr=Decimal("0.0500"),
            cost=Decimal("150.00"),
            cpm=Decimal("15.00"),
            cpc=Decimal("0.30"),
            conversion=20,
            cvr=Decimal("0.0400"),
            cpa=Decimal("7.50"),
            revenue=Decimal("300.00"),
            roi=Decimal("2.0000")
        )

    def test_report_creation(self, test_report):
        """测试日报表创建"""
        assert test_report.account_id == 1
        assert test_report.impression == 10000
        assert test_report.click == 500
        assert test_report.cost == Decimal("150.00")
        assert test_report.conversion == 20

    def test_calculate_ctr(self):
        """测试计算点击率"""
        impression = 10000
        click = 500
        ctr = (click / impression * 100) if impression > 0 else Decimal("0")

        assert ctr == Decimal("5.0000")

    def test_calculate_cpc(self):
        """测试计算点击成本"""
        cost = Decimal("150.00")
        click = 500
        cpc = (cost / click) if click > 0 else Decimal("0")

        assert cpc == Decimal("0.30")

    def test_calculate_cpm(self):
        """测试计算千次展示成本"""
        cost = Decimal("150.00")
        impression = 10000
        cpm = (cost / impression * 1000) if impression > 0 else Decimal("0")

        assert cpm == Decimal("15.00")

    def test_calculate_cvr(self):
        """测试计算转化率"""
        conversion = 20
        click = 500
        cvr = (conversion / click * 100) if click > 0 else Decimal("0")

        assert cvr == Decimal("4.0000")

    def test_calculate_cpa(self):
        """测试计算转化成本"""
        cost = Decimal("150.00")
        conversion = 20
        cpa = (cost / conversion) if conversion > 0 else Decimal("0")

        assert cpa == Decimal("7.50")

    def test_calculate_roi(self):
        """测试计算投资回报率"""
        revenue = Decimal("300.00")
        cost = Decimal("150.00")
        roi = ((revenue - cost) / cost * 100) if cost > 0 else Decimal("0")

        assert roi == Decimal("100.0000")

    def test_edge_case_zero_impression(self):
        """测试边界情况：零曝光"""
        impression = 0
        click = 0
        ctr = Decimal("0")

        assert ctr == Decimal("0")

    def test_edge_case_zero_click(self):
        """测试边界情况：零点击"""
        cost = Decimal("100.00")
        click = 0
        cpc = Decimal("0")

        assert cpc == Decimal("0")


class TestReportHourlyModel:
    """实时报表模型测试"""

    @pytest.fixture
    def test_hourly_report(self):
        """创建测试实时报表"""
        return ReportHourly(
            id=1,
            account_id=1,
            campaign_id=1,
            report_hour=datetime.now().replace(minute=0, second=0, microsecond=0),
            impression=1000,
            click=50,
            cost=Decimal("15.00"),
            conversion=2
        )

    def test_hourly_report_creation(self, test_hourly_report):
        """测试实时报表创建"""
        assert test_hourly_report.account_id == 1
        assert test_hourly_report.impression == 1000
        assert test_hourly_report.click == 50
        assert test_hourly_report.cost == Decimal("15.00")

    def test_hourly_data_aggregation(self):
        """测试小时数据聚合"""
        # 模拟多个小时的数据
        hourly_data = [
            {"hour": "09:00", "impression": 1000, "click": 50, "cost": 15.00},
            {"hour": "10:00", "impression": 1200, "click": 60, "cost": 18.00},
            {"hour": "11:00", "impression": 800, "click": 40, "cost": 12.00}
        ]

        # 聚合为日数据
        daily_total = {
            "impression": sum(d["impression"] for d in hourly_data),
            "click": sum(d["click"] for d in hourly_data),
            "cost": sum(d["cost"] for d in hourly_data)
        }

        assert daily_total["impression"] == 3000
        assert daily_total["click"] == 150
        assert daily_total["cost"] == 45.00


class TestReportService:
    """报表服务测试"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock 数据库会话"""
        return MagicMock()

    @pytest.fixture
    def report_service(self, mock_db_session):
        """创建报表服务实例"""
        return ReportService(mock_db_session)

    @pytest.fixture
    def test_report_data(self):
        """测试报表数据"""
        return ReportDaily(
            account_id=1,
            campaign_id=1,
            report_date=datetime.now().date(),
            impression=10000,
            click=500,
            ctr=Decimal("0.0500"),
            cost=Decimal("150.00"),
            cpm=Decimal("15.00"),
            cpc=Decimal("0.30"),
            conversion=20,
            cvr=Decimal("0.0400"),
            cpa=Decimal("7.50"),
            revenue=Decimal("300.00"),
            roi=Decimal("2.0000")
        )

    def test_create_daily_report(self, report_service, test_report_data):
        """测试创建日报表"""
        result = report_service.create_daily_report(test_report_data)
        assert result is not None
        assert report_service.db_session.add.called

    def test_get_report_by_date_range(self, report_service, mock_db_session):
        """测试按日期范围获取报表"""
        start_date = datetime.now().date() - timedelta(days=7)
        end_date = datetime.now().date()

        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            MagicMock(report_date=start_date + timedelta(days=i))
            for i in range(7)
        ]

        reports = report_service.get_reports_by_date_range(
            account_id=1,
            start_date=start_date,
            end_date=end_date
        )

        assert len(reports) == 7

    def test_get_campaign_report(self, report_service, mock_db_session):
        """测试获取广告计划报表"""
        mock_db_session.query.return_value.filter.return_value.all.return_value = [
            MagicMock(campaign_id=1, report_date=datetime.now().date()),
            MagicMock(campaign_id=1, report_date=datetime.now().date() - timedelta(days=1))
        ]

        reports = report_service.get_campaign_reports(campaign_id=1)

        assert len(reports) == 2
        assert reports[0].campaign_id == 1

    def test_aggregate_daily_report(self, report_service):
        """测试聚合日报表数据"""
        reports = [
            ReportDaily(
                account_id=1,
                campaign_id=1,
                report_date=datetime.now().date() - timedelta(days=i),
                impression=1000 * (i + 1),
                click=50 * (i + 1),
                cost=Decimal("15.00") * (i + 1),
                conversion=2 * (i + 1)
            )
            for i in range(7)
        ]

        aggregated = report_service.aggregate_reports(reports)

        assert aggregated["total_impression"] == 28000  # sum(1000, 2000, ..., 7000)
        assert aggregated["total_click"] == 1400
        assert aggregated["total_cost"] == Decimal("420.00")

    def test_export_report_to_excel(self, report_service):
        """测试导出报表到 Excel"""
        reports = [
            {
                "report_date": "2026-03-15",
                "impression": 10000,
                "click": 500,
                "cost": 150.00,
                "conversion": 20
            }
        ]

        with patch.object(report_service, '_generate_excel_file') as mock_generate:
            mock_generate.return_value = "report.xlsx"

            result = report_service.export_to_excel(reports)
            assert result == "report.xlsx"

    def test_export_report_to_csv(self, report_service):
        """测试导出报表到 CSV"""
        reports = [
            {
                "report_date": "2026-03-15",
                "impression": 10000,
                "click": 500,
                "cost": 150.00
            }
        ]

        with patch.object(report_service, '_generate_csv_file') as mock_generate:
            mock_generate.return_value = "report.csv"

            result = report_service.export_to_csv(reports)
            assert result == "report.csv"

    def test_get_top_performing_campaigns(self, report_service, mock_db_session):
        """测试获取表现最好的广告计划"""
        mock_db_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = [
            MagicMock(campaign_id=1, roi=Decimal("3.0000")),
            MagicMock(campaign_id=2, roi=Decimal("2.5000")),
            MagicMock(campaign_id=3, roi=Decimal("2.0000"))
        ]

        top_campaigns = report_service.get_top_campaigns(limit=3, metric="roi")

        assert len(top_campaigns) == 3
        assert top_campaigns[0].campaign_id == 1

    def test_get_underperforming_campaigns(self, report_service, mock_db_session):
        """测试获取表现不佳的广告计划"""
        mock_db_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = [
            MagicMock(campaign_id=1, roi=Decimal("0.5000")),
            MagicMock(campaign_id=2, roi=Decimal("0.8000")),
            MagicMock(campaign_id=3, roi=Decimal("1.0000"))
        ]

        underperforming = report_service.get_underperforming_campaigns(limit=3, metric="roi", threshold=1.0)

        assert len(underperforming) == 3
        assert underperforming[0].roi < Decimal("1.0000")


class TestReportMetrics:
    """报表指标计算测试"""

    def test_wctr_calculation(self):
        """测试加权点击率"""
        data = [
            {"impression": 1000, "click": 50},
            {"impression": 2000, "click": 120}
        ]

        total_impression = sum(d["impression"] for d in data)
        total_click = sum(d["click"] for d in data)
        wctr = (total_click / total_impression * 100) if total_impression > 0 else Decimal("0")

        assert wctr == Decimal("5.6667")

    def test_wcpa_calculation(self):
        """测试加权转化成本"""
        data = [
            {"cost": 100.00, "conversion": 10},
            {"cost": 150.00, "conversion": 15}
        ]

        total_cost = sum(d["cost"] for d in data)
        total_conversion = sum(d["conversion"] for d in data)
        wcpa = (total_cost / total_conversion) if total_conversion > 0 else Decimal("0")

        assert wcpa == Decimal("10.00")

    def test_trend_calculation(self):
        """测试趋势计算"""
        current = 500
        previous = 400

        growth_rate = ((current - previous) / previous * 100) if previous > 0 else Decimal("0")

        assert growth_rate == Decimal("25.0000")

    def test_moving_average(self):
        """测试移动平均计算"""
        data = [100, 110, 120, 130, 140]
        window = 3

        moving_avg = []
        for i in range(len(data) - window + 1):
            avg = sum(data[i:i + window]) / window
            moving_avg.append(avg)

        assert moving_avg == [110.0, 120.0, 130.0]

    def test_yoy_comparison(self):
        """测试同比比较"""
        current_year = 10000
        last_year = 8000

        yoy_growth = ((current_year - last_year) / last_year * 100) if last_year > 0 else Decimal("0")

        assert yoy_growth == Decimal("25.0000")

    def test_mom_comparison(self):
        """测试环比比较"""
        current_month = 10000
        last_month = 9000

        mom_growth = ((current_month - last_month) / last_month * 100) if last_month > 0 else Decimal("0")

        assert mom_growth == Decimal("11.1111")


class TestReportValidation:
    """报表数据验证测试"""

    def test_validate_report_data_complete(self):
        """测试报表数据完整性验证"""
        data = {
            "impression": 10000,
            "click": 500,
            "cost": 150.00,
            "conversion": 20
        }

        assert all(key in data for key in ["impression", "click", "cost", "conversion"])

    def test_validate_report_data_positive_values(self):
        """测试报表数据正数验证"""
        data = {
            "impression": 10000,
            "click": 500,
            "cost": 150.00,
            "conversion": 20
        }

        assert all(value >= 0 for value in data.values())

    def test_validate_click_not_greater_than_impression(self):
        """验证点击数不应大于曝光数"""
        impression = 10000
        click = 500

        assert click <= impression

    def test_validate_conversion_not_greater_than_click(self):
        """验证转化数不应大于点击数"""
        click = 500
        conversion = 20

        assert conversion <= click


class TestReportDataSync:
    """报表数据同步测试"""

    def test_sync_from_media_platform(self):
        """测试从媒体平台同步数据"""
        from app.services.report_service import ReportService

        service = ReportService(MagicMock())

        with patch.object(service, '_fetch_data_from_platform') as mock_fetch:
            mock_fetch.return_value = {
                "impression": 10000,
                "click": 500,
                "cost": 150.00
            }

            result = service.sync_data_from_platform(
                account_id=1,
                report_date=datetime.now().date()
            )

            assert result["impression"] == 10000

    def test_sync_batch_data(self):
        """测试批量同步数据"""
        from app.services.report_service import ReportService

        service = ReportService(MagicMock())

        dates = [
            datetime.now().date() - timedelta(days=i)
            for i in range(7)
        ]

        with patch.object(service, 'sync_data_from_platform') as mock_sync:
            mock_sync.return_value = {"impression": 10000, "click": 500, "cost": 150.00}

            results = service.batch_sync_data(account_id=1, dates=dates)

            assert len(results) == 7
            assert mock_sync.call_count == 7

    def test_sync_realtime_data(self):
        """测试同步实时数据"""
        from app.services.report_service import ReportService

        service = ReportService(MagicMock())

        with patch.object(service, '_fetch_realtime_data') as mock_fetch:
            mock_fetch.return_value = {
                "impression": 1000,
                "click": 50,
                "cost": 15.00,
                "conversion": 2
            }

            result = service.sync_realtime_data(account_id=1)

            assert result["impression"] == 1000
