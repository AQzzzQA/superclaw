# SuperClaw 🦞

> **Super Claw AI Platform** - 下一代智能体融合平台
>
> 双网关兼容 OpenClaw + LemClaw，更安全、更智能、更强大！

---

## 📋 项目简介

SuperClaw 是一个融合 OpenClaw 的易用性和 LemClaw 的安全性 + IronClaw 的 Echo Skills 特性的下一代智能体平台。

### 核心特性

- 🚀 **双网关兼容** - OpenClaw Gateway（WebSocket） + LemClaw Gateway（HTTP）
- 🛡️ **企业级安全** - WebAssembly 沙箱隔离、令牌白名单、多层防护
- 🤖 **智能体编排** - 并行/串行协作、任务分解、结果汇总
- 🔌 **灵活插件** - WASM 插件、多模型支持
- 📊 **自动化能力** - Echo Skills 自动修复、代码扫描、文档生成

---

## 🏗️ 技术栈

| 组件 | 技术选型 |
|------|---------|
| **后端** | Rust + Axum |
| **网关** | WebSocket + HTTP |
| **数据库** | SQLite + Redis |
| **AI 集成** | OpenAI + Claude + GLM |
| **前端** | Vue 3 + Naive UI |
| **容器化** | Docker + WebAssembly |

---

## 📂 项目结构

```
superclaw/
├── Cargo.toml          # Rust 项目配置
├── src/
│   ├── main.rs         # 入口
│   ├── gateway/        # 双网关
│   ├── agent/          # 智能体编排
│   ├── skill/          # 技能系统
│   └── security/       # 安全防护
├── frontend/           # Vue 3 前端
├── plugins/           # WASM 插件
└── docs/              # 文档
```

---

## 🚀 快速开始

### 环境要求

- Rust 1.70+
- Node.js 22.22.0+
- Python 3.11+

### 安装

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw

# 安装 Rust 依赖
cargo build --release

# 启动 LemClaw Gateway
cd LemClaw
pip install -r requirements.txt
python3 app.py

# 启动 SuperClaw
cd superclaw
cargo run --release
```

---

## 📚 文档

- [架构文档](docs/ARCHITECTURE.md)
- [API 文档](docs/API.md)
- [开发指南](docs/DEVELOPER.md)
- [安全文档](docs/SECURITY.md)

---

## 🤝 贡献

欢迎提交 PR！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

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
