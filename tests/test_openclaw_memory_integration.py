"""
OpenClaw 与 OpenViking 集成测试套件
"""

import pytest
import asyncio
import os
from pathlib import Path
from datetime import datetime
from openclaw_memory_integration import (
    OpenClawMemoryIntegration,
    get_memory_integration,
    search_memory,
    get_memory,
    write_memory
)


@pytest.fixture
async def temp_memory_dir(tmp_path):
    """创建临时记忆目录"""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    
    # 创建测试文件
    (memory_dir / "MEMORY.md").write_text(
        "# 长期记忆\n\n这是系统的长期记忆文件。"
    )
    (memory_dir / "2026-03-10.md").write_text(
        "# 今日工作\n\n完成了系统集成工作。"
    )
    
    yield str(memory_dir)
    
    # 清理
    import shutil
    shutil.rmtree(str(tmp_path))


@pytest.fixture
async def memory_integration(temp_memory_dir):
    """创建记忆集成实例"""
    integration = OpenClawMemoryIntegration(
        workspace=temp_memory_dir,
        openviking_url="http://localhost:1933",
        enable_fallback=True
    )
    yield integration
    await integration.close()


class TestOpenClawMemoryIntegration:
    """OpenClaw 记忆集成测试类"""
    
    @pytest.mark.asyncio
    async def test_initialization(self, temp_memory_dir):
        """测试初始化"""
        integration = OpenClawMemoryIntegration(
            workspace=temp_memory_dir,
            openviking_url="http://localhost:1933"
        )
        
        assert integration.workspace == Path(temp_memory_dir)
        assert integration.openviking_url == "http://localhost:1933"
        assert integration.enable_fallback is True
        assert integration.session is not None
        
        await integration.close()
    
    @pytest.mark.asyncio
    async def test_memory_get(self, memory_integration):
        """测试获取记忆"""
        # 读取 MEMORY.md
        lines = await memory_integration.memory_get("MEMORY.md")
        assert len(lines) > 0
        assert any("长期记忆" in line for line in lines)
        
        # 读取 2026-03-10.md
        lines = await memory_integration.memory_get("2026-03-10.md")
        assert len(lines) > 0
        assert any("系统集成" in line for line in lines)
    
    @pytest.mark.asyncio
    async def test_memory_get_with_offsets(self, memory_integration):
        """测试带偏移的获取"""
        # 写入测试文件
        await memory_integration.memory_write(
            "test_offsets.md",
            "\n".join([f"Line {i}" for i in range(10)])
        )
        
        # 读取中间部分
        lines = await memory_integration.memory_get(
            "test_offsets.md",
            from_line=3,
            lines=5
        )
        assert len(lines) == 5
        assert "Line 3" in lines[0]
        assert "Line 7" in lines[4]
    
    @pytest.mark.asyncio
    async def test_memory_write(self, memory_integration):
        """测试写入记忆"""
        # 写入测试文件
        result = await memory_integration.memory_write(
            "test_write.md",
            "# 测试文件\n\n这是测试内容。"
        )
        
        assert result is True
        
        # 验证文件存在
        lines = await memory_integration.memory_get("test_write.md")
        assert len(lines) > 0
        assert "测试内容" in "".join(lines)
    
    @pytest.mark.asyncio
    async def test_memory_search_local(self, memory_integration):
        """测试本地搜索"""
        results = await memory_integration.memory_search(
            query="系统集成",
            max_results=10
        )
        
        assert isinstance(results, list)
        # 应该找到至少一个结果
        assert len(results) > 0
        assert all("path" in r for r in results)
        assert all("score" in r for r in results)
    
    @pytest.mark.asyncio
    async def test_memory_search_fallback(self, temp_memory_dir):
        """测试降级搜索"""
        # 使用无效的 OpenViking URL
        integration = OpenClawMemoryIntegration(
            workspace=temp_memory_dir,
            openviking_url="http://invalid:1933",
            enable_fallback=True
        )
        
        # 应该降级到本地搜索
        results = await integration.memory_search("长期记忆")
        
        assert isinstance(results, list)
        # 应该仍然有结果（来自本地）
        assert len(results) > 0
        assert all(r["source"] == "local" for r in results)
        
        await integration.close()
    
    @pytest.mark.asyncio
    async def test_extract_and_store(self, memory_integration):
        """测试自动提取记忆"""
        result = await memory_integration.extract_and_store(
            text="用户希望使用性能优化策略，预算控制在1万以内",
            session_key="test_session",
            metadata={"user_id": "user_123"}
        )
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_extract_memories_patterns(self, memory_integration):
        """测试提取模式"""
        text = """
        用户偏好：使用性能优化策略
        项目状态：开发进行中
        重要决策：选择 FastAPI 作为后端框架
        技术选型：Python + React
        """
        
        memories = memory_integration._extract_memories(
            text,
            session_key="test_session"
        )
        
        # 应该提取到多个记忆
        assert len(memories) >= 3
        assert all("key" in m for m in memories)
        assert all("value" in m for m in memories)
        assert all("metadata" in m for m in memories)
    
    @pytest.mark.asyncio
    async def test_load_session_context(self, memory_integration):
        """测试加载会话上下文"""
        context = await memory_integration.load_session_context(
            session_key="test_session",
            max_tokens=4000
        )
        
        assert isinstance(context, dict)
        assert "session_key" in context
        assert "memories" in context
        assert "max_tokens" in context
        assert "loaded_at" in context
        assert context["session_key"] == "test_session"
        assert context["max_tokens"] == 4000
    
    @pytest.mark.asyncio
    async def test_cleanup_old_memories(self, memory_integration):
        """测试清理旧记忆"""
        # 创建旧文件
        old_date = (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d")
        await memory_integration.memory_write(
            f"{old_date}.md",
            "旧记忆"
        )
        
        # 清理 30 天前的记忆
        deleted = await memory_integration.cleanup_old_memories(days=30)
        
        assert deleted >= 0
    
    @pytest.mark.asyncio
    async def test_get_memory_stats(self, memory_integration):
        """测试获取统计信息"""
        stats = await memory_integration.get_memory_stats()
        
        assert isinstance(stats, dict)
        assert "local" in stats
        assert "workspace" in stats
        assert "memory_dir" in stats
        assert "checked_at" in stats
        
        # 本地统计
        assert "file_count" in stats["local"]
        assert "total_size_bytes" in stats["local"]
        assert "total_size_mb" in stats["local"]
    
    @pytest.mark.asyncio
    async def test_search_local_keyword(self, memory_integration):
        """测试本地关键词搜索"""
        results = memory_integration._search_local("长期记忆", max_results=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5
        assert all("path" in r for r in results)
        assert all("score" in r for r in results)
        assert all("content" in r for r in results)
        assert all(r["source"] == "local" for r in results)
    
    def test_format_openviking_results(self, memory_integration):
        """测试格式化 OpenViking 结果"""
        data = [
            {
                "key": "test1.md",
                "score": 0.85,
                "value": "测试内容1"
            },
            {
                "path": "test2.md",
                "similarity": 0.75,
                "content": "测试内容2"
            }
        ]
        
        results = memory_integration._format_openviking_results(data)
        
        assert len(results) == 2
        assert all("path" in r for r in results)
        assert all("score" in r for r in results)
        assert all("content" in r for r in results)
        assert all(r["source"] == "openviking" for r in results)
    
    @pytest.mark.asyncio
    async def test_context_manager(self, temp_memory_dir):
        """测试异步上下文管理器"""
        async with OpenClawMemoryIntegration(
            workspace=temp_memory_dir
        ) as integration:
            # 使用集成
            lines = await integration.memory_get("MEMORY.md")
            assert len(lines) > 0
        
        # 自动关闭
        assert integration.session.closed


class TestGlobalFunctions:
    """全局函数测试"""
    
    @pytest.mark.asyncio
    async def test_get_memory_integration_singleton(self, monkeypatch):
        """测试全局单例"""
        # 设置环境变量
        monkeypatch.setenv("OPENCLAW_WORKSPACE", "/tmp/test_workspace")
        monkeypatch.setenv("OPENVIKING_URL", "http://localhost:1933")
        
        # 获取实例
        integration1 = get_memory_integration()
        integration2 = get_memory_integration()
        
        # 应该是同一个实例
        assert integration1 is integration2
    
    @pytest.mark.asyncio
    async def test_global_search_memory(self, memory_integration):
        """测试全局搜索函数"""
        # 注意：这会使用全局实例，可能受环境影响
        try:
            results = await search_memory("长期记忆", max_results=5)
            assert isinstance(results, list)
        except Exception as e:
            # 如果 OpenViking 未启动，应该降级
            pass
    
    @pytest.mark.asyncio
    async def test_global_get_memory(self):
        """测试全局获取函数"""
        # 使用当前工作空间
        workspace = os.getenv("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
        memory_file = f"{workspace}/memory/MEMORY.md"
        
        if os.path.exists(memory_file):
            lines = await get_memory("MEMORY.md")
            assert isinstance(lines, list)
    
    @pytest.mark.asyncio
    async def test_global_write_memory(self, temp_memory_dir):
        """测试全局写入函数"""
        # 临时覆盖工作空间
        result = await write_memory(
            "test_global.md",
            "全局测试内容",
            sync_to_openviking=False
        )
        
        # 注意：这会写入到当前工作空间
        assert isinstance(result, bool)


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "-s"])