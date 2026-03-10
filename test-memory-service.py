#!/usr/bin/env python3
"""
测试 OpenClaw 记忆服务
"""

import sys
import asyncio
from pathlib import Path

# 添加到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from openclaw_memory_integration import (
    OpenClawMemoryIntegration,
    search_memory,
    get_memory,
    write_memory
)


async def test_basic_operations():
    """测试基本操作"""
    print("🧪 测试基本操作...")

    # 创建集成实例
    integration = OpenClawMemoryIntegration()

    try:
        # 测试 1: 读取 MEMORY.md
        print("\n1. 读取 MEMORY.md...")
        lines = await integration.memory_get("MEMORY.md")
        print(f"   ✅ 读取成功，共 {len(lines)} 行")

        # 测试 2: 搜索记忆
        print("\n2. 搜索记忆 '用户偏好'...")
        results = await integration.memory_search("用户偏好", max_results=5)
        print(f"   ✅ 搜索完成，找到 {len(results)} 条结果")

        # 测试 3: 写入测试文件
        print("\n3. 写入测试文件...")
        test_content = f"# 测试记忆\n\n测试时间: {asyncio.get_event_loop().time()}\n测试内容: 这是一条测试记忆。"
        await integration.memory_write("test_memory.md", test_content)
        print(f"   ✅ 写入成功")

        # 测试 4: 获取统计信息
        print("\n4. 获取统计信息...")
        stats = await integration.get_memory_stats()
        print(f"   ✅ 统计信息:")
        print(f"      - 本地文件: {stats['local']['file_count']} 个")
        print(f"      - 总大小: {stats['local']['total_size_mb']} MB")

        print("\n🎉 所有测试通过！")

    finally:
        await integration.close()


async def test_global_functions():
    """测试全局函数"""
    print("\n🧪 测试全局函数...")

    try:
        # 测试全局搜索
        print("\n1. 全局搜索 '长期记忆'...")
        results = await search_memory("长期记忆", max_results=3)
        print(f"   ✅ 搜索完成，找到 {len(results)} 条结果")

        # 测试全局获取
        print("\n2. 全局获取 'MEMORY.md'...")
        lines = await get_memory("MEMORY.md")
        print(f"   ✅ 获取成功，共 {len(lines)} 行")

        print("\n🎉 全局函数测试通过！")

    except Exception as e:
        print(f"❌ 全局函数测试失败: {e}")


async def main():
    """主函数"""
    print("==============================================")
    print("  OpenClaw 记忆服务测试")
    print("==============================================")

    # 测试基本操作
    await test_basic_operations()

    # 测试全局函数
    await test_global_functions()

    print("\n==============================================")
    print("  测试完成！")
    print("==============================================")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        sys.exit(1)