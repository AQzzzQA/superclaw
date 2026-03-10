# OpenClaw 本体与 OpenViking 集成文档

## 🎯 集成目标

将 OpenViking（字节跳动开源的 AI Agent 上下文数据库）无缝集成到 OpenClaw 本体中，实现：

1. **自动记忆提取**: 从对话中自动提取重要信息
2. **智能语义搜索**: 基于语义理解的记忆检索
3. **分层上下文加载**: L0/L1/L2 三层记忆结构，按需加载
4. **无缝降级**: OpenViking 不可用时自动降级到本地文件系统
5. **兼容现有系统**: 与 MEMORY.md 和 memory/*.md 文件系统完全兼容

## 🏗️ 架构设计

### 系统组件

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenClaw 本体                            │
│                   (主智能体核心系统)                             │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           OpenClaw Memory Integration                  │   │
│  │         (记忆集成层 - 透明代理)                        │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  - memory_search()  → 自动选择搜索源                   │   │
│  │  - memory_get()     → 读取记忆内容                     │   │
│  │  - memory_write()   → 写入并同步                       │   │
│  │  - extract_and_store() → 自动提取记忆                  │   │
│  │  - load_session_context() → 加载会话上下文             │   │
│  └─────────────────────────────────────────────────────────┘   │
│           │                    │                              │
│           ├────────────────────┴──────────────────────┐      │
│           │                                         │      │
│  ┌────────▼─────────┐                    ┌─────────▼─────────┐│
│  │  OpenViking API  │                    │  Local File       ││
│  │  (语义搜索/存储)  │                    │  System           ││
│  │  - L0/L1/L2      │                    │  - MEMORY.md      ││
│  │  - 向量检索       │                    │  - memory/*.md    ││
│  │  - 自动提取       │                    │  - 降级模式       ││
│  └──────────────────┘                    └──────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 数据流

1. **用户提问** → OpenClaw 主智能体
2. **记忆搜索** → 集成层自动选择搜索源
3. **优先级**: OpenViking 语义搜索 → 本地文件搜索
4. **返回结果** → 主智能体获取相关上下文
5. **提取新记忆** → 自动提取重要信息并存储

## 🚀 核心功能

### 1. 智能记忆搜索

```python
# 自动选择最优搜索源
results = await memory_search(
    query="用户偏好的广告投放策略",
    max_results=10,
    min_score=0.5
)

# 返回格式
[
  {
    "path": "memory/2026-03-05.md",
    "score": 0.85,
    "content": "...",
    "source": "openviking",  # 或 "local"
    "metadata": {...}
  },
  ...
]
```

**特性**:
- 优先使用 OpenViking 语义搜索（向量检索）
- 自动降级到本地文件关键词搜索
- 支持相关度阈值过滤
- 返回统一格式的结果

### 2. 记忆读写

```python
# 读取记忆
lines = await get_memory(
    path="MEMORY.md",
    from_line=0,
    lines=100
)

# 写入记忆（自动同步到 OpenViking）
await write_memory(
    path="memory/2026-03-10.md",
    content="# 今日工作\n...",
    sync_to_openviking=True
)
```

**特性**:
- 完全兼容现有的 MEMORY.md 和 memory/*.md 系统
- 写入时自动同步到 OpenViking
- 支持相对路径和绝对路径
- 错误处理和日志记录

### 3. 自动记忆提取

```python
# 从对话中自动提取记忆
await extract_and_store(
    text="用户希望使用性能优化策略，预算控制在1万以内",
    session_key="user_123_conversation",
    metadata={
        "user_id": "user_123",
        "conversation_id": "conv_456"
    }
)
```

**提取模式**:
- 用户偏好
- 项目状态
- 重要决策
- 技术选型
- 配置变更
- 问题解决
- 经验教训

### 4. 会话上下文加载

```python
# 加载会话上下文（智能分层）
context = await load_session_context(
    session_key="user_123_conversation",
    max_tokens=4000
)

# 返回内容
{
  "session_key": "user_123_conversation",
  "memories": [...],  # 相关记忆
  "max_tokens": 4000,
  "loaded_at": "2026-03-10T12:00:00",
  "memory_count": 5
}
```

### 5. 统计和维护

```python
# 获取统计信息
stats = await get_memory_stats()

# 返回内容
{
  "local": {
    "file_count": 25,
    "total_size_bytes": 524288,
    "total_size_mb": 0.5
  },
  "openviking": {
    "memory_count": 1000,
    "index_size": "10MB"
  },
  "workspace": "/root/.openclaw/workspace",
  "memory_dir": "/root/.openclaw/workspace/memory",
  "checked_at": "2026-03-10T12:00:00"
}

# 清理旧记忆
deleted = await cleanup_old_memories(days=30)
```

## 🔧 配置说明

### 环境变量

```bash
# OpenClaw 工作目录
export OPENCLAW_WORKSPACE="/root/.openclaw/workspace"

# OpenViking 服务器
export OPENVIKING_URL="http://localhost:1933"

# OpenViking API 密钥（可选）
export OPENVIKING_API_KEY="your-api-key"

# 启用降级模式
export OPENVIKING_ENABLE_FALLBACK="true"
```

### 配置文件

创建 `~/.openviking/ov.conf`:

```json
{
  "storage": {
    "workspace": "/root/.openviking/workspace"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "https://ark.cn-beijing.volces.com/api/v3",
      "api_key": "your-volcengine-api-key",
      "provider": "volcengine",
      "dimension": 1024,
      "model": "doubao-embedding-vision-250615"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "your-volcengine-api-key",
    "provider": "volcengine",
    "model": "doubao-seed-2-0-pro-260215",
    "max_concurrent": 100
  }
}
```

## 📊 分层记忆结构

### L0 层（热数据）
- **用途**: 核心偏好、常用策略
- **特点**: 高频访问，快速检索
- **示例**: 用户偏好、活跃项目状态

### L1 层（温数据）
- **用途**: 近期记忆、历史记录
- **特点**: 中频访问，相关度优先
- **示例**: 最近的对话、项目进展

### L2 层（冷数据）
- **用途**: 完整记录、归档数据
- **特点**: 低频访问，全量存储
- **示例**: 完整的历史记录、旧数据

## 🚀 使用方法

### 基础使用

```python
from openclaw_memory_integration import (
    search_memory,
    get_memory,
    write_memory,
    extract_and_store,
    load_session_context
)

# 搜索记忆
results = await search_memory("用户偏好")

# 读取记忆
content = await get_memory("MEMORY.md")

# 写入记忆
await write_memory("memory/2026-03-10.md", "# 今日工作\n...")

# 提取记忆
await extract_and_store(
    text="用户希望使用性能优化策略",
    session_key="session_123"
)

# 加载会话上下文
context = await load_session_context("session_123")
```

### 高级使用

```python
from openclaw_memory_integration import OpenClawMemoryIntegration

# 创建集成实例
async with OpenClawMemoryIntegration(
    workspace="/root/.openclaw/workspace",
    openviking_url="http://localhost:1933",
    enable_fallback=True
) as memory:
    # 使用记忆系统
    results = await memory.memory_search("查询内容")

    # 提取并存储
    await memory.extract_and_store(
        text="对话内容",
        session_key="session_key"
    )

    # 获取统计
    stats = await memory.get_memory_stats()

    # 清理旧记忆
    deleted = await memory.cleanup_old_memories(days=30)
```

## 🧪 测试方案

### 单元测试

```python
import pytest
from openclaw_memory_integration import OpenClawMemoryIntegration

@pytest.mark.asyncio
async def test_memory_search():
    """测试记忆搜索"""
    integration = OpenClawMemoryIntegration()
    results = await integration.memory_search("用户偏好", max_results=5)
    assert len(results) <= 5
    assert all("path" in r for r in results)
    assert all("score" in r for r in results)

@pytest.mark.asyncio
async def test_memory_write_and_read():
    """测试记忆读写"""
    integration = OpenClawMemoryIntegration()

    # 写入
    await integration.memory_write(
        "test_memory.md",
        "测试内容"
    )

    # 读取
    lines = await integration.memory_get("test_memory.md")
    assert len(lines) > 0
    assert "测试内容" in lines[0]
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_openviking_fallback():
    """测试 OpenViking 降级"""
    integration = OpenClawMemoryIntegration(
        openviking_url="http://invalid:1933",  # 无效地址
        enable_fallback=True
    )

    # 应该降级到本地搜索
    results = await integration.memory_search("测试")
    assert results  # 仍然有结果
```

## 📈 性能优化

### 缓存策略
- **搜索结果缓存**: 10 分钟过期
- **文件索引缓存**: 5 分钟过期
- **元数据缓存**: 15 分钟过期

### 批量操作
- **批量存储**: 减少网络开销
- **批量检索**: 提高响应速度
- **并发处理**: 异步提升性能

### 降级机制
- **自动降级**: OpenViking 不可用时自动切换到本地
- **超时控制**: 5 秒超时，避免阻塞
- **重试机制**: 3 次重试，指数退避

## 🔍 故障处理

### OpenViking 连接失败
```python
# 自动降级到本地文件搜索
results = await memory_search("查询")  # 仍然有效
```

### 磁盘空间不足
```python
# 清理旧记忆
await cleanup_old_memories(days=30)
```

### 数据不一致
```python
# 重建索引
integration._file_index = {}
integration._index_timestamp = None
```

## 📞 技术支持

### 联系方式
- 文档: `/root/.openclaw/workspace/OPENCLAW-OPENVIKING-INTEGRATION.md`
- 代码: `openclaw-memory-integration.py`
- 测试: `tests/test_openclaw_memory_integration.py`

### 问题反馈
- GitHub Issues
- 技术支持工单
- 在线社区

---

**文档版本**: v1.0
**最后更新**: 2026-03-10
**维护团队**: OpenClaw Architecture Team
