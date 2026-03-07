# LemClaw 增强开发方案

> **目标**: 在 OpenClaw 基础上增强 LemClaw 特性，打造双网关兼容的智能体平台
> **创建时间**: 2026-03-08
> **优先级**: 高

---

## 📊 现状分析

### 你已有的资源

1. **LemClaw 项目** ✅
   - 路径：`/root/.openclaw/workspace/LemClaw/`
   - 核心文件：`app.py`、`browser_bot.py`、`auth_codes.db`
   - 功能：授权系统、Web 服务器（8089 端口）、浏览器机器人

2. **OpenClaw 系统** ✅
   - 版本：v2026.3.2
   - Gateway：正常运行（端口 18789）
   - 技能系统：完整
   - 配置文件：`~/.openclaw/openclaw.json`

3. **你的经验** ✅
   - Ad Platform 项目（V2.0，1万+ 行代码）
   - Echo-2 智能体（自我增强系统）
   - 子智能体编排能力
   - 企业使用手册 + 5 个行业场景
   - 系统级 Node.js v22.22.0

---

## 🎯 增强目标

### 核心价值主张

1. **兼容优先**：无缝兼容现有 OpenClaw 生态
2. **安全增强**：集成 IronClaw 的多层安全防护
3. **智能编排**：多智能体并行/串行协作
4. **双网关优势**：WebSocket + HTTP 双协议支持
5. **Echo Skills**：自动化修复、代码扫描、文档生成

---

## 🏗️ 架构设计

### 双网关架构

```
┌─────────────────────────────────────────────────────┐
│                   Client / AI / Plugins           │
└─────────────────────────────────────────────────────┘
                      ↓↑
┌─────────────────────────────────────────────────────┐
│              SuperClaw Gateway Layer               │
├─────────────┬───────────────┬──────────────┐ │
│              │ WebSocket      │   HTTP        │              │
│              │ (OpenClaw)     │ (LemClaw)   │              │
├─────────────┼───────────────┼──────────────┤ │
│    Auth       │ Security       │  Orchestrator   │   Skills     │
└─────────────┴───────────────┴──────────────┘ │
└─────────────────────────────────────────────────────┘
                      ↓↑
┌─────────────────────────────────────────────────────┐
│             Model Provider Layer                   │
├─────────────┬───────────────┬──────────────┐ │
│             │   OpenAI       │   Claude       │   GLM        │
└─────────────┴─────────────┴───────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 技术实现方案

### 方案 A：OpenClaw 集成 LemClaw（推荐）

**优点**：
- ✅ 无缝兼容现有 OpenClaw 技能系统
- ✅ 充分利用已有插件和技能
- ✅ 减少开发工作量
- ✅ 保持系统一致性

**实现方式**：

#### 1. 在 OpenClaw 中添加 LemClaw 通道插件

创建文件：`~/.openclaw/extensions/lemclaw/index.ts`

```typescript
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';

interface LemClawChannelConfig {
  gatewayUrl: string;
  authToken?: string;
  clientName?: string;
}

export async function registerLemClawHandler(
  pluginApi: OpenClawPluginApi,
  config: LemClawChannelConfig
): Promise<void> {
  const { gatewayUrl, authToken, clientName } = config;

  // 检查 LemClaw Gateway 健康状态
  try {
    const healthCheck = await fetch(`${gatewayUrl}/health`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (!healthCheck.ok) {
      throw new Error('LemClaw Gateway not healthy');
    }

    // 注册 LemClaw 通道
    await pluginApi.tools.registerTool({
      id: 'lemclaw-send-message',
      name: 'LemClaw Message Sender',
      description: 'Send messages via LemClaw Gateway API',
      execute: async (params) => {
        const { message, to } = params;

        const response = await fetch(`${gatewayUrl}/api/agent`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            auth_code: clientName || 'default',
            message: message,
            to: to
          })
        });

        return {
          success: response.ok,
          data: await response.json(),
          raw: response
        };
      }
    });

    pluginApi.logger.info('LemClaw channel registered successfully');
  } catch (error) {
    pluginApi.logger.error(`Failed to register LemClaw: ${error.message}`);
    throw error;
  }
}
```

#### 2. 配置 OpenClaw 通道

在 `openclaw.json` 中添加：

```json
{
  "channels": {
    "lemclaw": {
      "enabled": true,
      "gatewayUrl": "http://localhost:8089",
      "authToken": "YOUR_TOKEN_HERE",
      "clientName": "SuperClaw"
    }
  }
}
}
```

---

### 方案 B：LemClaw 集成 OpenClaw 特性（增强版）

**优点**：
- ✅ 保留 LemClaw 的高性能 Rust 核心
- ✅ 添加 OpenClaw 的技能生态
- ✅ 集成 Echo Skills 自动化能力
- ✅ 支持多智能体编排

**实现方式**：

#### 1. 在 LemClaw 中添加 OpenClaw 兼容层

修改 `lemclaw/app.py`，添加 OpenClaw 兼容 API：

```python
from flask import Flask, request
import requests

app = Flask(__name__)

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL = os.getenv('OPENCLAW_GATEWAY_URL', 'http://localhost:18789')
OPENCLAW_TOKEN = os.getenv('OPENCLAW_TOKEN', '')

@app.route('/api/openclaw/<path:path>', methods=['GET', 'POST'])
def openclaw_proxy(path):
    """OpenClaw API 代理"""
    if request.method == 'POST':
        # 转发 POST 请求到 OpenClaw
        try:
            response = requests.post(
                f"{OPENCLAW_GATEWAY_URL}/api/{path}",
                json=request.json,
                headers={
                    'Authorization': f"Bearer {OPENCLAW_TOKEN}"
                },
                timeout=30
            )
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        # 代理 GET 请求
        try:
            response = requests.get(
                f"{OPENCLAW_GATEWAY_URL}/api/{path}",
                headers={
                    'Authorization': f" bearer {OPENCLAW_TOKEN}"
                },
                params=request.args.to_dict()
            )
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/skills/list', methods=['GET'])
def list_skills():
    """列出 OpenClaw 技能"""
    try:
        # 调用 OpenClaw API
        response = requests.get(
            f"{OPENCLAW_GATEWAY_URL}/api/skills/list",
            headers={
                'Authorization': f"Bearer {OPENCLAW_TOKEN}"
            }
        )
        skills = response.json().get('skills', [])
        return jsonify({'skills': skills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

#### 2. 添加 Echo Skills 能力

在 LemClaw 中实现 Echo Skills 的核心能力：

```python
# echo_skills.py

import subprocess
import os
from pathlib import Path

class EchoSkills:
    """Echo Skills 集成 - 自动化修复能力"""

    def auto_format_code(self, file_path: str) -> dict:
        """自动格式化代码"""
        try:
            # 运行 black
            result = subprocess.run(
                ['black', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'file': file_path
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def generate_changelog(self, changes: list) -> str:
        """生成 CHANGELOG"""
        changelog_text = "# Changelog\n\n"

        for change in changes:
            changelog_text += f"- {change.get('date')} - {change.get('message')}\n"

        # 追加到文件
        changelog_path = Path(__file__).parent / 'CHANGELOG.md'
        changelog_path.write_text(changelog_text, encoding='utf-8')

        return changelog_path.read_text()

    def auto_generate_license(self) -> dict:
        """自动生成 LICENSE 文件"""
        license_text = f"""MIT License

Copyright (c) 2026 SuperClaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
        return {
            'success': True,
            'content': license_text
        }

    def scan_codebase(self, workspace: str) -> dict:
        """扫描代码库，识别问题"""
        issues = []

        # 扫描 Python 文件
        workspace_path = Path(workspace)
        for py_file in workspace_path.rglob('**/*.py'):
            # 使用 flake8 检查
            result = subprocess.run(
                ['flake8', str(py_file)],
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

#### 3. 添加智能体编排能力

```python
# agent_orchestrator.py

import asyncio
from typing import List, Dict, Any
import requests
import json

class AgentOrchestrator:
    """智能体编排器 - 并行/串行任务执行"""

    def __init__(self, openclaw_url: str, token: str):
        self.openclaw_url = openclaw_url
        self.token = token

    async def execute_parallel(self, tasks: List[Dict[str, Any]]) -> List[Dict]:
        """并行执行多个任务"""
        results = []

        async def run_task(task):
            try:
                response = requests.post(
                    f"{self.openclaw_url}/api/agent/parallel",
                    json=task,
                    headers={'Authorization': f"Bearer {self.token}"},
                    timeout=30
                )
                results.append({
                    'task_id': task['task_id'],
                    'success': response.ok,
                    'data': await response.json()
                })
            except Exception as e:
                results.append({
                    'task_id': task['task'],
                    'success': False,
                    'error': str(e)
                })

        await asyncio.gather(*[run_task(task) for task in tasks])

        return results

    async def execute_sequential(self, tasks: List[Dict[str, Any]]) -> List[Dict]:
        """串行执行任务"""
        results = []

        for task in tasks:
            try:
                response = requests.post(
                    f"{self.openclaw_url}/api/agent/sequential",
                    json=task,
                    headers={'Authorization': f"Bearer {self.token}"}
                )

                if response.ok:
                    data = await response.json()
                    # 执行下一个任务
                    results.append({
                        'task_id': task['task'],
                        'success': True,
                        'data': data
                    })
                else:
                    results.append({
                        'task_id': task['task'],
                        'success': False,
                        'error': f"HTTP {response.status_code}"
                    })
            except Exception as e:
                results.append({
                    'token': task.get('token'),
                    'success': False,
                    'error': str(e)
                })

        return results
```

---

## 🚀 实施计划

### Phase 1: 快速原型（1周）

**目标**：实现基础双网关通信

**任务**：
- [ ] 在 OpenClaw 中创建 LemClaw 通道插件
- [ ] 配置双 Gateway 通信
- [ ] 测试消息互发
- [ ] 测试技能调用

**交付物**：
- 可运行的双网关系统
- 基础文档和测试报告

---

### Phase 2: 安全增强（2周）

**目标**：集成 LemClaw 的安全特性

**任务**：
- [ ] 实现授权码验证
- [ ] 添加速率限制
- [ ] 实现操作日志
- [ ] 添加异常检测

**交付物**：
- 完整的安全防护系统
- 安全审计 dashboard

---

### Phase 3: 智能体编排（3周）

**目标**：支持多智能体并行/串行协作

**任务**：
- [ ] 实现编排器核心
- [ ] 添加并行执行
- [ ] 添加串行执行
- [ ] 任务结果汇总

**交付物**：
- 完整的智能体编排系统
- 编排器 UI

---

### Phase 4: Echo Skills 集成（2周）

**目标**：集成 Echo Skills 自动化能力

**任务**：
- [ ] 实现代码格式化
- [ ] 实现 CHANGELOG 生成
- [ ] 实现 LICENSE 生成
- [ ] 实现代码扫描

**交付物**：
- 完整的自动化修复系统
- 技能报告生成

---

## 📊 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **OpenClaw** | TypeScript + Node.js | 现有系统 |
| **LemClaw** | Python + Flask | 已有项目 |
| **数据库** | SQLite | 轻量级存储 |
| **网络** | requests + asyncio | HTTP/HTTPS |
| **安全** | JWT + RateLimiting | 授权 + 速率限制 |

---

## 🎯 关键决策

### 集成方式选择

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **方案 A**：OpenClaw + LemClaw | 兼容性好、开发快 | 需要维护双系统 | ⭐⭐⭐⭐⭐ |
| **方案 B**：LemClaw + OpenClaw 特性 | 性能好、单系统 | 功能受限 | ⭐⭐⭐ |
| **方案 C**：全新开发 | 完全控制 | 开发成本高 | ⭐⭐ |

**推荐**：方案 A（兼容优先）

---

## 🚀 开始行动

### 立即任务（本周）

1. [ ] 创建 LemClaw 通道插件
2. [ ] 配置 OpenClaw 集成 LemClaw
3. [ ] 测试双网关通信
4. [ ] 编写集成文档

### 短期任务（2周）

1. [ ] Phase 1 完成验收
2. [ ] 启动 Phase 2
3. [ ] 开始 Phase 3 规划

### 长期任务（本季度）

1. [ ] Phase 3 完成
2. [ ] 启动 Phase 4
3. [ ] 性能优化和稳定性测试

---

## 📝 成功标准

### Phase 1 成功

- [x] 双网关可通信
- [x] 消息互发正常
- [x] 技能调用正常
- [x] 文档完整

### Phase 2 成功

- [x] 授权验证工作
- [x] 速率限制生效
- [x] 操作日志完整
- [x] 异常检测有效

### Phase 3 成功

- [x] 并行执行正常
- [x] 串行执行正常
- [x] 任务结果准确
- [x] 编排器 UI 可用

### Phase 4 成功

- [x] 代码格式化正常
- [x] CHANGELOG 自动生成
- [x] LICENSE 自动生成
- [x] 代码扫描报告

---

## 🔧 开发环境准备

### 环境变量

```bash
# OpenClaw Gateway
export OPENCLAW_GATEWAY_URL="http://localhost:18789"
export OPENCLAW_TOKEN="your_token_here"

# LemClaw Gateway
export LEMCLAW_GATEWAY_URL="http://localhost:8089"
export LEMCLAW_AUTH_TOKEN="your_token_here"
```

### 开发依赖

```bash
# 安装 Python 依赖
pip install flask flask-cors requests sqlalchemy python-dotenv

# 安装 Node 依赖（如需前端开发）
cd frontend && npm install
```

### 目录结构

```
superclaw/
├── src/
│   ├── main.rs
│   ├── gateway/
│   │   ├── websocket.rs  # WebSocket Gateway
│   │   ├── http.rs       # HTTP Gateway
│   │   ├── auth.rs        # 认证系统
│   ├── agent/
│   │   ├── orchestrator.rs  # 编排器
│   ├── skill/
│   │   ├── lemclaw.ts    # LemClaw 集成
│   │   └── echo/         # Echo Skills
│   └── security/
│       ├── audit.rs
│       ├── sandbox.rs
│       ├── ratelimit.rs
└── memory/
│           ├── store.rs
│           └── recall.rs
├── frontend/
│   └── src/
│       └── App.vue
├── plugins/
│   └── skills/
└── docs/
```

---

## 📋 下一步

### 开始 Phase 1

准备好了吗？我现在可以帮你：

1. **创建 LemClaw 通道插件**
   - 在 OpenClaw 中注册 LemClaw API
   - 添加配置文件

2. **修改 OpenClaw 配置**
   - 添加 lemclaw 通道配置
   - 测试双网关通信

3. **编写集成文档**
   - API 接口文档
   - 使用示例
   - 故障排查指南

4. **开始开发 Echo Skills**
   - 代码格式化实现
   - CHANGELOG 生成
   - 自动扫描系统

---

**立即开始 Phase 1 吗？** 🚀

---

**创建时间**：2026-03-08
**文档版本**：v1.0
**状态**：🔄 规划中

---

准备好开始了吗？我随时可以开始 Phase 1！🚀
