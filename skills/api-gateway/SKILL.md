# API Gateway 技能

**版本**: 1.0.0
**作者**: byungkyu
**说明**: 集成 100+ 第三方 API 的统一技能

---

## 📋 功能特性

### 1. OAuth 管理
- ✅ 自动处理 OAuth 流程
- ✅ 支持 100+ 第三方服务
- ✅ 令牌自动刷新

### 2. API 调用
- ✅ 统一的 API 调用接口
- ✅ 自动错误处理
- ✅ 速率限制保护
- ✅ 重试机制

### 3. 数据转换
- ✅ 自动 JSON 解析
- ✅ 响应格式化
- ✅ 错误信息统一

---

## 🚀 使用方法

### 初始化

```python
from api_gateway import APIGateway

# 初始化
gateway = APIGateway()

# 配置认证（如果需要）
gateway.config({
    "service_name": {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "redirect_uri": "http://localhost:8000/callback"
    }
})
```

### 添加服务

```python
# 添加 OpenAI 服务
openai = gateway.add_service("openai")

# 添加 Notion 服务
notion = gateway.add_service("notion")

# 添加 GitHub 服务
github = gateway.add_service("github")
```

### 调用 API

```python
# GET 请求
result = openai.get("/v1/models")

# POST 请求
result = notion.post("/pages", {
    "parent": {"database_id": "..."},
    "properties": {...}
})

# PUT 请求
result = github.put("/repos/owner/repo/issues/1", {
    "title": "New Title"
})

# DELETE 请求
result = openai.delete("/v1/files/file-abc123")
```

---

## 📊 支持的服务

### 生产力工具
- **OpenAI**: GPT-4, GPT-3.5
- **Anthropic**: Claude 3.5, Claude 3
- **Google**: Google Workspace (Gmail, Calendar, Drive, Docs)
- **Microsoft**: Microsoft 365 (Outlook, OneDrive, SharePoint)

### 开发工具
- **GitHub**: 代码仓库、Issues、PR
- **GitLab**: 代码仓库、CI/CD
- **Bitbucket**: 代码仓库

### 协作工具
- **Notion**: 文档和数据库
- **Slack**: 团队通信
- **Trello**: 项目管理
- **Airtable**: 数据库和表格

### 营销工具
- **Mailchimp**: 邮件营销
- **HubSpot**: CRM 和营销
- **Salesforce**: CRM

### 其他
- **Stripe**: 支付处理
- **Twilio**: 短信和电话
- **SendGrid**: 邮件发送

---

## 🔧 配置

### 环境变量

```bash
# API Gateway 配置
API_GATEWAY_CONFIG_FILE=/root/.openclaw/api-gateway.json
API_GATEWAY_CACHE_DIR=/tmp/api-gateway-cache
API_GATEWAY_TIMEOUT=30
API_GATEWAY_RETRY=3
```

### 配置文件

```json
{
  "services": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "api_key": "sk-...",
      "timeout": 30
    },
    "notion": {
      "base_url": "https://api.notion.com",
      "api_key": "secret_...",
      "timeout": 30
    }
  },
  "cache": {
    "enabled": true,
    "dir": "/tmp/api-gateway-cache",
    "ttl": 3600
  }
}
```

---

## 📊 错误处理

### 标准错误格式

```python
{
    "code": 400,
    "message": "Bad Request",
    "details": {
        "field": "email",
        "reason": "invalid format"
    }
}
```

### 错误码

- **200**: 成功
- **400**: 错误的请求
- **401**: 未授权
- **403**: 禁止访问
- **404**: 未找到
- **429**: 速率限制
- **500**: 服务器错误
- **503**: 服务不可用

---

## 🚀 快速开始

### 1. 安装

```bash
skillhub install api-gateway
```

### 2. 配置

```bash
openclaw configure --section api-gateway
```

### 3. 使用

```python
from api_gateway import APIGateway

gateway = APIGateway()
openai = gateway.add_service("openai")

# 调用 API
models = openai.get("/models")
print(models)
```

---

## 📞 获取帮助

- **文档**: https://docs.openclaw.ai/skills/api-gateway
- **GitHub**: https://github.com/byungkyu/api-gateway-skill
- **支持**: https://clawhub.ai/support

---

**创建时间**: 2026-03-07 02:15
**版本**: 1.0.0
**状态**: ✅ 手动创建完成
