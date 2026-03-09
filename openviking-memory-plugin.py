"""
OpenViking Memory Plugin for OpenClaw

这是一个集成 OpenViking（字节跳动开源的 AI Agent 上下文数据库）到 OpenClaw 的插件。

功能：
1. 存储记忆到 OpenViking
2. 从 OpenViking 检索相关记忆
3. 自动记忆提取
4. 分层上下文加载 (L0/L1/L2)
"""

import aiohttp
import json
import asyncio
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
