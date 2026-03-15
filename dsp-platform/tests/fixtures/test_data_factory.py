"""
测试数据工厂
用于生成各种测试数据
"""

from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from app.models.user import User, Role, Permission
from app.models.account import MediaAccount, MediaChannel
from app.models.campaign import Campaign, AdGroup, Creative
from app.models.report import ReportDaily, ReportHourly
from app.models.budget import BudgetConfig, BudgetWarning
from app.core.security import get_password_hash


faker = Faker("zh_CN")


class TestDataFactory:
    """测试数据工厂"""

    @staticmethod
    def create_user(**kwargs):
        """创建测试用户"""
        data = {
            "username": faker.user_name(),
            "email": faker.email(),
            "hashed_password": get_password_hash(faker.password()),
            "full_name": faker.name(),
            "is_active": True,
            "is_superuser": False,
            "role_code": "ADVERTISER"
        }
        data.update(kwargs)
        return User(**data)

    @staticmethod
    def create_admin_user(**kwargs):
        """创建管理员用户"""
        data = {
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("admin123"),
            "full_name": "系统管理员",
            "is_active": True,
            "is_superuser": True,
            "role_code": "ADMIN"
        }
        data.update(kwargs)
        return User(**data)

    @staticmethod
    def create_role(**kwargs):
        """创建测试角色"""
        data = {
            "role_code": faker.word().upper(),
            "role_name": faker.word(),
            "description": faker.sentence()
        }
        data.update(kwargs)
        return Role(**data)

    @staticmethod
    def create_permission(**kwargs):
        """创建测试权限"""
        data = {
            "permission_code": f"{faker.word().upper()}_{faker.word().upper()}",
            "permission_name": faker.sentence(),
            "resource_type": faker.word().upper(),
            "action": faker.word().upper()
        }
        data.update(kwargs)
        return Permission(**data)

    @staticmethod
    def create_media_channel(**kwargs):
        """创建测试媒体渠道"""
        data = {
            "channel_code": faker.word().upper(),
            "channel_name": faker.word(),
            "channel_type": "VIDEO",
            "oauth_url": faker.url(),
            "api_endpoint": faker.url(),
            "is_active": True
        }
        data.update(kwargs)
        return MediaChannel(**data)

    @staticmethod
    def create_media_account(**kwargs):
        """创建测试媒体账户"""
        data = {
            "account_id": faker.uuid4(),
            "account_name": faker.company(),
            "channel_code": "DOUYIN",
            "owner_id": 1,
            "balance": Decimal(str(faker.random_number(5))),
            "status": "ACTIVE",
            "auth_token": faker.uuid4(),
            "refresh_token": faker.uuid4(),
            "token_expires_at": datetime.now() + timedelta(days=30),
            "is_authorized": True
        }
        data.update(kwargs)
        return MediaAccount(**data)

    @staticmethod
    def create_campaign(**kwargs):
        """创建测试广告计划"""
        data = {
            "campaign_id": faker.uuid4(),
            "campaign_name": faker.sentence(),
            "account_id": 1,
            "owner_id": 1,
            "budget": Decimal(str(faker.random_number(4))),
            "budget_type": "DAILY",
            "bid_type": "CPC",
            "bid_amount": Decimal("1.50"),
            "start_date": datetime.now().date(),
            "end_date": (datetime.now() + timedelta(days=30)).date(),
            "status": "RUNNING"
        }
        data.update(kwargs)
        return Campaign(**data)

    @staticmethod
    def create_adgroup(**kwargs):
        """创建测试广告组"""
        data = {
            "adgroup_id": faker.uuid4(),
            "adgroup_name": faker.sentence(),
            "campaign_id": 1,
            "account_id": 1,
            "owner_id": 1,
            "budget": Decimal(str(faker.random_number(3))),
            "bid_type": "CPC",
            "bid_amount": Decimal("1.50"),
            "targeting": '{"age": ["18-24"], "gender": ["MALE"]}',
            "status": "RUNNING"
        }
        data.update(kwargs)
        return AdGroup(**data)

    @staticmethod
    def create_creative(**kwargs):
        """创建测试创意"""
        data = {
            "creative_id": faker.uuid4(),
            "creative_name": faker.sentence(),
            "adgroup_id": 1,
            "account_id": 1,
            "campaign_id": 1,
            "creative_type": "IMAGE",
            "material_url": faker.url(),
            "material_type": "IMAGE",
            "title": faker.sentence(),
            "description": faker.text(),
            "landing_url": faker.url(),
            "display_url": faker.domain_name(),
            "button_text": "立即购买",
            "audit_status": 1,
            "status": 1
        }
        data.update(kwargs)
        return Creative(**data)

    @staticmethod
    def create_report_daily(**kwargs):
        """创建测试日报表"""
        impression = faker.random_number(5)
        click = int(impression * faker.random.uniform(0.01, 0.1))
        cost = Decimal(str(click * faker.random.uniform(0.1, 1.0)))
        conversion = int(click * faker.random.uniform(0.01, 0.1))

        data = {
            "account_id": 1,
            "campaign_id": 1,
            "report_date": faker.date_between(start_date="-30d", end_date="today"),
            "impression": impression,
            "click": click,
            "ctr": Decimal(str(click / impression * 100)) if impression > 0 else Decimal("0"),
            "cost": cost,
            "cpm": Decimal(str(cost / impression * 1000)) if impression > 0 else Decimal("0"),
            "cpc": Decimal(str(cost / click)) if click > 0 else Decimal("0"),
            "conversion": conversion,
            "cvr": Decimal(str(conversion / click * 100)) if click > 0 else Decimal("0"),
            "cpa": Decimal(str(cost / conversion)) if conversion > 0 else Decimal("0"),
            "revenue": Decimal(str(conversion * faker.random.uniform(10, 50))),
            "roi": Decimal("0")
        }

        # 计算ROI
        if cost > 0:
            data["roi"] = (data["revenue"] - cost) / cost * 100

        data.update(kwargs)
        return ReportDaily(**data)

    @staticmethod
    def create_report_hourly(**kwargs):
        """创建测试小时报表"""
        impression = faker.random_number(3)
        click = int(impression * faker.random.uniform(0.01, 0.1))
        cost = Decimal(str(click * faker.random.uniform(0.1, 1.0)))
        conversion = int(click * faker.random.uniform(0.01, 0.1))

        data = {
            "account_id": 1,
            "campaign_id": 1,
            "report_hour": faker.date_time_this_year(),
            "impression": impression,
            "click": click,
            "cost": cost,
            "conversion": conversion
        }
        data.update(kwargs)
        return ReportHourly(**data)

    @staticmethod
    def create_budget_config(**kwargs):
        """创建测试预算配置"""
        data = {
            "campaign_id": 1,
            "total_budget": Decimal(str(faker.random_number(4))),
            "daily_budget": Decimal(str(faker.random_number(3))),
            "warning_threshold": faker.random.uniform(70, 90),
            "stop_threshold": 100.0,
            "is_auto_stop": True,
            "is_warning_enabled": True
        }
        data.update(kwargs)
        return BudgetConfig(**data)

    @staticmethod
    def create_budget_warning(**kwargs):
        """创建测试预算预警"""
        data = {
            "campaign_id": 1,
            "budget_config_id": 1,
            "warning_type": "DAILY_BUDGET",
            "current_spend": Decimal(str(faker.random_number(3))),
            "threshold": Decimal("80.00"),
            "severity": "WARNING",
            "message": faker.sentence(),
            "is_resolved": False
        }
        data.update(kwargs)
        return BudgetWarning(**data)


class CampaignDataFactory:
    """广告投放数据工厂"""

    @staticmethod
    def create_complete_campaign_chain():
        """创建完整的广告投放链（计划 → 组 → 创意）"""
        campaign = TestDataFactory.create_campaign()
        adgroup = TestDataFactory.create_adgroup(campaign_id=campaign.id)
        creative = TestDataFactory.create_creative(adgroup_id=adgroup.id)

        return {
            "campaign": campaign,
            "adgroup": adgroup,
            "creative": creative
        }


class ReportDataFactory:
    """报表数据工厂"""

    @staticmethod
    def create_time_series_reports(days=30):
        """创建时间序列报表数据"""
        reports = []
        for i in range(days):
            report = TestDataFactory.create_report_daily(
                report_date=datetime.now().date() - timedelta(days=i)
            )
            reports.append(report)
        return reports

    @staticmethod
    def create_multi_campaign_reports(campaign_count=5, days=30):
        """创建多广告计划报表数据"""
        all_reports = []
        for campaign_id in range(1, campaign_count + 1):
            for day in range(days):
                report = TestDataFactory.create_report_daily(
                    campaign_id=campaign_id,
                    report_date=datetime.now().date() - timedelta(days=day)
                )
                all_reports.append(report)
        return all_reports


class UserDataFactory:
    """用户数据工厂"""

    @staticmethod
    def create_users_with_roles(count=5):
        """创建带角色的用户列表"""
        users = []
        roles = ["ADVERTISER", "ANALYST", "MANAGER"]

        for i in range(count):
            user = TestDataFactory.create_user(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                role_code=roles[i % len(roles)]
            )
            users.append(user)

        return users


# 导出工厂函数
__all__ = [
    "TestDataFactory",
    "CampaignDataFactory",
    "ReportDataFactory",
    "UserDataFactory"
]
