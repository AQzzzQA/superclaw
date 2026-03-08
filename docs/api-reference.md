# SuperClaw API 文档

## 📡 概述

SuperClaw 提供了丰富的 API 接口，支持智能体编排、任务管理、记忆系统等功能。

---

## 🔌 接口列表

### 1. 智能体编排 API

#### 1.1 创建任务

**接口**: `POST /api/v1/tasks`

**请求体**:
```json
{
  "task_name": "代码审查",
  "agent_type": "code_reviewer",
  "parameters": {
    "code_path": "/path/to/code",
    "review_rules": ["flake8", "black"]
  },
  "priority": "high"
}
```

**响应**:
```json
{
  "task_id": "task_123456",
  "status": "pending",
  "created_at": "2026-03-08T22:00:00Z"
}
```

---

#### 1.2 并行执行任务

**接口**: `POST /api/v1/tasks/parallel`

**请求体**:
```json
{
  "tasks": [
    {
      "task_name": "代码审查",
      "agent_type": "code_reviewer",
      "parameters": {
        "code_path": "/path/to/code"
      }
    },
    {
      "task_name": "测试覆盖",
      "agent_type": "test_engineer",
      "parameters": {
        "test_path": "/path/to/tests"
      }
    }
  ]
}
```

**响应**:
```json
{
  "execution_id": "exec_789012",
  "tasks": [
    {
      "task_id": "task_123456",
      "task_name": "代码审查",
      "status": "completed",
      "result": {
        "issues_found": 10,
        "issues_fixed": 8
      },
      "duration": 5.2
    },
    {
      "task_id": "task_789012",
      "task_name": "测试覆盖",
      "status": "completed",
      "result": {
        "coverage": 85.5,
        "tests_passed": 150
      },
      "duration": 3.8
    }
  ],
  "total_duration": 5.2
}
```

---

#### 1.3 串行工作流

**接口**: `POST /api/v1/workflows`

**请求体**:
```json
{
  "workflow_name": "代码质量检查流程",
  "steps": [
    {
      "step_name": "代码审查",
      "agent_type": "code_reviewer",
      "depends_on": []
    },
    {
      "step_name": "运行测试",
      "agent_type": "test_engineer",
      "depends_on": ["代码审查"]
    },
    {
      "step_name": "生成报告",
      "agent_type": "data_analyst",
      "depends_on": ["运行测试"]
    }
  ]
}
```

**响应**:
```json
{
  "workflow_id": "wf_123456",
  "status": "running",
  "current_step": "运行测试",
  "progress": 66.67
}
```

---

### 2. 记忆系统 API

#### 2.1 存储记忆

**接口**: `POST /api/v1/memory`

**请求体**:
```json
{
  "memory_type": "experience",
  "content": "修复代码时，需要注意边界条件处理",
  "tags": ["bug_fix", "code_quality"],
  "importance": "high",
  "ttl": 2592000
}
```

**响应**:
```json
{
  "memory_id": "mem_123456",
  "status": "stored",
  "created_at": "2026-03-08T22:00:00Z"
}
```

---

#### 2.2 检索记忆

**接口**: `GET /api/v1/memory/search`

**查询参数**:
- `query`: 搜索关键词
- `tags`: 过滤标签（逗号分隔）
- `limit`: 返回结果数量（默认 10）
- `importance`: 最小重要性级别（low/medium/high）

**请求示例**:
```
GET /api/v1/memory/search?query=边界条件&tags=bug_fix,code_quality&importance=medium&limit=5
```

**响应**:
```json
{
  "memories": [
    {
      "memory_id": "mem_123456",
      "content": "修复代码时，需要注意边界条件处理",
      "tags": ["bug_fix", "code_quality"],
      "importance": "high",
      "created_at": "2026-03-08T22:00:00Z",
      "relevance": 0.95
    }
  ],
  "total": 1
}
```

---

### 3. LemClaw 集成 API

#### 3.1 模型列表

**接口**: `GET /api/v1/lemclaw/models`

**响应**:
```json
{
  "models": [
    {
      "model_id": "model_001",
      "name": "GPT-4",
      "provider": "openai",
      "capabilities": ["text", "code"],
      "cost_per_1k_tokens": 0.003,
      "status": "available"
    },
    {
      "model_id": "model_002",
      "name": "Claude-3",
      "provider": "anthropic",
      "capabilities": ["text", "analysis"],
      "cost_per_1k_tokens": 0.004,
      "status": "available"
    }
  ]
}
```

---

#### 3.2 调用模型

**接口**: `POST /api/v1/lemclaw/generate`

**请求体**:
```json
{
  "model_id": "model_001",
  "prompt": "请帮我优化这段代码",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**响应**:
```json
{
  "generation_id": "gen_123456",
  "text": "优化后的代码...",
  "tokens_used": 850,
  "cost": 0.00255,
  "model_used": "GPT-4"
}
```

---

### 4. 监控与统计 API

#### 4.1 任务统计

**接口**: `GET /api/v1/stats/tasks`

**查询参数**:
- `start_date`: 开始日期（ISO 8601）
- `end_date`: 结束日期（ISO 8601）
- `agent_type`: 过滤智能体类型

**响应**:
```json
{
  "total_tasks": 150,
  "completed_tasks": 135,
  "failed_tasks": 10,
  "success_rate": 90.0,
  "avg_duration": 5.2,
  "by_agent": {
    "code_reviewer": {
      "total": 50,
      "completed": 48,
      "success_rate": 96.0
    },
    "test_engineer": {
      "total": 50,
      "completed": 45,
      "success_rate": 90.0
    }
  }
}
```

---

#### 4.2 系统健康检查

**接口**: `GET /api/v1/health`

**响应**:
```json
{
  "status": "healthy",
  "services": {
    "orchestrator": "available",
    "lemclaw": "available",
    "memory": "available",
    "monitoring": "available"
  },
  "version": "1.0.0",
  "uptime": 86400
}
```

---

## 🔐 认证与授权

### API Key 认证

所有 API 请求需要在 Header 中包含 API Key：

```
Authorization: Bearer YOUR_API_KEY
```

### 获取 API Key

```bash
# 方式 1：通过控制台
# 登录 SuperClaw 控制台，在设置中生成 API Key

# 方式 2：通过 API
POST /api/v1/auth/login
{
  "username": "your_username",
  "password": "your_password"
}
```

---

## 📊 错误码

| 错误码 | 说明 | HTTP 状态码 |
|--------|------|-------------|
| 1001 | API Key 无效 | 401 |
| 1002 | API Key 过期 | 401 |
| 1003 | 权限不足 | 403 |
| 1004 | 参数错误 | 400 |
| 1005 | 资源不存在 | 404 |
| 1006 | 智能体不可用 | 503 |
| 1007 | 任务执行失败 | 500 |
| 1008 | 记忆存储失败 | 500 |
| 1009 | LemClaw 调用失败 | 502 |

### 错误响应示例

```json
{
  "error": {
    "code": 1004,
    "message": "参数错误：缺少必填字段 'task_name'",
    "details": {
      "field": "task_name",
      "reason": "required"
    }
  }
}
```

---

## 🔄 限流策略

| 资源类型 | 限制 | 时间窗口 |
|----------|------|----------|
| API 请求 | 1000 次/分钟 | 1 分钟 |
| 并行任务 | 10 个/用户 | 瞬时 |
| 记忆存储 | 100 条/小时 | 1 小时 |
| LemClaw 调用 | 10 次/分钟 | 1 分钟 |

### 限流响应

```json
{
  "error": {
    "code": 429,
    "message": "请求频率超过限制",
    "details": {
      "limit": 1000,
      "window": "1 分钟",
      "retry_after": 60
    }
  }
}
```

---

## 💡 使用示例

### Python 示例

```python
import requests
import json

# 配置
API_BASE = "https://api.superclaw.ai/v1"
API_KEY = "your_api_key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 创建并行任务
payload = {
    "tasks": [
        {
            "task_name": "代码审查",
            "agent_type": "code_reviewer",
            "parameters": {
                "code_path": "/path/to/code"
            }
        },
        {
            "task_name": "测试覆盖",
            "agent_type": "test_engineer",
            "parameters": {
                "test_path": "/path/to/tests"
            }
        }
    ]
}

response = requests.post(
    f"{API_BASE}/tasks/parallel",
    headers=headers,
    json=payload
)

result = response.json()
print(json.dumps(result, indent=2))
```

---

### cURL 示例

```bash
# 健康检查
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.superclaw.ai/v1/health

# 创建任务
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "task_name": "代码审查",
       "agent_type": "code_reviewer",
       "parameters": {
         "code_path": "/path/to/code"
       }
     }' \
     https://api.superclaw.ai/v1/tasks
```

---

## 📞 支持与联系

如有任何问题，请通过以下方式联系我们：

- **API 文档**: https://docs.superclaw.ai
- **技术支持**: support@superclaw.ai
- **GitHub Issues**: https://github.com/AQzzzQA/superclaw/issues

---

**最后更新**: 2026-03-08
