"""
完整业务流程 E2E 测试
使用 Playwright 进行端到端测试
"""

import pytest
from playwright.sync_api import Page, expect


class TestCompleteAdvertisingWorkflow:
    """完整广告投放流程 E2E 测试"""

    def test_login_authorize_create_campaign_workflow(self, page: Page, test_config):
        """测试完整工作流：登录 → 授权 → 创建广告计划 → 投放"""
        # 1. 访问登录页面
        page.goto(f"{test_config['base_url']}/login")

        # 2. 输入用户名和密码
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])

        # 3. 点击登录按钮
        page.click('button[type="submit"]')

        # 4. 等待登录成功，跳转到首页
        expect(page).to_have_url(f"{test_config['base_url']}/dashboard")

        # 5. 点击"媒体账户"菜单
        page.click('text=媒体账户')

        # 6. 点击"授权新账户"按钮
        page.click('text=授权新账户')

        # 7. 选择媒体渠道（抖音）
        page.select_option('select[name="channel_code"]', 'DOUYIN')

        # 8. 点击"前往授权"按钮
        page.click('button:has-text("前往授权")')

        # 9. 模拟 OAuth 授权成功（跳转回调）
        # 实际测试中需要处理真实的 OAuth 流程
        page.goto(f"{test_config['base_url']}/accounts/oauth/callback?code=test_code&state=test_state")

        # 10. 验证授权成功，账户列表显示新账户
        expect(page.locator('text=授权成功')).to_be_visible()

        # 11. 点击"广告投放"菜单
        page.click('text=广告投放')

        # 12. 点击"创建广告计划"按钮
        page.click('text=创建广告计划')

        # 13. 填写广告计划信息
        page.fill('input[name="campaign_name"]', 'E2E测试广告计划')
        page.select_option('select[name="account_id"]', '1')
        page.fill('input[name="budget"]', '5000')
        page.select_option('select[name="bid_type"]', 'CPC')
        page.fill('input[name="bid_amount"]', '1.50')
        page.fill('input[name="start_date"]', '2026-03-15')
        page.fill('input[name="end_date"]', '2026-04-15')

        # 14. 点击"下一步"按钮
        page.click('button:has-text("下一步")')

        # 15. 填写广告组信息
        page.fill('input[name="adgroup_name"]', 'E2E测试广告组')
        page.fill('input[name="budget"]', '1000')
        page.select_option('select[name="bid_type"]', 'CPC')
        page.fill('input[name="bid_amount"]', '1.50')

        # 16. 设置定向条件
        page.check('input[value="18-24"]')  # 年龄
        page.check('input[value="MALE"]')  # 性别
        page.fill('input[name="location"]', '北京,上海')

        # 17. 点击"下一步"按钮
        page.click('button:has-text("下一步")')

        # 18. 填写创意信息
        page.fill('input[name="creative_name"]', 'E2E测试创意')
        page.select_option('select[name="creative_type"]', 'IMAGE')
        page.fill('input[name="material_url"]', 'https://example.com/image.jpg')
        page.fill('input[name="title"]', '测试标题')
        page.fill('input[name="description"]', '测试描述')
        page.fill('input[name="landing_url"]', 'https://example.com/landing')
        page.fill('input[name="display_url"]', 'example.com')
        page.fill('input[name="button_text"]', '立即购买')

        # 19. 点击"提交审核"按钮
        page.click('button:has-text("提交审核")')

        # 20. 验证广告计划创建成功
        expect(page.locator('text=创建成功')).to_be_visible()
        expect(page.locator('text=E2E测试广告计划')).to_be_visible()

        # 21. 点击"启动"按钮启动广告计划
        page.click('button:has-text("启动")')

        # 22. 验证广告计划状态变为"投放中"
        expect(page.locator('text=投放中')).to_be_visible()

    def test_login_view_report_export_workflow(self, page: Page, test_config):
        """测试报表查看和导出工作流"""
        # 1. 登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])
        page.click('button[type="submit"]')

        # 2. 点击"数据报表"菜单
        page.click('text=数据报表')

        # 3. 选择报表类型（日报表）
        page.click('text=日报表')

        # 4. 设置日期范围
        page.fill('input[name="start_date"]', '2026-03-01')
        page.fill('input[name="end_date"]', '2026-03-15')

        # 5. 点击"查询"按钮
        page.click('button:has-text("查询")')

        # 6. 等待报表数据加载
        expect(page.locator('table')).to_be_visible()

        # 7. 验证报表数据展示
        expect(page.locator('text=曝光')).to_be_visible()
        expect(page.locator('text=点击')).to_be_visible()
        expect(page.locator('text=消耗')).to_be_visible()
        expect(page.locator('text=转化')).to_be_visible()

        # 8. 点击"导出"按钮
        page.click('button:has-text("导出")')

        # 9. 选择导出格式（Excel）
        page.click('text=Excel')

        # 10. 点击"确认导出"按钮
        page.click('button:has-text("确认导出")')

        # 11. 验证导出成功提示
        expect(page.locator('text=导出成功')).to_be_visible()

    def test_budget_control_workflow(self, page: Page, test_config):
        """测试预算控制和预警工作流"""
        # 1. 登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])
        page.click('button[type="submit"]')

        # 2. 点击"预算管理"菜单
        page.click('text=预算管理')

        # 3. 选择广告计划
        page.click('text=E2E测试广告计划')

        # 4. 点击"设置预算"按钮
        page.click('button:has-text("设置预算")')

        # 5. 填写预算配置
        page.fill('input[name="total_budget"]', '5000')
        page.fill('input[name="daily_budget"]', '100')
        page.fill('input[name="warning_threshold"]', '80')
        page.fill('input[name="stop_threshold"]', '100')
        page.check('input[name="is_auto_stop"]')
        page.check('input[name="is_warning_enabled"]')

        # 6. 点击"保存"按钮
        page.click('button:has-text("保存")')

        # 7. 验证预算配置成功
        expect(page.locator('text=保存成功')).to_be_visible()

        # 8. 模拟消耗达到预警阈值（通过 API 或直接修改数据库）
        # 这里假设系统会自动触发预警检查

        # 9. 查看预警通知
        page.click('text=通知')
        expect(page.locator('text=预算预警')).to_be_visible()

        # 10. 点击预警通知查看详情
        page.click('text=预算预警')

        # 11. 验证预警详情页面
        expect(page.locator('text=日预算即将耗尽')).to_be_visible()


class TestPermissionAndRoleWorkflow:
    """权限和角色工作流 E2E 测试"""

    def test_admin_workflow(self, page: Page, test_config):
        """测试管理员工作流"""
        # 1. 使用管理员账号登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['admin_user']['username'])
        page.fill('input[name="password"]', test_config['admin_user']['password'])
        page.click('button[type="submit"]')

        # 2. 点击"系统管理"菜单
        page.click('text=系统管理')

        # 3. 点击"用户管理"
        page.click('text=用户管理')

        # 4. 点击"新建用户"按钮
        page.click('button:has-text("新建用户")')

        # 5. 填写用户信息
        page.fill('input[name="username"]', 'testuser001')
        page.fill('input[name="email"]', 'testuser001@example.com')
        page.fill('input[name="password"]', 'password123')
        page.fill('input[name="full_name"]', '测试用户001')
        page.select_option('select[name="role_code"]', 'ADVERTISER')
        page.check('input[name="is_active"]')

        # 6. 点击"保存"按钮
        page.click('button:has-text("保存")')

        # 7. 验证用户创建成功
        expect(page.locator('text=创建成功')).to_be_visible()

        # 8. 查看用户列表，验证新用户已添加
        expect(page.locator('text=testuser001')).to_be_visible()

    def test_advertiser_workflow(self, page: Page, test_config):
        """测试广告主工作流"""
        # 1. 使用广告主账号登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])
        page.click('button[type="submit"]')

        # 2. 验证只能访问授权的资源
        # 可以创建广告计划
        page.click('text=广告投放')
        expect(page.locator('text=创建广告计划')).to_be_visible()

        # 可以查看自己的报表
        page.click('text=数据报表')
        expect(page.locator('text=查询')).to_be_visible()

        # 3. 验证不能访问管理员资源
        page.goto(f"{test_config['base_url']}/admin/users")

        # 应该跳转到无权限页面
        expect(page.locator('text=无权限')).to_be_visible()


class TestDataSyncWorkflow:
    """数据同步工作流 E2E 测试"""

    def test_real_time_data_sync(self, page: Page, test_config):
        """测试实时数据同步"""
        # 1. 登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])
        page.click('button[type="submit"]')

        # 2. 进入实时数据页面
        page.click('text=实时数据')

        # 3. 选择账户
        page.select_option('select[name="account_id"]', '1')

        # 4. 点击"刷新"按钮获取最新数据
        page.click('button:has-text("刷新")')

        # 5. 验证数据已更新
        expect(page.locator('text=更新时间')).to_be_visible()

        # 6. 查看实时指标
        expect(page.locator('text=曝光')).to_be_visible()
        expect(page.locator('text=点击')).to_be_visible()
        expect(page.locator('text=消耗')).to_be_visible()

    def test_historical_data_sync(self, page: Page, test_config):
        """测试历史数据同步"""
        # 1. 登录
        page.goto(f"{test_config['base_url']}/login")
        page.fill('input[name="username"]', test_config['test_user']['username'])
        page.fill('input[name="password"]', test_config['test_user']['password'])
        page.click('button[type="submit"]')

        # 2. 进入媒体账户管理页面
        page.click('text=媒体账户')

        # 3. 点击账户操作菜单
        page.click('button[aria-label="操作"]')

        # 4. 点击"同步数据"按钮
        page.click('text=同步数据')

        # 5. 设置同步日期范围
        page.fill('input[name="start_date"]', '2026-03-01')
        page.fill('input[name="end_date"]', '2026-03-15')

        # 6. 点击"开始同步"按钮
        page.click('button:has-text("开始同步")')

        # 7. 验证同步任务已创建
        expect(page.locator('text=同步任务已创建')).to_be_visible()

        # 8. 等待同步完成
        expect(page.locator('text=同步完成')).to_be_visible(timeout=60000)  # 60秒超时


# E2E 测试配置 fixture
@pytest.fixture
def test_config():
    """E2E 测试配置"""
    return {
        'base_url': 'http://localhost:8000',
        'test_user': {
            'username': 'testuser',
            'password': 'testpass123'
        },
        'admin_user': {
            'username': 'admin',
            'password': 'admin123'
        }
    }
