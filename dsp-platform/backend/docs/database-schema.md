# DSP广告平台 - 数据库Schema设计

## 数据库设计原则

1. **规范化设计**: 遵循第三范式，减少数据冗余
2. **性能优化**: 合理使用索引，避免过度规范化
3. **扩展性**: 预留扩展字段，支持JSON格式存储
4. **数据完整性**: 使用外键约束，保证数据一致性
5. **审计追踪**: 记录数据变更历史

## 数据库表清单

### 1. 用户相关表 (3张)
- `users` - 用户表
- `roles` - 角色表
- `user_roles` - 用户角色关联表

### 2. 广告相关表 (6张)
- `campaigns` - 广告计划表
- `creatives` - 创意素材表
- `audiences` - 受众定向表
- `strategies` - 投放策略表
- `campaign_audiences` - 广告计划受众关联表
- `campaign_creatives` - 广告计划创意关联表

### 3. 数据相关表 (3张)
- `impressions` - 曝光数据表
- `clicks` - 点击数据表
- `conversions` - 转化数据表

### 4. 报表相关表 (3张)
- `reports` - 报表配置表
- `report_data` - 报表数据表
- `report_schedules` - 报表定时任务表

### 5. 计费相关表 (3张)
- `accounts` - 账户表
- `transactions` - 交易记录表
- `invoices` - 发票表

### 6. 系统表 (3张)
- `platforms` - 媒体平台表
- `platform_accounts` - 平台账户表
- `notifications` - 系统通知表

**总计**: 21张表

---

## 表结构设计

### 1. users - 用户表

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(100),
    avatar_url VARCHAR(500),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    last_login_at DATETIME,
    last_login_ip VARCHAR(45),
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='用户表';
```

### 2. roles - 角色表

```sql
CREATE TABLE roles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100),
    description TEXT,
    permissions JSON COMMENT '权限列表',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='角色表';
```

### 3. user_roles - 用户角色关联表

```sql
CREATE TABLE user_roles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='用户角色关联表';
```

### 4. campaigns - 广告计划表

```sql
CREATE TABLE campaigns (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    platform ENUM('douyin', 'kuaishou', 'wechat', 'baidu', 'tencent', 'toutiao', 'bilibili', 'weibo') NOT NULL,
    platform_campaign_id VARCHAR(100) COMMENT '平台计划ID',
    budget DECIMAL(12, 2) NOT NULL,
    budget_daily DECIMAL(12, 2) COMMENT '日预算',
    budget_used DECIMAL(12, 2) DEFAULT 0,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai',
    status ENUM('draft', 'active', 'paused', 'completed', 'archived') DEFAULT 'draft',
    objective ENUM('awareness', 'traffic', 'conversion', 'app_install', 'lead_generation'),
    targeting JSON COMMENT '定向配置',
    schedule JSON COMMENT '投放时间表',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_dates (start_date, end_date),
    INDEX idx_platform_campaign_id (platform_campaign_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='广告计划表';
```

### 5. creatives - 创意素材表

```sql
CREATE TABLE creatives (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    campaign_id BIGINT UNSIGNED COMMENT '关联广告计划',
    name VARCHAR(200) NOT NULL,
    type ENUM('image', 'video', 'carousel', 'html5', 'native') NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    file_size BIGINT COMMENT '文件大小(字节)',
    width INT COMMENT '宽度(px)',
    height INT COMMENT '高度(px)',
    duration INT COMMENT '视频时长(秒)',
    title VARCHAR(100),
    description TEXT,
    call_to_action VARCHAR(50),
    status ENUM('draft', 'pending_review', 'approved', 'rejected', 'active', 'inactive') DEFAULT 'draft',
    review_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    review_reason TEXT COMMENT '审核原因',
    platform_creative_id VARCHAR(100) COMMENT '平台创意ID',
    metadata JSON COMMENT '元数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_review_status (review_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='创意素材表';
```

### 6. audiences - 受众定向表

```sql
CREATE TABLE audiences (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    type ENUM('custom', 'lookalike', 'behavioral', 'demographic') NOT NULL,
    targeting JSON NOT NULL COMMENT '定向配置',
    size INT COMMENT '受众规模估算',
    size_updated_at DATETIME,
    status ENUM('active', 'inactive', 'processing', 'failed') DEFAULT 'inactive',
    platform_audience_id VARCHAR(100) COMMENT '平台受众ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='受众定向表';
```

### 7. strategies - 投放策略表

```sql
CREATE TABLE strategies (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    campaign_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    type ENUM('manual', 'auto', 'smart', 'ai_optimized') NOT NULL,
    bidding_strategy ENUM('cpc', 'cpm', 'cpa', 'ocpc', 'ocpm', 'roi_optimized') NOT NULL,
    bid_amount DECIMAL(10, 2) COMMENT '出价',
    target_cpa DECIMAL(10, 2) COMMENT '目标CPA',
    target_roas DECIMAL(5, 2) COMMENT '目标ROAS',
    budget_allocation JSON COMMENT '预算分配',
    optimization_goals JSON COMMENT '优化目标',
    constraints JSON COMMENT '约束条件',
    status ENUM('active', 'paused', 'completed', 'archived') DEFAULT 'active',
    performance_metrics JSON COMMENT '性能指标',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='投放策略表';
```

### 8. campaign_audiences - 广告计划受众关联表

```sql
CREATE TABLE campaign_audiences (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT UNSIGNED NOT NULL,
    audience_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (audience_id) REFERENCES audiences(id) ON DELETE CASCADE,
    UNIQUE KEY uk_campaign_audience (campaign_id, audience_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_audience_id (audience_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='广告计划受众关联表';
```

### 9. campaign_creatives - 广告计划创意关联表

```sql
CREATE TABLE campaign_creatives (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT UNSIGNED NOT NULL,
    creative_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (creative_id) REFERENCES creatives(id) ON DELETE CASCADE,
    UNIQUE KEY uk_campaign_creative (campaign_id, creative_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_creative_id (creative_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='广告计划创意关联表';
```

### 10. impressions - 曝光数据表

```sql
CREATE TABLE impressions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    impression_id VARCHAR(100) NOT NULL UNIQUE,
    campaign_id BIGINT UNSIGNED NOT NULL,
    creative_id BIGINT UNSIGNED NOT NULL,
    user_id VARCHAR(100) COMMENT '用户ID',
    device_type ENUM('mobile', 'desktop', 'tablet', 'other'),
    os VARCHAR(50),
    browser VARCHAR(50),
    ip VARCHAR(45),
    location_country VARCHAR(50),
    location_province VARCHAR(50),
    location_city VARCHAR(50),
    platform VARCHAR(50),
    timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (creative_id) REFERENCES creatives(id) ON DELETE CASCADE,
    INDEX idx_impression_id (impression_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_creative_id (creative_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_platform (platform)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='曝光数据表'
PARTITION BY RANGE (YEAR(timestamp) * 100 + MONTH(timestamp)) (
    PARTITION p202603 VALUES LESS THAN (202604),
    PARTITION p202604 VALUES LESS THAN (202605),
    PARTITION p202605 VALUES LESS THAN (202606),
    PARTITION p202606 VALUES LESS THAN (202607),
    PARTITION p202607 VALUES LESS THAN (202608),
    PARTITION p202608 VALUES LESS THAN (202609),
    PARTITION p202609 VALUES LESS THAN (202610),
    PARTITION p202610 VALUES LESS THAN (202611),
    PARTITION p202611 VALUES LESS THAN (202612),
    PARTITION p202612 VALUES LESS THAN (202701),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 11. clicks - 点击数据表

```sql
CREATE TABLE clicks (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    click_id VARCHAR(100) NOT NULL UNIQUE,
    impression_id VARCHAR(100) NOT NULL,
    campaign_id BIGINT UNSIGNED NOT NULL,
    creative_id BIGINT UNSIGNED NOT NULL,
    user_id VARCHAR(100),
    device_type ENUM('mobile', 'desktop', 'tablet', 'other'),
    os VARCHAR(50),
    browser VARCHAR(50),
    ip VARCHAR(45),
    location_country VARCHAR(50),
    location_province VARCHAR(50),
    location_city VARCHAR(50),
    platform VARCHAR(50),
    click_url VARCHAR(500),
    timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (creative_id) REFERENCES creatives(id) ON DELETE CASCADE,
    INDEX idx_click_id (click_id),
    INDEX idx_impression_id (impression_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_creative_id (creative_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_platform (platform)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='点击数据表'
PARTITION BY RANGE (YEAR(timestamp) * 100 + MONTH(timestamp)) (
    PARTITION p202603 VALUES LESS THAN (202604),
    PARTITION p202604 VALUES LESS THAN (202605),
    PARTITION p202605 VALUES LESS THAN (202606),
    PARTITION p202606 VALUES LESS THAN (202607),
    PARTITION p202607 VALUES LESS THAN (202608),
    PARTITION p202608 VALUES LESS THAN (202609),
    PARTITION p202609 VALUES LESS THAN (202610),
    PARTITION p202610 VALUES LESS THAN (202611),
    PARTITION p202611 VALUES LESS THAN (202612),
    PARTITION p202612 VALUES LESS THAN (202701),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 12. conversions - 转化数据表

```sql
CREATE TABLE conversions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversion_id VARCHAR(100) NOT NULL UNIQUE,
    click_id VARCHAR(100) NOT NULL,
    campaign_id BIGINT UNSIGNED NOT NULL,
    creative_id BIGINT UNSIGNED NOT NULL,
    user_id VARCHAR(100),
    conversion_type ENUM('purchase', 'signup', 'download', 'lead', 'view', 'add_to_cart', 'checkout') NOT NULL,
    value DECIMAL(10, 2) COMMENT '转化价值',
    currency VARCHAR(10) DEFAULT 'CNY',
    device_type ENUM('mobile', 'desktop', 'tablet', 'other'),
    os VARCHAR(50),
    browser VARCHAR(50),
    ip VARCHAR(45),
    location_country VARCHAR(50),
    location_province VARCHAR(50),
    location_city VARCHAR(50),
    platform VARCHAR(50),
    timestamp DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (creative_id) REFERENCES creatives(id) ON DELETE CASCADE,
    INDEX idx_conversion_id (conversion_id),
    INDEX idx_click_id (click_id),
    INDEX idx_campaign_id (campaign_id),
    INDEX idx_creative_id (creative_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_conversion_type (conversion_type),
    INDEX idx_platform (platform)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='转化数据表'
PARTITION BY RANGE (YEAR(timestamp) * 100 + MONTH(timestamp)) (
    PARTITION p202603 VALUES LESS THAN (202604),
    PARTITION p202604 VALUES LESS THAN (202605),
    PARTITION p202605 VALUES LESS THAN (202606),
    PARTITION p202606 VALUES LESS THAN (202607),
    PARTITION p202607 VALUES LESS THAN (202608),
    PARTITION p202608 VALUES LESS THAN (202609),
    PARTITION p202609 VALUES LESS THAN (202610),
    PARTITION p202610 VALUES LESS THAN (202611),
    PARTITION p202611 VALUES LESS THAN (202612),
    PARTITION p202612 VALUES LESS THAN (202701),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 13. reports - 报表配置表

```sql
CREATE TABLE reports (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    report_type ENUM('campaign', 'creative', 'audience', 'performance', 'custom') NOT NULL,
    metrics JSON NOT NULL COMMENT '指标列表',
    dimensions JSON COMMENT '维度列表',
    filters JSON COMMENT '过滤条件',
    is_public BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_report_type (report_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='报表配置表';
```

### 14. report_data - 报表数据表

```sql
CREATE TABLE report_data (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_id BIGINT UNSIGNED NOT NULL,
    data_date DATE NOT NULL,
    data JSON NOT NULL COMMENT '报表数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id),
    INDEX idx_data_date (data_date),
    UNIQUE KEY uk_report_date (report_id, data_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='报表数据表';
```

### 15. report_schedules - 报表定时任务表

```sql
CREATE TABLE report_schedules (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(200) NOT NULL,
    frequency ENUM('daily', 'weekly', 'monthly') NOT NULL,
    schedule_time TIME NOT NULL,
    recipients JSON NOT NULL COMMENT '接收者列表',
    format ENUM('excel', 'pdf', 'csv') DEFAULT 'excel',
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at DATETIME,
    next_run_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE,
    INDEX idx_report_id (report_id),
    INDEX idx_next_run_at (next_run_at),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='报表定时任务表';
```

### 16. accounts - 账户表

```sql
CREATE TABLE accounts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    balance DECIMAL(12, 2) DEFAULT 0,
    credit_limit DECIMAL(12, 2) DEFAULT 0,
    currency VARCHAR(10) DEFAULT 'CNY',
    status ENUM('active', 'frozen', 'closed') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='账户表';
```

### 17. transactions - 交易记录表

```sql
CREATE TABLE transactions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT UNSIGNED NOT NULL,
    type ENUM('recharge', 'consume', 'refund', 'withdrawal') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    balance_before DECIMAL(12, 2) NOT NULL,
    balance_after DECIMAL(12, 2) NOT NULL,
    order_id VARCHAR(100) COMMENT '订单号',
    description TEXT,
    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    metadata JSON COMMENT '元数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    INDEX idx_account_id (account_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_order_id (order_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='交易记录表';
```

### 18. invoices - 发票表

```sql
CREATE TABLE invoices (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT UNSIGNED NOT NULL,
    invoice_no VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    tax_number VARCHAR(50) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2),
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'issued', 'sent') DEFAULT 'pending',
    email VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    invoice_url VARCHAR(500) COMMENT '发票文件URL',
    issued_at DATETIME,
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    INDEX idx_account_id (account_id),
    INDEX idx_invoice_no (invoice_no),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='发票表';
```

### 19. platforms - 媒体平台表

```sql
CREATE TABLE platforms (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    icon_url VARCHAR(500),
    oauth_url VARCHAR(500),
    api_base_url VARCHAR(500),
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    rate_limit INT COMMENT '请求限制(每分钟)',
    config JSON COMMENT '平台配置',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_name (name),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='媒体平台表';
```

### 20. platform_accounts - 平台账户表

```sql
CREATE TABLE platform_accounts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    platform_id BIGINT UNSIGNED NOT NULL,
    account_id VARCHAR(100) NOT NULL,
    account_name VARCHAR(200),
    access_token VARCHAR(500) COMMENT '加密存储',
    refresh_token VARCHAR(500) COMMENT '加密存储',
    token_expires_at DATETIME,
    status ENUM('active', 'expired', 'revoked') DEFAULT 'active',
    last_synced_at DATETIME,
    sync_status ENUM('idle', 'syncing', 'failed') DEFAULT 'idle',
    metadata JSON COMMENT '账户元数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_platform_account (user_id, platform_id, account_id),
    INDEX idx_user_id (user_id),
    INDEX idx_platform_id (platform_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='平台账户表';
```

### 21. notifications - 系统通知表

```sql
CREATE TABLE notifications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    type ENUM('campaign_alert', 'budget_warning', 'creative_review', 'system_announcement', 'payment_reminder') NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    is_read BOOLEAN DEFAULT FALSE,
    read_at DATETIME,
    action_url VARCHAR(500),
    metadata JSON COMMENT '通知元数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='系统通知表';
```

---

## 索引策略

### 主键索引
所有表使用 `BIGINT UNSIGNED AUTO_INCREMENT` 作为主键

### 唯一索引
- `users.username`, `users.email`
- `roles.name`
- `user_roles.user_id, user_roles.role_id`
- `campaign_audiences.campaign_id, campaign_audiences.audience_id`
- `campaign_creatives.campaign_id, campaign_creatives.creative_id`
- `impressions.impression_id`
- `clicks.click_id`
- `conversions.conversion_id`
- `report_data.report_id, report_data.data_date`
- `invoices.invoice_no`
- `platform_accounts.user_id, platform_accounts.platform_id, platform_accounts.account_id`

### 普通索引
- 外键字段
- 查询频繁的字段（status, created_at, timestamp）
- 组合查询字段（campaign_id + created_at）

---

## 数据分区策略

数据表按月分区，提升查询性能：
- `impressions`
- `clicks`
- `conversions`

分区字段：`timestamp`
分区粒度：按月
保留周期：12个月

---

## 数据清理策略

### 自动归档
- 超过12个月的数据归档到历史表
- 已删除的用户数据保留30天后永久删除

### 数据清理任务
- 每日凌晨执行数据归档
- 每周执行数据统计
- 每月执行数据备份

---

## 性能优化建议

1. **读写分离**: 主库写入，从库读取
2. **连接池**: 使用连接池管理数据库连接
3. **查询优化**: 避免SELECT *，使用索引
4. **批量操作**: 批量插入使用 INSERT ... VALUES
5. **缓存策略**: 热点数据使用Redis缓存

---

**文档版本**: 1.0
**最后更新**: 2026-03-15
**维护者**: Echo-2
