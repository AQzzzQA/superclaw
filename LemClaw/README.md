# LemClaw - OpenClaw 授权网关

为多个客户提供独立的 OpenClaw 访问能力，支持授权码管理和多租户隔离。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，设置 OpenClaw Gateway URL 和 Token
```

### 3. 启动服务器

```bash
python app.py
```

服务器将在 `http://localhost:8089` 启动

### 4. 生成授权码

```bash
python generate_codes.py
```

这将生成 50 个授权码，并保存到 `auth_codes.txt` 和 `auth_codes.json`

## 📋 功能特性

### 核心功能

- ✅ **授权码验证** - 验证授权码有效性
- ✅ **多租户隔离** - 每个授权码独立的会话
- ✅ **消息转发** - 将用户消息转发到 OpenClaw
- ✅ **状态管理** - 启用/禁用/过期授权码
- ✅ **使用统计** - 记录每个授权码的使用情况
- ✅ **批量生成** - 一次性生成多个授权码

### 管理功能

- 授权码生成（支持自定义数量和前缀）
- 授权码列表查看
- 授权码状态管理（active/disabled/expired）
- 授权码导出（CSV 格式）
- 使用统计（消息计数、最后使用时间）

## 🔌 API 接口

### 健康检查

```
GET /health
```

响应：
```json
{
  "status": "healthy",
  "gateway": "connected",
  "timestamp": "2026-03-06T09:00:00.000000"
}
```

### 验证授权码

```
POST /api/auth/verify
Content-Type: application/json

{
  "auth_code": "your_auth_code_here"
}
```

响应：
```json
{
  "success": true,
  "client_name": "Client_1",
  "message_count": 10
}
```

### 发送聊天消息

```
POST /api/chat
Content-Type: application/json

{
  "auth_code": "your_auth_code_here",
  "message": "你好"
}
```

响应：
```json
{
  "success": true,
  "reply": "你好！很高兴为您服务。",
  "client_name": "Client_1"
}
```

### 生成授权码（管理员）

```
POST /api/admin/codes/generate
Content-Type: application/json

{
  "count": 50,
  "client_name_prefix": "Client",
  "expire_days": null
}
```

响应：
```json
{
  "success": true,
  "count": 50,
  "codes": [
    {
      "auth_code": "abc123...",
      "client_name": "Client_1",
      "expires_at": null
    }
  ]
}
```

### 列出所有授权码（管理员）

```
GET /api/admin/codes/list
```

### 更新授权码状态（管理员）

```
PUT /api/admin/codes/<code_id>/status
Content-Type: application/json

{
  "status": "disabled"
}
```

### 导出授权码（管理员）

```
GET /api/admin/codes/export
```

返回 CSV 格式的授权码列表

## 🎨 前端界面

打开 `index.html` 即可使用：

1. 输入授权码
2. 点击验证
3. 开始与 AI 对话

前端特点：
- 现代化 UI 设计
- 响应式布局
- 实时消息显示
- 错误处理

## 🔐 安全建议

1. **授权码安全**
   - 授权码使用 `secrets.token_urlsafe()` 生成
   - 建议至少 32 位长度
   - 定期轮换授权码

2. **API 安全**
   - 使用 HTTPS 部署
   - 添加速率限制
   - 设置授权码过期时间

3. **会话隔离**
   - 每个授权码对应独立会话
   - 会话之间数据不互通
   - 可设置消息配额限制

## 📊 数据库结构

### auth_codes 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| auth_code | VARCHAR(64) | 授权码（唯一） |
| client_name | VARCHAR(100) | 客户名称 |
| status | ENUM | 状态（active/disabled/expired） |
| created_at | DATETIME | 创建时间 |
| expires_at | DATETIME | 过期时间 |
| last_used_at | DATETIME | 最后使用时间 |
| message_count | INTEGER | 消息计数 |

## 🛠️ 配置说明

### 环境变量（.env）

```bash
# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL=http://localhost:8080
GATEWAY_TOKEN=your-gateway-token-here

# 数据库配置
DATABASE_URL=sqlite:///auth_codes.db

# 服务器配置
HOST=0.0.0.0
PORT=8089
DEBUG=False

# 授权码配置
AUTH_CODE_LENGTH=32
DEFAULT_CODE_COUNT=50
```

## 🚦 使用流程

1. **管理员生成授权码**
   ```bash
   python generate_codes.py
   ```

2. **分发给客户**
   - 将授权码发给客户
   - 客户打开 index.html
   - 输入授权码

3. **客户开始使用**
   - 验证通过后进入聊天界面
   - 发送消息与 AI 对话
   - 每个授权码独立的会话

4. **管理员管理**
   - 查看授权码使用情况
   - 启用/禁用授权码
   - 导出授权码列表

## 📈 扩展功能

### 添加速率限制

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ... existing code
```

### 添加日志记录

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route('/api/chat', methods=['POST'])
def chat():
    auth_code = request.json.get('auth_code')
    message = request.json.get('message')
    logging.info(f"Message from {auth_code}: {message}")
    # ... existing code
```

### 添加 WebSocket 支持

```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    auth_code = data['auth_code']
    message = data['message']
    # Send to OpenClaw
    result = send_to_openclaw(auth_code, message)
    emit('response', result)
```

## 📝 许可证

MIT License

## 🤝 支持

如有问题，请联系管理员或查看文档。

---

**快速开始**: `pip install -r requirements.txt && python app.py && python generate_codes.py`
