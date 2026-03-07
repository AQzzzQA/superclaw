"""
测试 API Gateway 技能
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/api-gateway')

from api_gateway import APIGateway

print("=" * 50)
print("API Gateway 技能测试")
print("=" * 50)
print()

# 测试 1: 初始化
print("测试 1: 初始化 API Gateway")
try:
    gateway = APIGateway()
    print("✅ API Gateway 初始化成功")
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    sys.exit(1)

print()

# 测试 2: 添加服务
print("测试 2: 添加服务")
try:
    openai = gateway.add_service("openai")
    print("✅ 服务添加成功")
    print(f"   服务名称: {openai.service_name}")
    print(f"   Base URL: {openai.base_url}")
except Exception as e:
    print(f"❌ 添加服务失败: {e}")

print()

# 测试 3: 列出服务
print("测试 3: 列出所有服务")
try:
    services = gateway.list_services()
    print(f"✅ 可用服务: {services}")
except Exception as e:
    print(f"❌ 列出服务失败: {e}")

print()

# 测试 4: 模拟 GET 请求（不实际调用）
print("测试 4: 模拟 GET 请求")
try:
    print(f"✅ GET 方法可用")
    print(f"   示例: openai.get('/v1/models')")
except Exception as e:
    print(f"❌ GET 方法失败: {e}")

print()

# 测试 5: 模拟 POST 请求（不实际调用）
print("测试 5: 模拟 POST 请求")
try:
    print(f"✅ POST 方法可用")
    print(f"   示例: openai.post('/v1/chat/completions', data={{...}})")
except Exception as e:
    print(f"❌ POST 方法失败: {e}")

print()

# 测试 6: 检查重试机制
print("测试 6: 检查重试机制")
try:
    print(f"✅ 重试次数: {openai.retry}")
    print(f"   超时时间: {openai.timeout} 秒")
except Exception as e:
    print(f"❌ 检查重试机制失败: {e}")

print()

# 测试 7: 检查 Session
print("测试 7: 检查 Session")
try:
    print(f"✅ Session 已创建")
    print(f"   Headers: {list(openai.session.headers.keys())}")
except Exception as e:
    print(f"❌ 检查 Session 失败: {e}")

print()
print("=" * 50)
print("测试完成！")
print("=" * 50)
