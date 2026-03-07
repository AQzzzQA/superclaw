"""
测试广告优化专家
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from ads_expert import AdsOptimizationExpert

print("=" * 50)
print("广告优化专家 - 子代理测试")
print("=" * 50)
print()

# 创建专家实例
expert = AdsOptimizationExpert()

# 测试 1: 优化广告计划
print("测试 1: 优化广告计划")
campaign_data = {
    "impressions": 100000,
    "clicks": 5000,
    "conversions": 100,
    "cost": 500.00,
    "bid": 1.0
}
result = expert.optimize_campaign(campaign_data)
print(f"✅ 优化结果: {result['decision']}")
print(f"   原因: {result['reason']}")
print(f"   新出价: {result['new_bid']}")
print(f"   指标: {result['metrics']}")
print()

# 测试 2: 排序创意
print("测试 2: 排序创意")
creatives_data = [
    {"id": 1, "name": "创意A", "ctr": 3.5, "conversion_rate": 0.02, "roi": 2.5},
    {"id": 2, "name": "创意B", "ctr": 2.0, "conversion_rate": 0.01, "roi": 1.8},
    {"id": 3, "name": "创意C", "ctr": 1.0, "conversion_rate": 0.005, "roi": 0.8}
]
result = expert.rank_creatives(creatives_data)
print(f"✅ 排序完成，共 {len(result['ranked_creatives'])} 个创意")
for i, creative in enumerate(result['ranked_creatives']):
    print(f"   {i+1}. {creative['name']} - 得分: {creative['total_score']}")
print()
print("优化建议:")
for rec in result['recommendations']:
    print(f"   - {rec['action']}: {rec['reason']}")
print()

# 测试 3: 分层定向人群
print("测试 3: 分层定向人群")
audience_data = [
    {"id": 1, "name": "人群A", "roi": 3.2},
    {"id": 2, "name": "人群B", "roi": 2.0},
    {"id": 3, "name": "人群C", "roi": 1.2}
]
result = expert.segment_audience(audience_data)
print(f"✅ 分层完成 - 高性能 {len(result['segments']['high_performance'])}，中性能 {len(result['segments']['medium_performance'])}，低性能 {len(result['segments']['low_performance'])}")
print()
print("优化建议:")
for rec in result['recommendations']:
    print(f"   - {rec['action']}: {rec['reason']}")
print()

# 测试 4: 检查风险
print("测试 4: 检查风险")
campaign_data = {
    "roi": 0.8,
    "budget_remaining": 100.00,
    "budget_total": 1000.00,
    "ctr": 0.8
}
result = expert.check_risks(campaign_data)
print(f"✅ 风险检查完成，发现 {result['risk_count']} 个风险")
print()
for risk in result['risks']:
    print(f"   - {risk['type']} ({risk['severity']}): {risk['description']}")
    print(f"     建议: {risk['recommendation']}")
print()

print("=" * 50)
print("测试完成！")
print("=" * 50)
