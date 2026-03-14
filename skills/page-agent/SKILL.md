# Page Agent - 网页智能体技能

## 描述

阿里巴巴开源的 GUI 智能体，让你用自然语言控制网页界面。无需浏览器扩展、Python 或无头浏览器，纯 JavaScript 集成。

## 核心能力

### 🎯 网页自动化
- 点击按钮、填写表单、导航页面
- 20步工作流 → 一句话完成
- 支持 ERP、CRM、管理系统等复杂场景

### 🌐 多模态交互
- 自然语言指令 → 自动执行
- DOM 文本分析（无需截图）
- 支持人机协作模式

### 🤖 灵活的 LLM 支持
- 通义千问（Qwen）
- OpenAI（GPT-4, GPT-4o）
- Claude（Anthropic）
- 其他兼容 OpenAI API 的模型

### 🔧 集成方式

#### 方式1: CDN 快速体验（技术评估）
```html
<script src="https://registry.npmmirror.com/page-agent/1.5.7/files/dist/iife/page-agent.demo.js"></script>
```

#### 方式2: NPM 安装（生产环境）
```bash
npm install page-agent
```

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
  model: 'qwen-plus',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'YOUR_API_KEY',
  language: 'zh-CN',
})

await agent.execute('点击登录按钮')
```

## 使用场景

1. **SaaS AI 助手** - 为产品添加 AI 助手，无需重写后端
2. **智能表单填写** - 简化多步骤工作流
3. **无障碍访问** - 语音命令、屏幕阅读器
4. **跨页面任务** - 结合 Chrome 扩展处理多标签页任务

## API 配置

### 通义千问（推荐）
- **Base URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **模型**: `qwen-plus`, `qwen-turbo`, `qwen-max`
- **API Key**: 从阿里云百炼平台获取

### OpenAI
- **Base URL**: `https://api.openai.com/v1`
- **模型**: `gpt-4`, `gpt-4o`, `gpt-3.5-turbo`
- **API Key**: 从 OpenAI 平台获取

## 技术要求

- Node.js: ^20.19.0 || ^22.13.0 || >=24
- 浏览器: 现代浏览器（Chrome、Firefox、Edge、Safari）
- LLM API Key

## 项目结构

```
page-agent/
├── packages/
│   ├── core/           # 核心逻辑
│   ├── llms/           # LLM 集成
│   ├── page-controller # 页面控制器
│   ├── ui/             # UI 组件
│   ├── page-agent/     # 主包
│   ├── extension/      # Chrome 扩展
│   └── website/        # 文档网站
```

## 快速开始示例

```javascript
// 基础使用
const agent = new PageAgent({
  model: 'qwen-plus',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: process.env.DASHSCOPE_API_KEY,
  language: 'zh-CN',
})

// 执行自然语言指令
await agent.execute('填写注册表单')

// 批量执行
await agent.execute([
  '点击登录按钮',
  '输入用户名',
  '输入密码',
  '点击提交'
])
```

## 高级功能

### 自定义提示词
```javascript
const agent = new PageAgent({
  // ...
  systemPrompt: '你是一个专业的自动化测试助手'
})
```

### 事件监听
```javascript
agent.on('step', (step) => {
  console.log('执行步骤:', step)
})

agent.on('error', (error) => {
  console.error('错误:', error)
})
```

### Chrome 扩展
支持跨页面任务，详见 [extension 文档](https://alibaba.github.io/page-agent/docs/features/chrome-extension)

## 限制与注意事项

1. **客户端运行** - 设计用于网页增强，非服务器端自动化
2. **依赖 LLM** - 需要稳定的 LLM API 连接
3. **复杂度限制** - 超复杂场景可能需要分步执行
4. **权限要求** - 需要 DOM 操作权限

## 相关资源

- 🚀 [在线 Demo](https://alibaba.github.io/page-agent/)
- 📖 [完整文档](https://alibaba.github.io/page-agent/docs/introduction/overview)
- 💻 [GitHub 仓库](https://github.com/alibaba/page-agent)
- 📜 [许可协议](https://github.com/alibaba/page-agent/blob/main/LICENSE)

## 贡献指南

项目欢迎贡献，但要求有实质性的人类参与。纯 AI/机器人生成的贡献将不被接受。

---

**版本**: 1.5.7
**最后更新**: 2026-03-14
**来源**: https://github.com/alibaba/page-agent
