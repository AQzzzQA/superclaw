COMMENT '创意类型: IMAGE/VIDEO/TEXT',
  `material_url` VARCHAR(500) COMMENT '素材URL',
  `material_type` VARCHAR(20) COMMENT '素材类型',
  `title` VARCHAR(100) COMMENT '创意标题',
  `description` TEXT COMMENT '创意描述',
  `landing_url` VARCHAR(500) COMMENT '落地页URL',
  `display_url` VARCHAR(200) COMMENT '显示URL',
  `button_text` VARCHAR(20) COMMENT '按钮文案',
  `audit_status` TINYINT DEFAULT 0 COMMENT '审核状态: 0-待审核 1-审核通过 2-审核拒绝',
  `audit_reason` VARCHAR(500) COMMENT '审核原因',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 1-投放中 2-暂停',
  `created_by` BIGINT UNSIGNED COMMENT '创建人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_adgroup_creative` (`adgroup_id`, `creative_id`),
  KEY `idx_account_id` (`account_id`),
  KEY `idx_campaign_id` (`campaign_id`),
  KEY `idx_audit_status` (`audit_status`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='广告创意表';

-- 素材库表
CREATE TABLE `dsp_material` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '素材ID',
  `material_name` VARCHAR(200) NOT NULL COMMENT '素材名称',
  `material_type` VARCHAR(20) NOT NULL COMMENT '素材类型: IMAGE/VIDEO',
  `file_url` VARCHAR(500) NOT NULL COMMENT '文件URL',
  `file_size` BIGINT COMMENT '文件大小(字节)',
  `width` INT COMMENT '宽度(像素)',
  `height` INT COMMENT '高度(像素)',
  `duration` INT COMMENT '时长(秒,视频)',
  `format` VARCHAR(20) COMMENT '文件格式',
  `md5` VARCHAR(32) COMMENT '文件MD5',
  `owner_id` BIGINT UNSIGNED NOT NULL COMMENT '所有者ID',
  `folder_id` BIGINT UNSIGNED COMMENT '所属文件夹ID',
  `tags` VARCHAR(500) COMMENT '标签',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 1-正常 2-删除',
  `created_by` BIGINT UNSIGNED COMMENT '创建人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_folder_id` (`folder_id`),
  KEY `idx_material_type` (`material_type`),
  KEY `idx_md5` (`md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='素材库表';
```

#### 8.2.4 数据报表表

```sql
-- 广告数据日报表（按日汇总）
CREATE TABLE `dsp_report_daily` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `account_id` BIGINT UNSIGNED NOT NULL COMMENT '媒体账户ID',
  `campaign_id` BIGINT UNSIGNED COMMENT '计划ID',
  `adgroup_id` BIGINT UNSIGNED COMMENT '广告组ID',
  `creative_id` BIGINT UNSIGNED COMMENT '创意ID',
  `report_date` DATE NOT NULL COMMENT '报表日期',
  `impression` BIGINT DEFAULT 0 COMMENT '曝光量',
  `click` BIGINT DEFAULT 0 COMMENT '点击量',
  `ctr` DECIMAL(10,4) DEFAULT 0.0000 COMMENT '点击率',
  `cost` DECIMAL(15,2) DEFAULT 0.00 COMMENT '消耗金额',
  `cpm` DECIMAL(10,2) DEFAULT 0.00 COMMENT '千次展示成本',
  `cpc` DECIMAL(10,2) DEFAULT 0.00 COMMENT '点击成本',
  `conversion` BIGINT DEFAULT 0 COMMENT '转化量',
  `cvr` DECIMAL(10,4) DEFAULT 0.0000 COMMENT '转化率',
  `cpa` DECIMAL(10,2) DEFAULT 0.00 COMMENT '转化成本',
  `revenue` DECIMAL(15,2) DEFAULT 0.00 COMMENT '转化收入',
  `roi` DECIMAL(10,4) DEFAULT 0.0000 COMMENT '投资回报率',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_report` (`account_id`, `campaign_id`, `adgroup_id`, `creative_id`, `report_date`),
  KEY `idx_account_date` (`account_id`, `report_date`),
  KEY `idx_campaign_date` (`campaign_id`, `report_date`),
  KEY `idx_report_date` (`report_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='广告数据日报表';

-- 实时数据表（按小时）
CREATE TABLE `dsp_report_hourly` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `account_id` BIGINT UNSIGNED NOT NULL COMMENT '媒体账户ID',
  `campaign_id` BIGINT UNSIGNED COMMENT '计划ID',
  `adgroup_id` BIGINT UNSIGNED COMMENT '广告组ID',
  `report_hour` DATETIME NOT NULL COMMENT '报表小时',
  `impression` BIGINT DEFAULT 0 COMMENT '曝光量',
  `click` BIGINT DEFAULT 0 COMMENT '点击量',
  `cost` DECIMAL(15,2) DEFAULT 0.00 COMMENT '消耗金额',
  `conversion` BIGINT DEFAULT 0 COMMENT '转化量',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_report_hour` (`account_id`, `campaign_id`, `adgroup_id`, `report_hour`),
  KEY `idx_account_hour` (`account_id`, `report_hour`),
  KEY `idx_report_hour` (`report_hour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实时数据表';
```

#### 8.2.5 预算与风控表

```sql
-- 预算配置表
CREATE TABLE `dsp_budget_config` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `budget_type` TINYINT NOT NULL COMMENT '预算类型: 1-全局 2-渠道 3-账户 4-计划',
  `target_id` BIGINT UNSIGNED COMMENT '目标ID（预算类型非全局时使用）',
  `budget_amount` DECIMAL(15,2) NOT NULL COMMENT '预算金额',
  `budget_period` TINYINT DEFAULT 1 COMMENT '预算周期: 1-每日 2-每周 3-每月 4-总计',
  `start_date` DATE COMMENT '生效开始日期',
  `end_date` DATE COMMENT '生效结束日期',
  `control_action` TINYINT DEFAULT 1 COMMENT '控制动作: 1-自动暂停 2-仅预警',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 1-启用 2-禁用',
  `created_by` BIGINT UNSIGNED COMMENT '创建人',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_budget_type` (`budget_type`),
  KEY `idx_target_id` (`target_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预算配置表';

-- 预警记录表
CREATE TABLE `dsp_alert_record` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `alert_type` VARCHAR(50) NOT NULL COMMENT '预警类型: BUDGET_OVER/BALANCE_LOW/ABNORMAL_COST',
  `alert_level` TINYINT NOT NULL COMMENT '预警级别: 1-信息 2-警告 3-严重',
  `target_type` VARCHAR(20) NOT NULL COMMENT '目标类型: ACCOUNT/CAMPAIGN/ADGROUP',
  `target_id` BIGINT UNSIGNED NOT NULL COMMENT '目标ID',
  `alert_content` TEXT NOT NULL COMMENT '预警内容',
  `threshold_value` VARCHAR(100) COMMENT '阈值',
  `current_value` VARCHAR(100) COMMENT '当前值',
  `is_handled` TINYINT DEFAULT 0 COMMENT '是否已处理: 0-未处理 1-已处理',
  `handled_by` BIGINT UNSIGNED COMMENT '处理人',
  `handled_at` DATETIME COMMENT '处理时间',
  `handle_note` VARCHAR(500) COMMENT '处理说明',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_alert_type` (`alert_type`),
  KEY `idx_alert_level` (`alert_level`),
  KEY `idx_target` (`target_type`, `target_id`),
  KEY `idx_is_handled` (`is_handled`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预警记录表';
```

#### 8.2.6 操作日志表

```sql
-- 操作日志表
CREATE TABLE `sys_operation_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '操作用户ID',
  `username` VARCHAR(50) COMMENT '用户名',
  `module` VARCHAR(50) NOT NULL COMMENT '操作模块',
  `operation` VARCHAR(50) NOT NULL COMMENT '操作类型: CREATE/UPDATE/DELETE/QUERY/EXPORT',
  `description` VARCHAR(200) COMMENT '操作描述',
  `request_method` VARCHAR(10) COMMENT '请求方法: GET/POST/PUT/DELETE',
  `request_url` VARCHAR(500) COMMENT '请求URL',
  `request_params` TEXT COMMENT '请求参数',
  `response_result` TEXT COMMENT '响应结果',
  `ip_address` VARCHAR(50) COMMENT 'IP地址',
  `user_agent` VARCHAR(500) COMMENT '用户代理',
  `execute_time` INT COMMENT '执行时间(毫秒)',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 1-成功 2-失败',
  `error_msg` VARCHAR(500) COMMENT '错误信息',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_module` (`module`),
  KEY `idx_operation` (`operation`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
```

### 8.3 分表策略

对于大数据量表，采用以下分表策略：

| 表名 | 分表键 | 分表规则 | 说明 |
|------|--------|----------|------|
| dsp_report_daily | report_date | 按月分表 | 每月一张表，表名: dsp_report_daily_202601 |
| dsp_report_hourly | report_hour | 按月分表 | 每月一张表，表名: dsp_report_hourly_202601 |
| sys_operation_log | created_at | 按月分表 | 每月一张表，表名: sys_operation_log_202601 |

### 8.4 索引设计原则

1. **主键索引**: 所有表都有自增主键
2. **唯一索引**: 保证业务数据唯一性
3. **普通索引**: 针对高频查询字段
4. **联合索引**: 针对多字段组合查询
5. **覆盖索引**: 避免回表，提升查询性能

---

## 9. 系统架构设计

### 9.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         客户端层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web浏览器  │  │   移动端H5   │  │  开放API调用 │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                        接入层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Nginx     │  │   Kong网关   │  │   CDN加速    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                        应用层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  用户服务    │  │  账户服务    │  │  投放服务    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  数据服务    │  │  报表服务    │  │  预警服务    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       中间件层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Redis     │  │  RabbitMQ    │  │  Celery      │      │
│  │   缓存       │  │  消息队列    │  │  任务调度    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       数据层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   MySQL     │  │   Redis     │  │  Elasticsearch│     │
│  │  主数据库   │  │  缓存数据库  │  │  日志搜索    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  OSS存储    │  │   媒体API    │                         │
│  │  素材文件   │  │  第三方接口  │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 服务拆分

| 服务名称 | 职责 | 技术栈 |
|---------|------|--------|
| 用户服务 | 用户管理、角色权限、组织架构 | FastAPI + MySQL |
| 账户服务 | 媒体账户管理、授权接入、信息同步 | FastAPI + MySQL + Redis |
| 投放服务 | 广告计划/组/创意管理、批量操作 | FastAPI + MySQL + RabbitMQ |
| 数据服务 | 实时数据采集、数据同步、数据清洗 | FastAPI + MySQL + RabbitMQ + Celery |
| 报表服务 | 报表查询、数据分析、报表导出 | FastAPI + MySQL + Redis |
| 预警服务 | 预算控制、消耗预警、异常监测 | FastAPI + MySQL + Redis + RabbitMQ |
| 通知服务 | 站内消息、邮件、企业微信集成 | FastAPI + MySQL + RabbitMQ |

### 9.3 核心流程

#### 9.3.1 账户授权流程

```
用户发起授权请求
    ↓
系统生成OAuth授权URL
    ↓
用户跳转到媒体平台授权页面
    ↓
用户授权，媒体平台回调
    ↓
系统获取授权信息
    ↓
保存授权信息到数据库
    ↓
触发账户信息同步任务
    ↓
同步完成，通知用户
```

#### 9.3.2 数据同步流程

```
定时任务触发
    ↓
查询所有待同步账户
    ↓
调用媒体平台API获取数据
    ↓
解析并转换数据格式
    ↓
存储到数据库
    ↓
更新同步状态和时间
    ↓
如果失败，记录日志并重试
    ↓
发送同步完成通知
```

#### 9.3.3 预算控制流程

```
实时监控消耗
    ↓
计算预算使用率
    ↓
判断是否达到预警阈值
    ↓
如果达到，发送预警通知
    ↓
如果超过预算，自动暂停广告
    ↓
记录预警和处理日志
```

---

## 10. 开发计划

### 10.1 开发阶段划分

| 阶段 | 名称 | 周期 | 主要工作 |
|------|------|------|----------|
| Phase 1 | 基础框架搭建 | 2周 | 项目初始化、开发环境搭建、基础架构设计 |
| Phase 2 | 用户权限模块 | 2周 | 用户管理、角色权限、组织架构 |
| Phase 3 | 账户管理模块 | 3周 | 媒体账户管理、授权接入、信息同步 |
| Phase 4 | 广告投放模块 | 4周 | 广告计划/组/创意管理、批量操作 |
| Phase 5 | 数据监控模块 | 3周 | 实时数据看板、数据同步、数据报表 |
| Phase 6 | 预算风控模块 | 2周 | 预算控制、消耗预警、异常监测 |
| Phase 7 | 通知系统 | 1周 | 站内消息、邮件、企业微信集成 |
| Phase 8 | 测试与优化 | 2周 | 功能测试、性能优化、Bug修复 |
| Phase 9 | 部署上线 | 1周 | 生产环境部署、数据迁移、灰度发布 |

**总计**: 20周（约5个月）

### 10.2 里程碑

| 里程碑 | 完成时间 | 交付物 |
|--------|----------|--------|
| M1 | Phase 2结束 | 用户权限系统上线 |
| M2 | Phase 3结束 | 完成1个媒体渠道接入 |
| M3 | Phase 4结束 | 广告投放功能上线 |
| M4 | Phase 5结束 | 数据监控看板上线 |
| M5 | Phase 9结束 | 系统正式上线 |

### 10.3 资源需求

| 角色 | 人数 | 职责 |
|------|------|------|
| 产品经理 | 1 | 需求管理、产品设计、项目协调 |
| 后端开发 | 3 | 后端开发、API设计、数据库设计 |
| 前端开发 | 2 | 前端开发、UI实现、交互优化 |
| 测试工程师 | 1 | 功能测试、性能测试、自动化测试 |
| 运维工程师 | 1 | 环境搭建、部署运维、监控告警 |

---

## 11. 附录

### 11.1 术语表

| 术语 | 说明 |
|------|------|
| DSP | Demand Side Platform，需求方平台，广告主购买广告的平台 |
| 巨量引擎 | 字节跳动的广告投放平台 |
| 磁力引擎 | 快手的广告投放平台 |
| 广点通 | 腾讯广告投放平台 |
| 粉丝通 | 微博广告投放平台 |
| 花火 | B站广告投放平台 |
| OCPM | Optimized Cost Per Mille，优化千次展示成本 |
| CPC | Cost Per Click，按点击计费 |
| CPM | Cost Per Mille，按千次展示计费 |
| CPA | Cost Per Action，按转化计费 |
| ROI | Return On Investment，投资回报率 |
| CTR | Click Through Rate，点击率 |
| CVR | Conversion Rate，转化率 |

### 11.2 参考资料

- [抖音巨量引擎API文档](https://open.oceanengine.com/)
- [快手磁力引擎API文档](https://ad.e.kuaishou.com/)
- [微信广告API文档](https://developers.ad.qq.com/)
- [微博粉丝通API文档](https://open.weibo.com/)
- [B站花火API文档](https://business.bilibili.com/)

---

**文档结束**
