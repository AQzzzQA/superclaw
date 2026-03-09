# 巨量广告技能开发方案

> 对接巨量广告 API 的 OpenClaw Skill
> 创建时间：2026-03-09 15:44
> 开发者：奥特姆（Atom）

---

## 📋 需求分析

### 巨量广告平台
巨量广告是字节跳动的广告平台，包括：
- **巨量引擎**（今日头条广告）
- **巨量千川**（抖音广告）
- **穿山甲**（程序化广告）

### 核心功能需求
1. **广告账户管理**：查看账户信息、余额、资质
2. **广告计划管理**：创建、编辑、暂停、删除广告计划
3. **广告组管理**：管理广告组、设置预算、定向
4. **广告创意管理**：上传素材、管理创意
5. **数据报表**：查看广告数据、花费、转化
6. **优化建议**：基于数据分析提供优化建议

---

## 🔧 技术方案

### 1. API 对接

#### 巨量广告 API
- **API 文档**：https://ad.oceanengine.com/
- **认证方式**：OAuth 2.0
- **支持功能**：
  - 广告计划
  - 广告组
  - 广告创意
  - 数据报表
  - 定向标签
  - 账户管理

#### 技术栈
```
语言：Python
HTTP库：requests
认证：OAuth 2.0
数据格式：JSON
```

---

## 📁 技能文件结构

```
oceanengine-ads/
├── SKILL.md              # 技能说明文档
├── _meta.json            # 技能元数据
├── config.py             # 配置管理
├── auth.py               # OAuth 认证
├── api_client.py         # API 客户端
├── campaigns.py          # 广告计划管理
├── adgroups.py           # 广告组管理
├── creatives.py          # 广告创意管理
├── reports.py            # 数据报表
├── optimizer.py          # 优化建议
├── utils.py              # 工具函数
└── requirements.txt       # 依赖列表
```

---

## 🎯 功能模块设计

### 模块1：认证管理 (auth.py)

#### 功能
- OAuth 2.0 认证流程
- Access Token 管理
- Token 刷新

#### API 接口
```python
class OceanEngineAuth:
    def get_auth_url(self) -> str
    def exchange_code_for_token(self, code: str) -> dict
    def refresh_token(self, refresh_token: str) -> dict
    def get_valid_token(self) -> str
```

---

### 模块2：广告计划 (campaigns.py)

#### 功能
- 查询广告计划列表
- 创建广告计划
- 更新广告计划
- 暂停/启用广告计划
- 删除广告计划

#### API 接口
```python
class CampaignManager:
    def list_campaigns(self, account_id: str) -> list
    def get_campaign(self, campaign_id: str) -> dict
    def create_campaign(self, account_id: str, config: dict) -> dict
    def update_campaign(self, campaign_id: str, updates: dict) -> dict
    def pause_campaign(self, campaign_id: str) -> dict
    def resume_campaign(self, campaign_id: str) -> dict
    def delete_campaign(self, campaign_id: str) -> dict
```

#### 广告计划配置
```python
{
    "campaign_name": "测试广告计划",
    "campaign_type": "FEED",  # 信息流
    "objective": "CONVERSIONS",  # 转化
    "budget_mode": "BUDGET_MODE_DAY",  # 日预算
    "budget": 10000,  # 100元（单位：分）
    "start_time": "2026-03-10 00:00:00",
    "end_time": "2026-03-20 23:59:59",
    "targeting": {
        "gender": ["MALE", "FEMALE"],
        "age": [18, 65],
        "region": ["CN"]
    }
}
```

---

### 模块3：广告组 (adgroups.py)

#### 功能
- 查询广告组列表
- 创建广告组
- 更新广告组
- 设置定向

#### API 接口
```python
class AdGroupManager:
    def list_adgroups(self, campaign_id: str) -> list
    def get_adgroup(self, adgroup_id: str) -> dict
    def create_adgroup(self, campaign_id: str, config: dict) -> dict
    def update_adgroup(self, adgroup_id: str, updates: dict) -> dict
    def set_targeting(self, adgroup_id: str, targeting: dict) -> dict
```

#### 定向配置
```python
{
    "adgroup_name": "测试广告组",
    "budget": 5000,  # 50元
    "targeting": {
        "gender": ["MALE"],
        "age": [18, 35],
        "location": {
            "type": "CITY",
            "values": ["110000"]  # 北京
        },
        "interest": ["科技", "互联网"]
    }
}
```

---

### 模块4：广告创意 (creatives.py)

#### 功能
- 查询广告创意列表
- 上传图片素材
- 上传视频素材
- 创建广告创意

#### API 接口
```python
class CreativeManager:
    def list_creatives(self, account_id: str) -> list
    def get_creative(self, creative_id: str) -> dict
    def upload_image(self, image_path: str) -> dict
    def upload_video(self, video_path: str) -> dict
    def create_creative(self, adgroup_id: str, creative_config: dict) -> dict
```

#### 创意配置
```python
{
    "creative_name": "测试创意",
    "creative_type": "IMAGE",  # IMAGE/VIDEO
    "creative_material_id": "123456789",  # 素材ID
    "ad_text": "这是测试广告文案",
    "landing_page_url": "https://example.com"
}
```

---

### 模块5：数据报表 (reports.py)

#### 功能
- 查询广告数据报表
- 按日期范围筛选
- 按维度分组（计划/组/创意）
- 导出报表

#### API 接口
```python
class ReportManager:
    def get_campaign_report(self, account_id: str, start_date: str, end_date: str) -> list
    def get_adgroup_report(self, adgroup_id: str, start_date: str, end_date: str) -> list
    def get_creative_report(self, creative_id: str, start_date: str, end_date: str) -> list
    def get_account_report(self, account_id: str, start_date: str, end_date: str) -> dict
```

#### 报表指标
```python
{
    "date": "2026-03-09",
    "campaign_id": "123456789",
    "campaign_name": "测试广告计划",
    "impressions": 10000,      # 曝光
    "clicks": 500,             # 点击
    "ctr": 5.0,                # 点击率 (%)
    "cpc": 2.0,                # 点击成本（元）
    "cpm": 200.0,              # 千次曝光成本（元）
    "cost": 1000.0,             # 消耗（元）
    "conversions": 50,         # 转化数
    "cpa": 20.0                # 转化成本（元）
    "roi": 300.0               # 投入产出比（%）
}
```

---

### 模块6：优化建议 (optimizer.py)

#### 功能
- 分析广告数据
- 识别低效广告
- 提供优化建议
- 预算重新分配建议

#### API 接口
```python
class AdOptimizer:
    def analyze_campaign_performance(self, account_id: str, days: int) -> dict
    def identify_wasted_spend(self, account_id: str) -> list
    def suggest_budget_reallocation(self, account_id: str) -> dict
    def optimize_targeting(self, adgroup_id: str) -> dict
    def generate_optimization_report(self, account_id: str) -> str
```

---

## 📝 SKILL.md 文档

```markdown
---
name: oceanengine-ads
display_name: 巨量广告 API
version: 1.0.0
tags: [oceanengine, advertising, tiktok, bytedance]
---

# 巨量广告 API — Ocean Engine Ads

## Description

全功能集成巨量广告（Ocean Engine Ads）API，支持巨量引擎、巨量千川、穿山甲广告。管理广告计划、广告组、广告创意，查看数据报表，获取优化建议。

## Setup

### Environment Variables

- `OCEANENGINE_ACCESS_TOKEN` - 巨量广告访问令牌
- `OCEANENGINE_REFRESH_TOKEN` - 刷新令牌（可选）
- `OCEANENGINE_APP_ID` - 应用ID
- `OCEANENGINE_APP_SECRET` - 应用密钥

### Authentication

使用 OAuth 2.0 认证流程：

```bash
# 1. 获取授权URL
python3 -c "from auth import OceanEngineAuth; print(OceanEngineAuth().get_auth_url())"

# 2. 用户授权后，获取code
python3 -c "from auth import OceanEngineAuth; print(OceanEngineAuth().exchange_code_for_token('YOUR_CODE'))"
```

## API Reference

### 广告计划管理

#### 查询广告计划列表
```bash
curl -X GET "https://ad.oceanengine.com/open_api/v3.0/campaign/get/" \
  -H "Access-Token: $OCEANENGINE_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

#### 创建广告计划
```bash
curl -X POST "https://ad.oceanengine.com/open_api/v3.0/campaign/create/" \
  -H "Access-Token: $OCEANENGINE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "测试广告计划",
    "campaign_type": "FEED",
    "objective": "CONVERSIONS",
    "budget_mode": "BUDGET_MODE_DAY",
    "budget": 10000,
    "start_time": "2026-03-10 00:00:00",
    "end_time": "2026-03-20 23:59:59"
  }'
```

#### 暂停广告计划
```bash
curl -X POST "https://ad.oceanengine.com/open_api/v3.0/campaign/update_status/" \
  -H "Access-Token: $OCEANENGINE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_ids": ["123456789"],
    "opt_status": "DISABLE"
  }'
```

### 广告组管理

#### 创建广告组
```bash
curl -X POST "https://ad.oceanengine.com/open_api/v3.0/adgroup/create/" \
  -H "Access-Token: $OCEANENGINE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "123456789",
    "adgroup_name": "测试广告组",
    "budget": 5000,
    "targeting": {
      "gender": ["MALE"],
      "age": [18, 35],
      "location": {
        "type": "CITY",
        "values": ["110000"]
      }
    }
  }'
```

### 数据报表

#### 查询广告数据
```bash
curl -X GET "https://ad.oceanengine.com/open_api/v3.0/report/campaign/get/" \
  -H "Access-Token: $OCEANENGINE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2026-03-01",
    "end_date": "2026-03-09",
    "dimensions": ["CAMPAIGN"],
    "metrics": ["cost", "impressions", "clicks", "ctr", "cpc", "conversions", "cpa"]
  }'
```

## 功能特性

### 广告计划
- 创建、编辑、暂停、删除广告计划
- 支持多种广告类型（信息流、搜索、开屏等）
- 支持多种优化目标（转化、下载、激活等）

### 广告组
- 精细化定向（性别、年龄、地域、兴趣等）
- 预算控制
- 出价管理

### 广告创意
- 图片素材上传
- 视频素材上传
- 创意库管理
- A/B测试支持

### 数据报表
- 实时数据查询
- 多维度报表
- 自定义日期范围
- 数据导出

### 优化建议
- 识别低效广告
- 预算重新分配
- 定向优化建议
- ROI分析

## 安全规则

1. **所有创建操作需要用户确认**
2. **广告预算变更需要二次确认**
3. **Token 安全存储**
4. **操作日志记录**
5. **错误处理和重试机制**

## 使用示例

### 查询今日广告数据
```python
from api_client import OceanEngineClient
from reports import ReportManager

client = OceanEngineClient()
report_manager = ReportManager(client)

# 获取今日数据
report = report_manager.get_account_report(
    account_id="act_123456",
    start_date="2026-03-09",
    end_date="2026-03-09"
)

print(f"今日消耗: {report['cost']}元")
print(f"今日曝光: {report['impressions']}")
print(f"今日点击: {report['clicks']}")
```

### 创建测试广告
```python
from campaigns import CampaignManager
from adgroups import AdGroupManager
from creatives import CreativeManager

campaign_mgr = CampaignManager(client)
adgroup_mgr = AdGroupManager(client)
creative_mgr = CreativeManager(client)

# 1. 创建广告计划
campaign = campaign_mgr.create_campaign(
    account_id="act_123456",
    config={
        "campaign_name": "测试广告计划",
        "objective": "CONVERSIONS",
        "budget": 10000
    }
)

# 2. 创建广告组
adgroup = adgroup_mgr.create_adgroup(
    campaign_id=campaign['id'],
    config={
        "adgroup_name": "测试广告组",
        "budget": 5000
    }
)

# 3. 创建广告创意
creative = creative_mgr.create_creative(
    adgroup_id=adgroup['id'],
    creative_config={
        "creative_type": "IMAGE",
        "ad_text": "这是测试广告",
        "landing_page_url": "https://example.com"
    }
)

print(f"广告创建完成: {campaign['id']}")
```

## 价格说明

本技能完全免费，巨量广告API调用费用由巨量广告平台收取。

## 支持的广告平台

| 平台 | 广告类型 |
|------|----------|
| 巨量引擎 | 今日头条信息流、搜索广告 |
| 巨量千川 | 抖音信息流、开屏广告 |
| 穿山甲 | 程序化广告 |

## 开发者

- 技能名称：oceanengine-ads
- 版本：1.0.0
- 作者：奥特姆（Atom）
- 许可证：MIT

## 更新日志

### v1.0.0 (2026-03-09)
- 初始版本
- 支持广告计划管理
- 支持广告组管理
- 支持广告创意管理
- 支持数据报表查询
- 支持优化建议生成
```

---

## 🚀 开发步骤

### 第1步：搭建基础框架
- [ ] 创建项目目录结构
- [ ] 编写 SKILL.md 文档
- [ ] 编写 _meta.json 元数据
- [ ] 初始化 requirements.txt

### 第2步：实现认证模块
- [ ] OAuth 2.0 认证流程
- [ ] Token 管理和刷新
- [ ] 环境变量配置

### 第3步：实现API客户端
- [ ] HTTP 客户端封装
- [ ] 错误处理和重试机制
- [ ] 日志记录

### 第4步：实现核心功能
- [ ] 广告计划管理
- [ ] 广告组管理
- [ ] 广告创意管理
- [ ] 数据报表查询

### 第5步：实现优化模块
- [ ] 数据分析功能
- [ ] 优化建议生成
- [ ] ROI计算

### 第6步：测试和发布
- [ ] 单元测试
- [ ] 集成测试
- [ ] 文档完善
- [ ] 发布到 SkillHub

---

## 📦 依赖清单

```txt
# requirements.txt
requests>=2.28.0
python-dotenv>=1.0.0
pydantic>=2.0.0
python-dateutil>=2.8.0
```

---

## ⚠️ 注意事项

1. **API 限流**：巨量广告有API调用频率限制，需要实现限流处理
2. **数据准确性**：报表数据有延迟，注意查看更新时间
3. **审核机制**：广告创建后需要审核，注意审核状态
4. **预算单位**：预算单位是"分"，1元=100分
5. **时区处理**：巨量广告使用东八区时间，注意时区转换

---

## 🎯 预计工作量

| 阶段 | 工作量 | 时间 |
|------|--------|------|
| 框架搭建 | 4小时 | 0.5天 |
| 认证模块 | 4小时 | 0.5天 |
| API客户端 | 4小时 | 0.5天 |
| 核心功能 | 16小时 | 2天 |
| 优化模块 | 8小时 | 1天 |
| 测试调试 | 4小时 | 0.5天 |
| **总计** | **40小时** | **5天** |

---

## 💡 使用建议

### 适用场景
- 抖音广告投放
- 今日头条广告投放
- 穿山甲程序化广告
- 广告数据分析和优化

### 目标用户
- 抖音运营人员
- 广告优化师
- 数字营销经理
- 媒介采购人员

---

## 📞 后续扩展

### 未来功能
- 支持更多广告类型
- 智能出价建议
- 自动A/B测试
- 竞品广告分析
- 实时告警通知

---

**开发状态**：规划中
**预计完成时间**：2026-03-14（5个工作日）
**优先级**：高

---

需要我开始开发吗？😊
