# SuperClaw 🦞

> **Super Claw AI Platform** - 下一代智能体融合平台
>
> 双网关兼容 OpenClaw + LemClaw，更安全、更智能、更强大！

[![SuperClaw](https://img.shields.io/badge/Success)](https://img.shields.io/badge/v1.0.0-blue)
[![Rust](https://img.shields.io/badge/Rust-1.70+-blue)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/github/AQzzzQA/superclaw-orange.svg)](https://github.com/AQzzzQA/superclaw)

---

## 📋 项目简介

SuperClaw 是一个融合 OpenClaw 的易用性和 LemClaw 的安全性 + IronClaw 的 Echo Skills 特性的下一代智能体平台。

### 🌟 核心特性

- 🚀 **双网关兼容** - OpenClaw Gateway（WebSocket） + LemClaw Gateway（HTTP）
- 🛡️ **企业级安全** - 4 层安全防护（网络、应用、数据、沙箱、审计）
- 🤖 **智能体编排** - 并行/串行协作、任务分解、结果汇总
- 🔌 **灵活插件** - WASM 插件、多模型支持
- 📊 **自动化能力** - Echo Skills 自动修复、代码扫描、文档生成

---

## 🏗️ 技术栈

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| **后端** | Rust + Rocket | 高性能 Web 框架 |
| **网关** | WebSocket + HTTP | 双协议支持 |
| **数据库** | SQLite + Redis | 持久化 + 缓存 |
| **AI 集成** | OpenAI + Claude + GLM | 多模型支持 |
| **前端** | Vue 3 + Vite + Naive UI | 响应式 SPA |
| **容器化** | Docker + Docker Compose | 跨平台部署 |
| **沙箱** | WebAssembly (WASM) | 插件安全隔离 |

---

## 📂 项目结构

```
superclaw/
├── Cargo.toml          # Rust 项目配置
├── src/
│   ├── main.rs         # 入口
│   ├── gateway/        # 双网关
│   │   ├── websocket.rs   # WebSocket Gateway
│   │   ├── http.rs       # HTTP Gateway
│   │   ├── auth.rs        # 认证系统
│   ├── agents/          # 智能体编排
│   │   ├── orchestrator.rs   # 编排器核心
│   ├── skill/           # Echo Skills
│   │   ├── echo.rs       # 扫描/修复/生成
│   ├── api/             # API 路由
│   │   └── skills.rs      # Skills API
├── frontend/           # Vue 3 前端
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   ├── main.js        # 入口
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面组件
│   │   ├── composables/   # 组合式函数
│   ├── index.html        # 前端入口
│   ├── package.json      # 依赖配置
│   └── vite.config.js     # Vite 配置
├── docs/              # 文档目录
│   ├── ARCHITECTURE.md  # 架构文档
│   ├── API.md          # API 文档
│   ├── DEVELOPER.md       # 开发者指南
│   ├── SECURITY.md     # 安全文档
│   └── RELEASE_NOTES.md # 发布说明
├── .env.example        # 环境变量示例
├── .dockerignore       # Docker 忽略文件
└── README.md           # 项目说明
```

---

## 🚀 快速开始

### 环境要求

- **Rust**: 1.70+
- **Node.js**: 22.22.0+
- **Python**: 3.11+（LemClaw Gateway）
- **Git**: 最新版本

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw

# 2. 安装 Rust 依赖
cargo install

# 3. 安装前端依赖
cd frontend
npm install

# 4. 配置环境
cp .env.example .env

# 5. 启动开发服务器
cargo run

# 6. 启动 LemClaw Gateway
cd LemClaw
pip install -r requirements.txt
python3 app.py
```

### Docker 部署（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 访问地址
# 前端: http://localhost:5173
# API: http://localhost:3000
# 监控: http://localhost:8089/monitor.html
```

---

## 📚 文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **架构文档** | [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 系统架构、模块设计、数据流 |
| **API 文档** | [API.md](docs/API.md) | API 端点、请求/响应、错误码 |
| **开发者指南** | [DEVELOPER.md](docs/DEVELOPER.md) | 开发流程、代码规范、测试指南 |
| **安全文档** | [SECURITY.md](docs/SECURITY.md) | 安全架构、安全配置、审计流程 |
| **发布说明** | [RELEASE_NOTES.md](docs/RELEASE_NOTES.md) | 发布流程、版本说明 |

---

## 🎯 功能特性

### 1. 🚀 双网关

**WebSocket Gateway**
- ✨ 实时消息推送
- ✨ 连接池管理
- ✨ 心跳机制
- ✅ 断线重连
- ✅ 自动压缩
- ✅ 负载均衡

**HTTP Gateway**
- ✨ RESTful API 设计
- ✅ 标准化请求/响应
- ✅ CORS 支持
- ✅ 错误处理
- ✅ 请求验证
- ✅ 响应压缩

**双网关协同**
- ✅ 自动故障转移
- ✅ 负载均衡
- ✅ 熔断切换

---

### 2. 🔧 Echo Skills

**代码扫描器**
- ✅ flake8 - 代码规范检查
- ✅ mypy - 类型检查
- ✅ bandit - 安全扫描
- ✅ 并行扫描
- ✅ 智能分类
- ✅ 详细报告

**自动修复器**
- ✅ black - 自动格式化
- ✅ isort - import 排序
- ✅ 批量修复
- ✅ 修复前备份

**智能生成器**
- ✅ CHANGELOG 生成
- ✅ LICENSE 生成（MIT）
- ✅ .env.example 生成
- ✅ 自定义模板

---

### 3. 🎨 Vue 3 前端

**响应式设计**
- ✨ 移动端适配
- ✅ 深色/浅色主题
- ✨ 折叠侧边栏
- ✨ 组件化开发

**组件库**
- ✨ Naive UI 完整组件
- ✅ 图表组件
- ✨ 进度条
- 加载动画
- 对话组件
- 设置组件

**实时交互**
- ✨ WebSocket 实时通信
- ✅ 消息已读状态
- ✅ 消息加载骨架屏
- ✅ 在线用户数

---

### 4. 🌐 浏览器自动化

**agent-browser 集成**
- ✨ 网页截图
- ✅ 表单填写
- ✅ 页面滚动
- ✅ 元素点击
- ✅ 数据提取
- ✨ Cookie 管理

**监控面板**
- ✨ 实时监控图表
- ✅ 错误率追踪
- ✅ 响应时间热力图
- ✅ 日志实时查看
- ✅ 导出报告

---

### 5. 🤖 智能体编排

**内置智能体**
- 📋 代码审查员 - flake8、mypy、bandit
- 🧪 测试工程师 - 单元、集成、覆盖率
- 📊 数据分析师 - 数据处理、分析、报告
- 📝 文档编写员 - 文档生成、API 文档、用户指南
- 🔧 编排器核心 - 并行、串行、分解、汇总

**执行引擎**
- 🔥 并行引擎（信号量控制）
- ⏹️ 串行引擎（任务队列）
- 🔧 任务分解器（AI 驱动）
- 📊 结果汇总器（智能合并）

---

### 6. 🛡️ 安全防护

**4 层架构**
```
┌─────────────────────────────────┐
│  Layer 1: 网络层          │
│  - HTTPS/TLS 加密            │
│  - IP 白名单                │
│  - 速率限制（60/min）       │
├─────────────────────────────────┤
│  Layer 2: 应用层          │
│  - 授权码验证（5min 有效期） │
│  - 会话管理                  │
│  - 令牌白名单              │
├─────────────────────────────────┤
│  Layer 3: 数据层          │
│  - 数据加密存储（AES-256）    │
│  - 敏感信息脱敏              │
│  - 审计日志（WORM）          │
├─────────────────────────────────┤
│  Layer 4: 沙箱层          │
│  - WebAssembly 沙箱隔离          │
│  - 令牌白名单              │
│  - 操作日志                  │
└─────────────────────────────────┘
```

**审计功能**
- ✅ 完整操作日志
- ✅ 敏感操作脱敏
- ✅ 异常行为检测
- ✅ 自动归档
- ✅ 日志导出

---

## 📊 性能优化

| 指标 | 目标 |
|------|------|
| **WebSocket 响应时间** | < 50ms |
| **API 平均响应时间** | < 300ms |
| **并行智能体数** | 5 个 |
| **连接池复用** | 10 个连接 |
| **缓存命中率** | > 80% |
| **内存使用率** | < 70% |

---

## 📚 使用示例

### 发送消息

```bash
curl -X POST http://localhost:3000/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "auth_code": "your_auth_code",
    "message": "Hello, SuperClaw!"
  }'
```

### 代码扫描

```bash
curl -X POST http://localhost:3000/api/skills/scan \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_path": "/path/to/workspace"
  }'
```

### 智能体编排

```bash
curl -X POST http://localhost:3000/api/agents/parallel \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [...],
    "agent_types": [...]
  }'
```

### 获取状态

```bash
curl http://localhost:3000/api/status
```

---

## 🤝 贡献指南

欢迎贡献！查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 开发流程
1. Fork 项目
2. 创建功能分支
3. 提交 Pull Request
4. Code Review
5. 合并到 main

### 行为准则
- 遵循 Rust 代码规范
- 添加测试用例
- 更新相关文档
- 遵循提交规范

### 代码规范
- 使用 `cargo fmt` 格式化
- 通过 `cargo clippy` 检查
- 添加文档注释
- 编写测试用例

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AQzzzQA/superclaw&type=Date)](https://star-history.com/#AQzzzQA/superclaw&Date)

---

**创建时间**: 2026-03-08
**版本**: v1.0.0
**作者**: AQzzzQA 🚀
**状态**: 🟢 已发布 100%

---

# 🎉 SuperClaw - 让 AI 更强大、更安全、更智能！

**🦞 超爪出击！** 🌟
