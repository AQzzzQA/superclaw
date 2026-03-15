# DSP平台数据库设计文档

**版本**: V1.0
**文档日期**: 2026-03-15
**关联文档**: PRD.md

---

## 1. 数据库设计原则

### 1.1 设计规范

- 命名规范：小写字母+下划线，见名知意
- 字符集：utf8mb4
- 存储引擎：InnoDB（支持事务、外键、行锁）
- 主键：所有表必须有主键，优先使用自增BIGINT
- 时间戳：created_at和updated_at为必填字段
- 软删除：部分业务表使用deleted_at实现软删除

### 1.2 索引设计

- 主键索引：所有表默认创建
- 唯一索引：业务唯一字段创建唯一索引
- 普通索引：高频查询字段创建普通索引
- 联合索引：多字段组合查询创建联合索引
- 覆盖索引：避免回表，提升查询性能

### 1.3 分表策略

对于大数据量表，采用以下分表策略：

| 表名 | 分表键 | 分表规则 | 说明 |
|------|--------|----------|------|
| dsp_report_daily | report_date | 按月分表 | 每月一张表，表名: dsp_report_daily_202601 |
| dsp_report_hourly | report_hour | 按月分表 | 每月一张表，表名: dsp_report_hourly_202601 |
| sys_operation_log | created_at | 按月分表 | 每月一张表，表名: sys_operation_log_202601 |

---

## 2. 数据表清单

| 序号 | 表名 | 表名说明 | 表类型 | 分表 |
|------|------|---------|--------|------|
| 1 | sys_user | 用户表 | 业务表 | 否 |
| 2 | sys_role | 角色表 | 业务表 | 否 |
| 3 | sys_user_role | 用户角色关联表 | 关联表 | 否 |
| 4 | sys_permission | 权限表 | 业务表 | 否 |
| 5 | sys_role_permission | 角色权限关联表 | 关联表 | 否 |
| 6 | sys_organization | 组织架构表 | 业务表 | 否 |
| 7 | sys_operation_log | 操作日志表 | 日志表 | 是 |
| 8 | dsp_channel | 媒体渠道表 | 业务表 | 否 |
| 9 | dsp_media_account | 媒体账户表 | 业务表 | 否 |
| 10 | dsp_account_permission | 账户权限表 | 关联表 | 否 |
| 11 | dsp_campaign | 广告计划表 | 业务表 | 否 |
| 12 | dsp_adgroup | 广告组表 | 业务表 | 否 |
| 13 | dsp_creative | 广告创意表 | 业务表 | 否 |
| 14 | dsp_material | 素材库表 | 业务表 | 否 |
| 15 | dsp_report_daily | 广告数据日报表 | 报表表 | 是 |
| 16 | dsp_report_hourly | 实时数据表 | 报表表 | 是 |
| 17 | dsp_budget_config | 预算配置表 | 配置表 | 否 |
| 18 | dsp_alert_record | 预警记录表 | 业务表 | 否 |

**总计**: 18张数据表

---

## 3. ER图（简化版）

```
sys_user (用户)
    ├─> sys_user_role ──> sys_role (角色)
    │                          │
    │                          └─> sys_role_permission ──> sys_permission (权限)
    │
    ├─> sys_organization (组织)
    │
    └─> sys_operation_log (操作日志)

dsp_channel (媒体渠道)
    └─> dsp_media_account (媒体账户)
            ├─> dsp_account_permission (账户权限)
            ├─> dsp_campaign (广告计划)
            │       └─> dsp_adgroup (广告组)
            │               └─> dsp_creative (广告创意)
            │
            └─> dsp_report_daily / dsp_report_hourly (报表数据)

dsp_material (素材库)

dsp_budget_config (预算配置)
dsp_alert_record (预警记录)
```

---

## 4. 核心表详细设计

### 4.1 用户与权限表

详见 PRD.md 第8.2.1节

### 4.2 媒体账户表

详见 PRD.md 第8.2.2节

### 4.3 广告投放表

详见 PRD.md 第8.2.3节

### 4.4 数据报表表

详见 PRD.md 第8.2.4节

### 4.5 预算与风控表

详见 PRD.md 第8.2.5节

---

## 5. 数据字典

### 5.1 状态枚举

#### sys_user.status
- 1: 正常
- 2: 冻结
- 3: 禁用

#### sys_role.is_system
- 0: 否
- 1: 是

#### dsp_media_account.status
- 1: 正常
- 2: 异常
- 3: 冻结

#### dsp_campaign.status
- 1: 投放中
- 2: 暂停
- 3: 审核中
- 4: 审核失败

#### dsp_creative.audit_status
- 0: 待审核
- 1: 审核通过
- 2: 审核拒绝

#### dsp_alert_record.alert_level
- 1: 信息
- 2: 警告
- 3: 严重

### 5.2 渠道代码

| channel_code | channel_name |
|--------------|--------------|
| BYTEDANCE | 抖音巨量引擎 |
| KUAISHOU | 快手磁力引擎 |
| WECHAT | 微信广点通 |
| WEIBO | 微博粉丝通 |
| BSTATION | B站花火 |

---

## 6. SQL脚本位置

详细的建表SQL脚本请参考 `database/` 目录（待创建）：

- `database/schema/01_user_permission.sql` - 用户权限表
- `database/schema/02_media_account.sql` - 媒体账户表
- `database/schema/03_ad_delivery.sql` - 广告投放表
- `database/schema/04_report.sql` - 数据报表表
- `database/schema/05_budget_alert.sql` - 预算风控表

---

**文档结束**
