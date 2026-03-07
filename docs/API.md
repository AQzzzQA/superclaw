# SuperClaw API 文档

> **版本**: v1.0.0
> **创建时间**: 2026-03-08
> **作者**: AQzzzQA

---

## 📋 目录

- [概述](#概述)
- [认证](#认证)
- [WebSocket Gateway](#websocket-gateway)
- [HTTP Gateway](#http-gateway)
- [Echo Skills](#echo-skills)
- [LemClaw Gateway](#lemclaw-gateway)
- [错误码](#错误码)

---

## 概述

SuperClaw 提供双协议网关（WebSocket + HTTP）和丰富的 API 端点。

### Base URL

```
生产环境: https://api.superclaw.com
开发环境: http://localhost:3000
```

### 认证方式

- **授权码** - 短期授权码（5分钟有效）
- **Bearer Token** - 长期访问令牌

---

## 认证

### 生成授权码

```http
POST /api/auth/verify
Content-Type: application/json

{
  "auth_code": "your_auth_code"
}
```

**响应**：
```json
{
  "success": true,
  "auth_code": "new_auth_code",
  "expires_in": 300,
  "timestamp": 1704067200000
}
```

**错误码**：
- `400` - 授权码不能为空
- `401` - 授权码无效或已过期

---

## WebSocket Gateway

### 建立 WebSocket 连接

```javascript
const ws = new WebSocket('ws://localhost:3000/ws');
```

**消息格式**：
```json
{
  "message_type": "message",
  "session_id": "uuid",
  "user_id": "user_id",
  "payload": {
    "content": "Hello, SuperClaw!"
  },
  "timestamp": 1704067200000
}
```

### WebSocket API 消息

```http
POST /api/websocket/message
Content-Type: application/json

{
  "message_type": "message",
  "session_id": "uuid",
  "user_id": "user_id",
  "payload": {
    "content": "Hello, SuperClaw!"
  }
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "message": "Message received",
    "timestamp": 1704067200000
  },
  "error": null
}
```

### 列出连接

```http
GET /api/websocket/connections
```

**响应**：
```json
{
  "connections": 3,
  "session_ids": [
    "uuid1",
    "uuid2",
    "uuid3"
  ],
  "timestamp": 1704067200000
}
```

---

## HTTP Gateway

### 健康检查

```http
GET /health
```

**响应**：
```json
{
  "status": "healthy",
  "gateway": "connected",
  "timestamp": 1704067200000
}
```

### 发送消息到智能体

```http
POST /api/agent
Content-Type: application/json

{
  "auth_code": "your_auth_code",
  "message": "Hello, SuperClaw!",
  "model_provider": "openai",
  "max_tokens": 2048,
  "temperature": 0.7,
  "timeout_ms": 60000
}
```

**请求参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `auth_code` | string | ✅ | 授权码 |
| `message` | string | ✅ | 消息内容 |
| `model_provider` | string | ❌ | 模型提供商（openai/claude/glm） |
| `max_tokens` | number | ❌ | 最大 token 数（默认：2048） |
| `temperature` | number | ❌ | 温度（0.0-1.0，默认：0.7） |
| `timeout_ms` | number | ❌ | 超时时间（默认：60000） |

**响应**：
```json
{
  "success": true,
  "reply": "AI回复内容",
  "model_used": "openai",
  "tokens_used": 1234,
  "error": null,
  "timestamp": 1704067200000
}
```

### 双网关状态

```http
GET /api/status
```

**响应**：
```json
{
  "lemlaw_gateway": {
    "healthy": true,
    "url": "http://localhost:8089"
  },
  "openclaw_gateway": {
    "healthy": true,
    "url": "http://localhost:18789"
  },
  "timestamp": 1704067200000
}
```

---

## Echo Skills

### 扫描代码库

```http
POST /api/skills/scan
Content-Type: application/json

{
  "workspace_path": "/path/to/workspace"
}
```

**请求参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `workspace_path` | string | ✅ | 工作空间路径 |

**响应**：
```json
{
  "success": true,
  "issues": [
    {
      "file_path": "/path/to/file.py",
      "line_number": 10,
      "column": 5,
      "severity": "warning",
      "message": "unused variable",
      "code": "F841"
    }
  ],
  "total_issues": 1,
  "scan_duration_ms": 1500,
  "timestamp": 1704067200000
}
```

### 自动修复问题

```http
POST /api/skills/fix
Content-Type: application/json

{
  "workspace_path": "/path/to/workspace",
  "issues": [
    {
      "file_path": "/path/to/file.py",
      "line_number": 10,
      "column": 5,
      "severity": "warning",
      "message": "unused variable",
      "code": "F841"
    }
  ]
}
```

**响应**：
```json
{
  "success": true,
  "results": [
    {
      "success": true,
      "file_path": "/path/to/file.py",
      "fixes_applied": 5,
      "error": null,
      "timestamp": 1704067200000
    }
  ]
}
```

### 生成 CHANGELOG

```http
POST /api/skills/generate/changelog
Content-Type: application/json

{
  "workspace_path": "/path/to/workspace",
  "changes": [
    "实现双网关架构",
    "添加 Echo Skills"
  ]
}
```

**响应**：
```json
{
  "success": true,
  "content": "# SuperClaw Changelog...",
  "file_path": "/path/to/CHANGELOG.md",
  "error": null,
  "timestamp": 1704067200000
}
```

### 生成 LICENSE

```http
GET /api/skills/generate/license
Content-Type: application/json

{
  "workspace_path": "/path/to/workspace"
}
```

**响应**：
```json
{
  "success": true,
  "content": "MIT License...",
  "file_path": "/path/to/LICENSE",
  "error": null,
  "timestamp": 1704067200000
}
```

---

## LemClaw Gateway

### 浏览器截图

```http
POST /api/browser/screenshot
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**请求参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 要截图的 URL |

**响应**：
```json
{
  "success": true,
  "screenshot": "base64_encoded_image",
  "timestamp": 1704067200000
}
```

### 浏览器自动化

```http
POST /api/browser/automate
Content-Type: application/json

{
  "actions": [
    {
      "type": "click",
      "selector": "#submit-button"
    },
    {
      "type": "type",
      "selector": "#username-input",
      "value": "testuser"
    }
  ]
}
```

**请求参数**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `actions` | array | ✅ | 自动化操作列表 |

**响应**：
```json
{
  "success": true,
  "results": [
    {
      "action": "click",
      "success": true
    }
  ],
  "timestamp": 1704067200000
}
```

### 性能指标

```http
GET /api/monitoring/metrics
```

**响应**：
```json
{
  "requests": {
    "/api/agent": 1000,
    "/api/skills/scan": 50
  },
  "errors": {
    "/api/agent": 5,
    "/api/skills/scan": 2
  },
  "avg_response_times": {
    "/api/agent": 150,
    "/api/skills/scan": 300
  },
  "timestamp": 1704067200000
}
```

### 性能日志

```http
GET /api/monitoring/logs
```

**响应**：
```json
{
  "success": true,
  "logs": [
    {
      "id": 1,
      "timestamp": 1704067200000,
      "endpoint": "/api/agent",
      "response_time_ms": 120,
      "status_code": 200,
      "error_message": null
    }
  ]
}
```

---

## 错误码

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| `200` | 请求成功 |
| `400` | 请求参数错误 |
| `401` | 未授权 |
| `403` | 禁止访问 |
| `404` | 资源未找到 |
| `500` | 服务器内部错误 |

### 业务错误码

| 错误码 | 说明 |
|--------|------|
| `AUTH_CODE_REQUIRED` | 授权码不能为空 |
| `AUTH_CODE_INVALID` | 授权码无效或已过期 |
| `MESSAGE_REQUIRED` | 消息不能为空 |
| `GATEWAY_UNAVAILABLE` | 所有网关都不可用 |
| `SCAN_FAILED` | 代码扫描失败 |
| `FIX_FAILED` | 自动修复失败 |
| `BROWSER_ERROR` | 浏览器操作失败 |

---

## 速率限制

| 端点 | 限制 |
|--------|------|
| `/api/agent` | 60 请求/分钟 |
| `/api/skills/scan` | 30 请求/分钟 |
| `/api/browser/*` | 10 请求/分钟 |

---

## SDK 和客户端库

### JavaScript/TypeScript

```bash
npm install @superclaw/sdk
```

```typescript
import { SuperClawClient } from '@superclaw/sdk';

const client = new SuperClawClient({
  baseUrl: 'http://localhost:3000',
  authToken: 'your_token'
});

// 发送消息
const response = await client.sendMessage({
  authCode: 'your_auth_code',
  message: 'Hello, SuperClaw!'
});
```

### Python

```bash
pip install superclaw-python
```

```python
from superclaw import SuperClawClient

client = SuperClawClient(
    base_url='http://localhost:3000',
    auth_token='your_token'
)

# 发送消息
response = client.send_message(
    auth_code='your_auth_code',
    message='Hello, SuperClaw!'
)
```

---

**创建时间**: 2026-03-08
**版本**: v1.0.0
**作者**: AQzzzQA 🚀
