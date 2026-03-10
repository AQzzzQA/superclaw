#!/usr/bin/env python3
"""
OpenClaw + OpenViking 集成测试
验证集成功能是否正常工作
"""

import asyncio
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_memory_integration():
    """测试记忆集成"""
    print("🧠 测试 OpenClaw 记忆集成...")
    
    try:
        from openclaw_memory_integration import OpenClawMemoryIntegration
        from memory import MEMORY.md
        
        integration = OpenClawMemoryIntegration()
        
        # 测试存储
        print("\n1. 测试记忆存储...")
        result = await integration.memory_write("test_memory.md", f"# 测试记忆\n\n创建时间: {datetime.now().isoformat()}")
        print(f"   结果: {result['success']}")
        
        # 测试搜索
        print("\n2. 测试记忆搜索...")
        results = await integration.memory_search("用户偏好", max_results=5)
        print(f"   结果: {len(results)} 条")
        for i, r in enumerate(results[:3], 1):
            print(f"   {i}. {r.get('path', 'N/A')} - Score: {r.get('score', '0.0')}")

async def test_website_login():
    """测试网站登录功能"""
    print("\n🌐 测试网站登录...")
    
    try:
        from website_login import login_website, get_login_status
        
        # 测试状态检查
        status = await get_login_status("https://example.com/profile")
        print(f"   登录状态: {status}")
        
        # 测试表单登录
        print("\n3. 测试表单登录...")
        result = await login_website(
            "https://example.com/login",
            method="form",
            username="test_user",
            password="test_pass"
        )
        print(f"   结果: {result}")
        
    except Exception as e:
        logger.error(f"登录测试失败: {e}")


async def test_google_captcha():
    """测试谷歌验证码"""
    print("\n🔍 测试谷歌验证码...")
    
    try:
        from google_captcha_solver import solve_captcha_challenge
        
        # 测试音频验证码
        print("\n1. 音频验证码...")
        result = await solve_captcha_challenge(
            "https://www.google.com/recaptcha/api.js",
            "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
            "answer": ""
        )
        print(f"   音频验证码: {result.get('answer', 'N/A')}")
        
        # 测试图片验证码
        print("\n2. 图片验证码...")
        result = solve_captcha_challenge(
            "https://www.google.com/recaptcha/api.js",
            "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
            "challenge_type": "image"
        )
        print(f"   图片验证码: {result.get('message', 'N/A')}")
        
        # 测试选择题验证码
        print("\n3. 选择题验证码...")
        result = solve_captcha_challenge(
            "https://www.google.com/recaptcha/api.js",
            "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
            "challenge_type": "select"
        )
        print(f"   选择题验证码: {result.get('answer', 'N/A')}")
        
    except Exception as e:
        logger.error(f"验证码测试失败: {e}")


async def test_data_collection():
    """测试数据采集功能"""
    print("\n📊 测试数据采集...")
    
    try:
        from web_data_collector import collect_news, collect_data
        
        # 测试百度新闻采集
        print("\n1. 百度新闻采集...")
        news = await collect_news(max_results=3)
        print(f"   结果: {len(news)} 条")
        for i, item in enumerate(news[:2], 1):
            print(f"   {i}. {item.get('title', 'N/A')}")
            print(f"      URL: {item.get('url', 'N/A')}")
            print()
        
        # 测试搜索数据
        print("\n2. 搜索数据采集...")
        result = await collect_data("人工智能", "baidu", max_results=3)
        print(f"   结果: {len(result)} 条")
        for i, item in enumerate(result[:2], 1):
            print(f"   {i}. {item.get('title', 'N/A')}")
            print()
        
    except Exception as e:
        logger.error(f"数据采集测试失败: {e}")


async def test_multi_user_permission():
    """测试多用户权限"""
    print("\n👥 测试多用户权限...")
    
    try:
        from multi_user_permission import create_user, get_user, get_all_users
        from google_captcha_solver import solve_captcha_challenge
        
        # 创建管理员
        admin = create_user("admin001", "管理员", "admin@company.com", "admin")
        print(f"   创建管理员: {admin['success']}")
        
        # 创建普通用户
        user = create_user("user_001", "用户", "user@company.com", "user", "user")
        print(f"   创建用户: {user['success']}")
        
        # 创建访客
        guest = create_user("guest_001", "访客", "guest@company.com", "guest", role="guest")
        print(f"   创建访客: {guest['success']}")
        
        # 测试权限检查
        from multi_user_permission import check_permission
        has_read = check_permission("admin", "read")
        has_write = check_permission("admin", "write")
        has_execute = check_permission("admin", "execute")
        print(f"\n管理员权限: 读取-{has_read}, 写入-{has_write}, 执行-{has_execute}")
        
        # 测试会话管理
        print("\n📱 会话管理测试...")
        from multi_user_permission import get_user_sessions
        sessions = await get_user_sessions("user_001", active_only=True)
        print(f"   活跃会话数: {len(sessions)} 个")
        
    except Exception as e:
        logger.error(f"多用户权限测试失败: {e}")


async def test_enhanced_login():
    """测试增强登录"""
    print("\n🔐 测试增强登录...")
    
    try:
        from enhanced_login import enhanced_login
        from enhanced_website_login import auto_login_with_verification
        
        # 测试自动验证登录
        print("\n1. 测试表单登录 + 自动验证...")
        result = await enhanced_login(
            "https://example.com/login",
            "username": "test_user",
            "password": "test_pass",
            captcha_solution="auto"
        )
        print(f"   结果: {result}")
        
        # 测试 API 登录
        print("\n2. 测试 API 登录...")
        result = await enhanced_login(
            "https://api.example.com/login",
            "username": "test_user",
            "api_key": "test_api_key"
        )
        print(f"   结果: {result}")
        
    except Exception as e:
        logger.error(f"增强登录测试失败: {e}")


async def test_google_captcha_all():
    """测试谷歌验证码所有类型"""
    print("\n🔍 测试谷歌验证码全功能...")
    
    try:
        from google_captcha_solver import solve_captcha_challenge, solve_image_captcha, solve_select_captcha
        from enhanced_website_login import get_enhanced_login
        
        solver = google_captcha_solver()
        
        # 测试不同类型
        tests = [
            ("图片验证码", "image", {
                "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
                "challenge_type": "image",
                "challenge": "https://www.google.com/recaptcha/api.js",
                "image_path": "/tmp/captcha.jpg"
            }),
            ("选择题验证码", "select", {
                "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
                "challenge_type": "select",
                "challenge": "天/山/街道/颜色/红绿灯",
                "options": ["选项A", "选项B", "选项C"],
                "challenge": "https://www.google.com/recaptcha/api.js"
            }),
            ("滑块验证码", "slider", {
                "challenge_type": "slider",
                "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
                "challenge": "https://www.google.com/recaptcha/api.js",
                "position": 0.5,
                "slide_count": 4
            }),
            ("点字验证码", "input", {
                "challenge_type": "input_captcha",
                "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrQMy9749463",
                "challenge": "https://www.google.com/recaptcha/api.js",
                "characters": "ABCD"
            })
        ]
        
        for name, challenge_type, challenge_data in tests:
            print(f"\n3. 测试{name}...")
            print(f"   类型: {challenge_type}")
            
            result = await solve_captcha_challenge(
                challenge_data["url"],
                sitekey=challenge_data.get("sitekey"),
                challenge_type=challenge_data["type"],
                **challenge_data
            )
            
            print(f"   结果: {result}")
            print()
        
    except Exception as e:
        logger.error(f"谷歌验证码测试失败: {e}")


async def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 OpenClaw 集成测试套件")
    print("=" * 60)
    print("")
    
    tests = [
        ("OpenClaw + OpenViking", "openclaw-openviking.md", 15),
        ("网站登录", "website_login.py", "enhanced_website_login.py", 12),
        ("数据采集", "web_data_collector.py", "web_data_collector.py", 18),
        ("验证码", "google_captcha_solver.py", "enhanced_website_login.py", 25),
        ("多用户权限", "multi_user_permission.py", "multi_user_permission.py", 6)
    ]
    
    total = 0
    passed = 0
    failed = 0
    
    for name, file, expected_lines in tests:
        try:
            print(f"\n📋 测试: {name}")
            total += expected_lines
            
            # 动态加载
            import import importlib
            module = importlib.import_module(file.split('.')[0], '', '')
            
            # 导入测试模块
            if hasattr(module, 'main'):
                await module.main()
                passed += 1
                print(f"   ✅ {name} 测试通过")
            else:
                failed += 1
                print(f"   ❌ {name} 测试失败或不存在")
        except Exception as e:
            failed += 1
            print(f"   ⚠️ 错误: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    print("=" * 60)
    
    # 总结
    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查依赖安装")
        print(f"\n📝 可能的问题:")
        print("1. 依赖未安装: pip install aiohttp, bs4, requests,")
        print("2. 配置缺失: OPENCLAW_OPENVIKING_URL, API_KEY 等")
        print("3. 模块导入错误: 检查 Python 路径和模块名是否匹配")
        print("4. API 服务未启动: OpenViking 服务器需要手动启动")


if __name__ == "__main__":
    asyncio.run(main())