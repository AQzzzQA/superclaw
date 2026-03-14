# Ad Platform 客户代理对接指南

**文档版本**: v2.0
**更新时间**: 2026-03-01
**适用对象**: 广告代理商、第三方开发者

---

## 📖 文档概述

本文档详细介绍如何对接 Ad Platform 广告平台，包括 API 接入、账户授权、广告投放、数据回传等完整流程。

---

## 🎯 快速开始

### 1. 前置要求
- 已注册的 Ad Platform 账号
- 巨量引擎广告主账号
- 开发者密钥（从平台获取）

### 2. 获取 API 凭证
访问 [Ad Platform 控制台](https://platform.example.com)，在"开发者中心"获取：
- `client_id`: 客户端 ID
- `client_secret`: 客户端密钥
- `api_key`: API 密钥

### 3. 测试连接
```bash
curl -X GET "https://api.example.com/api/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🔐 认证授权

### OAuth2 授权流程

#### 1. 获取授权 URL
```http
GET /api/v1/oauth/authorize
```

**请求参数**:
- `redirect_uri`: 回调地址
- `scope`: 授权范围
- `state`: 防CSRF参数

**响应**:
```json
{
  "code": 200",
  "message": "success",
  "data": {
    "authorize_url": "https://ad.oceanengine.com/open_api/v2/oauth/authorize?client_id=..."
  }
}
```

#### 2. 用户授权
用户访问授权 URL，登录并授权。

#### 3. 获取 Access Token
```http
POST /api/v1/oauth/callback
```

**请求体**:
```json
{
  "code": "AUTHORIZATION_CODE",
  "redirect_uri": "REDIRECT_URI",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "ACCESS_TOKEN",
    "refresh_token": "REFRESH_TOKEN",
    "expires_in": 86400
  }
}
```

#### 4. 刷新 Token
```http
POST /api/v1/oauth/refresh
```

**请求体**:
```json
{
  "refresh_token": "REFRESH_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

---

## 📊 API 接口

### 通用说明

所有 API 请求需要包含认证头：
```http
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json
```

### 基础 URL
- **生产环境**: `https://api.example.com`
- **测试环境**: `https://api-test.example.com`

### 通用响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    // 具体数据
  },
  "timestamp": 1772371234567
}
```

---

## 🎯 核心功能 API

### 1. 账户管理

#### 1.1 创建广告账户
```http
POST /api/v1/account/create
```

**请求体**:
```json
{
  "advertiserId": "100000001",
  "advertiserName": "测试账户",
  "advertiserType": "直客账户",
  "balance": 5000
}
```

**响应**:
```json
{
  "code": 200,
  "message": "账户创建成功",
  "data": {
    "accountId": 1,
    "advertiserId": "100000001"
  }
}
```

#### 1.2 获取账户列表
```http
GET /api/v1/account/list
```

#### 1.3 更新账户
```http
POST /api/v1/account/{id}/update
```

#### 1.4 删除账户
```http
POST /api/v1/account/{id}/delete
```

### 2. 广告计划管理

#### 2.1 创建广告计划
```http
POST /api/v1/campaign/create
```

**请求体**:
```json
{
  "campaignId": 100001,
  "campaignName": "夏季促销活动",
  "objectiveType": "产品推广",
  "budget": 1000,
  "startDate": "2026-03-01",
  "endDate": "2026-03-31"
}
```

#### 2.2 获取计划列表
```http
GET /api/v1/campaign/list?advertiserId=100000001
```

#### 2.3 更新计划状态
```http
POST /api/v1/campaign/update-status
```

**请求体**:
```json
{
  "campaignId": 100001,
  "status": "enable"
}
```

#### 2.4 批量更新状态
```http
POST /api/v1/campaign/batch-update-status
```

**请求体**:
```json
{
  "ids": [100001, 100002, 100003],
  "status": "enable"
}
```

### 3. 广告组管理

#### 3.1 创建广告组
```http
POST /api/v1/adgroup/create
```

#### 3.2 获取广告组列表
```http
GET /api/v1/adgroup/list?campaignId=100001
```

### 4. 创意管理

#### 4.1 创建创意
```http
POST /api/v1/creative/create
```

**请求体**:
```json
{
  "creativeId": 200001,
  "creativeName": "夏日促销图片",
  "creativeType": "图片",
  "creativeMaterial": {
    "imageId": "IMAGE_ID",
    "imageUrl": "https://example.com/image.jpg",
    "width": 1080,
    "height": 1080
  }
}
```

#### 4.2 获取创意列表
```http
GET /api/v1/creative/list?adgroupId=100001
```

### 5. 数据报表

#### 5.1 获取日报表
```http
POST /api/v1/report/daily
```

**请求体**:
```json
{
  "startDate": "2026-03-01",
  "endDate": "2026-03-07",
  "advertiserId": "100000001",
  "granularity": "day"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "date": "2026-03-01",
      "cost": 10000,
      "show": 50000,
      "click": 1000,
      "ctr": 2.0,
      "convert": 50,
      "cpc": 10.0,
      "cpm": 200.0
    }
  ]
}
```

#### 5.2 导出报表
```http
GET /api/v1/report/export?startDate=2026-03-01&endDate=2026-03-07&format=xlsx
```

### 6. 转化回传

#### 6.1 上传转化数据
```http
POST /api/v1/conversion/upload
```

**请求体**:
```json
{
  "clickId": "click_001",
  "conversionType": "购买",
  "conversionTime": "2026-03-01 10:00:00",
  "value": 100.0
}
```

#### 6.2 批量上传转化
```http
POST /api/v1/conversion/batch-upload
```

---

## 🤖 智能化功能

### 1. 自动出价

#### 1.1 更新自动出价
```http
POST /api/v1/auto-bidding/update
```

**请求体**:
```json
{
  "campaignId": 100001,
  "historicalData": [
    {
      "date": "2026-02-27",
      "cost": 10000,
      "revenue": 20000,
      "bid": 1.5
    }
  ],
  "currentBudget": 10000,
  "currentCost": 5000
}
```

**响应**:
```json
{
  "code": 200,
  "message": "出价更新成功",
  "data": {
    "campaignId": 100001,
    "optimalBid": 1.8,
    "currentROI": 2.0,
    "trend": "up"
  }
}
```

### 2. A/B 测试

#### 2.1 创建 A/B 测试
```http
POST /api/v1/ab-test/create
```

**请求体**:
```json
{
  "name": "测试出价策略",
  "description": "测试不同出价策略的效果",
  "testType": "bid",
  "variants": [
    {
      "name": "变体 A",
      "config": {
        "bid": 1.5
      }
    },
    {
      "name": "变体 B",
      "config": {
        "bid": 2.0
      }
    }
  ],
  "durationDays": 7
}
```

#### 2.2 启动测试
```http
POST /api/v1/ab-test/{test_id}/start
```

#### 2.3 分析测试结果
```http
POST /api/v1/ab-test/{test_id}/analyze
```

### 3. 归因模型

#### 3.1 归因转化
```http
POST /api/v1/attribution/attribute
```

**请求体**:
```json
{
  "conversion": {
    "conversionId": "conv_001",
    "conversionTime": "2026-03-01 10:00:00",
    "value": 100.0
  },
  "touchpoints": [
    {
      "touchpointId": "tp_001",
      "channel": "search",
      "timestamp": "2026-03-01 09:00:00",
      "cost": 50.0
    },
    {
      "touchpointId": "tp_002",
      "channel": "social",
      "timestamp": "2026-03-01 09:30:00",
      "cost": 50.0
    }
  ],
  "model": "time_decay"
}
```

**支持的归因模型**:
- `last_click`: 最后点击归因
- `first_click`: 首次点击归因
- `linear`: 线性归因
- `time_decay`: 时间衰减归因
- `position_based`: 位置基础归因

---

## ⚡ 异步任务

### 1. 异步任务 API

所有耗时操作都支持异步执行，使用 Celery 异步任务队列。

#### 1.1 提交异步任务
```http
POST /api/v1/tasks/conversion/upload
```

**响应**:
```json
{
  "code": 200,
  "message": "转化上传任务已提交",
  "data": {
    "task_id": "TASK_ID",
    "status": "pending"
  }
}
```

#### 1.2 查询任务状态
```http
GET /api/v1/tasks/{task_id}/status
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "TASK_ID",
    "status": "success",
    "result": {
      "success_count": 100,
      "failed_count": 0
    }
  }
}
```

**任务状态**:
- `pending`: 等中
- `started`: 已开始
- `success`: 成功
- `failure`: 失败

---

## 🛠️ 错误处理

### 错误码
| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 未找到 |
| 422 | 限流 |
| 500 | 服务器错误 |

### 错误响应格式
```json
{
  "code": 400,
  "message": "请求参数错误",
  "data": {
    "errors": [
      {
        "field": "advertiserId",
        "message": "广告主ID 不能为空"
      }
    ]
  },
  "timestamp": 1772371234567
}
```

---

## 📋 最佳实践

### 1. Token 管理
- 使用 `refresh_token` 定期刷新 `access_token`
- 存储 Token 时注意加密
- Token 即将过期时自动刷新

### 2. 限流处理
- 遵守限流策略（100 req/s）
- 使用指数退避重试
- 记录限流触发时间

### 3. 错误处理
- 检查错误码和消息
- 实现重试机制
- 记录错误日志

### 4. 性能优化
- 使用批量操作减少请求次数
- 使用异步任务处理耗时操作
- 启用响应缓存

---

## 🧪 测试环境

### 测试账号
- 测试环境 URL: `https://api-test.example.com`
- 测试账户: `test_user`
- 测试密码: `test_password`

### 沙箱账号
- 沙箱账户: `sandbox`
- 沙箱密码: `sandbox123`
- 沙箱环境: `https://api-sandbox.example.com`

---

## 📞 技术支持

### 联系方式
- 技术支持邮箱: support@example.com
- 技术支持电话: 400-123-4567
- 工作时间: 周一至周五 9:00-18:00

### 文档资源
- API 文档: https://docs.example.com
- SDK 下载: https://sdk.example.com
- 示例代码: https://github.com/example/ad-platform-sdk

---

## 📚 附录

### A. 完整 API 列表
见《API 参考手册》

### B. SDK 使用指南
见《SDK 集成指南》

### C. Webhook 配置
见《Webhook 配置指南》

---

**文档版本**: v2.0
**更新时间**: 2026-03-01
**维护团队**: Ad Platform 团队

---

**如有问题，请联系技术支持。**
