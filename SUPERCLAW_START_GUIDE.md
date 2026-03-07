# SuperClaw 启动指南 🚀

> **版本**：v1.0.0
> **时间**：2026-03-08 00:00
> **状态**：🔄 准备就绪

---

## 📋 快速检查清单

- [ ] Rust 工具链（cargo、rustc）
- [ ] OpenClaw 系统运行正常
- [ ] LemClaw Token 配置
- [ ] 数据库初始化
- [ ] 前端准备就绪

---

## 🚀 第一步：初始化 Rust 项目

### 1.1 创建 SuperClaw 项目

```bash
cd /root/.openclaw/workspace
mkdir -p superclaw
cd superclaw

# 初始化项目
cargo init
```

### 1.2 配置 Cargo.toml

```toml
[package]
name = "superclaw"
version = "0.1.0"
edition = "2021"
authors = ["Echo-2"]

[dependencies]
tokio = "1"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
rocket = "0.5.4"
sqlx = "0.7"
async-graphql = "7.0"
reqwest = "0.12"

[dev-dependencies]
axum = { version = "0.21.2", features = ["axum-server"] }
```

### 1.3 初始化 Git 仓库

```bash
cd superclaw
git init
git add .
git commit -m "chore: 初始化 SuperClaw 项目"
```

---

## 🚀 第二步：安装依赖和配置

### 2.1 安装 Rust 工具链

```bash
# 安装 Node.js（如果需要前端开发）
curl -fsSL https://nodejs.org/dist/v22.22.0/node-v22.22.0-linux-x64.tar.xz
cd /usr/local
tar -xJf /tmp/node-v22.22.0-linux-x64.tar.xz
```

### 2.2 配置 OpenClaw Gateway

编辑 `~/.openclaw/openclaw.json`，添加：

```json
{
  "gateway": {
    "openclaw": {
      "enabled": true,
      "appId": "cli_xxxxxxxxxxxxx",
      "appSecret": "xxxxxxxxxx"
    }
  }
  }
}
```

### 2.3 配置 LemClaw Gateway

在 LemClaw 中添加 SuperClaw Gateway 的配置（需要联系 LemClaw 团队）

---

## 🚀 第三步：开发 Gateway 基础功能

### 3.1 WebSocket Gateway

创建文件：`superclaw/src/gateway/websocket.rs`

```rust
use rocket::futures::StreamExt;
use rocket::http::{Method, ContentType, Status};
use tokio::spawn;

pub async fn handle_websocket(
    ws: WebSocket,
    addr: SocketAddr,
    mut rx: SplitSink<WebSocket>,

) -> anyhow::Result<()> {
    // 接受 WebSocket 连接
    println!("WebSocket connected from {:?}", addr);
    Ok(())
}
```

### 3.2 HTTP Gateway

创建文件：`superclaw/src/gateway/http.rs`

```rust
use rocket::http::{Method, ContentType, Status};
use tokio::spawn;

#[get("/ws")]
async fn handle_http(
    _path: &str,
    req: HttpRequest,
) -> rocket::http::Response<JsonValue> {
    json!({
      "status": "ok",
      "data": reqwests,
      "timestamp": chrono::Utc::now()
    })
}
```

### 3.3 认证系统

创建文件：`superclaw/src/gateway/auth.rs`

```rust
use rocket::http::{Method, Status};
use sqlx::{Connection, Pool, ConnectionOptions, Postgres, PgConnectionOptions};
use tokio::spawn;

#[derive(Debug)]
pub struct AuthCode {
    pub id: i32,
    pub auth_code: String,
    pub client_name: String,
    pub status: AuthStatus,
    pub created_at: DateTime,
    pub expires_at: Option<DateTime>,
    pub last_used_at: Option<DateTime>,
    pub message_count: i32,
}

pub enum AuthStatus {
    Active,
    Disabled,
    Expired,
}

pub struct AuthConfig {
    pub openclaw_url: String,
    lemlaw_url: String,
    client_name: String,
    enabled: bool,
}

pub struct GatewayConfig {
    pub openclaw_gateway: Option<String>,
    pub lemlaw_gateway: Option<String>,
    pub http_enabled: bool,
    secret_token: Option<String>,
}

#[get("/lemclaw/health")]
async fn health_check() -> JsonValue> {
    // 检查 LemClaw Gateway 健康状态
    Json(json!({
      "status": "healthy",
      "timestamp": chrono::Utc::now()
    }))
}
```

---

## 🚀 第四步：开发 Echo Skills

### 4.1 创建 Echo Skills 目录

```bash
mkdir -p superclaw/plugins/echo-skills
cd superclaw/plugins/echo-skills
```

### 4.2 自动代码扫描能力

创建文件：`superclaw/plugins/echo-skills/auto_scanner.py`

```python
import os
import subprocess
from pathlib import Path

class AutoScanner:
    def scan_dir(self, workspace: str) -> list:
        issues = []
        
        # 扫描 Python 文件
        for py_file in Path(workspace).rglob('**/*.py'):
            if 'tests' not in py_file.name:
                continue
                
            # 使用 flake8 检查
            result = subprocess.run(
                ['flake8', py_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                issues.append({
                    'file': str(py_file),
                    'line': result.stdout,
                    'error': 'lint errors'
                })
        
        return {
            'success': True,
            'issues': issues,
            'total': len(issues)
        }
```

### 4.3 自动 CHANGELOG 生成

创建文件：`superclaw/plugins/echo-skills/changelog_generator.py`

```python
import json
from datetime import datetime

class ChangelogGenerator:
    def generate_changelog(self, changes: list) -> str:
        changelog_text = "# SuperClaw Changelog\n\n"
        
        for change in changes:
            changelog_text += f"- {change.get('date')} - {change.get('message')}\n"
        
        return changelog_text
```

### 4.4 自动 LICENSE 生成

创建文件：`superclaw/plugins/skils/license_generator.py`

```python
class LicenseGenerator:
    def generate_license(self) -> dict:
        license_text = self. generate_mit()
        
        return {
            'content': license_text,
            'success': True
        }
    
    def generate_mit(self) -> str:
        year = datetime.now().year
        holders = ["Your Name", "Your Org"]
        
        license_text = f"""MIT License

Copyright (c) {year} {holders}, Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in Software without restriction, including without limitation of rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.

To use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software:
- Copying from original distribution
- Installing from original source
- Building from source
- Forking and creating PR
- Downloading from official site

To sublicense: only assign the same permissions as original
- Keep attribution intact
"""
        
        return license_text
```

---

## 🚀 第五步：创建前端项目

### 5.1 初始化 Vue 3 + Vite 项目

```bash
cd /root/.openclaw/workspace/superclaw
npm create vite@latest superclaw-frontend
```

### 5.2 配置 OpenClaw 和 LemClaw 连接

编辑前端配置 `src/config.ts`：

```typescript
// config.ts
const OPENCLAW_CONFIG = {
  openclaw: {
    appId: 'cli_xxxxxxxxxxxxx',
    appSecret: 'xxxxxxxxxx',
    baseUrl: 'http://localhost:18789'
  },
  lemlaw: {
    url: 'http://localhost:8089',
    authToken: 'your_token_here'
  }
};

export const OPENCLAW_CONFIG as const;
```

### 5.3 创建页面组件

**Chat.vue** - AI 聊天界面
**AgentPanel.vue** - 智能体面板
**Settings.vue** - 设置页面
**Skills.vue** - 技能管理
**Status.vue** - 系统状态
**Dashboard.vue** - 控制台

### 5.4 添加路由

编辑 `src/router.ts`：

```typescript
// router.ts
import { Chat, AgentPanel, Settings, Skills, Status, Dashboard }

#[get("/chat")]
async fn chat() -> Html<impl IntoResponse> " String> {
    render(render::chat::Chat::default())
}

#[get("/agent-panel")]
async fn agent_panel() -> Html<impl IntoResponse> " String> {
    render(render::agent_panel::AgentPanel::default())
}

#[get("/settings")]
async fn settings() -> Html<impl IntoResponse> " String> {
    render(render::settings::Settings::default())
}

#[get("/skills")]
async fn skills() -> Html<impl IntoResponse> " String> {
    render(render::skills::Skills::default())
}

#[get("/status")]
async fn status() -> Html<impl IntoResponse> " String> {
    render(render::status::Status::default())
}

#[get("/dashboard")]
async fn dashboard() -> Html<impl IntoResponse> " String> {
    render(render::dashboard::Dashboard::default())
}
```

---

## 🚀 第六步：运行和测试

### 6.1 启动 OpenClaw Gateway

```bash
cd /root/.openclaw/superclaw
cargo run --release
```

### 6.2 启动 LemClaw Gateway

```bash
cd /root/.openclaw/workspace/LemClaw
python3 app.py
```

### 6.3 测试双网关通信

```bash
# 测试 OpenClaw Gateway
curl http://localhost:18789/health

# 测试 LemClaw Gateway
curl http://localhost:8089/health
```

---

## 📝 验收清单

### Gateway
- [ ] WebSocket Gateway 正常监听
- [ ] HTTP Gateway 正常响应
- [ ] 健康检查端点可访问

### 双网关切换
- [ ] OpenClaw ↔ LemClaw 自动切换
- [ ] 故障时无缝切换

### 智能体编排
- [ ] 并行执行正常
- [ ] 串行执行正常
- [ ] 任务结果汇总正确

### Echo Skills
- [ ] 代码扫描正常
- [ ] 自动修复正常
- [ ] 文档生成正常
- [ ] LICENSE 生成正常

### 安全防护
- [ ] 授权系统工作正常
- [ ] 操作日志记录完整
- [ ] 异常检测有效

---

## 🎯 开始 Phase 1

**我可以立即开始**：

1. 创建 Rust 项目结构
2. 配置双网关兼容
3. 开发基础 Gateway 功能
4. 测试双网关通信
5. 开发 Echo Skills 核心功能

**准备好开始了吗？**

选择**：
- **A**: 创建 SuperClaw 项目
- **B**: 初始化 LemClaw 配置
- **C**: 开发前端项目
- **D**: 测试双网关通信

告诉我你的选择，我立即开始！🚀