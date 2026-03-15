# DSP Platform Celery 服务故障报告

**问题**: Celery Worker, Beat, Flower 服务持续重启（exit code 2）
**发现时间**: 2026-03-15 16:26
**状态**: ⚠️ 严重问题

---

## 故障详情

### 受影响的服务
- dsp-celery-worker - 持续重启（exit code 2）
- dsp-celery-beat - 持续重启（exit code 2）
- dsp-flower - 持续重启（exit code 2）

### 错误日志
```
Error: Invalid value for '-A' / '--app': 
Unable to load celery application.
The module app.tasks.worker was not found.
```

---

## 问题分析

### 根本原因
Celery 应用无法启动，因为模块路径错误：
- **配置的路径**: `app.tasks.worker`
- **实际路径**: 应该是 `app.tasks.celery_app` 或类似的正确路径

### 影响范围
- ✅ 核心服务正常运行（Backend, MySQL, Redis, Nginx, Prometheus, Grafana）
- ❌ 后台任务系统完全瘫痪
- ❌ 定时任务无法执行
- ❌ 异步任务无法处理

---

## 临时解决方案

### 方案1：禁用Celery服务（推荐临时使用）

如果Celery功能暂时不需要，可以注释掉docker-compose.yml中的Celery服务：

```yaml
# celery-worker:
#   build:
#     context: ./backend
#     dockerfile: Dockerfile
#   ...

# celery-beat:
#   build:
#     context: ./backend
#     dockerfile: Dockerfile
#   ...

# flower:
#   build:
#     context: ./backend
#     dockerfile: Dockerfile
#   ...
```

重启服务：
```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose down
docker-compose up -d
```

### 方案2：检查并修复Celery配置

需要检查以下文件：

1. **backend/app/tasks/celery_app.py** - Celery应用配置
2. **backend/app/tasks/__init__.py** - 任务模块
3. **docker-compose.yml** - Celery命令配置

修复步骤：

#### 步骤1：检查Celery应用文件
```bash
ls -la /root/.openclaw/workspace/dsp-platform/backend/app/tasks/
cat /root/.openclaw/workspace/dsp-platform/backend/app/tasks/celery_app.py
```

#### 步骤2：修正docker-compose.yml配置
```yaml
celery-worker:
  command: celery -A app.tasks.celery_app worker --loglevel=info

celery-beat:
  command: celery -A app.tasks.celery_app beat --loglevel=info

flower:
  command: celery -A app.tasks.celery_app flower --port=5555
```

#### 步骤3：重启服务
```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose restart celery-worker celery-beat flower
```

---

## 完整修复计划

### Phase 1: 诊断（当前）
- ✅ 识别问题：Celery模块路径错误
- ✅ 检查错误日志
- ⏳ 检查实际文件结构
- ⏳ 确定正确的Celery应用路径

### Phase 2: 修复（待执行）
- ⏳ 修正docker-compose.yml中的Celery命令
- ⏳ 验证Celery应用配置
- ⏳ 测试Celery服务启动

### Phase 3: 验证（待执行）
- ⏳ 验证所有Celery服务正常运行
- ⏳ 测试异步任务
- ⏳ 测试定时任务

### Phase 4: 优化（长期）
- ⏳ 添加Celery健康检查
- ⏳ 配置Celery监控
- ⏳ 优化Celery性能

---

## 当前服务状态

### 正常运行 ✅
- dsp-backend (8000) - 健康
- dsp-mysql (3308) - 健康
- dsp-redis (6381) - 健康
- dsp-nginx (8080) - 运行中
- dsp-prometheus (9000) - 运行中
- dsp-grafana (8888) - 运行中

### 故障中 ⚠️
- dsp-celery-worker - 持续重启
- dsp-celery-beat - 持续重启
- dsp-flower - 持续重启

---

## 影响评估

### 功能影响
- ❌ 异步任务处理（邮件发送、报表生成等）
- ❌ 定时任务（数据清理、统计汇总等）
- ❌ Celery监控面板（Flower）

### 业务影响
- ⚠️ 中等 - 核心API功能正常
- ⚠️ 中等 - 如果依赖异步任务，部分功能可能受影响
- ⚠️ 低 - 如果主要是同步API，影响较小

---

## 建议行动

### 立即执行
1. **检查Celery配置文件**
   ```bash
   ls -la /root/.openclaw/workspace/dsp-platform/backend/app/tasks/
   cat /root/.openclaw/workspace/dsp-platform/backend/app/tasks/celery_app.py
   ```

2. **决定修复策略**
   - 选项A: 修复Celery配置（需要Celery功能）
   - 选项B: 临时禁用Celery（不需要Celery功能）

### 短期目标
- [ ] 修复Celery配置或禁用Celery服务
- [ ] 确保所有服务稳定运行
- [ ] 更新文档说明Celery状态

### 长期目标
- [ ] 添加Celery健康检查
- [ ] 配置Celery监控和告警
- [ ] 优化Celery性能和可靠性

---

## 相关文档

- `docker-compose.yml` - Docker Compose配置
- `backend/app/tasks/celery_app.py` - Celery应用配置
- `backend/app/tasks/__init__.py` - 任务模块

---

**报告时间**: 2026-03-15 16:26
**优先级**: 🔴 高
**状态**: ⚠️ 等待修复决策
**建议**: 检查Celery配置文件，决定修复或禁用
