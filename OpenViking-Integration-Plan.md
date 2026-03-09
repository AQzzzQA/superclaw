# 🚀 OpenViking 集成到 OpenClaw 本体 - 实施计划

> 任务：将 OpenViking（字节跳动开源的 AI Agent 上下文数据库）集成到 OpenClaw 本体中
> 时间：2026-03-09
> 优先级：高

---

## 📋 OpenViking 是什么？

### 核心概念
OpenViking 是一个专门为 AI Agents 设计的开源上下文数据库，采用「文件系统范式」统一管理记忆、资源和技能。

### 核心优势
1. **文件系统管理范式** - 统一管理记忆、资源、技能
2. **分层上下文加载** - L0/L1/L2 三层结构，按需加载，节省 Token 成本
3. **目录递归检索** - 原生文件系统检索方法，结合目录定位与语义搜索
4. **可视化检索轨迹** - 可观察上下文，便于调试
5. **自动会话管理** - 自动压缩内容、资源引用、工具调用，提取长期记忆

### 性能提升（实测数据）
- **任务完成率**：43% - 49% 提升
- **Token 成本**：83% - 96% 降低

---

## 🎯 集成目标

### 短期目标（1-2周）
1. ✅ 创建 OpenClaw Memory Plugin
2. ✅ 集成 OpenViking HTTP 服务
3. ✅ 实现上下文检索接口
4. ✅ 实现记忆存储接口
5. ✅ 实现记忆读取接口
6. ✅ 添加配置管理

### 中期目标（1个月）
1. ✅ 完善自动记忆提取
2. ✅ 优化检索策略
3. ✅ 添加可视化工具
4. ✅ 性能优化
5. ✅ 测试和验证

### 长期目标（2-3个月）
1. ✅ 完整的文档
2. ✅ 示例和教程
3. ✅ 社区支持
4. ✅ 持续优化

---

## 🏗️ 技术架构

### 组件设计

#### 1. OpenViking Server
```python
# 启动 OpenViking 服务器
openviking-server --with-bot
```

#### 2. OpenClaw Memory Plugin
```python
# OpenClaw 记忆插件
class OpenVikingMemoryPlugin:
    def __init__(self, config):
        self.server_url = config["server_url"]
        self.api_key = config["api_key"]

    async def store(self, key, value):
        # 存储记忆到 OpenViking
        await self._http_post("/api/memory/store", {key, value})

    async def retrieve(self, query, limit=10):
        # 从 OpenViking 检索记忆
        return await self._http_get("/api/memory/retrieve", {query, limit})
```

#### 3. 配置文件
```yaml
# ~/.openclaw/openviking.yaml
memory:
  enabled: true
  plugin: "openviking"
  server_url: "http://localhost:1933"
  api_key: "your-api-key"

context:
  provider: "openviking"
  workspace: "/root/.openviking/workspace"
```

---

## 📝 开发步骤

### Step 1: 安装 OpenViking
```bash
# 安装 OpenViking CLI
pip install openviking --upgrade --force-reinstall

# 安装 CLI 工具
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash

# 配置 OpenViking
mkdir -p ~/.openviking
cat > ~/.openviking/ov.conf << 'EOF'
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
EOF

# 配置 CLI
cat > ~/.openviking/ovcli.conf << 'EOF'
{
  "url": "http://localhost:1933",
  "timeout": 60.0,
  "output": "table"
}
EOF

# 启动服务器
openviking-server --with-bot
```

### Step 2: 创建 OpenClaw Memory Plugin
```python
# openviking-memory-plugin.py
import aiohttp
import json
from typing import Optional, List, Dict, Any

class OpenVikingMemoryPlugin:
    """OpenViking Memory Plugin for OpenClaw"""

    def __init__(self, server_url: str = "http://localhost:1933"):
        self.server_url = server_url
        self.session = aiohttp.ClientSession()

    async def store(self, key: str, value: str, metadata: Optional[Dict] = None):
        """存储记忆到 OpenViking"""
        try:
            async with self.session.post(
                f"{self.server_url}/api/memory/store",
                json={"key": key, "value": value, "metadata": metadata}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": await response.text()}
        except Exception as e:
            return {"error": str(e)}

    async def retrieve(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """从 OpenViking 检索记忆"""
        try:
            async with self.session.get(
                f"{self.server_url}/api/memory/retrieve",
                params={"query": query, "limit": limit, "threshold": threshold}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return []

    async def close(self):
        """关闭会话"""
        await self.session.close()
```

### Step 3: 集成到 OpenClaw
```python
# openclaw/openviking_integration.py
from openviking_memory_plugin import OpenVikingMemoryPlugin

class OpenClawWithOpenViking:
    """集成了 OpenViking 的 OpenClaw"""

    def __init__(self, config: Dict):
        # 初始化 OpenViking Memory Plugin
        self.memory = OpenVikingMemoryPlugin(
            server_url=config.get("server_url", "http://localhost:1933")
        )

    async def process_message(self, user_message: str, context: Dict):
        # 1. 从 OpenViking 检索相关记忆
        memories = await self.memory.retrieve(user_message, limit=5)

        # 2. 构建上下文
        context_with_memories = {
            **context,
            "retrieved_memories": memories
        }

        # 3. 处理消息
        response = await self._llm_generate(user_message, context_with_memories)

        # 4. 存储新记忆
        await self.memory.store(
            key=f"conversation_{context['conversation_id']}",
            value={"message": user_message, "response": response},
            metadata={"timestamp": context["timestamp"]}
        )

        return response

    async def _llm_generate(self, message: str, context: Dict):
        # 调用 LLM 生成响应
        # ...
        pass
```

### Step 4: 配置文件
```yaml
# ~/.openclaw/config.yaml
memory:
  enabled: true
  type: "openviking"
  openviking:
    server_url: "http://localhost:1933"
    api_key: "your-api-key"
    max_retrieved: 10
    threshold: 0.7

context:
  provider: "openviking"
  workspace: "/root/.openviking/workspace"
  layers:
    - L0  # Abstract - 快速检索
    - L1  # Overview - 规划阶段
    - L2  # Details - 深度阅读
```

---

## 🧪 测试计划

### 单元测试
```python
# tests/test_openviking_plugin.py
import pytest
from openviking_memory_plugin import OpenVikingMemoryPlugin

@pytest.mark.asyncio
async def test_store_memory():
    plugin = OpenVikingMemoryPlugin()
    result = await plugin.store("test_key", "test_value")
    assert "error" not in result

@pytest.mark.asyncio
async def test_retrieve_memory():
    plugin = OpenVikingMemoryPlugin()
    await plugin.store("test_key", "test_value")
    results = await plugin.retrieve("test_key")
    assert len(results) > 0
```

### 集成测试
```python
# tests/test_openclaw_integration.py
import pytest
from openclaw_with_openviking import OpenClawWithOpenViking

@pytest.mark.asyncio
async def test_memory_retrieval():
    agent = OpenClawWithOpenViking(config)
    response = await agent.process_message("Hello, how are you?", {})
    assert response is not None
```

---

## 📊 性能优化

### Token 成本优化
- **分层加载**：只加载 L0/L1，按需加载 L2
- **智能检索**：目录递归检索，减少不必要的内容
- **缓存策略**：缓存高频访问的记忆

### 检索效率优化
- **向量索引**：使用高效的向量数据库
- **并发检索**：支持并发检索请求
- **结果缓存**：缓存常见查询结果

---

## 📖 文档计划

1. **安装指南** - 如何安装和配置 OpenViking
2. **集成指南** - 如何集成到 OpenClaw
3. **API 文档** - 插件 API 文档
4. **示例代码** - 完整的使用示例
5. **故障排查** - 常见问题和解决方案

---

## 🚀 部署方案

### 本地部署
```bash
# 1. 启动 OpenViking 服务器
openviking-server --with-bot

# 2. 启动 OpenClaw
python3 main.py --with-openviking
```

### 生产部署（ECS）
```bash
# 1. 部署 OpenViking 到 ECS
# 参考：https://github.com/volcengine/OpenViking/blob/main/docs/en/getting-started/03-quickstart-server.md

# 2. 配置 OpenClaw 连接到生产环境
# ~/.openclaw/config.yaml
memory:
  openviking:
    server_url: "http://your-ecs-server:1933"

# 3. 启动 OpenClaw
python3 main.py --with-openviking
```

---

## ✅ 预期成果

### 功能完整度
- ✅ OpenViking Memory Plugin
- ✅ 上下文检索接口
- ✅ 记忆存储接口
- ✅ 自动记忆提取
- ✅ 配置管理
- ✅ 测试套件
- ✅ 完整文档

### 性能指标
- ✅ 任务完成率：提升 43% - 49%
- ✅ Token 成本：降低 83% - 96%
- ✅ 检索延迟：< 100ms
- ✅ 并发支持：10 个请求/秒

---

## 🎯 下一步行动

### 立即开始
1. ✅ 安装 OpenViking
2. ✅ 创建 Memory Plugin
3. ✅ 实现基础接口
4. ✅ 编写单元测试
5. ✅ 集成到 OpenClaw

### 后续优化
1. ⏳ 完善自动记忆提取
2. ⏳ 优化检索策略
3. ⏳ 添加可视化工具
4. ⏳ 性能优化
5. ⏳ 持续测试和验证

---

**🚀 准备开始集成 OpenViking 到 OpenClaw！**