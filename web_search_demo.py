#!/usr/bin/env python3
"""
OpenClaw 网络搜索演示
展示如何使用网络搜索功能
"""

import asyncio
import json
from pathlib import Path
import sys

# 添加到路径
sys.path.insert(0, str(Path(__file__).parent))

from web_search_integration import WebSearchService, get_web_search_service, web_search

async def demonstrate_web_search():
    """演示网络搜索功能"""
    print("🔍 OpenClaw 网络搜索功能演示")
    print("=" * 50)
    
    # 获取搜索服务
    service = get_web_search_service()
    
    print(f"Node.js 状态: {'✅ 可用' if service.node_available else '❌ 不可用'}")
    print(f"Tavily API 密钥: {'✅ 已配置' if service.api_key else '❌ 未配置'}")
    
    if not service.api_key:
        print("\n📝 配置说明:")
        print("1. 访问 https://tavily.com 注册账户")
        print("2. 获取 API 密钥")
        print("3. 运行: python3 web_search_test.py config --key YOUR_API_KEY")
        return
    
    print("\n🧪 开始搜索演示...")
    
    # 搜索查询列表
    queries = [
        "OpenClaw AI",
        "artificial intelligence 2024", 
        "machine learning trends"
    ]
    
    for query in queries:
        print(f"\n🔍 搜索: '{query}'")
        print("-" * 30)
        
        try:
            # 执行搜索
            results = await web_search(query, max_results=3)
            
            if results:
                print(f"✅ 找到 {len(results)} 个结果:")
                
                for i, result in enumerate(results, 1):
                    title = result.get('title', '无标题')
                    url = result.get('url', '无链接')
                    content = result.get('content', '无内容')
                    
                    print(f"\n{i}. {title}")
                    print(f"   URL: {url}")
                    print(f"   内容: {content[:100]}...")
                    print(f"   评分: {result.get('score', 0.0):.2f}")
            else:
                print("❌ 未找到结果")
                
        except Exception as e:
            print(f"❌ 搜索出错: {e}")
        
        print("\n" + "=" * 50)
        
        # 等待一下
        await asyncio.sleep(1)
    
    # 演示内容提取
    print("\n📄 内容提取演示:")
    print("-" * 30)
    
    test_url = "https://httpbin.org/json"
    try:
        content = await service.extract_url(test_url)
        print(f"✅ 内容提取成功:")
        print(f"内容长度: {len(content)} 字符")
        print(f"预览: {content[:200]}...")
    except Exception as e:
        print(f"❌ 内容提取失败: {e}")

async def demonstrate_memory_plus_search():
    """演示记忆 + 搜索功能"""
    print("\n🧠 记忆 + 搜索综合演示")
    print("=" * 50)
    
    # 模拟一个需要搜索的记忆场景
    scenarios = [
        {
            "query": "什么是智能体工程学",
            "context": "用户询问关于智能体工程学的概念"
        },
        {
            "query": "OpenViking 的特点",
            "context": "用户想了解 OpenViking 的优势"
        },
        {
            "query": "2024年 AI 发展趋势",
            "context": "用户询问最新的 AI 发展动向"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 场景: {scenario['context']}")
        print(f"💭 用户问题: '{scenario['query']}'")
        
        # 先尝试记忆搜索
        print("\n📂 先搜索记忆...")
        from openclaw_memory_integration import search_memory
        
        memory_results = await search_memory(scenario['query'], max_results=3)
        if memory_results:
            print(f"✅ 在记忆中找到 {len(memory_results)} 条相关信息:")
            for result in memory_results[:2]:
                print(f"   - {result.get('score', 0.0):.2f}: {result.get('content', 'N/A')[:50]}...")
        else:
            print("ℹ️ 记忆中没有相关信息")
        
        # 再执行网络搜索
        print("\n🌐 执行网络搜索...")
        
        search_results = await web_search(scenario['query'], max_results=2)
        if search_results:
            print(f"✅ 在网络中找到 {len(search_results)} 条信息:")
            for result in search_results:
                print(f"   - {result.get('title', 'N/A')}")
        else:
            print("ℹ️ 网络搜索未找到相关信息")
        
        print("\n" + "=" * 50)
        
        # 模拟整合回答
        print("\n🤖 模拟智能回答:")
        if memory_results and search_results:
            answer = f"根据我的记忆和最新的网络信息，我为你找到了一些关于'{scenario['query']}'的相关内容。"
        elif memory_results:
            answer = f"根据我的记忆，我可以为你提供关于'{scenario['query']}'的信息。"
        elif search_results:
            answer = f"通过网络搜索，我为你找到了关于'{scenario['query']}'的最新信息。"
        else:
            answer = f"很抱歉，我没有找到关于'{scenario['query']}'的明确信息。"
        
        print(f"   {answer}")
        
        await asyncio.sleep(2)

async def main():
    """主函数"""
    print("🚀 OpenClaw 网络搜索功能完整演示")
    print("=" * 60)
    
    # 检查依赖
    service = get_web_search_service()
    
    if not service.node_available:
        print("❌ Node.js 不可用，无法演示网络搜索")
        return
    
    if not service.api_key:
        print("❌ Tavily API 密钥未配置，无法进行网络搜索")
        print("\n📝 配置方法:")
        print("1. 访问 https://tavily.com 注册")
        print("2. 获取 API 密钥")
        print("3. 运行: python3 web_search_test.py config --key YOUR_API_KEY")
        return
    
    # 运行演示
    try:
        await demonstrate_web_search()
        print("\n" + "=" * 60)
        await demonstrate_memory_plus_search()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 演示被中断")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！")

if __name__ == "__main__":
    asyncio.run(main())