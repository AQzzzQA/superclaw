"""
OpenClaw with OpenViking Integration

将 OpenViking（字节跳动开源的 AI Agent 上下文数据库）集成到 OpenClaw 本体
实现自动记忆提取、分层上下文加载、智能检索等功能
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from openviking_memory_plugin import OpenVikingMemoryPlugin

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OpenClawWithOpenViking:
    """
    集成了 OpenViking 的 OpenClaw

    功能：
    1. 自动记忆提取和存储
    2. 智能上下文检索
    3. 分层上下文加载 (L0/L1/L2)
    4. 记忆自迭代
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        memory_plugin: Optional[OpenVikingMemoryPlugin] = None
    ):
        """
        初始化 OpenClaw with OpenViking

        Args:
            config: 配置字典
            memory_plugin: OpenViking Memory Plugin 实例（可选）
        """
        self.config = config or self._default_config()

        # 初始化 Memory Plugin
        self.memory = memory_plugin or OpenVikingMemoryPlugin(
            server_url=self.config.get("server_url", "http://localhost:1933"),
            api_key=self.config.get("api_key"),
            timeout=self.config.get("timeout", 60)
        )

        # 对话历史
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

        logger.info("OpenClaw with OpenViking initialized")

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "server_url": "http://localhost:1933",
            "api_key": None,
            "timeout": 60,
            "max_retrieved_memories": 10,
            "retrieval_threshold": 0.7,
            "auto_extract_memories": True,
            "context_layer": "L1"  # 默认加载 L1 层
        }

    # ============ 记忆管理 ============

    async def store_memory(
        self,
        key: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None,
        layer: str = "L1"
    ) -> Dict[str, Any]:
        """
        存储记忆

        Args:
            key: 记忆键
            value: 记忆值
            metadata: 元数据
            layer: 上下文层

        Returns:
            存储结果
        """
        logger.info(f"Storing memory: {key}")
        return await self.memory.store(key, value, metadata, layer)

    async def retrieve_memories(
        self,
        query: str,
        limit: int = None,
        layer: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        检索记忆

        Args:
            query: 查询文本
            limit: 返回数量
            layer: 上下文层

        Returns:
            记忆列表
        """
        limit = limit or self.config.get("max_retrieved_memories", 10)
        threshold = self.config.get("retrieval_threshold", 0.7)

        logger.info(f"Retrieving memories: {query}")
        return await self.memory.retrieve(query, limit, threshold, layer)

    # ============ 消息处理 ============

    async def process_message(
        self,
        message: str,
        conversation_id: str,
        role: str = "user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        处理消息（用户或助手）

        Args:
            message: 消息内容
            conversation_id: 对话ID
            role: 角色（user/assistant）
            metadata: 元数据

        Returns:
            处理结果
        """
        timestamp = datetime.now().isoformat()

        # 1. 存储消息到对话历史
        self._add_to_conversation(
            conversation_id=conversation_id,
            message={
                "content": message,
                "role": role,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }
        )

        # 2. 如果是用户消息，检索相关记忆
        if role == "user":
            # 检索相关记忆
            retrieved = await self.retrieve_memories(
                query=message,
                limit=self.config.get("max_retrieved_memories", 10),
                layer=self.config.get("context_layer", "L1")
            )

            logger.info(f"Retrieved {len(retrieved)} memories")

            # 3. 自动提取新记忆
            if self.config.get("auto_extract_memories", True):
                extracted = await self._extract_and_store_memories(
                    conversation_id=conversation_id
                )
                logger.info(f"Extracted {extracted['extracted_count']} new memories")

            return {
                "retrieved_memories": retrieved,
                "conversation_id": conversation_id,
                "timestamp": timestamp
            }

        return {
            "conversation_id": conversation_id,
            "timestamp": timestamp
        }

    # ============ 对话历史管理 ============

    def _add_to_conversation(
        self,
        conversation_id: str,
        message: Dict[str, Any]
    ) -> None:
        """添加消息到对话历史"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append(message)

        # 限制对话历史长度（防止内存溢出）
        max_history = self.config.get("max_conversation_length", 100)
        if len(self.conversations[conversation_id]) > max_history:
            self.conversations[conversation_id] = self.conversations[conversation_id][-max_history:]

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取对话历史"""
        history = self.conversations.get(conversation_id, [])
        return history[-limit:]

    # ============ 自动记忆提取 ============

    async def _extract_and_store_memories(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        自动提取并存储记忆

        Args:
            conversation_id: 对话ID

        Returns:
            提取结果
        """
        conversation = self.conversations.get(conversation_id, [])

        if not conversation:
            return {"extracted_count": 0, "conversation_id": conversation_id}

        # 调用 OpenViking Memory Plugin 的提取方法
        result = await self.memory.extract_memories_from_conversation(
            conversation=conversation,
            conversation_id=conversation_id
        )

        return result

    # ============ 上下文构建 ============

    async def build_context(
        self,
        query: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        构建上下文

        Args:
            query: 查询文本
            conversation_id: 对话ID（可选）

        Returns:
            上下文字典
        """
        context = {}

        # 1. 检索相关记忆
        memories = await self.retrieve_memories(
            query=query,
            limit=self.config.get("max_retrieved_memories", 10),
            layer=self.config.get("context_layer", "L1")
        )
        context["retrieved_memories"] = memories

        # 2. 获取对话历史
        if conversation_id:
            history = self.get_conversation_history(
                conversation_id=conversation_id,
                limit=10
            )
            context["conversation_history"] = history

        # 3. 添加检索统计
        context["retrieval_stats"] = {
            "memories_retrieved": len(memories),
            "history_length": len(context.get("conversation_history", [])),
            "timestamp": datetime.now().isoformat()
        }

        return context

    # ============ 工具方法 ============

    async def health_check(self) -> bool:
        """检查 OpenViking 服务器健康状态"""
        return await self.memory.health_check()

    async def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = await self.memory.get_stats()

        # 添加 OpenClaw 特定统计
        stats["openclaw"] = {
            "conversations": len(self.conversations),
            "total_messages": sum(
                len(conv) for conv in self.conversations.values()
            ),
            "config": self.config
        }

        return stats

    async def close(self) -> None:
        """关闭连接"""
        if self.memory:
            await self.memory.close()


# ============ 使用示例 ============

async def main():
    """使用示例"""

    # 初始化 OpenClaw with OpenViking
    async with OpenClawWithOpenViking(
        config={
            "server_url": "http://localhost:1933",
            "max_retrieved_memories": 5,
            "auto_extract_memories": True,
            "context_layer": "L1"
        }
    ) as agent:

        # 1. 检查健康状态
        if not await agent.health_check():
            print("OpenViking 服务器未启动")
            return

        # 2. 存储用户偏好
        await agent.store_memory(
            key="user_writing_style",
            value="简洁、直接",
            metadata={"type": "preference", "user_id": "demo_user"},
            layer="L1"
        )

        # 3. 处理用户消息
        result = await agent.process_message(
            message="帮我写一个Python脚本",
            conversation_id="demo_conversation",
            role="user"
        )

        print(f"处理结果:")
        print(f"  检索到 {len(result.get('retrieved_memories', []))} 条记忆")
        print(f"  对话ID: {result['conversation_id']}")

        # 4. 构建上下文
        context = await agent.build_context(
            query="Python脚本开发",
            conversation_id="demo_conversation"
        )

        print(f"\n上下文:")
        print(f"  记忆数量: {len(context.get('retrieved_memories', []))}")
        print(f"  历史长度: {len(context.get('conversation_history', []))}")

        # 5. 获取统计信息
        stats = await agent.get_stats()
        print(f"\n统计信息:")
        print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
