#!/usr/bin/env python3
"""
网络搜索功能测试和配置脚本
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加到路径
sys.path.insert(0, str(Path(__file__).parent))

from web_search_integration import WebSearchService, get_web_search_service, configure_tavily_api_key

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    # 检查 Node.js
    service = get_web_search_service()
    print(f"Node.js 可用: {'✅' if service.node_available else '❌'}")
    print(f"Tavily API 密钥: {'✅' if service.api_key else '❌'}")
    
    return service.node_available

def test_without_api_key():
    """测试没有 API 密钥的情况"""
    print("\n🧪 测试没有 API 密钥...")
    
    service = get_web_search_service()
    
    # 测试搜索（应该失败）
    async def test():
        results = await service.search("test query", max_results=2)
        print(f"搜索结果数量: {len(results)}")
        return results
    
    results = asyncio.run(test())
    print("结果: 无 API 密钥时搜索返回空结果")

def configure_tavily():
    """配置 Tavily API 密钥"""
    print("\n⚙️ 配置 Tavily API 密钥...")
    
    # 检查是否已有密钥
    service = get_web_search_service()
    if service.api_key:
        print("✅ 已有 Tavily API 密钥")
        print(f"密钥: {service.api_key[:10]}...")
        return
    
    # 提示用户获取 API 密钥
    print("❌ 缺少 Tavily API 密钥")
    print("\n获取步骤:")
    print("1. 访问: https://tavily.com")
    print("2. 注册账户")
    print("3. 获取 API 密钥")
    print("4. 运行:")
    print(f"   python3 {__file__} config --key YOUR_API_KEY")
    
    # 尝试从用户输入获取
    try:
        api_key = input("\n输入你的 Tavily API 密钥 (或按 Enter 跳过): ").strip()
        if api_key:
            configure_tavily_api_key(api_key)
            print("✅ API 密钥已配置")
        else:
            print("❌ 跳过 API 密钥配置")
    except KeyboardInterrupt:
        print("\n❌ 用户取消配置")

def test_with_config():
    """测试配置后的搜索功能"""
    print("\n🧪 测试搜索功能...")
    
    service = get_web_search_service()
    
    if not service.api_key:
        print("❌ 无 API 密钥，跳过搜索测试")
        return
    
    # 测试搜索
    async def test():
        queries = [
            "OpenClaw AI",
            "artificial intelligence 2024",
            "machine learning trends"
        ]
        
        for query in queries:
            print(f"\n搜索: {query}")
            results = await service.search(query, max_results=3)
            
            if results:
                print(f"✅ 找到 {len(results)} 个结果")
                for i, result in enumerate(results[:2], 1):
                    print(f"  {i}. {result.get('title', 'N/A')}")
                    if result.get('url'):
                        print(f"     URL: {result.get('url', 'N/A')}")
            else:
                print("❌ 未找到结果")
        
        # 测试内容提取
        print("\n📄 测试内容提取...")
        url = "https://example.com"
        content = await service.extract_url(url)
        print(f"内容提取示例: {content[:100]}...")
    
    asyncio.run(test())

def generate_config():
    """生成配置文件"""
    print("\n📝 生成配置文件...")
    
    config_file = Path("/root/.openclaw/workspace/.env")
    
    # 添加网络搜索配置
    config_content = """
# 网络搜索配置
TAVILY_API_KEY=your_tavily_api_key_here
"""
    
    with open(config_file, 'a') as f:
        f.write(config_content)
    
    print(f"配置已添加到: {config_file}")
    print("请编辑文件，设置你的 API 密钥")

def show_usage():
    """显示使用方法"""
    print("\n📖 使用方法:")
    print("1. 配置 API 密钥:")
    print("   python3 web_search_test.py config --key YOUR_API_KEY")
    print("   或编辑 ~/.openclaw/workspace/.env 文件")
    print("\n2. 测试搜索功能:")
    print("   python3 web_search_test.py test")
    print("\n3. 代码中使用:")
    print("""
   from web_search_integration import web_search, extract_web_content
   
   # 搜索
   results = await web_search("OpenClaw AI", max_results=5)
   
   # 提取内容
   content = await extract_web_content("https://example.com")
   """)

def main():
    """主函数"""
    print("==============================================")
    print("  OpenClaw 网络搜索功能测试")
    print("==============================================")
    
    # 检查依赖
    if not check_dependencies():
        print("❌ Node.js 不可用，无法使用网络搜索")
        return
    
    # 测试无 API 密钥的情况
    test_without_api_key()
    
    # 检查是否配置 API 密钥
    if not get_web_search_service().api_key:
        configure_tavily()
    
    # 测试功能
    if get_web_search_service().api_key:
        test_with_config()
    
    # 生成配置文件
    generate_config()
    
    # 显示使用方法
    show_usage()
    
    print("\n==============================================")
    print("  测试完成！")
    print("==============================================")

if __name__ == "__main__":
    # 命行行参数处理
    import argparse
    
    parser = argparse.ArgumentParser(description="网络搜索功能测试")
    parser.add_argument("action", nargs='?', choices=['test', 'config'], help="执行的动作")
    parser.add_argument("--key", help="Tavily API 密钥")
    
    args = parser.parse_args()
    
    if args.action == 'config' and args.key:
        configure_tavily_api_key(args.key)
        print("✅ API 密钥已配置")
    elif args.action == 'test':
        check_dependencies()
        test_without_api_key()
        if get_web_search_service().api_key:
            test_with_config()
    else:
        main()