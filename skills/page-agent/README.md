# Page Agent 技能

这是一个将阿里巴巴 page-agent 项目集成到 OpenClaw 技能生态的包装器。

## 技能信息

- **名称**: page-agent
- **来源**: https://github.com/alibaba/page-agent
- **版本**: 1.5.7
- **许可证**: MIT
- **类型**: 网页自动化智能体

## 快速开始

### 1. 克隆项目

```bash
cd /root/.openclaw/workspace/page-agent
```

### 2. 安装依赖

```bash
npm install
```

### 3. 构建项目

```bash
npm run build
```

### 4. 使用方式

#### CDN 快速体验（技术评估）

```html
<script src="https://registry.npmmirror.com/page-agent/1.5.7/files/dist/iife/page-agent.demo.js"></script>
```

#### NPM 安装（生产环境）

```bash
npm install page-agent
```

### 5. 配置 LLM

需要配置 LLM API Key，支持：
- 通义千问（推荐，阿里云百炼）
- OpenAI
- Claude
- 其他兼容 OpenAI API 的模型

## 技术要求

- Node.js: ^20.19.0 || ^22.13.0 || >=24
- 现代浏览器
- LLM API Key

## 文件结构

```
page-agent/
├── SKILL.md         # 技能文档
├── README.md        # 本文件
├── examples/        # 示例代码
├── packages/        # 核心包
└── docs/            # 项目文档
```

## 相关链接

- 🚀 [在线 Demo](https://alibaba.github.io/page-agent/)
- 📖 [完整文档](https://alibaba.github.io/page-agent/docs/introduction/overview)
- 💻 [GitHub 仓库](https://github.com/alibaba/page-agent)

## 集成状态

- [x] 项目克隆
- [x] 技能文档创建
- [x] 依赖安装待完成
- [ ] 示例代码创建
- [ ] 测试验证

---

**最后更新**: 2026-03-14
