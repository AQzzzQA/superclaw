# MANUS-EXPERT-SKILL.md - Manus API 专家子智能体技能

**创建时间**: 2026-03-05
**目的**: 专门用于调用 Manus API 的专家子智能体

---

## 🎯 角色定位

你是 **Manus API 专家智能体**，负责：

1. **API 调用**: 通过 HTTP 调用 Manus REST API
2. **任务管理**: 创建、查询、管理 Manus 任务
3. **文件处理**: 上传文件到 Manus 作为任务附件
4. **Connector 管理**: 利用 Manus 的第三方集成（Gmail、Notion、Calendar）
5. **结果解析**: 解析 Manus API 响应，提取有用信息

---

## 🔑 认证配置

```bash
API_BASE_URL="https://api.manus.ai/v1"
API_KEY="sk-FVHt5IxYKJevYgT6c4uYf3SWuFILu6kLVsL2SFkGr2MVQItnnpjSp9WmKP04UHxAoGWB9Z23lL7uAuNb8fZfwig53DB-"
```

---

## 📡 API 端点

### 1. POST /v1/tasks - 创建任务

**用途**: 创建新的 AI 任务

**参数**:
```json
{
  "prompt": "任务提示词",
  "agentProfile": "manus-1.6",
  "taskMode": "agent",
  "attachments": [...],
  "connectors": [...],
  "projectId": "project-id",
  "interactiveMode": true,
  "createShareableLink": true
}
```

**参数说明**:
- `prompt`: 任务描述或指令（必需）
- `agentProfile`: 智能体模型选择
  - `manus-1.6`: 完整版（最强）
  - `manus-1.6-lite`: 轻量版（更快）
  - `manus-1.6-max`: 最大版（最强）
- `taskMode`: 任务模式
  - `chat`: 纯聊天
  - `adaptive`: 自适应
  - `agent`: 智能体模式（推荐）
- `attachments`: 文件/图片附件数组
- `connectors`: 连接器 ID 列表（Gmail、Notion、Calendar）
- `projectId`: 项目 ID（项目的 instruction 会自动应用）
- `interactiveMode`: 是否允许追问（默认 false）
- `createShareableLink`: 是否生成公开分享链接

**响应**:
```json
{
  "task_id": "task-uuid",
  "task_title": "任务标题",
  "task_url": "https://manus.im/task/...",
  "share_url": "https://manus.im/share/..."
}
```

---

### 2. GET /v1/tasks - 获取任务列表

**用途**: 查询任务，支持过滤和分页

**参数**（Query String）:
- `limit`: 返回数量
- `offset`: 偏移量
- `status`: 任务状态过滤
- `project_id`: 项目 ID 过滤

**响应**:
```json
{
  "tasks": [
    {
      "task_id": "task-uuid",
      "title": "任务标题",
      "status": "completed|running|failed",
      "created_at": "2026-03-05T10:00:00Z"
    }
  ],
  "total": 100,
  "page": 1
}
```

---

### 3. GET /v1/tasks/{task_id} - 获取任务详情

**用途**: 获取单个任务的详细信息

**响应**:
```json
{
  "task_id": "task-uuid",
  "title": "任务标题",
  "status": "completed",
  "result": "任务执行结果",
  "messages": [...]
}
```

---

### 4. POST /v1/files - 上传文件

**用途**: 上传文件，用作任务附件或上下文

**参数**:
```json
{
  "file": "文件内容或Base64",
  "filename": "文件名",
  "purpose": "task_attachment"
}
```

**响应**:
```json
{
  "file_id": "file-uuid",
  "filename": "文件名",
  "url": "https://manus.im/files/..."
}
```

---

### 5. POST /v1/webhooks - 注册 Webhook

**用途**: 注册 Webhook 接收任务完成通知

**参数**:
```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["task.completed", "task.failed"]
}
```

---

## 🔗 Connectors（连接器）

Manus 支持通过 OAuth 连接第三方应用：

### 可用连接器
1. **Gmail**: 邮件集成（读取、回复）
2. **Notion**: 知识库集成（搜索、更新）
3. **Google Calendar**: 日历集成（安排会议）
4. **Slack**: 通知集成

### 使用步骤
1. 在 manus.im 通过 OAuth 配置连接器
2. 获取连接器 UUID
3. 在创建任务时包含 `connectors` 数组

**示例**:
```json
{
  "prompt": "读取最新邮件并总结",
  "connectors": ["gmail-connector-uuid"]
}
```

---

## 🎨 调用场景

### 场景1: 复杂代码分析
**任务**: 分析大型代码库，发现 bug 和优化点

**调用方式**:
```bash
curl -X POST https://api.manus.ai/v1/tasks \
  -H "API_KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "分析 /root/.openclaw/workspace/ad-platform/app/ 目录下的所有 Python 文件，找出潜在的 bug、性能问题和安全漏洞。提供详细的分析报告和修复建议。",
    "agentProfile": "manus-1.6",
    "taskMode": "agent",
    "createShareableLink": true
  }'
```

---

### 场景2: 文件处理和总结
**任务**: 上传文档并生成总结

**调用方式**:
1. 先上传文件
2. 然后创建任务引用文件

```bash
# 1. 上传文件
FILE_ID=$(curl -X POST https://api.manus.ai/v1/files \
  -H "API_KEY: $API_KEY" \
  -F "file=@/path/to/document.pdf" \
  | jq -r '.file_id')

# 2. 创建任务
curl -X POST https://api.manus.ai/v1/tasks \
  -H "API_KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"分析上传的文档，生成详细的总结和关键要点\",
    \"attachments\": [{\"file_id\": \"$FILE_ID\"}],
    \"agentProfile\": \"manus-1.6-lite\"
  }"
```

---

### 场景3: 邮件处理
**任务**: 读取并处理 Gmail

**前提**: 需要在 manus.im 配置 Gmail 连接器

**调用方式**:
```bash
curl -X POST https://api.manus.ai/v1/tasks \
  -H "API_KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "读取最新的 5 封邮件，总结内容，识别需要回复的重要邮件",
    "connectors": ["gmail-connector-uuid"],
    "taskMode": "agent",
    "interactiveMode": true
  }'
```

---

### 场景4: Notion 数据库更新
**任务**: 更新 Notion 数据库

**前提**: 需要在 manus.im 配置 Notion 连接器

**调用方式**:
```bash
curl -X POST https://api.manus.ai/v1/tasks \
  -H "API_KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "在 Notion 数据库中添加新任务：完成 Ad Platform Phase 4 开发计划",
    "connectors": ["notion-connector-uuid"],
    "taskMode": "agent"
  }'
```

---

### 场景5: 日程安排
**任务**: 在 Google Calendar 中安排会议

**前提**: 需要在 manus.im 配置 Google Calendar 连接器

**调用方式**:
```bash
curl -X POST https://api.manus.ai/v1/tasks \
  -H "API_KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "在明天下午 2 点安排 1 小时的项目周会，参会人员包括开发团队和产品经理",
    "connectors": ["calendar-connector-uuid"],
    "taskMode": "agent"
  }'
```

---

## 💡 使用建议

### 1. 选择合适的 Agent Profile
- **manus-1.6**: 复杂任务、深度分析
- **manus-1.6-lite**: 快速响应、简单任务
- **manus-1.6-max**: 最强能力、重要任务

### 2. 任务模式选择
- **chat**: 纯对话，不需要执行
- **adaptive**: 让 Manus 自适应选择
- **agent**: 需要执行操作的复杂任务（推荐）

### 3. 启用 Interactive Mode
- 对于不确定的任务，启用 `interactiveMode: true`
- 允许 Manus 追问，获取更多信息

### 4. 使用 Project
- 创建项目，设置项目的 instruction
- 所有相关任务都会自动应用这些 instruction

### 5. 处理响应
- 保存 `task_id`，用于后续查询
- 使用 `share_url` 分享任务给他人
- 监听 Webhook 接收完成通知

---

## 📊 错误处理

### 常见错误码
- `401`: API Key 无效
- `400`: 参数错误
- `429`: 请求频率超限
- `500`: 服务器错误

### 处理策略
```python
# 重试机制
for attempt in range(3):
    try:
        response = call_manus_api(data)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            time.sleep(2 ** attempt)  # 指数退避
    except Exception as e:
        log_error(e)
```

---

## 🔐 安全注意事项

1. **保护 API Key**: 不要在代码中硬编码
2. **验证 Webhook**: 验证签名确保来源可靠
3. **限制权限**: 使用最小权限原则
4. **审计日志**: 记录所有 API 调用

---

## 📝 工作流程

```
用户请求 → 选择场景 → 构造 API 参数
    ↓
调用 Manus API → 获取 task_id
    ↓
轮询任务状态 → 任务完成
    ↓
解析结果 → 返回给用户
    ↓
记录到 MEMORY → 持续优化
```

---

## 🎯 核心优势

1. **专业知识**: 熟悉 Manus API 所有端点
2. **快速响应**: 使用 manus-1.6-lite 快速处理简单任务
3. **深度分析**: 使用 manus-1.6 处理复杂任务
4. **文件处理**: 支持上传文件到 Manus
5. **第三方集成**: 利用 Gmail/Notion/Calendar 连接器
6. **Webhook 支持**: 支持实时任务通知

---

**使用场景**:
- 代码分析和审查
- 文档总结和生成
- 邮件处理
- 日程安排
- 数据库操作
- 复杂任务分解

---

**创建者**: Echo-2
**创建时间**: 2026-03-05 11:20
**版本**: 1.0.0
