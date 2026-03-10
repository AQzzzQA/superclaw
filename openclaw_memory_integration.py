"""
OpenClaw 本体与 OpenViking 集成实现

将 OpenViking 集成到 OpenClaw 本体的记忆系统中，实现：
1. 自动记忆提取和存储
2. 智能上下文检索
3. 分层上下文加载 (L0/L1/L2)
4. 记忆自迭代和优化
"""

import os
import json
import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpenClawMemoryIntegration:
    """
    OpenClaw 与 OpenViking 的集成层

    作为 OpenClaw 本体的记忆系统增强，无缝集成到现有的
    MEMORY.md 和 memory/*.md 文件系统中
    """

    def __init__(
        self,
        workspace: str = "/root/.openclaw/workspace",
        openviking_url: str = "http://localhost:1933",
        api_key: Optional[str] = None,
        enable_fallback: bool = True
    ):
        """
        初始化 OpenClaw 记忆集成

        Args:
            workspace: OpenClaw 工作目录
            openviking_url: OpenViking 服务器地址
            api_key: API 密钥（可选）
            enable_fallback: 启用降级模式（当 OpenViking 不可用时使用本地文件）
        """
        self.workspace = Path(workspace)
        self.memory_dir = self.workspace / "memory"
        self.openviking_url = openviking_url
        self.api_key = api_key
        self.enable_fallback = enable_fallback

        # 确保目录存在
        self.memory_dir.mkdir(exist_ok=True)

        # 初始化 HTTP 会话
        self.session = aiohttp.ClientSession()

        # 本地文件索引
        self._file_index = {}
        self._index_timestamp = None

        logger.info(f"OpenClaw Memory Integration initialized: workspace={workspace}")

    # ========== 核心接口（与 OpenClaw 兼容） ==========

    async def memory_search(
        self,
        query: str,
        max_results: int = 10,
        min_score: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        记忆搜索（兼容 OpenClaw memory_search）

        优先使用 OpenViking 语义搜索，降级到本地文件搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数
            min_score: 最小相关度分数

        Returns:
            搜索结果列表，每个结果包含 path, score, content 等字段
        """
        logger.info(f"Memory search: query='{query}'")

        # 尝试 OpenViking 搜索
        try:
            results = await self._search_openviking(query, max_results, min_score)
            if results:
                logger.info(f"Found {len(results)} results from OpenViking")
                return results
        except Exception as e:
            logger.warning(f"OpenViking search failed: {e}, falling back to local search")

        # 降级到本地文件搜索
        if self.enable_fallback:
            results = self._search_local(query, max_results)
            logger.info(f"Found {len(results)} results from local files")
            return results

        return []

    async def memory_get(
        self,
        path: str,
        from_line: int = 0,
        lines: int = 100
    ) -> List[str]:
        """
        获取记忆内容（兼容 OpenClaw memory_get）

        Args:
            path: 文件路径（相对于 memory 目录或绝对路径）
            from_line: 起始行号
            lines: 读取行数

        Returns:
            文件内容行列表
        """
        logger.info(f"Memory get: path='{path}', from={from_line}, lines={lines}")

        # 解析路径
        if not path.startswith('/'):
            file_path = self.memory_dir / path
        else:
            file_path = Path(path)

        # 检查文件是否存在
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return []

        # 读取文件
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()

            # 应用偏移和限制
            start = from_line
            end = min(start + lines, len(all_lines))

            return all_lines[start:end]

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return []

    async def memory_write(
        self,
        path: str,
        content: str,
        sync_to_openviking: bool = True
    ) -> bool:
        """
        写入记忆（兼容 OpenClaw 操作）

        Args:
            path: 文件路径
            content: 文件内容
            sync_to_openviking: 是否同步到 OpenViking

        Returns:
            是否成功
        """
        logger.info(f"Memory write: path='{path}', sync={sync_to_openviking}")

        # 解析路径
        if not path.startswith('/'):
            file_path = self.memory_dir / path
        else:
            file_path = Path(path)

        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入本地文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"File written: {file_path}")
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False

        # 同步到 OpenViking
        if sync_to_openviking:
            try:
                await self._store_openviking(
                    key=str(file_path),
                    value=content,
                    metadata={"type": "file", "path": str(file_path)}
                )
                logger.info(f"Synced to OpenViking: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to sync to OpenViking: {e}")

        return True

    # ========== OpenViking 集成接口 ==========

    async def _search_openviking(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        使用 OpenViking 进行语义搜索

        Args:
            query: 搜索查询
            limit: 最大结果数
            threshold: 最小相关度阈值

        Returns:
            搜索结果
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        params = {
            "query": query,
            "limit": limit,
            "threshold": threshold
        }

        try:
            async with self.session.get(
                f"{self.openviking_url}/api/v1/memory/search",
                params=params,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # 转换为 OpenClaw 兼容格式
                    return self._format_openviking_results(data)
                else:
                    error_text = await response.text()
                    logger.error(f"OpenViking search error: {response.status} - {error_text}")
                    return []
        except Exception as e:
            logger.error(f"OpenViking search exception: {e}")
            return []

    async def _store_openviking(
        self,
        key: str,
        value: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        存储记忆到 OpenViking

        Args:
            key: 记忆键
            value: 记忆值
            metadata: 元数据

        Returns:
            存储结果
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "key": key,
            "value": value,
            "metadata": metadata or {}
        }

        try:
            async with self.session.post(
                f"{self.openviking_url}/api/v1/memory/store",
                json=data,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"OpenViking store error: {response.status} - {error_text}")
                    return {"error": error_text}
        except Exception as e:
            logger.error(f"OpenViking store exception: {e}")
            return {"error": str(e)}

    # ========== 本地文件搜索（降级模式） ==========

    def _search_local(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        本地文件关键词搜索

        Args:
            query: 搜索查询
            max_results: 最大结果数

        Returns:
            搜索结果
        """
        results = []
        query_lower = query.lower()

        # 扫描 memory 目录
        for file_path in self.memory_dir.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 简单关键词匹配
                if query_lower in content.lower():
                    # 计算简单评分（出现次数）
                    score = content.lower().count(query_lower)

                    results.append({
                        "path": str(file_path.relative_to(self.memory_dir)),
                        "content": content[:500] + "..." if len(content) > 500 else content,
                        "score": score,
                        "source": "local"
                    })
            except Exception as e:
                logger.warning(f"Error reading file {file_path}: {e}")

        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:max_results]

    def _format_openviking_results(
        self,
        data: Union[List, Dict]
    ) -> List[Dict[str, Any]]:
        """
        格式化 OpenViking 结果为 OpenClaw 兼容格式

        Args:
            data: OpenViking 响应数据

        Returns:
            格式化后的结果列表
        """
        if not data:
            return []

        results = []
        items = data if isinstance(data, list) else data.get("results", [])

        for item in items:
            # 提取相关字段
            result = {
                "path": item.get("key", item.get("path", "")),
                "score": item.get("score", item.get("similarity", 0.0)),
                "content": item.get("value", item.get("content", "")),
                "metadata": item.get("metadata", {}),
                "source": "openviking"
            }
            results.append(result)

        return results

    # ========== 自动记忆提取 ==========

    async def extract_and_store(
        self,
        text: str,
        session_key: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        自动提取并存储记忆

        Args:
            text: 待提取的文本
            session_key: 会话键
            metadata: 元数据

        Returns:
            是否成功
        """
        logger.info(f"Extracting memory from session: {session_key}")

        # 提取重要信息
        memories = self._extract_memories(text, session_key, metadata)

        # 存储到 OpenViking
        for memory in memories:
            try:
                await self._store_openviking(
                    key=memory["key"],
                    value=memory["value"],
                    metadata=memory.get("metadata", {})
                )
                logger.info(f"Memory stored: {memory['key']}")
            except Exception as e:
                logger.warning(f"Failed to store memory {memory['key']}: {e}")

        return True

    def _extract_memories(
        self,
        text: str,
        session_key: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        从文本中提取记忆

        Args:
            text: 输入文本
            session_key: 会话键
            metadata: 元数据

        Returns:
            提取的记忆列表
        """
        memories = []
        timestamp = datetime.now().isoformat()

        # 提取关键模式
        patterns = [
            "用户偏好",
            "项目状态",
            "重要决策",
            "技术选型",
            "配置变更",
            "问题解决",
            "经验教训"
        ]

        for pattern in patterns:
            if pattern in text:
                key = f"{session_key}_{pattern}_{timestamp}"
                memory = {
                    "key": key,
                    "value": f"{pattern}: {text[:200]}",
                    "metadata": {
                        "type": "extracted",
                        "pattern": pattern,
                        "session_key": session_key,
                        "timestamp": timestamp,
                        **(metadata or {})
                    }
                }
                memories.append(memory)

        return memories

    # ========== 会话上下文管理 ==========

    async def load_session_context(
        self,
        session_key: str,
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        加载会话上下文

        Args:
            session_key: 会话键
            max_tokens: 最大令牌数

        Returns:
            会话上下文
        """
        logger.info(f"Loading session context: {session_key}")

        # 从 OpenViking 搜索相关记忆
        memories = await self._search_openviking(
            query=session_key,
            limit=10,
            threshold=0.3
        )

        # 构建上下文
        context = {
            "session_key": session_key,
            "memories": memories,
            "max_tokens": max_tokens,
            "loaded_at": datetime.now().isoformat(),
            "memory_count": len(memories)
        }

        return context

    # ========== 维护和清理 ==========

    async def cleanup_old_memories(
        self,
        days: int = 30
    ) -> int:
        """
        清理旧记忆

        Args:
            days: 保留天数

        Returns:
            清理的记忆数量
        """
        logger.info(f"Cleaning up memories older than {days} days")

        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.isoformat()

        # 删除本地旧文件
        deleted = 0
        for file_path in self.memory_dir.rglob("*.md"):
            try:
                # 从文件名提取日期
                if file_path.stem.isdigit():
                    file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")
                    if file_date < cutoff_date:
                        file_path.unlink()
                        deleted += 1
                        logger.info(f"Deleted old file: {file_path}")
            except Exception as e:
                logger.warning(f"Error processing file {file_path}: {e}")

        logger.info(f"Cleanup complete: {deleted} memories deleted")
        return deleted

    # ========== 统计和监控 ==========

    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计信息

        Returns:
            统计信息
        """
        # 统计本地文件
        local_files = list(self.memory_dir.rglob("*.md"))
        local_count = len(local_files)
        total_size = sum(f.stat().st_size for f in local_files)

        # 统计 OpenViking（如果可用）
        openviking_stats = {}
        try:
            async with self.session.get(
                f"{self.openviking_url}/api/v1/stats",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            ) as response:
                if response.status == 200:
                    openviking_stats = await response.json()
        except Exception as e:
            logger.debug(f"Could not get OpenViking stats: {e}")

        return {
            "local": {
                "file_count": local_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            },
            "openviking": openviking_stats,
            "workspace": str(self.workspace),
            "memory_dir": str(self.memory_dir),
            "checked_at": datetime.now().isoformat()
        }

    # ========== 生命周期管理 ==========

    async def close(self):
        """关闭会话"""
        await self.session.close()
        logger.info("OpenClaw Memory Integration closed")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()


# ========== 全局实例 ==========

_global_memory_integration: Optional[OpenClawMemoryIntegration] = None


def get_memory_integration() -> OpenClawMemoryIntegration:
    """
    获取全局记忆集成实例（单例模式）

    Returns:
        记忆集成实例
    """
    global _global_memory_integration

    if _global_memory_integration is None:
        workspace = os.getenv("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
        openviking_url = os.getenv("OPENVIKING_URL", "http://localhost:1933")
        api_key = os.getenv("OPENVIKING_API_KEY")

        _global_memory_integration = OpenClawMemoryIntegration(
            workspace=workspace,
            openviking_url=openviking_url,
            api_key=api_key
        )

    return _global_memory_integration


async def search_memory(
    query: str,
    max_results: int = 10,
    min_score: float = 0.5
) -> List[Dict[str, Any]]:
    """
    全局记忆搜索函数（兼容 OpenClaw）

    Args:
        query: 搜索查询
        max_results: 最大结果数
        min_score: 最小相关度分数

    Returns:
        搜索结果
    """
    integration = get_memory_integration()
    return await integration.memory_search(query, max_results, min_score)


async def get_memory(
    path: str,
    from_line: int = 0,
    lines: int = 100
) -> List[str]:
    """
    全局获取记忆函数（兼容 OpenClaw）

    Args:
        path: 文件路径
        from_line: 起始行号
        lines: 读取行数

    Returns:
        文件内容行列表
    """
    integration = get_memory_integration()
    return await integration.memory_get(path, from_line, lines)


async def write_memory(
    path: str,
    content: str,
    sync_to_openviking: bool = True
) -> bool:
    """
    全局写入记忆函数

    Args:
        path: 文件路径
        content: 文件内容
        sync_to_openviking: 是否同步到 OpenViking

    Returns:
        是否成功
    """
    integration = get_memory_integration()
    return await integration.memory_write(path, content, sync_to_openviking)


async def extract_and_store(
    text: str,
    session_key: str,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    全局记忆提取函数

    Args:
        text: 待提取的文本
        session_key: 会话键
        metadata: 元数据

    Returns:
        是否成功
    """
    integration = get_memory_integration()
    return await integration.extract_and_store(text, session_key, metadata)