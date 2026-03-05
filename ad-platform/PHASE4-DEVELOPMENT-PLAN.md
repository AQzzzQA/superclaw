# Phase 4 开发计划 - 智能化与审计功能

**更新时间**: 2026-03-01 22:15
**预估工期**: 9周
**当前版本**: V2.0 → V3.0

---

## 📋 开发原则

### 代码规范
- 单文件行数超过 500 行 → 警告
- 单文件行数超过 800-1000 行 → **强制拆分**
- 按功能模块拆分，不改变界面和功能
- 保持API接口不变，向下兼容

### 拆分原则
1. 按功能模块拆分（如：定向、出价、监控）
2. 按层级拆分（API层、Service层、Model层）
3. 按职责拆分（Controller、Service、Repository）
4. 保持单一职责原则

---

## 🚀 Phase 4 功能清单

### Week 1-2: 定向投放功能

#### 后端模块

**文件拆分规划**

```
app/api/
├── targeting.py          (新建) 定向管理API (~200行)
└── __init__.py          (更新) 注册路由

app/models/
├── targeting.py          (新建) 定向数据模型 (~100行)
└── __init__.py          (更新) 导入模型

app/services/
├── targeting.py          (新建) 定向业务逻辑 (~300行)
└── __init__.py          (更新) 导入服务

app/schemas/
├── targeting.py          (新建) 定向数据验证 (~150行)
└── __init__.py          (更新) 导入schemas
```

**API 端点**

```python
# app/api/targeting.py

- GET    /api/targeting/audience      # 人群定向列表
- POST   /api/targeting/audience      # 创建人群定向
- PUT    /api/targeting/audience/{id} # 更新人群定向
- DELETE /api/targeting/audience/{id} # 删除人群定向

- GET    /api/targeting/device       # 设备定向列表
- POST   /api/targeting/device       # 创建设备定向
- PUT    /api/targeting/device/{id}  # 更新设备定向
- DELETE /api/targeting/device/{id}  # 删除设备定向

- GET    /api/targeting/geo          # 地域定向列表
- POST   /api/targeting/geo          # 创建地域定向
- PUT    /api/targeting/geo/{id}     # 更新地域定向
- DELETE /api/targeting/geo/{id}     # 删除地域定向

- GET    /api/targeting/time         # 时间定向列表
- POST   /api/targeting/time         # 创建时间定向
- PUT    /api/targeting/time/{id}    # 更新时间定向
- DELETE /api/targeting/time/{id}    # 删除时间定向

- GET    /api/targeting/environment  # 环境定向列表
- POST   /api/targeting/environment  # 创建环境定向
- PUT    /api/targeting/environment/{id} # 更新环境定向
- DELETE /api/targeting/environment/{id} # 删除环境定向
```

**数据模型**

```python
# app/models/targeting.py

class AudienceTargeting(Base):
    """人群定向模型"""
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    targeting_type = Column(String(50))  # interest, behavior, custom
    targeting_value = Column(Text)  # JSON格式存储标签列表
    is_include = Column(Boolean, default=True)  # 包含/排除

class DeviceTargeting(Base):
    """设备定向模型"""
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    os_type = Column(String(50))  # iOS, Android, All
    os_version = Column(String(50))  # 版本号
    device_brand = Column(String(100))  # 品牌名称
    device_model = Column(String(100))  # 型号名称

class GeoTargeting(Base):
    """地域定向模型"""
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    targeting_type = Column(String(50))  # province, city, district,商圈, LBS
    geo_level = Column(Integer)  # 地域级别
    geo_list = Column(Text)  # JSON格式存储地域列表

class TimeTargeting(Base):
    """时间定向模型"""
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    targeting_type = Column(String(50))  # hour, day, week
    time_config = Column(Text)  # JSON格式存储时间配置

class EnvironmentTargeting(Base):
    """环境定向模型"""
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    network_type = Column(String(50))  # WiFi, 4G, 5G, All
    carrier = Column(String(100))  # 运营商
```

**前端模块**

```
web/src/
├── pages/
│   ├── targeting/
│   │   ├── Audience.tsx        (~200行) 人群定向页面
│   │   ├── Device.tsx          (~150行) 设备定向页面
│   │   ├── Geo.tsx             (~180行) 地域定向页面
│   │   ├── Time.tsx            (~150行) 时间定向页面
│   │   ├── Environment.tsx     (~150行) 环境定向页面
│   │   └── index.tsx           (~100行) 定向主页
└── App.tsx                    (更新) 添加路由
```

---

### Week 3: 实时监控与预警

#### 后端模块

**文件拆分规划**

```
app/api/
├── monitoring.py         (新建) 监控API (~150行)
└── __init__.py          (更新) 注册路由

app/services/
├── alerting.py          (新建) 预警服务 (~200行)
└── __init__.py          (更新) 导入服务

app/schemas/
├── monitoring.py        (新建) 监控数据验证 (~100行)
└── __init__.py          (更新) 导入schemas

app/workers/
├── monitor_worker.py    (新建) 监控任务 (~200行)
└── __init__.py          (新建)
```

**API 端点**

```python
- GET    /api/monitoring/realtime      # 实时数据
- GET    /api/monitoring/alerts        # 预警列表
- POST   /api/monitoring/alerts        # 创建预警规则
- PUT    /api/monitoring/alerts/{id}  # 更新预警规则
- DELETE /api/monitoring/alerts/{id}  # 删除预警规则
- POST   /api/monitoring/test         # 测试预警
```

**预警规则类型**

```python
# 消耗预警
{
    "type": "cost_alert",
    "threshold": 10000,  # 日消耗超过10000
    "period": "daily",
    "action": "pause_campaign"  # 自动暂停计划
}

# 效果预警
{
    "type": "performance_alert",
    "metric": "ctr",  # CTR下降
    "threshold": 0.5,  # 阈值
    "period": "hourly",
    "action": "send_notification"
}

# 异常检测
{
    "type": "anomaly_detection",
    "metric": "click_rate",
    "method": "zscore",  # 统计方法
    "threshold": 3.0,  # 3倍标准差
    "action": "pause_campaign"
}
```

**前端模块**

```
web/src/
├── pages/
│   └── monitoring/
│       ├── Realtime.tsx        (~200行) 实时监控页面
│       ├── Alerts.tsx          (~180行) 预警列表页面
│       ├── AlertConfig.tsx     (~150行) 预警配置页面
│       └── index.tsx           (~100行) 监控主页
└── components/
    └── charts/
        └── RealtimeChart.tsx   (~200行) 实时图表组件
```

---

### Week 4: 出价策略优化

#### 后端模块

**文件拆分规划**

```
app/api/
├── bidding.py            (新建) 出价API (~180行)
└── __init__.py          (更新) 注册路由

app/services/
├── bidding.py            (新建) 出价服务 (~350行)
└── __init__.py          (更新) 导入服务

app/schemas/
├── bidding.py            (新建) 出价数据验证 (~120行)
└── __init__.py          (更新) 导入schemas

app/algorithms/
├── ocpa.py              (新建) oCPA算法 (~250行)
├── ocpc.py              (新建) oCPC算法 (~250行)
└── roas.py              (新建) ROAS优化算法 (~200行)
```

**API 端点**

```python
- GET    /api/bidding/strategies        # 出价策略列表
- POST   /api/bidding/strategies        # 创建出价策略
- PUT    /api/bidding/strategies/{id}   # 更新出价策略
- DELETE /api/bidding/strategies/{id}   # 删除出价策略
- GET    /api/bidding/strategies/{id}/performance # 策略效果
- POST   /api/bidding/strategies/{id}/activate  # 激活策略
- POST   /api/bidding/strategies/{id}/deactivate # 暂停策略

- GET    /api/bidding/rules             # 出价规则列表
- POST   /api/bidding/rules             # 创建出价规则
- PUT    /api/bidding/rules/{id}        # 更新出价规则
- DELETE /api/bidding/rules/{id}        # 删除出价规则
```

**出价策略类型**

```python
# oCPA (优化转化成本)
{
    "type": "ocpa",
    "target_cpa": 50.0,  # 目标转化成本
    "min_bid": 0.10,  # 最低出价
    "max_bid": 10.0,  # 最高出价
    "learning_period": 7  # 学习周期（天）
}

# oCPC (优化点击成本)
{
    "type": "ocpc",
    "target_cpc": 2.0,  # 目标点击成本
    "target_ctr": 0.02,  # 目标CTR
    "min_bid": 0.10,
    "max_bid": 5.0
}

# ROAS优化
{
    "type": "roas",
    "target_roas": 3.0,  # 目标ROI
    "conversion_value": True,  # 使用转化价值
    "min_bid": 0.10,
    "max_bid": 20.0
}
```

**前端模块**

```
web/src/
├── pages/
│   └── bidding/
│       ├── Strategies.tsx      (~200行) 出价策略页面
│       ├── Rules.tsx          (~180行) 出价规则页面
│       ├── Performance.tsx     (~150行) 策略效果页面
│       └── index.tsx          (~100行) 出价主页
└── components/
    └── bidding/
        ├── StrategyForm.tsx   (~150行) 策略表单
        └── RuleForm.tsx       (~120行) 规则表单
```

---

### Week 5-6: 数据不可篡改机制

#### 后端模块

**文件拆分规划**

```
app/api/
├── audit.py              (新建) 审计API (~150行)
└── __init__.py          (更新) 注册路由

app/services/
├── audit.py              (新建) 审计服务 (~300行)
├── integrity.py          (新建) 数据完整性服务 (~250行)
└── __init__.py          (更新) 导入服务

app/models/
├── audit_log.py         (新建) 审计日志模型 (~150行)
├── data_hash.py         (新建) 数据哈希模型 (~100行)
└── __init__.py          (更新) 导入模型

app/middleware/
├── audit.py             (新建) 审计中间件 (~200行)
└── integrity.py         (新建) 完整性中间件 (~180行)

app/utils/
├── crypto.py            (新建) 加密工具 (~200行)
├── signature.py         (新建) 签名工具 (~150行)
└── __init__.py          (更新) 导入工具
```

**API 端点**

```python
- GET    /api/audit/logs                    # 审计日志列表
- GET    /api/audit/logs/{id}               # 审计日志详情
- GET    /api/audit/integrity               # 数据完整性检查
- POST   /api/audit/integrity/verify        # 验证数据完整性
- GET    /api/audit/exports                # 审计导出
- POST   /api/audit/sign                   # 数据签名
```

**数据模型**

```python
class AuditLog(Base):
    """审计日志模型"""
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100))  # 操作类型
    resource_type = Column(String(50))  # 资源类型
    resource_id = Column(String(100))  # 资源ID
    old_value = Column(Text)  # 旧值（JSON）
    new_value = Column(Text)  # 新值（JSON）
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.now)
    session_id = Column(String(100))

class DataHash(Base):
    """数据哈希模型"""
    id = Column(BigInteger, primary_key=True)
    table_name = Column(String(100))
    record_id = Column(String(100))
    data_hash = Column(String(64))  # SHA256
    previous_hash = Column(String(64))  # 链式哈希
    timestamp = Column(DateTime, default=datetime.now)
    signed_by = Column(String(100))  # 签名者
    signature = Column(Text)  # 数字签名
```

**完整性检查**

```python
def check_integrity(table_name: str, record_id: str) -> dict:
    """
    检查数据完整性

    Returns:
        {
            "valid": True/False,
            "hash_valid": True/False,
            "signature_valid": True/False,
            "chain_valid": True/False,
            "details": {...}
        }
    """
```

**前端模块**

```
web/src/
├── pages/
│   └── audit/
│       ├── Logs.tsx            (~200行) 审计日志页面
│       ├── Integrity.tsx       (~180行) 完整性检查页面
│       ├── Verification.tsx    (~150行) 验证页面
│       └── index.tsx           (~100行) 审计主页
└── components/
    └── audit/
        ├── LogTable.tsx        (~150行) 日志表格
        └── IntegrityCard.tsx   (~120行) 完整性卡片
```

---

### Week 7: 反作弊系统

#### 后端模块

**文件拆分规划**

```
app/api/
├── antifraud.py           (新建) 反作弊API (~150行)
└── __init__.py          (更新) 注册路由

app/services/
├── antifraud.py          (新建) 反作弊服务 (~400行)
└── __init__.py          (更新) 导入服务

app/models/
├── fraud_detection.py    (新建) 欺诈检测模型 (~200行)
├── ip_blacklist.py       (新建) IP黑名单模型 (~100行)
├── device_fingerprint.py (新建) 设备指纹模型 (~150行)
└── __init__.py          (更新) 导入模型

app/algorithms/
├── click_fraud.py       (新建) 点击欺诈检测 (~300行)
├── conversion_fraud.py  (新建) 转化欺诈检测 (~250行)
└── bot_detection.py     (新建) 机器人检测 (~200行)
```

**API 端点**

```python
- GET    /api/antifraud/incidents         # 欺诈事件列表
- POST   /api/antifraud/incidents         # 创建欺诈事件
- PUT    /api/antifraud/incidents/{id}    # 更新欺诈事件
- DELETE /api/antifraud/incidents/{id}    # 删除欺诈事件
- GET    /api/antifraud/stats             # 欺诈统计
- POST   /api/antifraud/detect            # 手动检测

- GET    /api/antifraud/ip-blacklist      # IP黑名单列表
- POST   /api/antifraud/ip-blacklist      # 添加IP黑名单
- DELETE /api/antifraud/ip-blacklist/{id} # 删除IP黑名单

- GET    /api/antifraud/device-fingerprint # 设备指纹列表
- POST   /api/antifraud/device-fingerprint # 添加设备指纹
```

**检测规则**

```python
# 点击欺诈检测
{
    "type": "click_fraud",
    "rules": [
        {"type": "high_frequency", "threshold": 100, "period": "hour"},
        {"type": "same_pattern", "threshold": 10},
        {"type": "invalid_user_agent"},
        {"type": "proxy_ip"}
    ]
}

# 转化欺诈检测
{
    "type": "conversion_fraud",
    "rules": [
        {"type": "too_fast", "threshold": 5},  # 5秒内转化
        {"type": "same_device", "threshold": 20},  # 同设备多次转化
        {"type": "suspicious_pattern"}
    ]
}
```

**前端模块**

```
web/src/
├── pages/
│   └── antifraud/
│       ├── Incidents.tsx       (~200行) 欺诈事件页面
│       ├── IPBlacklist.tsx     (~150行) IP黑名单页面
│       ├── DeviceFingerprint.tsx (~180行) 设备指纹页面
│       └── index.tsx           (~100行) 反作弊主页
└── components/
    └── antifraud/
        ├── FraudChart.tsx      (~150行) 欺诈图表
        └── IncidentTable.tsx   (~120行) 事件表格
```

---

### Week 8: 智能预测系统

#### 后端模块

**文件拆分规划**

```
app/api/
├── prediction.py         (新建) 预测API (~150行)
└── __init__.py          (更新) 注册路由

app/services/
├── prediction.py         (新建) 预测服务 (~350行)
└── __init__.py          (更新) 导入服务

app/algorithms/
├── cost_prediction.py    (新建) 消耗预测 (~300行)
├── performance_prediction.py (新建) 效果预测 (~300行)
├── traffic_prediction.py (新建) 流量预测 (~250行)
└── budget_optimization.py (新建) 预算优化 (~250行)

app/models/
├── prediction_log.py    (新建) 预测日志模型 (~100行)
└── __init__.py          (更新) 导入模型
```

**API 端点**

```python
- GET    /api/prediction/cost              # 消耗预测
- GET    /api/prediction/performance       # 效果预测
- GET    /api/prediction/traffic           # 流量预测
- GET    /api/prediction/budget            # 预算优化建议
- GET    /api/prediction/history          # 预测历史
- GET    /api/prediction/accuracy         # 预测准确率
```

**预测算法**

```python
# 时间序列预测（ARIMA/Prophet）
def predict_cost(
    campaign_id: int,
    days: int = 7
) -> List[dict]:
    """
    预测未来消耗

    Returns:
        [
            {"date": "2026-03-02", "predicted_cost": 1200, "confidence": 0.85},
            {"date": "2026-03-03", "predicted_cost": 1150, "confidence": 0.82},
            ...
        ]
    """
```

**前端模块**

```
web/src/
├── pages/
│   └── prediction/
│       ├── CostPrediction.tsx       (~200行) 消耗预测页面
│       ├── PerformancePrediction.tsx (~180行) 效果预测页面
│       ├── TrafficPrediction.tsx    (~150行) 流量预测页面
│       ├── BudgetOptimization.tsx   (~160行) 预算优化页面
│       └── index.tsx               (~100行) 预测主页
└── components/
    └── prediction/
        ├── PredictionChart.tsx      (~200行) 预测图表
        └── ConfidenceBand.tsx       (~150行) 置信区间
```

---

### Week 9: DCO动态创意优化

#### 后端模块

**文件拆分规划**

```
app/api/
├── dco.py                (新建) DCO API (~180行)
└── __init__.py          (更新) 注册路由

app/services/
├── dco.py                (新建) DCO服务 (~400行)
└── __init__.py          (更新) 导入服务

app/algorithms/
├── creative_generator.py (新建) 创意生成器 (~350行)
├── creative_optimizer.py (新建) 创意优化器 (~300行)
└── ab_test.py           (更新) A/B测试优化 (~200行)

app/models/
├── dco_template.py       (新建) DCO模板模型 (~150行)
├── creative_pool.py      (新建) 创意池模型 (~150行)
└── __init__.py          (更新) 导入模型
```

**API 端点**

```python
- GET    /api/dco/templates              # DCO模板列表
- POST   /api/dco/templates              # 创建DCO模板
- PUT    /api/dco/templates/{id}         # 更新DCO模板
- DELETE /api/dco/templates/{id}         # 删除DCO模板

- GET    /api/dco/creative-pool         # 创意池列表
- POST   /api/dco/creative-pool         # 添加创意到池
- DELETE /api/dco/creative-pool/{id}    # 从池中删除创意

- GET    /api/dco/generate              # 自动生成创意组合
- POST   /api/dco/optimize              # 优化创意
- GET    /api/dco/performance           # 创意表现分析
```

**DCO模板**

```python
{
    "name": "夏季促销DCO",
    "elements": {
        "titles": ["夏季大促", "限时优惠", "超值特卖"],
        "descriptions": ["全场5折起", "满300减50", "新品上市"],
        "images": ["img1.jpg", "img2.jpg", "img3.jpg"],
        "ctas": ["立即购买", "了解更多", "免费试听"]
    },
    "optimization_target": "ctr",  # 优化目标
    "test_percentage": 0.1,  # 测试流量比例
    "auto_optimize": True  # 自动优化
}
```

**前端模块**

```
web/src/
├── pages/
│   └── dco/
│       ├── Templates.tsx          (~200行) DCO模板页面
│       ├── CreativePool.tsx       (~180行) 创意池页面
│       ├── Generation.tsx         (~150行) 生成页面
│       ├── Performance.tsx        (~160行) 表现分析页面
│       └── index.tsx             (~100行) DCO主页
└── components/
    └── dco/
        ├── TemplateBuilder.tsx    (~250行) 模板构建器
        └── CreativePreview.tsx    (~150行) 创意预览
```

---

## 📂 文件结构总览

### 后端结构

```
ad-platform/
├── app/
│   ├── api/                     # API层
│   │   ├── __init__.py          (~50行)
│   │   ├── main.py              (V2.0, ~100行)
│   │   ├── campaigns.py         (V2.0, ~200行)
│   │   ├── targeting.py         (V3.0, ~200行) ⭐ NEW
│   │   ├── monitoring.py        (V3.0, ~150行) ⭐ NEW
│   │   ├── bidding.py           (V3.0, ~180行) ⭐ NEW
│   │   ├── audit.py             (V3.0, ~150行) ⭐ NEW
│   │   ├── antifraud.py         (V3.0, ~150行) ⭐ NEW
│   │   ├── prediction.py        (V3.0, ~150行) ⭐ NEW
│   │   └── dco.py               (V3.0, ~180行) ⭐ NEW
│   │
│   ├── models/                  # 数据模型
│   │   ├── __init__.py          (~100行)
│   │   ├── targeting.py         (V3.0, ~100行) ⭐ NEW
│   │   ├── audit_log.py         (V3.0, ~150行) ⭐ NEW
│   │   ├── data_hash.py         (V3.0, ~100行) ⭐ NEW
│   │   ├── fraud_detection.py   (V3.0, ~200行) ⭐ NEW
│   │   └── dco_template.py      (V3.0, ~150行) ⭐ NEW
│   │
│   ├── services/                # 业务逻辑
│   │   ├── __init__.py          (~50行)
│   │   ├── targeting.py         (V3.0, ~300行) ⭐ NEW
│   │   ├── alerting.py          (V3.0, ~200行) ⭐ NEW
│   │   ├── bidding.py           (V3.0, ~350行) ⭐ NEW
│   │   ├── audit.py             (V3.0, ~300行) ⭐ NEW
│   │   ├── integrity.py         (V3.0, ~250行) ⭐ NEW
│   │   ├── antifraud.py         (V3.0, ~400行) ⭐ NEW
│   │   ├── prediction.py        (V3.0, ~350行) ⭐ NEW
│   │   └── dco.py               (V3.0, ~400行) ⭐ NEW
│   │
│   ├── algorithms/              # 算法模块
│   │   ├── __init__.py          (V3.0, ~30行) ⭐ NEW
│   │   ├── ocpa.py              (V3.0, ~250行) ⭐ NEW
│   │   ├── ocpc.py              (V3.0, ~250行) ⭐ NEW
│   │   ├── roas.py              (V3.0, ~200行) ⭐ NEW
│   │   ├── click_fraud.py       (V3.0, ~300行) ⭐ NEW
│   │   ├── conversion_fraud.py  (V3.0, ~250行) ⭐ NEW
│   │   ├── bot_detection.py     (V3.0, ~200行) ⭐ NEW
│   │   ├── cost_prediction.py    (V3.0, ~300行) ⭐ NEW
│   │   ├── performance_prediction.py (V3.0, ~300行) ⭐ NEW
│   │   ├── traffic_prediction.py (V3.0, ~250行) ⭐ NEW
│   │   ├── budget_optimization.py (V3.0, ~250行) ⭐ NEW
│   │   ├── creative_generator.py (V3.0, ~350行) ⭐ NEW
│   │   └── creative_optimizer.py (V3.0, ~300行) ⭐ NEW
│   │
│   ├── schemas/                 # 数据验证
│   │   ├── __init__.py          (~50行)
│   │   ├── targeting.py         (V3.0, ~150行) ⭐ NEW
│   │   ├── monitoring.py        (V3.0, ~100行) ⭐ NEW
│   │   ├── bidding.py           (V3.0, ~120行) ⭐ NEW
│   │   └── dco.py               (V3.0, ~150行) ⭐ NEW
│   │
│   ├── middleware/              # 中间件
│   │   ├── __init__.py          (~30行)
│   │   ├── audit.py             (V3.0, ~200行) ⭐ NEW
│   │   └── integrity.py         (V3.0, ~180行) ⭐ NEW
│   │
│   ├── workers/                 # 异步任务
│   │   ├── __init__.py          (V3.0, ~30行) ⭐ NEW
│   │   └── monitor_worker.py    (V3.0, ~200行) ⭐ NEW
│   │
│   └── utils/                   # 工具类
│       ├── __init__.py          (~50行)
│       ├── crypto.py            (V3.0, ~200行) ⭐ NEW
│       └── signature.py         (V3.0, ~150行) ⭐ NEW
│
└── web/
    └── src/
        ├── pages/               # 页面组件
        │   ├── targeting/        (V3.0, ~780行) ⭐ NEW
        │   ├── monitoring/       (V3.0, ~630行) ⭐ NEW
        │   ├── bidding/          (V3.0, ~630行) ⭐ NEW
        │   ├── audit/            (V3.0, ~630行) ⭐ NEW
        │   ├── antifraud/        (V3.0, ~630行) ⭐ NEW
        │   ├── prediction/       (V3.0, ~790行) ⭐ NEW
        │   └── dco/              (V3.0, ~890行) ⭐ NEW
        │
        └── components/          # 通用组件
            ├── targeting/        (V3.0, ~0行) ⭐ NEW
            ├── bidding/          (V3.0, ~270行) ⭐ NEW
            ├── audit/            (V3.0, ~270行) ⭐ NEW
            ├── antifraud/        (V3.0, ~270行) ⭐ NEW
            ├── prediction/       (V3.0, ~350行) ⭐ NEW
            └── dco/              (V3.0, ~400行) ⭐ NEW
```

---

## 📊 开发进度追踪

| Week | 功能模块 | 后端文件数 | 前端文件数 | 状态 |
|------|----------|-----------|-----------|------|
| 1-2 | 定向投放 | 5 | 6 | ⏳ 待开发 |
| 3 | 实时监控 | 4 | 5 | ⏳ 待开发 |
| 4 | 出价优化 | 4 | 6 | ⏳ 待开发 |
| 5-6 | 数据审计 | 7 | 6 | ⏳ 待开发 |
| 7 | 反作弊 | 4 | 6 | ⏳ 待开发 |
| 8 | 智能预测 | 4 | 7 | ⏳ 待开发 |
| 9 | DCO优化 | 4 | 7 | ⏳ 待开发 |
| **合计** | **7大模块** | **32个** | **43个** | ⏳ 0% |

---

## ✅ 质量保证

### 代码审查
- 每个模块完成后进行代码审查
- 确保文件行数不超过限制
- 检查命名规范和注释完整性

### 测试覆盖
- 单元测试覆盖率 > 80%
- 集成测试覆盖率 > 70%
- API测试覆盖率 100%

### 文档更新
- 每个模块完成后更新API文档
- 更新数据库设计文档
- 更新前端开发文档

---

**准备就绪，开始 Phase 4 开发！**
