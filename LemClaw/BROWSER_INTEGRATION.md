# LemClaw - 浏览器集成说明

## 📋 架构说明

LemClaw 现在使用 **agent-browser** 模拟终端操作，而不是直接调用 OpenClaw Gateway API。

### 工作流程

```
用户 → LemClaw 授权验证 → 浏览器机器人 → OpenClaw 网页界面
                                   ↓
                            输入消息 → 点击发送 → 获取回复
```

### 优势

1. **更简单** - 不需要复杂的 Gateway API 集成
2. **更稳定** - 使用标准的网页操作
3. **更灵活** - 可以处理任何网页界面

## 🔧 当前状态

### ✅ 已完成

1. **授权系统** - 完整的授权码管理
2. **Web 服务器** - Flask API 运行在 8089 端口
3. **前端界面** - 美观的聊天页面
4. **浏览器机器人** - OpenClawBrowserBot 类

### ⏳ 待完善

1. **OpenClaw 网页界面适配** - 需要找到正确的输入框和发送按钮
2. **响应解析** - 需要从网页中提取 AI 回复
3. **会话管理** - 优化浏览器会话的生命周期

## 🐛 当前问题

### 问题 1：找不到输入字段

浏览器机器人无法在 OpenClaw 网页界面找到输入框。

**原因**：
- OpenClaw 网页界面可能使用了特殊的元素选择器
- 需要实际的页面快照来分析

**解决方案**：

需要手动测试 agent-browser 来找到正确的元素：

```bash
# 1. 打开 OpenClaw 网页
agent-browser open http://localhost:18789

# 2. 获取快照
agent-browser snapshot -i

# 3. 分析快照输出，找到输入框和发送按钮的引用

# 4. 更新 browser_bot.py 中的 _find_element 方法
```

### 问题 2：AI 回复提取

当前实现只是简化版本，需要实际的解析逻辑。

**解决方案**：

1. 获取消息区域的快照
2. 查找最新的 AI 消息
3. 提取文本内容

## 🎯 建议的完整方案

### 方案 A：简化方案（推荐）

**直接调用 LLM API**，而不是通过浏览器：

```python
import openai

class DirectLLMBot:
    def send_message(self, message: str, system_prompt: str = "") -> str:
        response = openai.ChatCompletion.create(
            model="glm-4.7",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
```

**优点**：
- 简单直接
- 响应快速
- 无需浏览器

**缺点**：
- 需要管理 API Key
- 丢失 OpenClaw 的高级功能

### 方案 B：完善浏览器集成

继续使用 agent-browser，但完善元素定位和响应提取：

1. **手动分析页面结构**
2. **优化元素查找逻辑**
3. **实现响应提取**
4. **添加错误处理**

**优点**：
- 完全利用 OpenClaw 功能
- 保留会话历史

**缺点**：
- 实现复杂
- 性能较慢

### 方案 C：混合方案

根据配置选择不同的后端：

- **开发模式**: 直接调用 LLM API（快速）
- **生产模式**: 使用浏览器集成（完整功能）

## 💡 下一步建议

### 立即行动（推荐）

**采用方案 A**，直接调用 LLM API：

1. 创建 `llm_bot.py`
2. 修改 `app.py` 使用 `llm_bot.py`
3. 测试完整流程

### 长期优化

如果需要完整的 OpenClaw 功能，可以：

1. 手动测试 agent-browser
2. 分析 OpenClaw 网页结构
3. 完善浏览器机器人

## 📝 测试命令

### 测试浏览器机器人

```bash
cd /root/.openclaw/workspace/LemClaw

# 单独测试
python3 browser_bot.py

# 或通过 API 测试
curl -X POST http://localhost:8089/api/chat \
  -H "Content-Type: application/json" \
  -d '{"auth_code": "YOUR_CODE", "message": "你好"}'
```

### 手动测试 agent-browser

```bash
# 打开 OpenClaw
agent-browser open http://localhost:18789

# 获取快照
agent-browser snapshot -i

# 查找输入框（需要查看快照输出）
agent-browser fill @e1 "测试消息"

# 查找发送按钮
agent-browser snapshot -i

# 发送
agent-browser click @e2

# 获取回复
agent-browser snapshot -i
```

## 🔗 相关文件

- `app.py` - 主应用
- `browser_bot.py` - 浏览器机器人
- `index.html` - 前端界面
- `.env` - 环境配置

## 📞 帮助

如果需要帮助：
1. 查看 agent-browser 文档
2. 测试 OpenClaw 网页界面
3. 调整元素查找逻辑

---

**更新时间**: 2026-03-06 11:00
**状态**: 🔄 开发中
