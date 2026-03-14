# Page Agent 安装指南

## 前置要求

- Node.js: ^20.19.0 || ^22.13.0 || >=24
- npm 或 yarn 或 pnpm

## 安装步骤

### 1. 克隆项目

```bash
cd /root/.openclaw/workspace
git clone https://github.com/alibaba/page-agent.git
cd page-agent
```

### 2. 安装依赖

```bash
npm install
```

或者使用 yarn/pnpm：

```bash
yarn install
# 或
pnpm install
```

### 3. 构建项目

```bash
npm run build
```

这将构建所有库和文档网站。

### 4. 本地开发

#### 启动文档网站
```bash
npm start
```

#### 启动扩展开发
```bash
npm run dev:ext
```

#### 启动 Demo 开发
```bash
npm run dev:demo
```

### 5. 使用

#### 在网页中使用（CDN）

```html
<script src="https://registry.npmmirror.com/page-agent/1.5.7/files/dist/iife/page-agent.demo.js"></script>
```

#### 在 Node.js/前端项目中使用（NPM）

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

## 配置 LLM API Key

### 通义千问（推荐）

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 创建 API Key
3. 在代码中配置：

```javascript
const agent = new PageAgent({
  model: 'qwen-plus',
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: 'your-dashscope-api-key',
  language: 'zh-CN',
})
```

### OpenAI

1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 创建 API Key
3. 在代码中配置：

```javascript
const agent = new PageAgent({
  model: 'gpt-4o',
  baseURL: 'https://api.openai.com/v1',
  apiKey: 'your-openai-api-key',
  language: 'zh-CN',
})
```

## 故障排除

### 问题 1: Node.js 版本不兼容

```bash
# 检查 Node.js 版本
node --version

# 如果版本过低，使用 nvm 升级
nvm install 22
nvm use 22
```

### 问题 2: 依赖安装失败

```bash
# 清理缓存并重新安装
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 问题 3: 构建失败

```bash
# 检查是否安装了所有依赖
npm install

# 检查 TypeScript 版本
npm list typescript

# 如果版本不匹配，可以强制升级
npm install typescript@latest --save-dev
```

### 问题 4: API Key 无效

- 检查 API Key 是否正确复制
- 确认 API Key 是否有足够的配额
- 检查 baseURL 是否正确

## 验证安装

```bash
# 检查项目结构
ls -la packages/

# 运行测试（如果有）
npm test

# 检查构建输出
ls -la packages/page-agent/dist/
```

## 下一步

- 查看 [基础使用示例](./basic-usage.js)
- 打开 [快速开始 HTML](./quick-start.html)
- 阅读 [官方文档](https://alibaba.github.io/page-agent/docs/introduction/overview)

## 需要帮助？

- 📖 [完整文档](https://alibaba.github.io/page-agent/docs/introduction/overview)
- 💬 [GitHub Issues](https://github.com/alibaba/page-agent/issues)
- 📢 [HN 讨论](https://news.ycombinator.com/item?id=47264138)

---

**最后更新**: 2026-03-14
