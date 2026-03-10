"""
OpenViking Memory Plugin for OpenClaw

这是一个集成 OpenViking（字节跳动开源的 AI Agent 上下文数据库）到 OpenClaw 的插件。

功能：
1. 存储记忆到 OpenViking
2. 从 OpenViking 检索相关记忆
3. 自动记忆提取
4. 分层上下文加载 (L0/L1/L2)
5. 兼容 OpenClaw Memory 系统
"""

import aiohttp
import json
import asyncio
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 兼容 OpenClaw Memory 系统
try:
    from memory import memory_get, memory_search, memory_write
except ImportError:
    # fallback to basic file operations
    def memory_get(path: str, from_line: int = 0, lines: int = 100):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines_list = f.readlines()
                start = from_line if from_line < len(lines_list) else 0
                end = min(start + lines, len(lines_list))
                return lines_list[start:end]
        except FileNotFoundError:
            return []
    
    def memory_search(query: str, max_results: int = 10):
        # Simple keyword search in memory files
        results = []
        memory_dir = os.path.join(os.path.dirname(__file__), 'memory')
        if os.path.exists(memory_dir):
            for file in os.listdir(memory_dir):
                if file.endswith('.md'):
                    try:
                        with open(os.path.join(memory_dir, file), 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                results.append({
                                    'path': file,
                                    'content': content[:200] + '...' if len(content) > 200 else content
                                })
                    except:
                        continue
        return results[:max_results]
    
    def memory_write(path: str, content: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


class OpenVikingMemoryPlugin:
    """
    OpenViking Memory Plugin for OpenClaw

    集成 OpenViking（字节跳动开源的 AI Agent 上下文数据库）到 OpenClaw
    支持存储、检索、自动记忆提取和分层上下文加载
    """

    def __init__(
        self,
        server_url: str = "http://localhost:1933",
        api_key: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3
    ):
        """
        初始化 OpenViking Memory Plugin

        Args:
            server_url: OpenViking 服务器地址（默认：http://localhost:1933）
            api_key: OpenViking API密钥（可选）
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.server_url = server_url.rstrip("/")
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None

        logger.info(f"OpenViking Memory Plugin initialized: {self.server_url}")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def _http_post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        发送 POST 请求

        Args:
            endpoint: API 端点
            data: 请求数据
            retry_count: 当前重试次数

        Returns:
            响应数据
        """
        try:
            async with self.session.post(
                f"{self.server_url}{endpoint}",
                json=data,
                headers=self._get_headers()
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"HTTP {response.status}: {error_text}")
                    return {"error": error_text, "status_code": response.status}

        except aiohttp.ClientError as e:
            if retry_count < self.max_retries:
                logger.warning(f"Retry {retry_count + 1}/{self.max_retries}: {e}")
                await asyncio.sleep(1)  # 等待 1 秒后重试
                return await self._http_post(endpoint, data, retry_count + 1)
            else:
                logger.error(f"Failed after {self.max_retries} retries: {e}")
                return {"error": str(e)}

    async def _http_get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        发送 GET 请求

        Args:
            endpoint: API 端点
            params: 查询参数
            retry_count: 当前重试次数

        Returns:
            响应数据
        """
        try:
            async with self.session.get(
                f"{self.server_url}{endpoint}",
                params=params,
                headers=self._get_headers()
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"HTTP {response.status}: {error_text}")
                    return []

        except aiohttp.ClientError as e:
            if retry_count < self.max_retries:
                logger.warning(f"Retry {retry_count + 1}/{self.max_retries}: {e}")
                await asyncio.sleep(1)  # 等待 1 秒后重试
                return await self._http_get(endpoint, params, retry_count + 1)
            else:
                logger.error(f"Failed after {self.max_retries} retries: {e}")
                return []

    # ============ 存储接口 ============

    async def store(
        self,
        key: str,
        value: Union[str, Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
        layer: str = "L1"
    ) -> Dict[str, Any]:
        """
        存储记忆到 OpenViking

        Args:
            key: 记忆键
            value: 记忆值
            metadata: 元数据（可选）
            layer: 上下文层（L0/L1/L2，默认：L1）

        Returns:
            存储结果
        """
        data = {
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "layer": layer
        }

        logger.info(f"Storing memory: {key} (layer: {layer})")
        return await self._http_post("/api/memory/store", data)

    async def store_batch(
        self,
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        批量存储记忆

        Args:
            items: 记忆项列表

        Returns:
            存储结果
        """
        logger.info(f"Batch storing {len(items)} memories")
        return await self._http_post("/api/memory/store_batch", {"items": items})

    # ============ 检索接口 ============

    async def search_memory(
        self,
        query: str,
        max_results: int = 10,
        layers: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        搜索相关记忆

        Args:
            query: 搜索查询
            max_results: 最大结果数
            layers: 上下文层过滤（可选）
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）

        Returns:
            搜索结果列表
        """
        params = {
            "query": query,
            "max_results": max_results,
            "layers": layers or ["L0", "L1", "L2"],
            "start_time": start_time,
            "end_time": end_time
        }

        logger.info(f"Searching memories: {query}")
        results = await self._http_get("/api/memory/search", params)
        
        # 兼容 OpenClaw Memory 系统
        if not results or isinstance(results, dict) and 'error' in results:
            fallback_results = memory_search(query, max_results)
            for result in fallback_results:
                result['source'] = 'fallback'
            return fallback_results
        
        return results

    async def get_memory(self, key: str) -> Optional[Dict[str, Any]]:
        """
        获取特定记忆

        Args:
            key: 记忆键

        Returns:
            记忆数据
        """
        result = await self._http_get(f"/api/memory/{key}")
        return result[0] if result else None

    async def get_layer_memories(self, layer: str) -> List[Dict[str, Any]]:
        """
        获取特定层的所有记忆

        Args:
            layer: 上下文层（L0/L1/L2）

        Returns:
            记忆列表
        """
        result = await self._http_get(f"/api/memory/layer/{layer}")
        return result or []

    # ============ OpenClaw 兼容接口 ============

    async def store_memory(self, session_key: str, content: str, metadata: Optional[Dict] = None):
        """
        兼容 OpenClaw Memory 系统的记忆存储接口
        
        Args:
            session_key: 会话键
            content: 记忆内容
            metadata: 元数据
        """
        # 格式：日期_会话键_类型
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        memory_key = f"{timestamp}_{session_key}"
        
        if metadata is None:
            metadata = {}
        metadata.update({
            "session_key": session_key,
            "created_at": timestamp,
            "source": "openclaw"
        })
        
        return await self.store(memory_key, content, metadata, layer="L1")

    async def load_context(self, session_key: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        加载上下文，兼容 OpenClaw 会话系统
        
        Args:
            session_key: 会话键
            max_tokens: 最大令牌数
        """
        # 从 OpenViking 获取相关记忆
        recent_memories = await self.search_memory(
            query=session_key,
            max_results=10,
            layers=["L0", "L1"]
        )
        
        # 构建上下文
        context = {
            "session_key": session_key,
            "memories": recent_memories,
            "max_tokens": max_tokens,
            "created_at": datetime.now().isoformat()
        }
        
        return context

    # ============ 自动记忆提取 ============

    async def extract_memory(
        self,
        text: str,
        session_key: str,
        extraction_rules: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        从文本中自动提取记忆

        Args:
            text: 输入文本
            session_key: 会话键
            extraction_rules: 提取规则（可选）

        Returns:
            提取的记忆列表
        """
        # 默认提取规则
        if extraction_rules is None:
            extraction_rules = {
                "min_length": 10,
                "key_phrases": ["用户偏好", "项目状态", "重要决策", "技术选型"],
                "timestamp": True
            }
        
        # 这里可以实现 NLP 处理逻辑
        # 现在使用简单的关键词提取
        extracted_memories = []
        
        if len(text) >= extraction_rules["min_length"]:
            memory = {
                "key": f"{session_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "value": text,
                "metadata": {
                    "session_key": session_key,
                    "extraction_method": "keyword",
                    "extraction_rules": extraction_rules,
                    "timestamp": datetime.now().isoformat()
                },
                "layer": "L1"
            }
            extracted_memories.append(memory)
        
        if extracted_memories:
            await self.store_batch(extracted_memories)
        
        return extracted_memories

    async def retrieve(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.7,
        layer: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        从 OpenViking 检索记忆

        Args:
            query: 查询文本
            limit: 返回结果数量（默认：10）
            threshold: 相似度阈值（默认：0.7）
            layer: 上下文层（可选）

        Returns:
            检索结果列表
        """
        params = {
            "query": query,
            "limit": limit,
            "threshold": threshold
        }
        if layer:
            params["layer"] = layer

        logger.info(f"Retrieving memories: {query} (limit: {limit})")
        results = await self._http_get("/api/memory/retrieve", params)

        if not isinstance(results, list):
            logger.error(f"Unexpected response type: {type(results)}")
            return []

        return results[:limit]

    async def retrieve_by_key(
        self,
        key: str
    ) -> Optional[Dict[str, Any]]:
        """
        通过键检索记忆

        Args:
            key: 记忆键

        Returns:
            记忆数据或None
        """
        logger.info(f"Retrieving memory by key: {key}")
        results = await self.retrieve(query=key, limit=1)

        if results:
            return results[0]
        return None

    # ============ 目录检索接口 ============

    async def list_directory(
        self,
        uri: str,
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        列出目录内容

        Args:
            uri: viking:// URI
            recursive: 是否递归列出

        Returns:
            文件/目录列表
        """
        params = {
            "uri": uri,
            "recursive": recursive
        }

        logger.info(f"Listing directory: {uri}")
        results = await self._http_get("/api/fs/list", params)

        if not isinstance(results, list):
            logger.error(f"Unexpected response type: {type(results)}")
            return []

        return results

    async def find(
        self,
        query: str,
        uri: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        在目录中搜索

        Args:
            query: 查询文本
            uri: 起始 URI（可选）
            limit: 返回结果数量

        Returns:
            搜索结果列表
        """
        params = {
            "query": query,
            "limit": limit
        }
        if uri:
            params["uri"] = uri

        logger.info(f"Finding: {query} (uri: {uri})")
        results = await self._http_get("/api/fs/find", params)

        if not isinstance(results, list):
            logger.error(f"Unexpected response type: {type(results)}")
            return []

        return results[:limit]

    # ============ 自动记忆提取接口 ============

    async def extract_memories_from_conversation(
        self,
        conversation: List[Dict[str, Any]],
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        从对话中自动提取记忆

        Args:
            conversation: 对话列表
            conversation_id: 对话ID

        Returns:
            提取的记忆统计
        """
        extracted = []

        for i, message in enumerate(conversation):
            # 提取用户偏好
            if message.get("role") == "user":
                # 检测偏好
                if "prefer" in message.get("content", "").lower():
                    extracted.append({
                        "key": f"preference_{conversation_id}_{i}",
                        "value": message["content"],
                        "metadata": {
                            "type": "preference",
                            "conversation_id": conversation_id,
                            "timestamp": message.get("timestamp", datetime.now().isoformat())
                        },
                        "layer": "L1"
                    })

            # 提取任务记忆
            if message.get("role") == "assistant":
                content = message.get("content", "")
                if "task" in content.lower() or "goal" in content.lower():
                    extracted.append({
                        "key": f"task_{conversation_id}_{i}",
                        "value": content,
                        "metadata": {
                            "type": "task",
                            "conversation_id": conversation_id,
                            "timestamp": message.get("timestamp", datetime.now().isoformat())
                        },
                        "layer": "L1"
                    })

        # 批量存储提取的记忆
        if extracted:
            logger.info(f"Extracted {len(extracted)} memories from conversation {conversation_id}")
            await self.store_batch(extracted)

        return {
            "extracted_count": len(extracted),
            "conversation_id": conversation_id
        }

    # ============ 工具方法 ============

    async def health_check(self) -> bool:
        """
        检查 OpenViking 服务器健康状态

        Returns:
            服务器是否健康
        """
        try:
            async with self.session.get(f"{self.server_url}/health") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """
        获取 OpenViking 统计信息

        Returns:
            统计数据
        """
        logger.info("Getting OpenViking stats")
        return await self._http_get("/api/stats", {})


# ============ 使用示例 ============

async def main():
    """使用示例"""

    async with OpenVikingMemoryPlugin(server_url="http://localhost:1933") as plugin:
        # 1. 检查服务器健康状态
        if not await plugin.health_check():
            print("OpenViking 服务器未启动")
            return

        # 2. 存储记忆
        result = await plugin.store(
            key="user_preference",
            value={"writing_style": "简洁、直接"},
            metadata={"type": "preference", "user_id": "test_user"},
            layer="L1"
        )
        print(f"存储结果: {result}")

        # 3. 检索记忆
        memories = await plugin.retrieve(query="写作风格", limit=5)
        print(f"检索到 {len(memories)} 条记忆:")
        for memory in memories:
            print(f"  - {memory['key']}: {memory.get('value', '')[:50]}")

        # 4. 列出目录
        files = await plugin.list_directory("viking://user/memories/")
        print(f"目录内容: {files}")

        # 5. 搜索文件
        search_results = await plugin.find(query="preference")
        print(f"搜索结果: {search_results}")

        # 6. 获取统计信息
        stats = await plugin.get_stats()
        print(f"统计信息: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
