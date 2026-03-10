#!/usr/bin/env python3
"""
OpenClaw 智能系统 - 简化版
集成网络搜索和记忆功能
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

class SimpleOpenClawSystem:
    """简化的 OpenClaw 智能系统"""
    
    def __init__(self):
        self.system_name = "OpenClaw"
        self.version = "2.0"
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        """处理查询"""
        print(f"\n🤖 {self.system_name} v{self.version} 处理中...")
        print(f"📝 查询: '{query}'")
        
        result = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": [],
            "response": ""
        }
        
        # 1. 记忆搜索
        print("📂 搜索记忆...")
        try:
            from openclaw_memory_integration import search_memory
            memory_results = await search_memory(query, max_results=3)
            if memory_results:
                print(f"   ✅ 记忆: {len(memory_results)} 条")
                result["sources"].extend([{"type": "memory", "data": r} for r in memory_results])
            else:
                print("   ℹ️ 无记忆信息")
        except Exception as e:
            print(f"   ❌ 记忆搜索失败: {e}")
        
        # 2. 网络搜索和采集
        print("🌐 网络搜索和采集...")
        web_results = []
        collected_data = []
        
        try:
            # 检查是否是资讯查询
            is_news_query = any(keyword in query.lower() for keyword in ['新闻', '资讯', '最新', '百度', '搜索', '采集', '数据', '登录'])
            
            # 如果是资讯/采集查询，使用数据采集器
            if is_news_query:
                from fixed_web_automation import get_fixed_automation
                automation = get_fixed_automation()
                
                print("   📰 启动网页采集...")
                
                # 采集百度新闻
                news_data = automation.extract_data("https://news.baidu.com")
                collected_data.append({
                    "type": "news",
                    "data": news_data,
                    "source": "百度新闻"
                })
                
                # 如果结果不够，采集搜索结果
                if news_data.get("extracted_data", {}).get("links_count", 0) < 3:
                    print("   🔍 补充搜索数据采集...")
                    search_data = automation.extract_data("https://www.baidu.com/s?wd=" + query)
                    collected_data.append({
                        "type": "search",
                        "data": search_data,
                        "source": "百度搜索"
                    })
                
                print(f"   ✅ 采集完成: {len(collected_data)} 个数据源")
                
                # 将采集的数据转换为结果格式
                for item in collected_data:
                    links = item.get("data", {}).get("extracted_data", {}).get("links", [])[:3]
                    for link in links:
                        web_results.append({
                            "type": "collected",
                            "data": {
                                "title": link.get("text", ""),
                                "url": link.get("url", ""),
                                "content": "来自网页采集的数据"
                            }
                        })
            
            # 如果是普通查询，使用搜索
            if not web_results and not is_news_query:
                from local_web_search import local_search
                search_results = await local_search(query, engine='wikipedia', max_results=3)
                
                if search_results:
                    web_results.extend([{"type": "search", "data": r} for r in search_results])
                    print(f"   ✅ 本地搜索: {len(search_results)} 条")
            
            # 如果还不够，尝试百度新闻
            if len(web_results) < 3:
                from baidu_news_search import get_baidu_latest_news
                baidu_results = await get_baidu_latest_news()
                if baidu_results:
                    web_results.extend([{"type": "baidu_news", "data": r} for r in baidu_results])
                    print(f"   ✅ 百度新闻: {len(baidu_results)} 条")
            
            if web_results:
                result["sources"].extend(web_results)
                print(f"   📊 网络数据: {len(web_results)} 条")
            else:
                print("   ℹ️ 无网络数据")
                
        except Exception as e:
            print(f"   ❌ 网络搜索失败: {e}")
        
        # 3. 生成回答
        print("🧠 生成回答...")
        response = self._generate_response(query, memory_results, web_results)
        result["response"] = response
        
        # 4. 存储记忆
        print("💾 存储记忆...")
        try:
            from openclaw_memory_integration import write_memory
            await self._store_memory(query, response)
            print("   ✅ 记忆已存储")
        except Exception as e:
            print(f"   ❌ 存储失败: {e}")
        
        print("✅ 完成！")
        return result
    
    def _generate_response(self, query: str, memory_results: List, web_results: List) -> str:
        """生成回答"""
        
        context_parts = []
        
        # 添加记忆信息
        if memory_results:
            context_parts.append("📂 记忆信息:")
            for result in memory_results[:2]:
                content = result.get('content', '')[:80]
                if content:
                    context_parts.append(f"- {content}...")
        
        # 添加网络信息
        if web_results:
            context_parts.append("🌐 网络信息:")
            for result in web_results[:2]:
                title = result.get('title', '无标题')
                content = result.get('content', '')[:80]
                if content:
                    context_parts.append(f"- {title}: {content}...")
        
        # 生成回答
        if context_parts:
            full_context = "\n".join(context_parts)
            response = f"🤖 根据相关信息，我的回答是：\n\n{full_context}\n\n💡 基于这些信息，我认为..."
        else:
            response = "🤖 抱歉，我没有找到相关信息。建议重新表述问题或提供更多背景。"
        
        # 模拟智能增强
        if "OpenClaw" in query:
            response += "\n\n🎯 关于 OpenClaw：这是一个具有记忆和网络搜索能力的智能体系统。"
        elif "AI" in query:
            response += "\n\n🤖 关于 AI：人工智能正在快速发展，深度学习和机器学习是核心。"
        
        return response
    
    async def _store_memory(self, query: str, response: str):
        """存储记忆到文件"""
        memory_file = f"memory/{datetime.now().strftime('%Y-%m-%d')}_query.md"
        
        content = f"""# 记忆记录

## 查询
{query}

## 回答
{response}

## 时间
{datetime.now().isoformat()}

## 来源
- OpenClaw 系统
- 网络搜索
- 记忆检索
"""
        
        from openclaw_memory_integration import write_memory
        await write_memory(memory_file, content)

async def test_system():
    """测试系统"""
    print("🚀 OpenClaw 智能系统测试")
    print("=" * 50)
    
    system = SimpleOpenClawSystem()
    
    # 测试查询
    queries = [
        "什么是 OpenClaw AI",
        "机器学习的特点",
        "2024年技术趋势"
    ]
    
    for query in queries:
        print(f"\n🎯 测试查询: '{query}'")
        print("-" * 30)
        
        result = await system.process_query(query)
        
        print(f"\n📋 结果:")
        print(f"🤖 回答: {result['response']}")
        print(f"📊 来源: {len(result['sources'])} 个")
        
        # 等待一下
        await asyncio.sleep(1)

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 智能系统")
    parser.add_argument("query", nargs='?', help="查询问题")
    parser.add_argument("--test", action="store_true", help="运行测试")
    
    args = parser.parse_args()
    
    if args.test:
        await test_system()
    elif args.query:
        system = SimpleOpenClawSystem()
        result = await system.process_query(args.query)
        print(f"\n📋 结果: {result['response']}")
    else:
        print("🚀 OpenClaw 智能系统")
        print("输入问题或 --test 进行测试")
        
        system = SimpleOpenClawSystem()
        
        while True:
            try:
                query = input("\n🤖 请输入问题 (或输入 'exit' 退出): ").strip()
                
                if query.lower() in ['exit', 'quit']:
                    print("👋 再见！")
                    break
                elif query:
                    result = await system.process_query(query)
                    print(f"\n🤖 回答: {result['response']}")
                    
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break

if __name__ == "__main__":
    asyncio.run(main())