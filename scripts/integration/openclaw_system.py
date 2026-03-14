#!/usr/bin/env python3
"""
OpenClaw 智能体主系统 - 集成网络搜索功能
将网络搜索能力集成到 OpenClaw 主智能体中
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from openclaw_memory_integration import OpenClawMemoryIntegration, search_memory, write_memory
from web_search_integration import web_search, extract_web_content, configure_tavily_api_key

class OpenClawSystem:
    """OpenClaw 主智能体系统"""
    
    def __init__(self):
        self.system_name = "OpenClaw"
        self.version = "2.0"
        self.capabilities = ["memory", "web_search", "reasoning"]
        
    async def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        处理用户查询
        
        Args:
            query: 用户查询
            context: 上下文信息
            
        Returns:
            处理结果
        """
        print(f"\n🤖 {self.system_name} v{self.version} 开始处理...")
        print(f"📝 用户查询: '{query}'")
        
        result = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": [],
            "response": "",
            "context": context or {}
        }
        
        # 步骤 1: 搜索相关记忆
        print("📂 步骤 1: 搜索记忆...")
        memory_results = await self._search_memory_context(query)
        result["sources"].extend([{"type": "memory", "data": r} for r in memory_results])
        
        # 步骤 2: 网络搜索
        print("🌐 步骤 2: 网络搜索...")
        web_results = await self._perform_web_search(query)
        result["sources"].extend([{"type": "web", "data": r} for r in web_results])
        
        # 步骤 3: 整合信息并生成回答
        print("🧠 步骤 3: 整合信息...")
        response = await self._generate_response(query, memory_results, web_results)
        result["response"] = response
        
        # 步骤 4: 提取并存储新记忆
        print("💾 步骤 4: 提取记忆...")
        await self._extract_new_memory(query, response, context)
        
        print("✅ 处理完成！")
        return result
    
    async def _search_memory_context(self, query: str) -> List[Dict[str, Any]]:
        """搜索记忆上下文"""
        try:
            results = await search_memory(query, max_results=5)
            if results:
                print(f"   ✅ 在记忆中找到 {len(results)} 条信息")
                return results
            else:
                print("   ℹ️ 记忆中未找到相关信息")
                return []
        except Exception as e:
            print(f"   ❌ 记忆搜索失败: {e}")
            return []
    
    async def _perform_web_search(self, query: str) -> List[Dict[str, Any]]:
        """执行网络搜索"""
        try:
            results = await web_search(query, max_results=3)
            if results:
                print(f"   ✅ 在网络中找到 {len(results)} 条信息")
                return results
            else:
                print("   ℹ️ 网络搜索未找到相关信息")
                return []
        except Exception as e:
            print(f"   ❌ 网络搜索失败: {e}")
            return []
    
    async def _generate_response(
        self, 
        query: str, 
        memory_results: List[Dict[str, Any]], 
        web_results: List[Dict[str, Any]]
    ) -> str:
        """生成回答"""
        
        # 构建上下文
        context_parts = []
        
        # 添加记忆信息
        if memory_results:
            context_parts.append("📂 记忆信息:")
            for result in memory_results[:2]:
                content = result.get('content', '')[:100]
                if content:
                    context_parts.append(f"- {content}...")
        
        # 添加网络信息
        if web_results:
            context_parts.append("🌐 网络信息:")
            for result in web_results[:2]:
                title = result.get('title', '无标题')
                content = result.get('content', '')[:100]
                if content:
                    context_parts.append(f"- {title}: {content}...")
        
        # 生成回答
        if context_parts:
            full_context = "\n".join(context_parts)
            response = f"🤖 根据相关信息，我为你分析以下内容：\n\n{full_context}\n\n💡 基于这些信息，我的回答是..."
        else:
            response = "🤖 抱歉，我没有找到与你的问题相关的记忆或网络信息。请尝试重新表述问题，或者提供更多背景信息。"
        
        # 这里可以集成更复杂的语言模型
        # 目前使用简单的模式匹配
        self._enhance_response_with_patterns(query, response)
        
        return response
    
    def _enhance_response_with_patterns(self, query: str, response: str) -> str:
        """使用模式增强回答"""
        
        # 模式匹配示例
        patterns = {
            "OpenClaw": [
                "OpenClaw 是一个智能体框架",
                "具有记忆能力和搜索功能",
                "支持网络搜索和上下文理解"
            ],
            "AI": [
                "人工智能正在快速发展",
                "AI 技术在各个领域都有广泛应用",
                "机器学习和深度学习是 AI 的核心技术"
            ],
            "搜索": [
                "网络搜索可以帮助找到最新信息",
                "记忆搜索可以回顾历史经验",
                "两种搜索方式相结合效果更佳"
            ]
        }
        
        # 添加相关模式信息
        for pattern, info in patterns.items():
            if pattern.lower() in query.lower():
                response += f"\n\n💭 关于 {pattern}：{' '.join(info)}"
                break
    
    async def _extract_new_memory(
        self, 
        query: str, 
        response: str, 
        context: Optional[Dict[str, Any]]
    ) -> None:
        """提取并存储新记忆"""
        try:
            # 构造记忆文本
            memory_text = f"""
用户查询: {query}
系统回答: {response}
处理时间: {datetime.now().isoformat()}
上下文: {context or {}}
"""
            
            # 提取重要信息
            session_key = context.get('session_id', 'default') if context else 'default'
            
            await extract_and_store(
                text=memory_text,
                session_key=session_key,
                metadata={
                    "query": query,
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                    "context": context or {}
                }
            )
            
            print(f"   ✅ 提取并存储了新记忆")
            
        except Exception as e:
            print(f"   ❌ 记忆提取失败: {e}")

async def interactive_demo():
    """交互式演示"""
    print("🚀 OpenClaw 智能系统 - 交互式演示")
    print("=" * 60)
    
    system = OpenClawSystem()
    
    # 演示查询
    demo_queries = [
        "什么是 OpenClaw AI",
        "智能体工程学有什么特点",
        "2024年的技术发展趋势"
    ]
    
    for query in demo_queries:
        print(f"\n🎯 演示查询: '{query}'")
        print("=" * 60)
        
        result = await system.process_query(query)
        
        print(f"\n📋 处理结果:")
        print(f"回答: {result['response']}")
        print(f"来源数量: {len(result['sources'])}")
        print(f"时间: {result['timestamp']}")
        
        # 等待用户输入继续
        try:
            input("\n按 Enter 继续下一个演示...")
        except KeyboardInterrupt:
            print("\n\n⏹️ 演示中断")
            break
    
    print("\n🎉 演示完成！")

async def single_query_demo(query: str):
    """单个查询演示"""
    system = OpenClawSystem()
    result = await system.process_query(query)
    
    print(f"\n📋 处理结果:")
    print(f"🤖 回答: {result['response']}")
    print(f"📊 来源: {len(result['sources'])} 个")
    print(f"⏰ 时间: {result['timestamp']}")

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 智能系统")
    parser.add_argument("query", nargs='?', help="要查询的问题")
    parser.add_argument("--demo", action="store_true", help="运行交互式演示")
    parser.add_argument("--config", action="store_true", help="配置 Tavily API 密钥")
    
    args = parser.parse_args()
    
    if args.config:
        # 配置模式
        api_key = input("输入 Tavily API 密钥: ").strip()
        if api_key:
            configure_tavily_api_key(api_key)
            print("✅ API 密钥已配置")
        return
    
    if args.demo:
        # 演示模式
        await interactive_demo()
    elif args.query:
        # 单查询模式
        await single_query_demo(args.query)
    else:
        # 默认交互模式
        print("🚀 OpenClaw 智能系统")
        print("输入 'help' 查看帮助，'exit' 退出")
        
        system = OpenClawSystem()
        
        while True:
            try:
                query = input("\n🤖 请输入你的问题: ").strip()
                
                if query.lower() in ['exit', 'quit']:
                    print("👋 再见！")
                    break
                elif query.lower() in ['help', 'h']:
                    print("使用说明:")
                    print("- 输入问题即可查询")
                    print('- 输入 "demo" 运行演示')
                    print('- 输入 "exit" 退出')
                elif query.lower() == 'demo':
                    await interactive_demo()
                elif query:
                    await single_query_demo(query)
                    
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except EOFError:
                print("\n\n👋 再见！")
                break

if __name__ == "__main__":
    asyncio.run(main())