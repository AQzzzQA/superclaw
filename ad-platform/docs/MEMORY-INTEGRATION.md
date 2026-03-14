# Ad Platform 记忆系统集成文档

## 📚 概述

本文档描述了 Ad Platform 与 OpenViking Memory Plugin 的集成方案，实现了智能记忆存储、检索和优化建议功能。

## 🎯 集成目标

1. **用户偏好记忆**: 存储和检索用户广告投放偏好
2. **历史记录**: 保存广告计划和优化策略的执行历史
3. **智能推荐**: 基于历史数据生成优化建议
4. **上下文感知**: 为用户提供个性化的广告服务体验

## 🏗️ 架构设计

### 系统组件
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ad Platform   │    │ Memory Service  │    │  OpenViking     │
│   (FastAPI)     │◄──►│   (Python)      │◄──►│   (Memory DB)   │
│                 │    │                 │    │                 │
│ - API Endpoints │    │ - User Storage  │    │ - L0/L1/L2 Layers│
│ - Business Logic │    │ - Campaign Hist │    │ - Context Search │
│ - Data Models   │    │ - Strategy Rec  │    │ - Memory Extract │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 数据流
1. 用户请求 → Ad Platform API
2. 业务逻辑处理 → Memory Service
3. 存储操作 → OpenViking Database
4. 检索操作 → Context + Recommendations
5. 响应用户 → 个性化服务

## 🚀 功能特性

### 1. 用户偏好管理
- **存储**: 用户ID、广告计划类型、偏好设置
- **检索**: 按用户ID和类型查询偏好
- **更新**: 实时更新用户偏好

### 2. 广告计划历史
- **存储**: 创建数据、执行结果、性能指标
- **检索**: 按计划ID查询历史记录
- **分析**: 生成结果摘要和效果评分

### 3. 策略优化建议
- **分析**: 偏好与历史数据关联分析
- **建议**: 基于数据的个性化推荐
- **评分**: 优化建议的置信度评估

### 4. 上下文感知
- **会话管理**: 用户会话数据存储
- **上下文加载**: 相关记忆检索
- **持续学习**: 自动提取和存储新信息

## 🔧 API 接口

### 用户偏好接口
```bash
# 获取用户偏好
GET /api/v1/memory/user/{user_id}/preferences

# 存储用户偏好
POST /api/v1/memory/user/{user_id}/preferences
{
    "campaign_type": "brand",
    "preference": {
        "budget": 10000,
        "target_audience": "年轻人"
    },
    "metadata": {"source": "api"}
}
```

### 广告历史接口
```bash
# 获取广告计划历史
GET /api/v1/memory/campaign/{campaign_id}/history?limit=10

# 存储广告历史
POST /api/v1/memory/campaign/{campaign_id}/history
{
    "data": {"name": "春季活动", "budget": 50000},
    "result": {"clicks": 1000, "impressions": 50000, "spend": 10000},
    "metadata": {"source": "api"}
}
```

### 优化建议接口
```bash
# 获取优化建议
GET /api/v1/memory/optimization/suggestions/{user_id}?campaign_type=brand

# 获取用户上下文
GET /api/v1/memory/context/{user_id}
```

## 📊 数据模型

### 用户偏好记忆
```python
{
    "key": "user_{user_id}_preference_{campaign_type}",
    "value": {
        "user_id": "string",
        "campaign_type": "string",
        "preference": {
            "budget": number,
            "target_audience": "string",
            "creative_style": "string",
            "bidding_strategy": "string"
        },
        "created_at": "ISO datetime"
    },
    "metadata": {
        "type": "user_preference",
        "user_id": "string"
    },
    "layer": "L1"
}
```

### 广告计划历史
```python
{
    "key": "campaign_history_{campaign_id}_{timestamp}",
    "value": {
        "campaign_id": "string",
        "creation_data": {
            "name": "string",
            "budget": number,
            "targeting": {}
        },
        "execution_result": {
            "clicks": number,
            "impressions": number,
            "spend": number,
            "conversions": number
        },
        "result_summary": "string",
        "created_at": "ISO datetime"
    },
    "metadata": {
        "type": "campaign_history",
        "campaign_id": "string"
    },
    "layer": "L1"
}
```

### 优化建议
```python
{
    "key": "optimization_{user_id}_{timestamp}",
    "value": {
        "type": "optimization",
        "based_on": "string",
        "suggestion": "string",
        "confidence": 0.8,
        "created_at": "ISO datetime"
    },
    "metadata": {
        "type": "optimization",
        "user_id": "string"
    },
    "layer": "L0"
}
```

## 🧪 测试方案

### 单元测试
- 用户偏好存储/检索测试
- 历史记录功能测试
- 优化建议生成测试
- 上下文加载测试

### 集成测试
- API 端点测试
- OpenViking 连接测试
- 数据一致性测试

### 性能测试
- 大规模数据存储测试
- 检索响应时间测试
- 并发访问测试

## 🔍 配置说明

### 环境变量
```bash
# OpenViking 配置
OCEAN_VIKING_URL=http://localhost:1933
OCEAN_VIKING_API_KEY=your-api-key

# 记忆服务配置
MEMORY_SERVICE_TIMEOUT=60
MEMORY_SERVICE_MAX_RETRIES=3
MEMORY_CACHE_SIZE=1000
```

### 配置文件
```python
# app/core/memory_config.py
MEMORY_CONFIG = {
    "server_url": "http://localhost:1933",
    "api_key": None,
    "timeout": 60,
    "max_retries": 3,
    "cache_size": 1000,
    "default_layer": "L1",
    "optimization_threshold": 0.8
}
```

## 📈 性能优化

### 缓存策略
- **用户偏好缓存**: 10分钟过期
- **历史记录缓存**: 5分钟过期
- **优化建议缓存**: 15分钟过期

### 分层存储
- **L0层**: 核心优化建议（热数据）
- **L1层**: 用户偏好和历史记录（温数据）
- **L2层**: 完整记录（冷数据）

### 批量操作
- 批量存储减少网络开销
- 批量检索提高响应速度
- 异步处理提升用户体验

## 🚨 故障处理

### 连接失败
- 自动重试机制
- 本地缓存降级
- 用户友好的错误提示

### 数据不一致
- 定期数据校验
- 自动修复机制
- 备份恢复策略

### 性能问题
- 监控和告警系统
- 自动扩容机制
- 负载均衡配置

## 🔮 未来规划

### Phase 1 - 当前实现 ✅
- 基础记忆存储和检索
- 用户偏好管理
- 简单优化建议

### Phase 2 - 增强功能 🔄
- 高级分析算法
- A/B 测试集成
- 实时优化建议

### Phase 3 - 人工智能 🌟
- 机器学习优化
- 预测分析
- 自动化策略调整

### Phase 4 - 生态扩展 🚀
- 第三方集成
- 多语言支持
- 企业级功能

## 📞 技术支持

### 联系方式
- 邮箱: memory-support@adplatform.com
- 文档: https://docs.adplatform.com
- 社区: https://community.adplatform.com

### 问题反馈
- GitHub Issues
- 技术支持工单
- 在线客服系统

---

**文档版本**: v1.0
**最后更新**: 2026-03-10
**维护团队**: Ad Platform Architecture Team