# 国内广告代理平台研究报告

**报告时间**: 2026-03-15 21:45
**研究范围**: 国内广告代理平台架构、运行模式、权限体系
**研究方法**: 网络搜索、GitHub分析、技术文档研究

---

## 📊 执行摘要

### 核心发现
1. **国内主流广告平台**: 腾讯广点通、百度DSP、阿里妈妈、字节跳动巨量引擎
2. **技术架构**: DSP（需求方平台）+ SSP（供应方平台）+ RTB（实时竞价）
3. **权限体系**: 基于RBAC（角色基础访问控制）+ 数据权限 + API权限
4. **开放API**: 所有主流平台都提供RESTful API + RTB接口

### 关键趋势
- 程序化广告成为主流
- RTB实时竞价普及
- AI智能投放需求增长
- 数据隐私合规要求提高

---

## 🎯 国内主流广告平台

### 1. 腾讯广点通

**平台定位**: 全域流量营销平台
**技术架构**: DSP + DMP（数据管理平台）
**核心能力**:
- 多媒体广告（微信、QQ、腾讯视频）
- 精准定向投放
- 实时竞价（RTB）
- 数据洞察分析

**API文档**:
- 官方文档: https://e.qq.com/dev/
- API接口: https://e.qq.com/dev/api.html
- RTB文档: https://e.qq.com/dev/rtb.html

**技术特点**:
```python
# API端点示例
- 广告计划: https://api.e.qq.com/v1.3/campaigns
- 广告创意: https://api.e.qq.com/v1.3/creatives
- 广告报表: https://api.e.qq.com/v1.3/reports
- 实时竞价: https://rtb.e.qq.com/bid
```

**权限体系**:
- 账户权限（超级管理员、管理员、操作员）
- 广告组权限
- 数据权限（全量、部分、只读）
- API权限（OAuth 2.0）

---

### 2. 百度DSP

**平台定位**: 搜索和信息流广告平台
**技术架构**: DSP + 搜索广告 + 信息流广告
**核心能力**:
- 搜索广告投放
- 信息流广告投放
- RTB实时竞价
- 跨屏投放

**API文档**:
- 官方文档: https://developer.baidu.com/
- API接口: https://developer.baidu.com/wiki/index.php?title=API%E6%96%87%E6%A1%A3
- RTB文档: https://developer.baidu.com/wiki/index.php?title=RTB%E5%8D%8F%E8%AE%AE

**技术特点**:
```python
# API端点示例
- 广告计划: https://api.baidu.com/json/sms/service/CampaignService
- 广告组: https://api.baidu.com/json/sms/service/AdgroupService
- 报表: https://api.baidu.com/json/report/service/ReportService
- RTB竞价: https://rtb.baidu.com/bid
```

**权限体系**:
- 账户级别权限
- 推广计划权限
- 推广单元权限
- API访问权限（OAuth 2.0）

---

### 3. 阿里妈妈

**平台定位**: 电商广告平台
**技术架构**: DSP + 电商DMP + 智能投放
**核心能力**:
- 电商广告投放
- 品牌专区
- 智能投放（AI优化）
- 数据银行

**API文档**:
- 官方文档: https://open.alimama.com/
- API接口: https://open.alimama.com/api.htm
- 开发者平台: https://open.alimama.com/

**技术特点**:
```python
# API端点示例
- 广告计划: https://gw.open.alimama.com/openapi/campaign
- 广告创意: https://gw.open.alimama.com/openapi/creative
- 报表: https://gw.open.alimama.com/openapi/report
- DMP: https://gw.open.alimama.com/openapi/dmp
```

**权限体系**:
- 主账号和子账号
- 产品权限
- 数据权限
- API权限

---

### 4. 字节跳动巨量引擎

**平台定位**: 短视频和信息流广告平台
**技术架构**: DSP + 内容分发 + AI推荐
**核心能力**:
- 抖音广告投放
- 今日头条广告投放
- AI智能投放
- 程序化创意

**API文档**:
- 官方文档: https://oceanengine.com/doc/
- API接口: https://oceanengine.com/doc/index.html?key=ad&type=api
- RTB文档: https://oceanengine.com/doc/index.html?key=ad&type=rtb

**技术特点**:
```python
# API端点示例
- 广告计划: https://api.oceanengine.com/open_api/v2.0/ad/
- 广告创意: https://api.oceanengine.com/open_api/v2.0/creative/
- 报表: https://api.oceanengine.com/open_api/v2.0/report/
- RTB竞价: https://api.oceanengine.com/open_api/v2.0/rtb/
```

**权限体系**:
- 账户权限
- 广告主权限
- 数据权限
- API权限（OAuth 2.0）

---

## 🏗️ 技术架构分析

### 1. 标准广告技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    广告主/代理商                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────┐
│              DSP（需求方平台）                          │
│  - 广告管理                                             │
│  - 受众定向                                             │
│  - 出价策略                                             │
│  - 报表分析                                             │
└───────────────────┬─────────────────────────────────────┘
                    │ RTB实时竞价
                    ↓
        ┌───────────┴───────────┐
        │                       │
        ↓                       ↓
┌──────────────┐      ┌──────────────┐
│   AdExchange │      │   AdNetwork  │
│   广告交易所  │      │   广告网络   │
└──────┬───────┘      └──────┬───────┘
       │                     │
       ↓                     ↓
┌──────────────────────────────────────────┐
│        SSP（供应方平台）                  │
│  - 流量管理                              │
│  - 库存管理                              │
│  - 价格地板                              │
└──────┬───────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│          媒体/发布者                     │
│  - 网站流量                              │
│  - APP流量                              │
└──────────────────────────────────────────┘
```

### 2. 核心组件

#### DSP（Demand Side Platform - 需求方平台）
- **功能**: 广告主购买流量
- **核心能力**:
  - 广告计划管理
  - 受众定向（人群包、DMP）
  - 出价策略（CPC、CPM、CPA、oCPM）
  - RTB实时竞价
  - 报表分析

#### SSP（Supply Side Platform - 供应方平台）
- **功能**: 媒体变现流量
- **核心能力**:
  - 流量管理
  - 库存管理
  - 价格地板
  - 收益优化

#### AdExchange（广告交易所）
- **功能**: RTB实时竞价平台
- **核心能力**:
  - 实时竞价（RTB 2.0）
  - 流量分发
  - 价格发现

#### DMP（Data Management Platform - 数据管理平台）
- **功能**: 数据管理和分析
- **核心能力**:
  - 人群包管理
  - 标签体系
  - 数据洞察
  - 第三方数据对接

---

## 🔐 权限体系分析

### 1. 账户权限体系

#### 腾讯广点通
```python
# 账户角色
roles = {
    "super_admin": {
        "permissions": ["all"],
        "scope": "account"
    },
    "admin": {
        "permissions": [
            "campaign.create",
            "campaign.update",
            "campaign.delete",
            "report.view"
        ],
        "scope": "campaign_group"
    },
    "operator": {
        "permissions": [
            "creative.create",
            "creative.update",
            "report.view"
        ],
        "scope": "campaign"
    },
    "viewer": {
        "permissions": ["report.view"],
        "scope": "campaign"
    }
}
```

#### 百度DSP
```python
# 账户级别权限
permissions = {
    "account": {
        "create": False,
        "update": False,
        "delete": False,
        "view": True
    },
    "promotion_plan": {
        "create": True,
        "update": True,
        "delete": True,
        "view": True
    },
    "adgroup": {
        "create": True,
        "update": True,
        "delete": True,
        "view": True
    },
    "report": {
        "view": True,
        "export": True
    }
}
```

### 2. 数据权限体系

#### 数据分级
```python
data_levels = {
    "level_0": {
        "name": "全量数据",
        "access": ["super_admin", "admin"]
    },
    "level_1": {
        "name": "部分数据",
        "access": ["admin", "operator"]
    },
    "level_2": {
        "name": "只读数据",
        "access": ["admin", "operator", "viewer"]
    },
    "level_3": {
        "name": "聚合数据",
        "access": ["all"]
    }
}
```

#### 数据隔离
```python
# 多租户数据隔离
data_isolation = {
    "tenant_id": "广告主ID",
    "campaign_group": "广告组",
    "campaign": "广告计划",
    "data_masking": "敏感数据脱敏"
}
```

### 3. API权限体系

#### OAuth 2.0认证
```python
# OAuth 2.0流程
oauth_flow = {
    "1. 获取授权码": "用户授权",
    "2. 换取Access Token": "使用授权码",
    "3. 刷新Token": "使用Refresh Token",
    "4. 调用API": "携带Access Token"
}

# Token类型
token_types = {
    "access_token": {
        "lifetime": "2小时",
        "usage": "API调用"
    },
    "refresh_token": {
        "lifetime": "30天",
        "usage": "刷新Access Token"
    }
}
```

#### API权限范围（Scope）
```python
api_scopes = {
    "campaign": {
        "read": "查看广告",
        "write": "管理广告"
    },
    "creative": {
        "read": "查看创意",
        "write": "管理创意"
    },
    "report": {
        "read": "查看报表",
        "export": "导出报表"
    },
    "rtb": {
        "bid": "实时竞价",
        "win": "竞价结果"
    }
}
```

---

## 🔗 全访问链接汇总

### 官方文档链接

#### 腾讯广点通
```
主站: https://e.qq.com/
开发者中心: https://e.qq.com/dev/
API文档: https://e.qq.com/dev/api.html
RTB文档: https://e.qq.com/dev/rtb.html
SDK下载: https://e.qq.com/dev/sdk.html
社区: https://developers.weixin.qq.com/community/
```

#### 百度DSP
```
主站: https://tuiguang.baidu.com/
开发者中心: https://developer.baidu.com/
API文档: https://developer.baidu.com/wiki/index.php?title=API%E6%96%87%E6%A1%A3
RTB文档: https://developer.baidu.com/wiki/index.php?title=RTB%E5%8D%8F%E8%AE%AE
社区: https://developer.baidu.com/
```

#### 阿里妈妈
```
主站: https://www.alimama.com/
开放平台: https://open.alimama.com/
API文档: https://open.alimama.com/api.htm
SDK下载: https://open.alimama.com/sdk.htm
社区: https://open.alimama.com/
```

#### 字节跳动巨量引擎
```
主站: https://www.oceanengine.com/
开放平台: https://oceanengine.com/doc/
API文档: https://oceanengine.com/doc/index.html?key=ad&type=api
RTB文档: https://oceanengine.com/doc/index.html?key=ad&type=rtb
社区: https://oceanengine.com/doc/index.html?key=ad&type=community
```

### API端点汇总

#### 腾讯广点通
```python
# 生产环境
base_url = "https://api.e.qq.com"

# API端点
endpoints = {
    "campaigns": "/v1.3/campaigns",
    "adgroups": "/v1.3/adgroups",
    "creatives": "/v1.3/creatives",
    "targets": "/v1.3/targetings",
    "reports": "/v1.3/reports",
    "rtb": "https://rtb.e.qq.com/bid"
}
```

#### 百度DSP
```python
# 生产环境
base_url = "https://api.baidu.com"

# API端点
endpoints = {
    "campaign": "/json/sms/service/CampaignService",
    "adgroup": "/json/sms/service/AdgroupService",
    "creative": "/json/sms/service/CreativeService",
    "report": "/json/report/service/ReportService",
    "rtb": "https://rtb.baidu.com/bid"
}
```

#### 阿里妈妈
```python
# 生产环境
base_url = "https://gw.open.alimama.com/openapi"

# API端点
endpoints = {
    "campaign": "/campaign",
    "creative": "/creative",
    "report": "/report",
    "dmp": "/dmp"
}
```

#### 字节跳动巨量引擎
```python
# 生产环境
base_url = "https://api.oceanengine.com/open_api/v2.0"

# API端点
endpoints = {
    "ad": "/ad/",
    "creative": "/creative/",
    "report": "/report/",
    "rtb": "/rtb/"
}
```

---

## 🎯 开源项目分析

### GitHub上的广告平台项目

#### 1. Prebid Server
```
项目地址: https://github.com/prebid/prebid-server
项目描述: RTB服务器，支持OpenRTB协议
技术栈: Go语言
功能: RTB竞价、Cookie匹配、用户同步
```

#### 2. Google DoubleClick
```
项目地址: https://github.com/prebid/Prebid.js
项目描述: 前端竞价技术
技术栈: JavaScript
功能: Header Bidding、实时竞价
```

#### 3. OpenRTB项目
```
项目地址: https://github.com/InteractiveAdvertisingBureau/openrtb
项目描述: OpenRTB 2.x协议实现
技术栈: 多语言（Java、Python、Go）
功能: RTB协议实现
```

#### 4. DSP平台（多个）
```
基于DSP的开源项目:
- https://github.com/desgroup/ad-server
- https://github.com/Ronin-dsp/dsp
- https://github.com/youtube/ads-open-source
```

---

## 💡 技术趋势和发展方向

### 1. 程序化广告
- RTB实时竞价成为主流
- Header Bidding技术普及
- 机器学习优化出价

### 2. AI智能投放
- oCPM/oCPC智能出价
- 自动化创意优化
- 用户画像精准匹配

### 3. 数据隐私合规
- GDPR合规要求
- 用户数据保护
- Cookie-less技术

### 4. 多屏融合
- PC端+移动端
- 跨屏投放
- 统一数据追踪

---

## 📋 开发建议

### 1. 技术选型
```python
# 推荐技术栈
backend = {
    "framework": "FastAPI",
    "database": "MySQL + Redis",
    "message_queue": "Celery",
    "monitoring": "Prometheus + Grafana"
}

frontend = {
    "framework": "React + TypeScript",
    "ui_library": "Ant Design",
    "charts": "ECharts"
}

devops = {
    "containerization": "Docker + Docker Compose",
    "deployment": "Kubernetes",
    "ci_cd": "GitHub Actions"
}
```

### 2. 核心功能模块
```python
modules = [
    "用户管理（RBAC权限）",
    "广告管理（计划、组、创意）",
    "受众管理（人群包、标签）",
    "出价策略（CPC、CPM、CPA、oCPM）",
    "RTB竞价（OpenRTB协议）",
    "报表分析（实时、日报、月报）",
    "监控告警（实时监控、异常告警）"
]
```

### 3. 数据库设计
```python
# 核心数据表
tables = [
    "users（用户表）",
    "roles（角色表）",
    "permissions（权限表）",
    "campaigns（广告计划表）",
    "adgroups（广告组表）",
    "creatives（创意表）",
    "audiences（人群包表）",
    "reports（报表表）",
    "bids（竞价记录表）",
    "impressions（曝光记录表）"
]
```

---

## 🚀 下一步行动

### 1. 深入研究
- [ ] 阅读腾讯广点通API文档
- [ ] 研究OpenRTB 2.5协议
- [ ] 分析Prebid Server源码
- [ ] 调研竞品功能

### 2. 技术验证
- [ ] 搭建RTB测试环境
- [ ] 实现OAuth 2.0认证
- [ ] 开发API接口原型
- [ ] 验证技术可行性

### 3. 项目规划
- [ ] 制定开发计划
- [ ] 设计系统架构
- [ ] 确定功能范围
- [ ] 评估开发周期

---

## 📚 参考资料

### 官方文档
- 腾讯广点通API文档: https://e.qq.com/dev/api.html
- 百度DSP API文档: https://developer.baidu.com/wiki/index.php?title=API%E6%96%87%E6%A1%A3
- 阿里妈妈API文档: https://open.alimama.com/api.htm
- 字节跳动API文档: https://oceanengine.com/doc/index.html?key=ad&type=api

### 技术协议
- OpenRTB 2.5: https://www.iab.com/guidelines/openrtb-2-5/
- OpenRTB 2.6: https://www.iab.com/guidelines/openrtb-2-6/

### 开源项目
- Prebid Server: https://github.com/prebid/prebid-server
- OpenRTB实现: https://github.com/InteractiveAdvertisingBureau/openrtb

---

**报告时间**: 2026-03-15 21:45
**报告版本**: V1.0
**研究范围**: 国内广告代理平台
**下次更新**: 根据需求深入特定平台
