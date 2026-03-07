# 斑布纸广告投放 - API 需求总结

**创建时间**: 2026-03-07 01:50
**目的**: 列出巨量广告投放所需的 API 接口

---

## 🔍 巨量广告 API 分类

### 1. 账户管理 API
```json
账户相关 API:
{
  "api_name": "Account Management",
  "endpoints": [
    "POST /account/get - 获取账户信息",
    "POST /account/update - 更新账户信息",
    "POST /account/balance - 查询账户余额"
  ]
}
```

### 2. 广告计划 API
```json
广告计划相关 API:
{
  "api_name": "Campaign Management",
  "endpoints": [
    "POST /campaign/add - 创建广告计划",
    "POST /campaign/update - 更新广告计划",
    "POST /campaign/get - 获取广告计划列表",
    "POST /campaign/delete - 删除广告计划"
  ]
}
```

### 3. 广告创意 API
```json
创意相关 API:
{
  "api_name": "Creative Management",
  "endpoints": [
    "POST /creative/add - 创建广告创意",
    "POST /creative/update - 更新广告创意",
    "POST /creative/get - 获取创意列表",
    "POST /creative/upload - 上传素材（视频/图片）",
    "POST /creative/delete - 删除创意"
  ]
}
```

### 4. 定向人群 API
```json
定向相关 API:
{
  "api_name": "Targeting Management",
  "endpoints": [
    "POST /targeting/get - 获取定向人群",
    "POST /targeting/update - 更新定向设置",
    "POST /targeting/add - 添加定向人群",
    "POST /targeting/delete - 删除定向人群"
  ]
}
```

### 5. 数据报告 API
```json
数据报告相关 API:
{
  "api_name": "Report Management",
  "endpoints": [
    "POST /report/campaign - 获取广告计划数据",
    "POST /report/creative - 获取创意数据",
    "POST /report/targeting - 获取定向数据",
    "POST /report/custom - 自定义数据报告"
  ]
}
```

### 6. 出价管理 API
```json
出价相关 API:
{
  "api_name": "Bid Management",
  "endpoints": [
    "POST /bid/update - 更新出价",
    "POST /bid/get - 获取出价信息",
    "POST /bid/suggest - 出价建议"
  ]
}
```

### 7. 资质管理 API
```json
资质相关 API:
{
  "api_name": "Qualification Management",
  "endpoints": [
    "POST /qualification/upload - 上传资质材料",
    "POST /qualification/get - 获取资质信息",
    "POST /qualification/status - 查询审核状态"
  ]
}
```

---

## 📊 第三方 API（可选）

### 1. 百度统计 API
```json
百度统计 API:
{
  "api_name": "Baidu Analytics",
  "purpose": "监控网站流量和转化",
  "endpoints": [
    "POST /data/get - 获取访问数据",
    "POST /data/realtime - 获取实时数据",
    "POST /event/track - 追踪事件"
  ]
}
```

### 2. 友盟统计 API
```json
友盟统计 API:
{
  "api_name": "Umeng Analytics",
  "purpose": "APP 数据分析和用户行为追踪",
  "endpoints": [
    "POST /data/get - 获取 APP 数据",
    "POST /user/profile - 用户画像",
    "POST /event/track - 事件追踪"
  ]
}
```

### 3. 神策数据 API
```json
神策数据 API:
{
  "api_name": "Sensors Analytics",
  "purpose": "用户行为分析和转化漏斗",
  "endpoints": [
    "POST /data/get - 获取用户数据",
    "POST /funnel/analysis - 转化漏斗分析",
    "POST /user/segment - 用户分群"
  ]
}
```

---

## 🚀 集成方案

### 方案 1: 使用 API Gateway 技能（推荐）

**优势**:
- ✅ 无需编写代码
- ✅ 支持 OAuth 管理
- ✅ 支持 100+ API
- ✅ 快速集成

**使用方法**:
```bash
# 安装 API Gateway 技能
skillhub install api-gateway

# 配置巨量广告 API
openclaw configure --section api-gateway
```

### 方案 2: 使用 mcporter 技能

**优势**:
- ✅ 直接调用 MCP 服务器
- ✅ 支持自定义配置
- ✅ 支持复杂集成

**使用方法**:
```bash
# 安装 mcporter 技能
skillhub install mcporter

# 配置 MCP 服务器
mcporter config add oceanengine https://api.oceanengine.com
```

---

## 📋 需要的 API 权限

### 1. 基础权限
- ✅ 账户读取权限
- ✅ 广告计划管理权限
- ✅ 创意上传权限
- ✅ 定向人群管理权限
- ✅ 数据报告读取权限

### 2. 高级权限（可选）
- ✅ 出价修改权限
- ✅ 资质上传权限
- ✅ 实时数据推送权限

---

## 💡 开发建议

### 1. 使用 API Gateway 快速集成
```python
from api_gateway import APIGateway

# 初始化
gateway = APIGateway()

# 配置巨量广告 API
oceanengine = gateway.add_service("oceanengine")

# 获取账户信息
account = oceanengine.get("/account/get")
print(account)
```

### 2. 使用 mcporter 进行深度集成
```bash
# 配置 MCP 服务器
mcporter config add oceanengine https://api.oceanengine.com

# 调用 API
mcporter call oceanengine /account/get
```

---

## 📞 获取 API

### 1. 巨量广告官方
- **官网**: https://www.oceanengine.com
- **文档**: https://www.oceanengine.com/doc
- **申请**: 注册广告主账户

### 2. API Gateway
- **技能**: api-gateway
- **版本**: 1.0.54
- **安装**: skillhub install api-gateway

### 3. mcporter
- **技能**: mcporter
- **版本**: 1.0.0
- **安装**: skillhub install mcporter

---

**创建时间**: 2026-03-07 01:50
**状态**: ✅ API 需求总结完成

---

## 🎯 立即行动

**你现在想要**：
1. **安装 API Gateway**？（快速集成）
2. **安装 mcporter**？（深度集成）
3. **查看巨量广告文档**？（了解 API）
4. **开始开发**？（创建广告管理系统）

**告诉我你的选择！🚀**
