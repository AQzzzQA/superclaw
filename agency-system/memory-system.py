#!/usr/bin/env python3
"""
多层次记忆系统
支持短期记忆、长期记忆、共享记忆
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"      # 短期记忆（当前会话）
    LONG_TERM = "long_term"        # 长期记忆（持久化）
    SHARED = "shared"               # 共享记忆（协作池）


class MemoryCategory(Enum):
    """记忆分类"""
    EXPERIENCE = "experience"       # 经验教训
    KNOWLEDGE = "knowledge"         # 知识库
    TASK = "task"                   # 任务历史
    COLLABORATION = "collaboration" # 协作历史
    PERFORMANCE = "performance"     # 性能数据


@dataclass
class MemoryItem:
    """记忆项"""
    id: str
    agent_id: str
    category: MemoryCategory
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5        # 0.0 - 1.0
    access_count: int = 0
    last_accessed: str = ""
    created_at: str = ""
    expires_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.last_accessed:
            self.last_accessed = self.created_at
        if not self.id:
            # 基于内容和时间生成唯一ID
            content_hash = hashlib.md5(
                f"{self.agent_id}{self.category.value}{self.content}{self.created_at}".encode()
            ).hexdigest()[:16]
            self.id = f"mem_{content_hash}"

    def to_dict(self):
        """转换为字典"""
        return asdict(self)

    def access(self):
        """访问记忆（更新访问计数和时间）"""
        self.access_count += 1
        self.last_accessed = datetime.now().isoformat()

    def is_expired(self) -> bool:
        """检查是否过期"""
        if not self.expires_at:
            return False
        expires_at = datetime.fromisoformat(self.expires_at)
        return datetime.now() > expires_at


class MemorySystem:
    """记忆系统"""

    def __init__(self):
        self.short_term: Dict[str, MemoryItem] = {}
        self.long_term: Dict[str, MemoryItem] = {}
        self.shared: Dict[str, MemoryItem] = {}

    def _generate_key(self, agent_id: str, memory_type: MemoryType) -> str:
        """生成存储键"""
        return f"{memory_type.value}_{agent_id}"

    def store(
        self,
        agent_id: str,
        category: MemoryCategory,
        content: str,
        memory_type: MemoryType = MemoryType.SHORT_TERM,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
        expires_hours: Optional[int] = None
    ) -> MemoryItem:
        """存储记忆"""
        # 计算过期时间
        expires_at = None
        if expires_hours:
            expires_at = (datetime.now() + timedelta(hours=expires_hours)).isoformat()

        # 创建记忆项
        memory = MemoryItem(
            agent_id=agent_id,
            category=category,
            content=content,
            memory_type=memory_type,
            importance=importance,
            metadata=metadata or {},
            expires_at=expires_at
        )

        # 存储到对应的记忆类型
        if memory_type == MemoryType.SHORT_TERM:
            self.short_term[memory.id] = memory
        elif memory_type == MemoryType.LONG_TERM:
            self.long_term[memory.id] = memory
        elif memory_type == MemoryType.SHARED:
            self.shared[memory.id] = memory

        print(f"💾 记忆已存储: {category.value} ({memory_type.value}) - {content[:50]}...")
        return memory

    def recall(
        self,
        agent_id: str,
        category: Optional[MemoryCategory] = None,
        memory_type: MemoryType = MemoryType.SHORT_TERM,
        limit: int = 10
    ) -> List[MemoryItem]:
        """回忆记忆"""
        # 选择记忆类型
        if memory_type == MemoryType.SHORT_TERM:
            memories = list(self.short_term.values())
        elif memory_type == MemoryType.LONG_TERM:
            memories = list(self.long_term.values())
        elif memory_type == MemoryType.SHARED:
            memories = list(self.shared.values())
        else:
            memories = []

        # 过滤智能体
        if agent_id != "all":
            memories = [m for m in memories if m.agent_id == agent_id]

        # 过滤分类
        if category:
            memories = [m for m in memories if m.category == category]

        # 过滤过期记忆
        memories = [m for m in memories if not m.is_expired()]

        # 按重要性和访问次数排序
        memories.sort(key=lambda m: (m.importance, m.access_count), reverse=True)

        # 更新访问计数
        for memory in memories[:limit]:
            memory.access()

        return memories[:limit]

    def search(
        self,
        query: str,
        agent_id: str = "all",
        memory_type: MemoryType = MemoryType.SHORT_TERM,
        category: Optional[MemoryCategory] = None
    ) -> List[MemoryItem]:
        """搜索记忆"""
        # 获取所有记忆
        memories = self.recall(agent_id, category, memory_type, limit=1000)

        # 搜索匹配的内容
        results = []
        query_lower = query.lower()

        for memory in memories:
            if query_lower in memory.content.lower():
                # 计算匹配度
                match_count = memory.content.lower().count(query_lower)
                score = match_count * memory.importance

                results.append((memory, score))

        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)

        return [m for m, _ in results]

    def delete(self, memory_id: str, memory_type: MemoryType) -> bool:
        """删除记忆"""
        memory_dict = None
        if memory_type == MemoryType.SHORT_TERM:
            memory_dict = self.short_term
        elif memory_type == MemoryType.LONG_TERM:
            memory_dict = self.long_term
        elif memory_type == MemoryType.SHARED:
            memory_dict = self.shared

        if memory_dict and memory_id in memory_dict:
            del memory_dict[memory_id]
            print(f"🗑️ 记忆已删除: {memory_id}")
            return True

        return False

    def promote(self, memory_id: str, from_type: MemoryType, to_type: MemoryType) -> bool:
        """提升记忆（从短期到长期）"""
        # 找到原始记忆
        source_dict = None
        if from_type == MemoryType.SHORT_TERM:
            source_dict = self.short_term
        elif from_type == MemoryType.LONG_TERM:
            source_dict = self.long_term

        if memory_id not in source_dict:
            return False

        memory = source_dict[memory_id]

        # 删除原始记忆
        del source_dict[memory_id]

        # 添加到目标记忆
        if to_type == MemoryType.LONG_TERM:
            self.long_term[memory_id] = memory
        elif to_type == MemoryType.SHARED:
            self.shared[memory_id] = memory

        print(f"📈 记忆已提升: {memory_id} ({from_type.value} → {to_type.value})")
        return True

    def cleanup(self):
        """清理过期和低价值的短期记忆"""
        # 清理过期记忆
        expired_short = [m.id for m in self.short_term.values() if m.is_expired()]
        for mem_id in expired_short:
            del self.short_term[mem_id]

        # 清理低价值记忆（重要性 < 0.3）
        low_value = [m.id for m in self.short_term.values() if m.importance < 0.3]
        for mem_id in low_value:
            del self.short_term[mem_id]

        # 保留最近的100条短期记忆
        if len(self.short_term) > 100:
            sorted_memories = sorted(
                self.short_term.values(),
                key=lambda m: m.created_at,
                reverse=True
            )
            self.short_term = {m.id: m for m in sorted_memories[:100]}

        print(f"🧹 记忆清理完成: 短期记忆 {len(self.short_term)} 条")

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'short_term': {
                'total': len(self.short_term),
                'by_category': {
                    cat.value: len([m for m in self.short_term.values() if m.category == cat])
                    for cat in MemoryCategory
                }
            },
            'long_term': {
                'total': len(self.long_term),
                'by_category': {
                    cat.value: len([m for m in self.long_term.values() if m.category == cat])
                    for cat in MemoryCategory
                }
            },
            'shared': {
                'total': len(self.shared),
                'by_category': {
                    cat.value: len([m for m in self.shared.values() if m.category == cat])
                    for cat in MemoryCategory
                }
            }
        }

    def export(self, memory_type: MemoryType) -> str:
        """导出记忆为 JSON"""
        if memory_type == MemoryType.SHORT_TERM:
            memories = self.short_term
        elif memory_type == MemoryType.LONG_TERM:
            memories = self.long_term
        elif memory_type == MemoryType.SHARED:
            memories = self.shared
        else:
            return ""

        data = [m.to_dict() for m in memories.values()]
        return json.dumps(data, indent=2, ensure_ascii=False)

    def load(self, json_data: str, memory_type: MemoryType):
        """从 JSON 加载记忆"""
        data = json.loads(json_data)

        if memory_type == MemoryType.SHORT_TERM:
            self.short_term = {}
            for item_data in data:
                memory = MemoryItem(**item_data)
                self.short_term[memory.id] = memory
        elif memory_type == MemoryType.LONG_TERM:
            self.long_term = {}
            for item_data in data:
                memory = MemoryItem(**item_data)
                self.long_term[memory.id] = memory
        elif memory_type == MemoryType.SHARED:
            self.shared = {}
            for item_data in data:
                memory = MemoryItem(**item_data)
                self.shared[memory.id] = memory

        print(f"📥 记忆已加载: {len(data)} 条 ({memory_type.value})")


# 初始化全局记忆系统
memory_system = MemorySystem()


def seed_initial_memories(system: MemorySystem):
    """初始化种子记忆"""

    # 经验教训
    system.store(
        agent_id="code-reviewer",
        category=MemoryCategory.EXPERIENCE,
        content="使用 black 自动格式化代码可以保持代码风格一致",
        memory_type=MemoryType.LONG_TERM,
        importance=0.9
    )

    system.store(
        agent_id="test-engineer",
        category=MemoryCategory.EXPERIENCE,
        content="测试覆盖率应该保持在 80% 以上",
        memory_type=MemoryType.LONG_TERM,
        importance=0.95
    )

    system.store(
        agent_id="backend-expert",
        category=MemoryCategory.EXPERIENCE,
        content="FastAPI 是高性能的 Python Web 框架",
        memory_type=MemoryType.LONG_TERM,
        importance=0.9
    )

    # 知识库
    system.store(
        agent_id="all",
        category=MemoryCategory.KNOWLEDGE,
        content="OpenClaw 是一个智能体框架，支持技能系统和多智能体协作",
        memory_type=MemoryType.SHARED,
        importance=1.0
    )

    system.store(
        agent_id="all",
        category=MemoryCategory.KNOWLEDGE,
        content="Agency-Agents 是一个自主协作的智能体框架",
        memory_type=MemoryType.SHARED,
        importance=1.0
    )

    # 性能数据
    system.store(
        agent_id="code-reviewer",
        category=MemoryCategory.PERFORMANCE,
        content="平均审查时间: 2.5 分钟",
        memory_type=MemoryType.LONG_TERM,
        importance=0.8
    )

    system.store(
        agent_id="test-engineer",
        category=MemoryCategory.PERFORMANCE,
        content="测试成功率: 95%",
        memory_type=MemoryType.LONG_TERM,
        importance=0.8
    )

    print(f"\n✅ 已初始化 {len(system.short_term)} 条短期记忆, {len(system.long_term)} 条长期记忆, {len(system.shared)} 条共享记忆\n")


if __name__ == "__main__":
    # 初始化记忆系统
    seed_initial_memories(memory_system)

    # 打印统计信息
    print("=== 记忆系统统计 ===")
    stats = memory_system.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # 搜索记忆
    print("\n=== 搜索记忆 ===")
    results = memory_system.search("FastAPI")
    for memory in results[:3]:
        print(f"{memory.category.value}: {memory.content}")

    # 回忆记忆
    print("\n=== 回忆记忆 (code-reviewer) ===")
    memories = memory_system.recall("code-reviewer", limit=5)
    for memory in memories:
        print(f"{memory.category.value}: {memory.content}")

    # 存储新记忆
    print("\n=== 存储新记忆 ===")
    memory_system.store(
        agent_id="frontend-tester",
        category=MemoryCategory.EXPERIENCE,
        content="使用 Agent Browser 可以自动化浏览器测试",
        memory_type=MemoryType.SHORT_TERM,
        importance=0.9
    )

    # 清理记忆
    memory_system.cleanup()
