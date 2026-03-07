# 斑布纸广告投放 - API Gateway 配置指南

**创建时间**: 2026-03-07 01:55
**目的**: 配置 API Gateway 以集成巨量广告 API

---

## ✅ 已安装的技能

- ✅ **api-gateway**: 已安装（但目录为空，需要重新配置）
- ✅ **baidu-search**: 已安装（可用于搜索百度信息）

---

## 🔧 配置 API Gateway

### 步骤 1: 重新安装 API Gateway

```bash
# 强制重新安装
skillhub install api-gateway --force
```

### 步骤 2: 配置 API Gateway

```bash
# 配置 API Gateway
openclaw configure --section api-gateway
```

### 步骤 3: 添加巨量广告 API 服务

```bash
# 使用 mcporter 添加 MCP 服务器
mcporter config add oceanengine https://api.oceanengine.com
```

### 步骤 4: 验证配置

```bash
# 验证 API Gateway 配置
openclaw status
```

---

## 🚀 使用 API Gateway

### 1. 创建广告计划

```python
from api_gateway import APIGateway

# 初始化
gateway = APIGateway()

# 配置巨量广告 API
oceanengine = gateway.add_service("oceanengine")

# 创建广告计划
campaign = oceanengine.post("/campaign/add", {
    "campaign_name": "斑布纸广告计划",
    "campaign_type": "INFO_FLOW",
    "budget": 10000,
    "start_date": "2026-03-07",
    "end_date": "2026-05-07"
})
```

### 2. 上传广告创意

```python
# 上传视频创意
video_creative = oceanengine.post("/creative/upload", {
    "creative_type": "VIDEO",
    "creative_name": "斑布纸-去油污",
    "video_url": "https://example.com/banbu-video.mp4",
    "duration": 15
})

# 上传图文创意
image_creative = oceanengine.post("/creative/upload", {
    "creative_type": "IMAGE",
    "creative_name": "斑布纸-安全环保",
    "image_url": "https://example.com/banbu-image.jpg"
})
```

### 3. 设置定向人群

```python
# 设置定向人群
targeting = oceanengine.post("/targeting/add", {
    "targeting_name": "斑布纸-25-40岁女性",
    "age_range": [25, 40],
    "gender": "FEMALE",
    "geo": ["北京", "上海", "广州", "深圳"],
    "interests": ["家庭清洁", "母婴用品"]
})
```

### 4. 获取数据报告

```python
# 获取广告计划数据
report = oceanengine.post("/report/campaign", {
    "start_date": "2026-03-07",
    "end_date": "2026-03-14",
    "metrics": ["impressions", "clicks", "conversions", "cost"]
})
```

---

## 📊 数据分析

### 1. 使用百度搜索 API

```bash
# 使用百度搜索 API 获取竞争对手信息
baidu_search "斑布纸 竞争对手"
```

### 2. 使用百度统计 API

```python
# 监控网站流量
analytics = api_gateway.add_service("baidu_analytics")
data = analytics.post("/data/get", {
    "start_date": "2026-03-07",
    "end_date": "2026-03-14"
})
```

---

## 🎯 下一步行动

**你现在想要**：

1. **重新安装 API Gateway**？（强制重新安装）
2. **配置 API Gateway**？（开始配置）
3. **添加巨量广告 API**？（连接巨量广告）
4. **查看完整文档**？（深入了解）

---

**创建时间**: 2026-03-07 01:55
**状态**: ✅ 配置指南已创建

---

## 📞 获取帮助

- **API Gateway 文档**: https://docs.openclaw.ai/skills/api-gateway
- **巨量广告文档**: https://www.oceanengine.com/doc
- **mcporter 文档**: https://docs.openclaw.ai/tools/mcporter

---

**告诉我你的选择，我帮你继续！🚀**
