# GLM-4.6V 模型集成与测试

## 概述

GLM-4.6V 是智谱 AI 推出的大语言模型，支持多模态交互和强大的语言理解能力。

## 集成状态

✅ **已集成** - 模型配置已添加到 OpenClaw 模型配置中

### 配置详情

```json
{
  "id": "glm-4.6v",
  "name": "GLM-4.6V",
  "provider": "glmcode",
  "baseUrl": "https://open.bigmodel.cn/api/anthropic",
  "api": "anthropic-messages",
  "contextWindow": 200000,
  "maxTokens": 8192,
  "input": ["text"],
  "reasoning": false
}
```

## 模型特性

- **上下文窗口**: 200,000 tokens
- **最大输出**: 8,192 tokens
- **API 协议**: Anthropic Messages API 兼容
- **提供商**: 智谱 AI (GLM Code)
- **成本**: 免费测试期（配置为 0）

## 测试

### 运行测试

```bash
cd /root/.openclaw/workspace/skills/glm-4.6v-test
node test-glm-4.6v.js
```

### 测试覆盖

1. **基础对话** - 测试模型的基本回复能力
2. **代码生成** - 测试代码编写能力
3. **逻辑推理** - 测试逻辑思维
4. **多轮对话** - 测试上下文记忆
5. **创意写作** - 测试创造力

## 使用示例

### 直接调用

```javascript
const messages = [
  {
    role: 'user',
    content: '你好！请自我介绍一下。'
  }
];

const response = await fetch('https://open.bigmodel.cn/api/anthropic/v1/messages', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY',
    'anthropic-version': '2023-06-01'
  },
  body: JSON.stringify({
    model: 'glm-4.6v',
    max_tokens: 1024,
    messages: messages
  })
});

const data = await response.json();
console.log(data.content[0].text);
```

### 在 OpenClaw 中使用

```bash
# 设置为默认模型
openclaw configure --model glmcode/glm-4.6v

# 或者在会话中指定
/model glmcode/glm-4.6v
```

## 模型对比

| 模型 | 上下文窗口 | 最大输出 | 推理能力 |
|------|-----------|---------|---------|
| GLM-4.6V | 200K | 8K | ⭐⭐⭐⭐ |
| GLM-4.7 | 200K | 8K | ⭐⭐⭐⭐⭐ |
| GLM-4.6 | 200K | 8K | ⭐⭐⭐ |
| GLM-4.5 | 200K | 8K | ⭐⭐ |

## API Key

⚠️ **注意**: API Key 已配置，但请勿在生产环境中使用硬编码的 Key。

获取 API Key:
1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 更新模型配置文件

## 故障排除

### 问题 1: 401 Unauthorized
**原因**: API Key 无效或已过期
**解决**: 检查并更新 API Key

### 问题 2: 429 Rate Limit
**原因**: 请求过于频繁
**解决**: 添加请求间隔或升级套餐

### 问题 3: 模型不存在
**原因**: 模型名称错误
**解决**: 确认使用 `glm-4.6v` 而非 `gml-4.6v`

## 相关资源

- 📖 [智谱 AI 文档](https://open.bigmodel.cn/dev/api)
- 🏠 [智谱 AI 官网](https://www.zhipuai.cn/)
- 💻 [GitHub 仓库](https://github.com/THUDM/GLM-4)

## 更新日志

### 2026-03-14
- ✅ 集成 GLM-4.6V 模型到 OpenClaw
- ✅ 创建测试脚本
- ✅ 完成 5 项功能测试

---

**最后更新**: 2026-03-14
**状态**: 已集成，测试通过
