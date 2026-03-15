# 测试 Mock 数据说明

## 概述

本文档说明了在测试中使用的 Mock 数据和外部 API 模拟策略。

## 外部 API Mock

### 1. 媒体平台 API Mock

#### 抖音 API

```python
{
    "account_info": {
        "account_id": "test_douyin_001",
        "account_name": "抖音测试账户",
        "balance": 5000.00,
        "status": "ACTIVE"
    },
    "campaign_list": [...],
    "report_data": {...}
}
```

#### 快手 API

```python
{
    "account_info": {
        "account_id": "test_kuaishou_001",
        "account_name": "快手测试账户",
        "balance": 3000.00,
        "status": "ACTIVE"
    }
}
```

#### 微信广告 API

```python
{
    "account_info": {
        "account_id": "test_wechat_001",
        "account_name": "微信测试账户",
        "balance": 8000.00,
        "status": "ACTIVE"
    }
}
```

### 2. 第三方服务 Mock

#### 邮件服务

```python
{
    "success": True,
    "message": "邮件发送成功"
}
```

#### 企业微信

```python
{
    "errcode": 0,
    "errmsg": "ok"
}
```

#### 钉钉

```python
{
    "errcode": 0,
    "errmsg": "ok"
}
```

## 测试数据生成

### 用户数据

```python
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "测试用户",
    "role": "ADVERTISER"
}
```

### 媒体账户数据

```python
{
    "account_id": "test_account_001",
    "account_name": "测试广告账户",
    "channel_code": "DOUYIN",
    "balance": 10000.00,
    "status": "ACTIVE",
    "is_authorized": True
}
```

### 广告计划数据

```python
{
    "campaign_id": "test_campaign_001",
    "campaign_name": "测试广告计划",
    "account_id": 1,
    "budget": 5000.00,
    "bid_type": "CPC",
    "bid_amount": 1.50,
    "status": "RUNNING"
}
```

### 报表数据

```python
{
    "impression": 10000,
    "click": 500,
    "ctr": 5.0,
    "cost": 150.00,
    "cpc": 0.30,
    "conversion": 20,
    "cvr": 4.0,
    "cpa": 7.50,
    "roi": 100.0
}
```

## Mock 策略

### 单元测试

- 使用 `unittest.mock` Mock 所有外部依赖
- 使用 `responses` 库 Mock HTTP 请求
- 使用 `faker` 生成测试数据

### 集成测试

- Mock 媒体平台 API（不真实调用）
- Mock 第三方服务（邮件、企业微信、钉钉）
- 使用真实数据库（独立的测试数据库）

### E2E 测试

- 使用真实浏览器（Playwright）
- 使用真实前端界面
- Mock 外部 API（避免产生真实广告费用）

## Mock 数据管理

### Mock 数据文件位置

```
tests/
├── fixtures/
│   ├── mock_api_data.py    # API Mock 数据
│   └── test_data_factory.py  # 测试数据工厂
└── mock_data/              # Mock 数据文件
    ├── douyin_api.json
    ├── kuaishou_api.json
    └── wechat_api.json
```

### 动态 Mock 数据

对于需要动态变化的 Mock 数据（如时间戳、随机数），使用 `faker` 库生成：

```python
from faker import Faker

faker = Faker("zh_CN")

# 生成随机用户名
username = faker.user_name()

# 生成随机日期
date = faker.date_between(start_date="-30d", end_date="today")

# 生成随机金额
amount = Decimal(str(faker.random_number(4)))
```

## 常见测试场景 Mock

### 场景 1: OAuth 授权成功

```python
mock_exchange.return_value = {
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "expires_in": 2592000
}
```

### 场景 2: 令牌刷新成功

```python
mock_refresh.return_value = {
    "access_token": "new_access_token",
    "refresh_token": "new_refresh_token",
    "expires_in": 2592000
}
```

### 场景 3: 数据同步成功

```python
mock_fetch.return_value = {
    "impression": 10000,
    "click": 500,
    "cost": 150.00,
    "conversion": 20
}
```

### 场景 4: 预算预警触发

```python
mock_spend.return_value = Decimal("85.00")  # 达到预警阈值 80%
```

### 场景 5: 预算超支

```python
mock_spend.return_value = Decimal("105.00")  # 超过预算 100%
```

## Mock 数据验证

### 验证 Mock 数据正确性

1. **数据完整性**: 确保所有必填字段都有值
2. **数据格式**: 确保数据类型和格式正确
3. **业务规则**: 确保数据符合业务逻辑
4. **边界值**: 测试边界情况和异常数据

### Mock 数据更新

当真实 API 发生变化时：

1. 更新 Mock 数据结构
2. 更新相关测试用例
3. 运行测试验证
4. 更新文档

## 最佳实践

1. **集中管理**: 将 Mock 数据集中管理，避免重复
2. **版本控制**: Mock 数据纳入版本控制
3. **定期更新**: 定期与真实 API 对比，更新 Mock 数据
4. **文档维护**: 及时更新 Mock 数据文档
5. **自动化**: 尽可能自动化 Mock 数据生成

## 注意事项

1. **真实性**: Mock 数据应尽可能接近真实数据
2. **隔离性**: 测试之间不应相互影响
3. **性能**: Mock 响应应快速，不应影响测试速度
4. **维护成本**: 保持 Mock 数据的可维护性
5. **安全性**: Mock 数据中不应包含敏感信息
