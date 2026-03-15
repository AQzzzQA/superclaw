# DSP广告平台 - Celery任务队列设计

## 任务队列架构

### 架构组件
- **Celery Worker**: 任务执行节点
- **Celery Beat**: 定时任务调度器
- **Redis**: 消息代理 + 结果存储
- **Flower**: 任务监控面板

### 队列划分
```
default_queue      # 默认队列（低优先级）
high_priority      # 高优先级队列（紧急任务）
data_upload        # 数据上传队列（批量数据处理）
report_generation  # 报表生成队列（报表计算）
data_sync          # 数据同步队列（平台数据同步）
notification       # 通知队列（邮件/短信/推送）
```

---

## 任务分类

### 1. 数据回传任务 (Data Upload Tasks)
- **实时数据接收**: 接收曝光、点击、转化数据
- **批量数据处理**: 批量上传数据的验证和存储
- **数据清洗**: 清洗异常数据
- **数据标准化**: 统一不同平台的数据格式

### 2. 报表生成任务 (Report Generation Tasks)
- **实时报表计算**: 实时计算报表数据
- **自定义报表生成**: 生成用户自定义报表
- **报表导出**: Excel/PDF报表导出
- **定时报表**: 按计划生成报表

### 3. 数据同步任务 (Data Sync Tasks)
- **平台数据同步**: 同步媒体平台数据
- **账户信息同步**: 同步账户余额、状态
- **广告状态同步**: 同步广告计划状态
- **审核状态同步**: 同步创意审核状态

### 4. 通知任务 (Notification Tasks)
- **邮件通知**: 发送邮件通知
- **短信通知**: 发送短信通知
- **推送通知**: 发送APP推送通知
- **系统通知**: 生成系统内通知

### 5. 定时任务 (Scheduled Tasks)
- **数据归档**: 归档历史数据
- **数据统计**: 生成统计数据
- **预算检查**: 检查预算使用情况
- **系统清理**: 清理临时数据

---

## 任务详细设计

### 1. 数据回传任务

#### 1.1 实时曝光数据接收
```python
@celery_app.task(name='tasks.data.receive_impression', queue='data_upload')
def receive_impression(impression_data: dict):
    """
    接收实时曝光数据

    任务流程:
    1. 验证数据格式
    2. 检查重复数据
    3. 存储到数据库
    4. 更新Redis缓存
    5. 触发实时通知
    """
    # 验证数据
    validate_impression_data(impression_data)

    # 检查重复
    if is_duplicate_impression(impression_data['impression_id']):
        return {'status': 'skipped', 'reason': 'duplicate'}

    # 存储数据
    store_impression(impression_data)

    # 更新缓存
    update_impression_cache(impression_data)

    # 触发通知
    trigger_realtime_notification('impression', impression_data)

    return {'status': 'success', 'impression_id': impression_data['impression_id']}
```

#### 1.2 批量点击数据处理
```python
@celery_app.task(name='tasks.data.process_batch_clicks', queue='data_upload')
def process_batch_clicks(clicks_data: list):
    """
    批量处理点击数据

    任务流程:
    1. 验证批量数据
    2. 过滤无效数据
    3. 批量插入数据库
    4. 更新统计缓存
    """
    valid_clicks = []
    skipped_count = 0

    for click_data in clicks_data:
        try:
            validate_click_data(click_data)
            valid_clicks.append(click_data)
        except ValidationError:
            skipped_count += 1

    # 批量插入
    if valid_clicks:
        batch_insert_clicks(valid_clicks)
        update_click_cache(len(valid_clicks))

    return {
        'status': 'success',
        'processed': len(valid_clicks),
        'skipped': skipped_count
    }
```

#### 1.3 转化数据验证与存储
```python
@celery_app.task(name='tasks.data.process_conversion', queue='data_upload', bind=True, max_retries=3)
def process_conversion(self, conversion_data: dict):
    """
    处理转化数据

    任务流程:
    1. 验证转化数据
    2. 关联点击数据
    3. 计算转化价值
    4. 更新ROI
    5. 触发转化通知
    """
    try:
        # 验证数据
        validate_conversion_data(conversion_data)

        # 关联点击
        click_data = get_click_by_id(conversion_data['click_id'])
        if not click_data:
            raise ValueError('Click not found')

        # 计算价值
        conversion_value = calculate_conversion_value(conversion_data)

        # 存储转化
        store_conversion(conversion_data)

        # 更新ROI
        update_campaign_roi(click_data['campaign_id'], conversion_value)

        # 通知
        trigger_conversion_notification(conversion_data)

        return {'status': 'success', 'conversion_id': conversion_data['conversion_id']}

    except Exception as exc:
        # 重试机制
        raise self.retry(exc=exc, countdown=60)
```

#### 1.4 数据清洗任务
```python
@celery_app.task(name='tasks.data.clean_data', queue='data_upload')
def clean_data(data_type: str, start_date: str, end_date: str):
    """
    清洗指定时间段的数据

    任务流程:
    1. 查询原始数据
    2. 识别异常数据
    3. 修正或标记异常
    4. 生成清洗报告
    """
    anomalies = detect_anomalies(data_type, start_date, end_date)

    cleaned_count = 0
    for anomaly in anomalies:
        if anomaly['type'] == 'fixable':
            fix_anomaly(anomaly)
            cleaned_count += 1
        else:
            flag_anomaly(anomaly)

    generate_cleaning_report(data_type, start_date, end_date, cleaned_count)

    return {
        'status': 'success',
        'cleaned': cleaned_count,
        'flagged': len(anomalies) - cleaned_count
    }
```

---

### 2. 报表生成任务

#### 2.1 实时报表计算
```python
@celery_app.task(name='tasks.reports.calculate_realtime', queue='report_generation')
def calculate_realtime_report(campaign_id: int, metrics: list):
    """
    计算实时报表数据

    任务流程:
    1. 查询实时数据
    2. 聚合指标
    3. 计算衍生指标（CTR、CVR、ROI等）
    4. 更新缓存
    5. 推送WebSocket消息
    """
    # 查询数据
    data = query_realtime_data(campaign_id)

    # 聚合
    aggregated = aggregate_metrics(data, metrics)

    # 计算衍生指标
    if 'impressions' in metrics and 'clicks' in metrics:
        aggregated['ctr'] = aggregated['clicks'] / aggregated['impressions'] * 100

    if 'clicks' in metrics and 'conversions' in metrics:
        aggregated['cvr'] = aggregated['conversions'] / aggregated['clicks'] * 100

    # 更新缓存
    cache_key = f"realtime_report:{campaign_id}"
    redis_client.set(cache_key, json.dumps(aggregated), ex=300)  # 5分钟缓存

    # WebSocket推送
    broadcast_report_update(campaign_id, aggregated)

    return {'status': 'success', 'data': aggregated}
```

#### 2.2 自定义报表生成
```python
@celery_app.task(name='tasks.reports.generate_custom', queue='report_generation')
def generate_custom_report(report_id: int, start_date: str, end_date: str):
    """
    生成自定义报表

    任务流程:
    1. 获取报表配置
    2. 查询数据
    3. 按维度聚合
    4. 计算指标
    5. 存储结果
    """
    # 获取配置
    report_config = get_report_config(report_id)

    # 查询数据
    raw_data = query_report_data(
        report_config['filters'],
        start_date,
        end_date
    )

    # 聚合
    result = aggregate_by_dimensions(
        raw_data,
        report_config['dimensions'],
        report_config['metrics']
    )

    # 存储
    store_report_data(report_id, start_date, result)

    return {'status': 'success', 'rows': len(result)}
```

#### 2.3 报表导出任务
```python
@celery_app.task(name='tasks.reports.export_report', queue='report_generation')
def export_report(report_id: int, export_format: str, start_date: str, end_date: str):
    """
    导出报表

    任务流程:
    1. 获取报表数据
    2. 格式化数据
    3. 生成文件
    4. 上传到存储
    5. 返回下载链接
    """
    # 获取数据
    data = get_report_data(report_id, start_date, end_date)

    # 格式化
    if export_format == 'excel':
        file_path = generate_excel(data)
    elif export_format == 'pdf':
        file_path = generate_pdf(data)
    elif export_format == 'csv':
        file_path = generate_csv(data)

    # 上传
    file_url = upload_file(file_path)

    # 清理临时文件
    os.remove(file_path)

    # 发送通知
    notify_export_ready(report_id, file_url)

    return {'status': 'success', 'download_url': file_url}
```

#### 2.4 定时报表任务
```python
@celery_app.task(name='tasks.reports.scheduled_report', queue='report_generation')
def generate_scheduled_report(schedule_id: int):
    """
    生成定时报表

    任务流程:
    1. 获取调度配置
    2. 计算时间范围
    3. 生成报表
    4. 发送给接收者
    """
    # 获取配置
    schedule = get_schedule_config(schedule_id)
    report_config = get_report_config(schedule['report_id'])

    # 计算时间范围
    date_range = calculate_date_range(schedule['frequency'])

    # 生成报表
    result = generate_report_data(
        report_config,
        date_range['start'],
        date_range['end']
    )

    # 导出文件
    file_url = export_report_file(result, schedule['format'])

    # 发送
    for recipient in schedule['recipients']:
        send_report_email(recipient['email'], file_url)

    # 更新下次执行时间
    update_next_run_time(schedule_id)

    return {'status': 'success', 'sent_to': len(schedule['recipients'])}
```

---

### 3. 数据同步任务

#### 3.1 平台账户同步
```python
@celery_app.task(name='tasks.sync.platform_account', queue='data_sync', bind=True, max_retries=3)
def sync_platform_account(self, user_id: int, platform_id: int):
    """
    同步平台账户信息

    任务流程:
    1. 获取平台配置
    2. 刷新访问令牌
    3. 拉取账户列表
    4. 更新数据库
    5. 记录同步日志
    """
    try:
        # 获取平台配置
        platform = get_platform_config(platform_id)
        platform_accounts = get_platform_accounts(user_id, platform_id)

        # 同步每个账户
        for account in platform_accounts:
            # 刷新令牌
            refresh_access_token(account)

            # 拉取数据
            account_data = fetch_account_data(account, platform)

            # 更新数据库
            update_account_data(account, account_data)

        # 记录日志
        log_sync_operation(user_id, platform_id, 'success')

        return {'status': 'success', 'synced': len(platform_accounts)}

    except Exception as exc:
        log_sync_operation(user_id, platform_id, 'failed', str(exc))
        raise self.retry(exc=exc, countdown=60)
```

#### 3.2 广告计划同步
```python
@celery_app.task(name='tasks.sync.campaigns', queue='data_sync')
def sync_campaigns(user_id: int, platform_id: int):
    """
    同步广告计划

    任务流程:
    1. 获取平台账户
    2. 拉取广告计划列表
    3. 对比本地数据
    4. 更新变更
    5. 触发状态变更通知
    """
    platform_accounts = get_platform_accounts(user_id, platform_id)

    updated_count = 0
    for account in platform_accounts:
        # 拉取数据
        remote_campaigns = fetch_remote_campaigns(account)

        # 对比更新
        for remote in remote_campaigns:
            local = get_local_campaign(remote['platform_id'])

            if local:
                # 更新
                update_campaign(local, remote)
                updated_count += 1

                # 状态变更通知
                if local['status'] != remote['status']:
                    notify_campaign_status_change(local, remote['status'])
            else:
                # 新建
                create_campaign_from_remote(remote)

    return {'status': 'success', 'updated': updated_count}
```

#### 3.3 创意审核状态同步
```python
@celery_app.task(name='tasks.sync.creative_review', queue='data_sync')
def sync_creative_review_status(creative_id: int):
    """
    同步创意审核状态

    任务流程:
    1. 获取创意信息
    2. 查询平台审核状态
    3. 更新本地状态
    4. 发送审核结果通知
    """
    creative = get_creative(creative_id)

    # 查询平台状态
    platform = get_platform_config(creative['platform_id'])
    review_status = query_creative_review_status(creative, platform)

    # 更新本地
    update_creative_review_status(creative_id, review_status)

    # 通知
    if review_status['status'] in ['approved', 'rejected']:
        notify_creative_review_result(creative, review_status)

    return {'status': 'success', 'review_status': review_status['status']}
```

---

### 4. 通知任务

#### 4.1 邮件通知
```python
@celery_app.task(name='tasks.notification.send_email', queue='notification', bind=True, max_retries=3)
def send_email_notification(self, to_email: str, subject: str, body: str):
    """
    发送邮件通知

    任务流程:
    1. 渲染邮件模板
    2. 发送邮件
    3. 记录发送日志
    """
    try:
        # 渲染模板
        html_body = render_email_template(subject, body)

        # 发送
        send_mail(to_email, subject, html_body)

        # 记录日志
        log_notification('email', to_email, 'success')

        return {'status': 'success'}

    except Exception as exc:
        log_notification('email', to_email, 'failed', str(exc))
        raise self.retry(exc=exc, countdown=60)
```

#### 4.2 短信通知
```python
@celery_app.task(name='tasks.notification.send_sms', queue='notification')
def send_sms_notification(phone: str, message: str):
    """
    发送短信通知

    任务流程:
    1. 格式化短信内容
    2. 调用短信API
    3. 记录发送日志
    """
    # 格式化
    formatted_message = format_sms_message(message)

    # 发送
    result = send_sms(phone, formatted_message)

    # 记录
    log_notification('sms', phone, 'success' if result else 'failed')

    return {'status': 'success' if result else 'failed'}
```

#### 4.3 系统内通知
```python
@celery_app.task(name='tasks.notification.create_system_notification', queue='notification')
def create_system_notification(user_id: int, notification_type: str, title: str, content: str, priority: str = 'normal'):
    """
    创建系统内通知

    任务流程:
    1. 保存通知到数据库
    2. 更新未读计数
    3. 推送WebSocket消息
    """
    # 保存
    notification_id = save_notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        content=content,
        priority=priority
    )

    # 更新计数
    increment_unread_count(user_id)

    # 推送
    push_websocket_notification(user_id, notification_id)

    return {'status': 'success', 'notification_id': notification_id}
```

---

### 5. 定时任务 (Scheduled Tasks)

#### 5.1 数据归档任务
```python
@celery_app.task(name='tasks.scheduled.archive_data')
def archive_old_data():
    """
    归档12个月前的数据

    执行频率: 每月1日凌晨2点
    """
    archive_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m')

    # 归档曝光数据
    archived_impressions = archive_table('impressions', archive_date)

    # 归档点击数据
    archived_clicks = archive_table('clicks', archive_date)

    # 归档转化数据
    archived_conversions = archive_table('conversions', archive_date)

    # 生成归档报告
    generate_archive_report(archived_impressions, archived_clicks, archived_conversions)

    return {
        'status': 'success',
        'impressions': archived_impressions,
        'clicks': archived_clicks,
        'conversions': archived_conversions
    }
```

#### 5.2 预算检查任务
```python
@celery_app.task(name='tasks.scheduled.check_budget')
def check_campaign_budget():
    """
    检查广告计划预算

    执行频率: 每小时
    """
    # 获取所有活跃广告计划
    active_campaigns = get_active_campaigns()

    warnings = []
    for campaign in active_campaigns:
        # 计算已使用预算
        used_budget = get_used_budget(campaign['id'])

        # 检查是否超预算
        if used_budget >= campaign['budget']:
            # 暂停广告
            pause_campaign(campaign['id'])

            # 发送通知
            send_budget_exceeded_notification(campaign)
            warnings.append({
                'campaign_id': campaign['id'],
                'type': 'exceeded'
            })

        # 检查是否接近预算（90%）
        elif used_budget >= campaign['budget'] * 0.9:
            send_budget_warning_notification(campaign)
            warnings.append({
                'campaign_id': campaign['id'],
                'type': 'warning'
            })

    return {'status': 'success', 'warnings': len(warnings)}
```

#### 5.3 数据统计任务
```python
@celery_app.task(name='tasks.scheduled.generate_statistics')
def generate_daily_statistics():
    """
    生成每日统计数据

    执行频率: 每日凌晨3点
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # 广告计划统计
    campaign_stats = calculate_campaign_statistics(yesterday)

    # 创意统计
    creative_stats = calculate_creative_statistics(yesterday)

    # 受众统计
    audience_stats = calculate_audience_statistics(yesterday)

    # 平台统计
    platform_stats = calculate_platform_statistics(yesterday)

    # 保存统计数据
    save_daily_statistics({
        'date': yesterday,
        'campaigns': campaign_stats,
        'creatives': creative_stats,
        'audiences': audience_stats,
        'platforms': platform_stats
    })

    return {'status': 'success', 'date': yesterday}
```

#### 5.4 系统清理任务
```python
@celypy.task(name='tasks.scheduled.cleanup_temp_data')
def cleanup_temporary_data():
    """
    清理临时数据

    执行频率: 每周日凌晨4点
    """
    # 清理7天前的临时文件
    deleted_files = cleanup_temp_files(days=7)

    # 清理过期缓存
    expired_keys = cleanup_expired_cache()

    # 清理已读通知（30天前）
    deleted_notifications = cleanup_read_notifications(days=30)

    return {
        'status': 'success',
        'files': deleted_files,
        'cache_keys': expired_keys,
        'notifications': deleted_notifications
    }
```

#### 5.5 健康检查任务
```python
@celery_app.task(name='tasks.scheduled.health_check')
def system_health_check():
    """
    系统健康检查

    执行频率: 每5分钟
    """
    health_status = {
        'database': check_database_health(),
        'redis': check_redis_health(),
        'celery': check_celery_health(),
        'disk': check_disk_usage(),
        'memory': check_memory_usage()
    }

    # 记录状态
    log_health_status(health_status)

    # 发送告警
    if not all(health_status.values()):
        send_health_alert(health_status)

    return {'status': 'success', 'health': health_status}
```

---

## 任务监控

### Flower监控面板
- 任务执行状态
- 任务执行时间
- 任务成功/失败率
- Worker负载

### 监控指标
- 任务队列长度
- 任务执行延迟
- 任务失败率
- Worker CPU/内存使用

### 告警规则
- 队列积压超过1000
- 任务失败率超过5%
- 任务执行时间超过阈值
- Worker离线

---

## 任务配置

### Celery配置
```python
# config/celery.py
CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/1',
    'task_routes': {
        'tasks.data.*': {'queue': 'data_upload'},
        'tasks.reports.*': {'queue': 'report_generation'},
        'tasks.sync.*': {'queue': 'data_sync'},
        'tasks.notification.*': {'queue': 'notification'},
    },
    'task_time_limit': 3600,  # 1小时
    'task_soft_time_limit': 3300,  # 55分钟
    'task_acks_late': True,
    'worker_prefetch_multiplier': 1,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
}
```

### Beat调度配置
```python
# config/beat_schedule.py
CELERY_BEAT_SCHEDULE = {
    # 每月数据归档
    'archive-data': {
        'task': 'tasks.scheduled.archive_data',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),
    },
    # 每小时预算检查
    'check-budget': {
        'task': 'tasks.scheduled.check_budget',
        'schedule': crontab(minute=0),
    },
    # 每日统计数据
    'generate-statistics': {
        'task': 'tasks.scheduled.generate_statistics',
        'schedule': crontab(hour=3, minute=0),
    },
    # 每周数据清理
    'cleanup-temp-data': {
        'task': 'tasks.scheduled.cleanup_temp_data',
        'schedule': crontab(day_of_week=0, hour=4, minute=0),
    },
    # 健康检查
    'health-check': {
        'task': 'tasks.scheduled.health_check',
        'schedule': crontab(minute='*/5'),
    },
}
```

---

## 最佳实践

### 1. 任务设计
- 任务幂等性：重复执行不会产生副作用
- 任务原子性：单个任务完成一个完整操作
- 任务可追踪：记录任务执行日志

### 2. 错误处理
- 合理的重试机制
- 异常捕获和记录
- 失败通知

### 3. 性能优化
- 批量处理优于单条处理
- 使用事务保证数据一致性
- 合理设置超时时间

### 4. 监控告警
- 实时监控任务状态
- 设置合理的告警阈值
- 定期分析任务性能

---

**文档版本**: 1.0
**最后更新**: 2026-03-15
**维护者**: Echo-2
