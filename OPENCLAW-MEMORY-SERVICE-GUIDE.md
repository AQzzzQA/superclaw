# OpenClaw 记忆服务使用指南

## ✅ 服务状态

**状态**: ✅ 已启动并持续运行
**PID**: 2226213
**启动方式**: systemd (开机自启)
**降级模式**: ✅ 已启用
**工作目录**: `/root/.openclaw/workspace`
**日志文件**: `/var/log/openclaw-memory.log`

## 🎯 已完成配置

### 1. 系统服务
- ✅ systemd 服务已创建
- ✅ 开机自动启动已启用
- ✅ 自动重启机制已配置
- ✅ 日志记录已设置

### 2. 记忆功能
- ✅ 记忆服务运行正常
- ✅ 本地文件搜索正常工作
- ✅ 自动降级机制正常
- ✅ 全局函数可正常调用

### 3. 管理工具
- ✅ 管理脚本已创建 (`manage-memory-service.sh`)
- ✅ 测试脚本已创建 (`test-memory-service.py`)
- ✅ 环境变量已配置

## 🚀 使用方法

### 方法 1: 使用全局函数（推荐）

```python
from openclaw_memory_integration import (
    search_memory,
    get_memory,
    write_memory
)

# 搜索记忆
results = await search_memory("用户偏好", max_results=10)

# 读取记忆
lines = await get_memory("MEMORY.md")

# 写入记忆
await write_memory("memory/2026-03-10.md", "# 今日工作")
```

### 方法 2: 使用集成实例

```python
from openclaw_memory_integration import OpenClawMemoryIntegration

# 创建实例
integration = OpenClawMemoryIntegration()

# 使用功能
results = await integration.memory_search("查询")
context = await integration.load_session_context("session_key")

# 关闭连接
await integration.close()
```

### 方法 3: 在 OpenClaw 主智能体中使用

需要在 OpenClaw 的代码中添加以下内容：

```python
# 在 OpenClaw 主智能体初始化时
from openclaw_memory_integration import search_memory, extract_and_store

# 在处理问题时
async def handle_question(question: str):
    # 搜索相关记忆
    results = await search_memory(question, max_results=5)

    # 使用记忆结果
    if results:
        context = results[0]['content']
        # 基于上下文回答问题...

    # 提取新记忆
    await extract_and_store(text=question, session_key="session_key")
```

## 📊 服务管理

### 查看状态
```bash
./manage-memory-service.sh status
# 或
systemctl status openclaw-memory.service
```

### 查看日志
```bash
./manage-memory-service.sh logs
# 或
tail -f /var/log/openclaw-memory.log
```

### 重启服务
```bash
./manage-memory-service.sh restart
# 或
systemctl restart openclaw-memory.service
```

### 停止服务
```bash
./manage-memory-service.sh stop
# 或
systemctl stop openclaw-memory.service
```

### 健康检查
```bash
./manage-memory-service.sh health
```

### 清理旧记忆
```bash
./manage-memory-service.sh cleanup
```

## 🧪 测试验证

### 运行测试
```bash
python3 test-memory-service.py
```

### 预期结果
```
==============================================
  OpenClaw 记忆服务测试
==============================================
🧪 测试基本操作...

1. 读取 MEMORY.md...
   ✅ 读取成功，共 XX 行

2. 搜索记忆 '用户偏好'...
   ✅ 搜索完成，找到 X 条结果

3. 写入测试文件...
   ✅ 写入成功

4. 获取统计信息...
   ✅ 统计信息:
      - 本地文件: XX 个
      - 总大小: XX.XX MB

🎉 所有测试通过！
```

## 📈 监控指标

### 记忆统计
```bash
cd /root/.openclaw/workspace
python3 -c "
import asyncio
from openclaw_memory_integration import OpenClawMemoryIntegration

async def stats():
    integration = OpenClawMemoryIntegration()
    stats = await integration.get_memory_stats()
    print('记忆统计:')
    print(f'  - 本地文件: {stats[\"local\"][\"file_count\"]} 个')
    print(f'  - 总大小: {stats[\"local\"][\"total_size_mb\"]} MB')
    print(f'  - 工作目录: {stats[\"workspace\"]}')
    print(f'  - 记忆目录: {stats[\"memory_dir\"]}')
    await integration.close()

asyncio.run(stats())
"
```

### 服务日志
```bash
# 实时监控
tail -f /var/log/openclaw-memory.log

# 查看最近日志
tail -100 /var/log/openclaw-memory.log

# 搜索错误
grep ERROR /var/log/openclaw-memory.log
```

## 🔧 故障处理

### 问题 1: 服务未启动
```bash
# 检查服务状态
systemctl status openclaw-memory.service

# 手动启动
systemctl start openclaw-memory.service

# 查看错误日志
journalctl -u openclaw-memory.service -n 50
```

### 问题 2: 记忆搜索无结果
- 检查 memory 目录中是否有文件
- 验证降级模式是否启用
- 查看日志中的搜索查询

### 问题 3: OpenViking 连接失败
- 这是正常的，服务会自动降级到本地文件
- 如果需要 OpenViking，运行 `./deploy-openclaw-openviking.sh`

### 问题 4: 模块导入失败
```bash
# 检查文件是否存在
ls -la openclaw_memory_integration.py

# 检查 Python 路径
python3 -c "import sys; print('\n'.join(sys.path))"

# 测试导入
python3 -c "from openclaw_memory_integration import *"
```

## 📝 使用示例

### 示例 1: 在智能体对话中使用

```python
# 当用户提问时
async def handle_user_query(query: str):
    # 搜索相关记忆
    results = await search_memory(query, max_results=3)

    # 构建上下文
    context = ""
    if results:
        context = f"参考信息: {results[0]['content']}\n"

    # 生成回答
    answer = f"{context}根据我的理解，{query}..."

    # 提取新记忆
    await extract_and_store(
        text=query,
        session_key="user_conversation"
    )

    return answer
```

### 示例 2: 记录重要决策

```python
# 记录重要决策到记忆
decision_text = """
重要决策：选择 FastAPI 作为后端框架
理由：性能优秀、文档完善、异步支持
时间：2026-03-10
"""

await write_memory(
    "memory/decisions/2026-03-10-fastapi.md",
    decision_text
)
```

### 示例 3: 搜索历史经验

```python
# 搜索相关的历史经验
results = await search_memory(
    query="性能优化",
    max_results=5
)

# 使用经验
if results:
    for result in results:
        print(f"来源: {result['path']}")
        print(f"内容: {result['content']}")
        print(f"相关度: {result['score']}")
```

## 🎯 下一步优化

### 短期（1周）
1. 启动 OpenViking 服务器（可选）
2. 在 OpenClaw 主智能体中集成记忆功能
3. 添加更多记忆提取模式

### 中期（1个月）
1. 优化记忆检索算法
2. 添加机器学习特征提取
3. 实现记忆去重和压缩

### 长期（3个月）
1. 构建知识图谱
2. 实现跨会话记忆关联
3. 添加记忆可视化工具

## 📞 技术支持

### 快速命令
```bash
# 查看状态
./manage-memory-service.sh status

# 查看日志
./manage-memory-service.sh logs

# 运行测试
python3 test-memory-service.py

# 清理旧记忆
./manage-memory-service.sh cleanup
```

### 文档位置
- 集成文档: `OPENCLAW-OPENVIKING-INTEGRATION.md`
- 完成报告: `OPENCLAW-OPENVIKING-COMPLETION.md`
- 使用指南: 本文档

---

**创建时间**: 2026-03-10 13:30
**服务状态**: ✅ 运行中
**维护团队**: OpenClaw Architecture Team