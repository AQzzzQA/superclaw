# DSP平台测试框架

完整的测试框架，用于DSP国内全媒体广告平台的测试。

## 📁 目录结构

```
tests/
├── unit/                      # 单元测试
│   ├── test_auth.py          # 用户权限模块测试
│   ├── test_account.py       # 媒体账户模块测试
│   ├── test_campaign.py      # 广告投放模块测试
│   ├── test_report.py        # 数据报表模块测试
│   └── test_budget.py        # 预算风控模块测试
├── integration/              # 集成测试
│   ├── test_auth_flow.py     # 媒体账户授权流程测试
│   ├── test_campaign_crud.py # 广告投放CRUD测试
│   ├── test_data_callback.py # 实时数据回传接口测试
│   ├── test_budget_control.py# 预算控制和预警逻辑测试
│   ├── test_rbac.py          # 权限系统(RBAC)测试
│   └── test_report_export.py # 报表生成和导出测试
├── e2e/                      # E2E测试
│   ├── test_complete_workflow.py # 完整业务流程测试
│   └── conftest.py          # E2E测试配置
├── fixtures/                 # 测试工具
│   └── test_data_factory.py # 测试数据工厂
├── conftest.py              # 全局fixtures
├── pytest.ini               # pytest配置
├── requirements-test.txt    # 测试依赖
├── README.md                # 本文件
├── TEST_CHECKLIST.md        # 测试用例清单
└── MOCK_DATA.md             # Mock数据说明
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements-test.txt
```

### 安装 Playwright 浏览器

```bash
playwright install
```

### 初始化测试数据库

```bash
# 确保有测试数据库配置
export TEST_DB_URL="sqlite:///./test.db"

# 运行数据库迁移
python -m alembic upgrade head
```

## 📝 运行测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行单元测试

```bash
pytest tests/unit -v
```

### 运行集成测试

```bash
pytest tests/integration -v
```

### 运行E2E测试

```bash
pytest tests/e2e -v --browser=chromium
```

### 运行特定测试文件

```bash
pytest tests/unit/test_auth.py -v
```

### 运行特定测试用例

```bash
pytest tests/unit/test_auth.py::TestPasswordSecurity::test_password_hashing -v
```

### 运行带标记的测试

```bash
# 只运行单元测试
pytest tests/ -v -m unit

# 运行除慢速测试外的所有测试
pytest tests/ -v -m "not slow"

# 运行认证相关测试
pytest tests/ -v -m auth
```

## 📊 测试覆盖率

### 生成覆盖率报告

```bash
# 生成HTML覆盖率报告
pytest --cov=app --cov-report=html tests/

# 生成终端覆盖率报告
pytest --cov=app --cov-report=term-missing tests/

# 生成XML覆盖率报告（CI/CD使用）
pytest --cov=app --cov-report=xml tests/
```

### 查看覆盖率报告

```bash
# 在浏览器中打开HTML报告
open htmlcov/index.html

# 或使用浏览器工具
python -m http.server 8000
# 访问 http://localhost:8000/htmlcov/index.html
```

### 覆盖率目标

- **总体覆盖率**: > 80%
- **核心业务逻辑**: > 90%
- **API接口层**: > 85%
- **工具函数**: > 90%

## 🧪 测试类型

### 单元测试

测试单个函数或类的功能，使用 mock 隔离外部依赖。

**特点**:
- 快速执行
- 隔离性好
- 覆盖率高

**示例**:

```python
def test_password_hashing():
    password = "test_password_123"
    hashed = get_password_hash(password)

    assert hashed != password
    assert hashed.startswith("$2b$")
```

### 集成测试

测试多个模块之间的交互，使用真实数据库但 mock 外部API。

**特点**:
- 测试业务流程
- 使用真实数据库
- Mock外部依赖

**示例**:

```python
def test_create_campaign_success(client, auth_headers, test_media_account):
    response = client.post(
        "/api/v1/campaigns",
        json={
            "campaign_name": "测试广告计划",
            "account_id": test_media_account.id,
            "budget": 5000.00
        },
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_201_CREATED
```

### E2E测试

使用 Playwright 测试完整的用户交互流程。

**特点**:
- 真实浏览器
- 测试UI交互
- 完整业务流程

**示例**:

```python
def test_login_workflow(page: Page, test_config):
    page.goto(f"{test_config['base_url']}/login")
    page.fill('input[name="username"]', test_config['test_user']['username'])
    page.fill('input[name="password"]', test_config['test_user']['password'])
    page.click('button[type="submit"]')

    expect(page).to_have_url(f"{test_config['base_url']}/dashboard")
```

## 🎯 测试标记

使用 pytest 标记对测试进行分类：

```bash
# 测试类型
pytest -m unit        # 单元测试
pytest -m integration # 集成测试
pytest -m e2e         # E2E测试

# 测试速度
pytest -m fast        # 快速测试
pytest -m slow        # 慢速测试

# 功能模块
pytest -m auth        # 认证相关
pytest -m campaign    # 广告相关
pytest -m report      # 报表相关
pytest -m budget      # 预算相关

# 测试场景
pytest -m happy_path  # 正常场景
pytest -m error_case  # 异常场景
pytest -m edge_case   # 边界场景
```

## 📋 测试用例统计

当前测试框架包含：

- **单元测试**: 40个
- **集成测试**: 30个
- **E2E测试**: 5个
- **总计**: 75个测试用例

详见 [TEST_CHECKLIST.md](TEST_CHECKLIST.md)

## 🛠️ Fixtures

测试框架提供了丰富的 fixtures 来简化测试编写：

### 数据库 Fixtures

```python
@pytest.fixture
def db_session():
    """创建数据库会话"""
    yield session

@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    user = User(username="testuser", ...)
    db_session.add(user)
    db_session.commit()
    return user
```

### HTTP 客户端 Fixtures

```python
@pytest.fixture
def client():
    """创建FastAPI测试客户端"""
    yield TestClient(app)

@pytest.fixture
def auth_headers(client, test_user):
    """获取认证头"""
    response = client.post("/api/v1/auth/login", json={...})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### 业务数据 Fixtures

```python
@pytest.fixture
def test_media_account():
    """创建测试媒体账户"""
    return MediaAccount(...)

@pytest.fixture
def test_campaign():
    """创建测试广告计划"""
    return Campaign(...)
```

详见 [conftest.py](conftest.py)

## 🧪 Mock 数据

测试框架使用 `test_data_factory.py` 生成测试数据：

```python
from tests.fixtures.test_data_factory import TestDataFactory

# 创建用户
user = TestDataFactory.create_user()

# 创建广告计划
campaign = TestDataFactory.create_campaign()

# 创建报表数据
report = TestDataFactory.create_report_daily()
```

详见 [fixtures/test_data_factory.py](fixtures/test_data_factory.py) 和 [MOCK_DATA.md](MOCK_DATA.md)

## 📊 测试报告

### JUnit XML 报告

```bash
pytest --junitxml=junit-report.xml tests/
```

### Allure 报告

```bash
pytest --alluredir=allure-results tests/
allure generate allure-results -o allure-report
allure open allure-report
```

### HTML 报告

```bash
pytest --html=report.html --self-contained-html tests/
```

## 🔄 CI/CD 集成

### GitLab CI 示例

```yaml
test:
  script:
    - pip install -r requirements-test.txt
    - pytest tests/unit -v --cov=app --cov-report=xml
    - pytest tests/integration -v
  coverage: '/TOTAL\s+\d+\s+\d+/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### GitHub Actions 示例

```yaml
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest tests/ -v --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## 🐛 调试测试

### 运行单个测试

```bash
pytest tests/unit/test_auth.py::TestPasswordSecurity::test_password_hashing -v
```

### 进入调试模式

```bash
pytest --pdb tests/
```

### 只运行失败的测试

```bash
pytest --lf tests/
```

### 先运行失败的测试，再运行其他测试

```bash
pytest --ff tests/
```

### 显示详细输出

```bash
pytest -vv tests/
```

### 显示打印输出

```bash
pytest -s tests/
```

## 📚 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [FastAPI 测试文档](https://fastapi.tiangolo.com/tutorial/testing/)
- [Playwright 文档](https://playwright.dev/python/)
- [pytest-cov 文档](https://pytest-cov.readthedocs.io/)

## 🤝 贡献指南

### 添加新的测试用例

1. 在对应的测试文件中添加测试函数
2. 遵循 AAA 模式（Arrange-Act-Assert）
3. 添加适当的文档字符串
4. 运行测试确保通过
5. 更新测试用例清单

### 添加新的测试模块

1. 创建新的测试文件
2. 添加必要的 fixtures
3. 编写测试用例
4. 运行测试确保通过
5. 更新文档

## 📞 支持

如有问题，请联系测试工程师智能体。

---

**版本**: V1.0
**最后更新**: 2026-03-15
**维护者**: 测试工程师智能体
