# DSP广告平台 - API端点清单

## 目录
- [认证授权](#认证授权)
- [用户管理](#用户管理)
- [广告计划](#广告计划)
- [创意素材](#创意素材)
- [受众定向](#受众定向)
- [投放策略](#投放策略)
- [数据回传](#数据回传)
- [报表分析](#报表分析)
- [计费管理](#计费管理)
- [系统通知](#系统通知)
- [媒体平台](#媒体平台)
- [审计日志](#审计日志)
- [实时推送](#实时推送)

---

## 认证授权

### POST /api/v1/auth/register
**描述**: 用户注册
**请求**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "company_name": "string"
}
```
**响应**: 201 Created

### POST /api/v1/auth/login
**描述**: 用户登录
**请求**:
```json
{
  "username": "string",
  "password": "string"
}
```
**响应**:
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "expires_in": 3600
}
```

### POST /api/v1/auth/logout
**描述**: 用户登出
**认证**: JWT
**响应**: 200 OK

### POST /api/v1/auth/refresh
**描述**: 刷新访问令牌
**请求**:
```json
{
  "refresh_token": "string"
}
```
**响应**: 200 OK

### POST /api/v1/auth/change-password
**描述**: 修改密码
**认证**: JWT
**请求**:
```json
{
  "old_password": "string",
  "new_password": "string"
}
```
**响应**: 200 OK

### POST /api/v1/auth/forgot-password
**描述**: 忘记密码
**请求**:
```json
{
  "email": "string"
}
```
**响应**: 200 OK

### POST /api/v1/auth/reset-password
**描述**: 重置密码
**请求**:
```json
{
  "token": "string",
  "new_password": "string"
}
```
**响应**: 200 OK

---

## 用户管理

### GET /api/v1/users
**描述**: 获取用户列表
**认证**: JWT
**权限**: admin
**查询参数**: page, page_size, search, role
**响应**: 200 OK

### GET /api/v1/users/{user_id}
**描述**: 获取用户详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/users/{user_id}
**描述**: 更新用户信息
**认证**: JWT
**请求**:
```json
{
  "username": "string",
  "email": "string",
  "phone": "string"
}
```
**响应**: 200 OK

### DELETE /api/v1/users/{user_id}
**描述**: 删除用户
**认证**: JWT
**权限**: admin
**响应**: 204 No Content

### PUT /api/v1/users/{user_id}/role
**描述**: 更新用户角色
**认证**: JWT
**权限**: admin
**请求**:
```json
{
  "role": "admin|advertiser|analyst"
}
```
**响应**: 200 OK

### GET /api/v1/users/me
**描述**: 获取当前用户信息
**认证**: JWT
**响应**: 200 OK

---

## 广告计划

### GET /api/v1/campaigns
**描述**: 获取广告计划列表
**认证**: JWT
**查询参数**: page, page_size, status, platform, date_range
**响应**: 200 OK

### POST /api/v1/campaigns
**描述**: 创建广告计划
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "platform": "douyin|kuaishou|wechat|baidu",
  "budget": 10000,
  "start_date": "2026-03-15",
  "end_date": "2026-04-15",
  "status": "active|paused|completed"
}
```
**响应**: 201 Created

### GET /api/v1/campaigns/{campaign_id}
**描述**: 获取广告计划详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/campaigns/{campaign_id}
**描述**: 更新广告计划
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "budget": 15000,
  "status": "active"
}
```
**响应**: 200 OK

### DELETE /api/v1/campaigns/{campaign_id}
**描述**: 删除广告计划
**认证**: JWT
**响应**: 204 No Content

### POST /api/v1/campaigns/{campaign_id}/pause
**描述**: 暂停广告计划
**认证**: JWT
**响应**: 200 OK

### POST /api/v1/campaigns/{campaign_id}/resume
**描述**: 恢复广告计划
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/campaigns/{campaign_id}/performance
**描述**: 获取广告计划性能数据
**认证**: JWT
**查询参数**: date_range, granularity
**响应**: 200 OK

---

## 创意素材

### GET /api/v1/creatives
**描述**: 获取创意素材列表
**认证**: JWT
**查询参数**: page, page_size, type, status
**响应**: 200 OK

### POST /api/v1/creatives
**描述**: 上传创意素材
**认证**: JWT
**请求**: multipart/form-data
- file: 媒体文件
- name: 素材名称
- type: 素材类型
- campaign_id: 关联广告计划
**响应**: 201 Created

### GET /api/v1/creatives/{creative_id}
**描述**: 获取创意素材详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/creatives/{creative_id}
**描述**: 更新创意素材
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "status": "active|inactive"
}
```
**响应**: 200 OK

### DELETE /api/v1/creatives/{creative_id}
**描述**: 删除创意素材
**认证**: JWT
**响应**: 204 No Content

### POST /api/v1/creatives/{creative_id}/review
**描述**: 提交审核
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/creatives/{creative_id}/review-status
**描述**: 获取审核状态
**认证**: JWT
**响应**: 200 OK

---

## 受众定向

### GET /api/v1/audiences
**描述**: 获取受众列表
**认证**: JWT
**查询参数**: page, page_size, type
**响应**: 200 OK

### POST /api/v1/audiences
**描述**: 创建受众
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "type": "custom|lookalike|behavioral",
  "targeting": {
    "age": {"min": 18, "max": 35},
    "gender": "male|female|all",
    "interests": ["technology", "sports"],
    "location": ["Beijing", "Shanghai"]
  }
}
```
**响应**: 201 Created

### GET /api/v1/audiences/{audience_id}
**描述**: 获取受众详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/audiences/{audience_id}
**描述**: 更新受众
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "targeting": {...}
}
```
**响应**: 200 OK

### DELETE /api/v1/audiences/{audience_id}
**描述**: 删除受众
**认证**: JWT
**响应**: 204 No Content

### GET /api/v1/audiences/{audience_id}/estimate
**描述**: 获取受众规模估算
**认证**: JWT
**响应**: 200 OK

---

## 投放策略

### GET /api/v1/strategies
**描述**: 获取投放策略列表
**认证**: JWT
**查询参数**: page, page_size, type
**响应**: 200 OK

### POST /api/v1/strategies
**描述**: 创建投放策略
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "campaign_id": "string",
  "type": "manual|auto|smart",
  "bidding_strategy": "cpc|cpm|cpa",
  "budget_allocation": {...}
}
```
**响应**: 201 Created

### GET /api/v1/strategies/{strategy_id}
**描述**: 获取策略详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/strategies/{strategy_id}
**描述**: 更新策略
**认证**: JWT
**请求**:
```json
{
  "bidding_strategy": "cpa",
  "target_cpa": 50
}
```
**响应**: 200 OK

### DELETE /api/v1/strategies/{strategy_id}
**描述**: 删除策略
**认证**: JWT
**响应**: 204 No Content

### POST /api/v1/strategies/{strategy_id}/optimize
**描述**: 执行智能优化
**认证**: JWT
**响应**: 200 OK

---

## 数据回传

### POST /api/v1/data/impression
**描述**: 曝光数据回传
**认证**: API Key
**请求**:
```json
{
  "campaign_id": "string",
  "creative_id": "string",
  "impression_id": "string",
  "user_id": "string",
  "timestamp": 1678867200000,
  "device": "mobile|desktop",
  "platform": "douyin"
}
```
**响应**: 200 OK

### POST /api/v1/data/click
**描述**: 点击数据回传
**认证**: API Key
**请求**:
```json
{
  "campaign_id": "string",
  "impression_id": "string",
  "click_id": "string",
  "user_id": "string",
  "timestamp": 1678867201000,
  "click_url": "string"
}
```
**响应**: 200 OK

### POST /api/v1/data/conversion
**描述**: 转化数据回传
**认证**: API Key
**请求**:
```json
{
  "campaign_id": "string",
  "click_id": "string",
  "conversion_id": "string",
  "conversion_type": "purchase|signup|download",
  "value": 100,
  "timestamp": 1678867205000
}
```
**响应**: 200 OK

### POST /api/v1/data/batch
**描述**: 批量数据回传
**认证**: API Key
**请求**:
```json
{
  "data": [
    {
      "type": "impression|click|conversion",
      "payload": {...}
    }
  ]
}
```
**响应**: 200 OK

### GET /api/v1/data/status/{batch_id}
**描述**: 查询批量数据处理状态
**认证**: API Key
**响应**: 200 OK

---

## 报表分析

### GET /api/v1/reports/campaign
**描述**: 广告计划报表
**认证**: JWT
**查询参数**: campaign_id, start_date, end_date, granularity
**响应**: 200 OK

### GET /api/v1/reports/creative
**描述**: 创意素材报表
**认证**: JWT
**查询参数**: creative_id, start_date, end_date
**响应**: 200 OK

### GET /api/v1/reports/audience
**描述**: 受众分析报表
**认证**: JWT
**查询参数**: audience_id, start_date, end_date
**响应**: 200 OK

### GET /api/v1/reports/performance
**描述**: 综合性能报表
**认证**: JWT
**查询参数**: start_date, end_date, group_by
**响应**: 200 OK

### POST /api/v1/reports/custom
**描述**: 创建自定义报表
**认证**: JWT
**请求**:
```json
{
  "name": "string",
  "metrics": ["impressions", "clicks", "conversions"],
  "dimensions": ["date", "platform"],
  "filters": {...},
  "schedule": {
    "frequency": "daily|weekly|monthly",
    "time": "09:00"
  }
}
```
**响应**: 201 Created

### GET /api/v1/reports/custom/{report_id}
**描述**: 获取自定义报表
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/reports/custom/{report_id}/data
**描述**: 获取自定义报表数据
**认证**: JWT
**查询参数**: start_date, end_date
**响应**: 200 OK

### DELETE /api/v1/reports/custom/{report_id}
**描述**: 删除自定义报表
**认证**: JWT
**响应**: 204 No Content

### POST /api/v1/reports/{report_id}/export
**描述**: 导出报表
**认证**: JWT
**请求**:
```json
{
  "format": "excel|pdf|csv",
  "start_date": "2026-03-01",
  "end_date": "2026-03-15"
}
```
**响应**: 200 OK (文件下载)

### GET /api/v1/reports/{report_id}/export-status/{task_id}
**描述**: 查询导出任务状态
**认证**: JWT
**响应**: 200 OK

---

## 计费管理

### GET /api/v1/billing/balance
**描述**: 获取账户余额
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/billing/transactions
**描述**: 获取交易记录
**认证**: JWT
**查询参数**: page, page_size, type, date_range
**响应**: 200 OK

### POST /api/v1/billing/recharge
**描述**: 账户充值
**认证**: JWT
**请求**:
```json
{
  "amount": 10000,
  "payment_method": "alipay|wechat|bank_transfer"
}
```
**响应**: 201 Created

### GET /api/v1/billing/recharge/{order_id}
**描述**: 查询充值订单
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/billing/invoices
**描述**: 获取发票列表
**认证**: JWT
**查询参数**: page, page_size, status
**响应**: 200 OK

### GET /api/v1/billing/invoices/{invoice_id}
**描述**: 获取发票详情
**认证**: JWT
**响应**: 200 OK

### POST /api/v1/billing/invoices/{invoice_id}/apply
**描述**: 申请开票
**认证**: JWT
**请求**:
```json
{
  "title": "string",
  "tax_number": "string",
  "email": "string",
  "address": "string"
}
```
**响应**: 201 Created

### GET /api/v1/billing/consumption
**描述**: 获取消费统计
**认证**: JWT
**查询参数**: start_date, end_date, granularity
**响应**: 200 OK

---

## 系统通知

### GET /api/v1/notifications
**描述**: 获取通知列表
**认证**: JWT
**查询参数**: page, page_size, type, is_read
**响应**: 200 OK

### GET /api/v1/notifications/{notification_id}
**描述**: 获取通知详情
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/notifications/{notification_id}/read
**描述**: 标记为已读
**认证**: JWT
**响应**: 200 OK

### PUT /api/v1/notifications/read-all
**描述**: 全部标记为已读
**认证**: JWT
**响应**: 200 OK

### DELETE /api/v1/notifications/{notification_id}
**描述**: 删除通知
**认证**: JWT
**响应**: 204 No Content

### POST /api/v1/notifications/settings
**描述**: 更新通知设置
**认证**: JWT
**请求**:
```json
{
  "email_enabled": true,
  "sms_enabled": false,
  "push_enabled": true,
  "notification_types": ["campaign_alert", "budget_warning"]
}
```
**响应**: 200 OK

---

## 媒体平台

### GET /api/v1/platforms
**描述**: 获取媒体平台列表
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/platforms/{platform_id}
**描述**: 获取平台详情
**认证**: JWT
**响应**: 200 OK

### POST /api/v1/platforms/{platform_id}/authorize
**描述**: 媒体平台授权
**认证**: JWT
**请求**:
```json
{
  "auth_code": "string",
  "redirect_uri": "string"
}
```
**响应**: 200 OK

### GET /api/v1/platforms/{platform_id}/accounts
**描述**: 获取平台账户列表
**认证**: JWT
**响应**: 200 OK

### POST /api/v1/platforms/{platform_id}/accounts/sync
**描述**: 同步平台账户数据
**认证**: JWT
**响应**: 200 OK

### GET /api/v1/platforms/{platform_id}/status
**描述**: 获取平台连接状态
**认证**: JWT
**响应**: 200 OK

---

## 审计日志

### GET /api/v1/audit-logs
**描述**: 获取审计日志
**认证**: JWT
**权限**: admin
**查询参数**: page, page_size, user_id, action, date_range
**响应**: 200 OK

### GET /api/v1/audit-logs/{log_id}
**描述**: 获取日志详情
**认证**: JWT
**权限**: admin
**响应**: 200 OK

---

## 实时推送

### WebSocket /ws/realtime
**描述**: 实时数据推送连接
**认证**: JWT Token in query string
**事件**:
- `campaign_update`: 广告计划更新
- `data_update`: 数据更新
- `notification`: 新通知
- `alert`: 告警信息

**连接示例**:
```javascript
const ws = new WebSocket('ws://api.example.com/ws/realtime?token=xxx');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data.payload);
};
```

---

## 系统管理

### GET /api/v1/system/health
**描述**: 健康检查
**认证**: None
**响应**: 200 OK

### GET /api/v1/system/info
**描述**: 系统信息
**认证**: JWT
**权限**: admin
**响应**: 200 OK

### GET /api/v1/system/metrics
**描述**: 系统指标
**认证**: JWT
**权限**: admin
**响应**: 200 OK

---

## API端点统计

| 模块 | 端点数量 | 说明 |
|-----|---------|------|
| 认证授权 | 7 | 注册、登录、令牌管理 |
| 用户管理 | 6 | 用户CRUD、角色管理 |
| 广告计划 | 8 | 计划管理、性能查询 |
| 创意素材 | 6 | 素材上传、审核 |
| 受众定向 | 5 | 受众创建、规模估算 |
| 投放策略 | 5 | 策略管理、智能优化 |
| 数据回传 | 5 | 实时数据、批量上传 |
| 报表分析 | 9 | 标准报表、自定义报表、导出 |
| 计费管理 | 8 | 余额、充值、发票 |
| 系统通知 | 6 | 通知管理、设置 |
| 媒体平台 | 6 | 平台授权、数据同步 |
| 审计日志 | 2 | 日志查询 |
| 实时推送 | 1 | WebSocket连接 |
| 系统管理 | 3 | 健康、指标 |

**总计**: 77个API端点

---

## 统一响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": {...},
  "timestamp": 1678867200000
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "Bad Request",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ],
  "timestamp": 1678867200000
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  },
  "timestamp": 1678867200000
}
```

---

## 错误码定义

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 无内容 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器错误 |
| 503 | 服务不可用 |

---

**文档版本**: 1.0
**最后更新**: 2026-03-15
**维护者**: Echo-2
