# 运维智能体（Operations Agent）部署计划

**创建时间**: 2026-03-15
**目标**: 为DSP Platform部署运维智能体，实现自动化运维管理

---

## 部署概述

### 智能体职责

运维智能体负责：
- 📊 系统监控（CPU、内存、磁盘、网络）
- 🚨 异常告警（服务故障、性能下降、安全事件）
- 🔄 自动修复（服务重启、日志清理、资源优化）
- 📈 容量规划（资源趋势分析、扩容建议）
- 🔒 安全审计（漏洞扫描、配置检查）

### 技术栈

- **运行环境**: Docker + OpenClaw
- **监控工具**: Prometheus + Grafana
- **告警通知**: QQ Bot / Email / Webhook
- **任务调度**: Celery Beat
- **日志收集**: ELK Stack（可选）

---

## 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Operations Agent                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ 监控模块      │  │ 告警模块      │  │ 自动修复模块  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ↓                    ↓                    ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Prometheus  │    │  QQ Bot API  │    │  Docker API  │
│  + Grafana   │    │  + Email     │    │  + System    │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 端口分配

根据 `TOOLS.md` 部署规范：

| 服务 | 端口 | 说明 |
|------|------|------|
| 运维智能体主服务 | 8001 | FastAPI后端 |
| 监控数据采集 | 8002 | Prometheus metrics |
| 告警通知服务 | 8003 | Webhook endpoint |
| 管理控制台 | 8004 | Admin dashboard |

**注意**: 端口 8000 已被DSP Platform主应用使用

---

## 部署步骤

### 阶段1: 基础设施准备（10分钟）

#### 1.1 创建目录结构

```bash
cd /root/.openclaw/workspace
mkdir -p ops-agent/{backend,scripts,config,logs}
mkdir -p ops-agent/backend/{app,tests}
mkdir -p ops-agent/backend/app/{api,core,services,models,schemas}
mkdir -p ops-agent/scripts/{monitor,alert,repair}
```

#### 1.2 初始化项目

```bash
cd ops-agent

# 创建 requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
pymysql==1.1.0
redis==5.0.1
celery==5.3.4
prometheus-client==0.19.0
psutil==5.9.6
requests==2.31.0
python-dotenv==1.0.0
aiohttp==3.9.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
EOF

# 创建 Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
EOF

# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  ops-agent:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ops-agent
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8001:8001"
      - "8002:8002"
    volumes:
      - ./backend:/app
      - ./logs:/app/logs
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - ops-network
    depends_on:
      - redis

  redis:
    image: redis:7.0-alpine
    container_name: ops-redis
    restart: unless-stopped
    ports:
      - "6382:6379"
    networks:
      - ops-network

networks:
  ops-network:
    external: true
EOF
```

#### 1.3 创建环境配置

```bash
cat > .env << 'EOF'
# Application
APP_NAME="Operations Agent"
APP_VERSION="1.0.0"
DEBUG=False
ENVIRONMENT=production

# Server
HOST=0.0.0.0
PORT=8001
METRICS_PORT=8002

# Database
DATABASE_HOST=dsp-mysql
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=DspSecurePassword2026
DATABASE_NAME=ops_agent

# Redis
REDIS_HOST=ops-redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# JWT
JWT_SECRET_KEY=ops-agent-secret-key-2026
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Monitoring
PROMETHEUS_URL=http://dsp-prometheus:9090
GRAFANA_URL=http://dsp-grafana:3000

# Alerting
ALERT_ENABLED=True
ALERT_QQ_BOT_ENABLED=True
ALERT_EMAIL_ENABLED=False
ALERT_EMAIL_SMTP_HOST=
ALERT_EMAIL_SMTP_PORT=587
ALERT_EMAIL_USER=
ALERT_EMAIL_PASSWORD=

# Auto-Repair
AUTO_REPAIR_ENABLED=True
AUTO_REPAIR_CONFIRMED=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/ops-agent.log
EOF
```

### 阶段2: 核心模块开发（30分钟）

#### 2.1 主应用入口

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import logging

from app.core.config import settings
from app.api.v1 import api_router

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Operations Agent - Automated Operations Management"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} starting...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Monitoring: {settings.PROMETHEUS_URL}")
    logger.info(f"Alerting: {'Enabled' if settings.ALERT_ENABLED else 'Disabled'}")

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "metrics": "/metrics",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
```

#### 2.2 配置管理

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Operations Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    METRICS_PORT: int = 8002

    # Database
    DATABASE_HOST: str
    DATABASE_PORT: int = 3306
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Monitoring
    PROMETHEUS_URL: str
    GRAFANA_URL: str

    # Alerting
    ALERT_ENABLED: bool = True
    ALERT_QQ_BOT_ENABLED: bool = True
    ALERT_EMAIL_ENABLED: bool = False
    ALERT_EMAIL_SMTP_HOST: str = ""
    ALERT_EMAIL_SMTP_PORT: int = 587
    ALERT_EMAIL_USER: str = ""
    ALERT_EMAIL_PASSWORD: str = ""

    # Auto-Repair
    AUTO_REPAIR_ENABLED: bool = True
    AUTO_REPAIR_CONFIRMED: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/app/logs/ops-agent.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### 2.3 监控服务

```python
# backend/app/services/monitor.py
import psutil
import asyncio
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MonitorService:
    """系统监控服务"""

    def __init__(self):
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'load_avg_1m': 5.0
        }

    async def get_system_metrics(self) -> Dict:
        """获取系统指标"""
        try:
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu': self._get_cpu_metrics(),
                'memory': self._get_memory_metrics(),
                'disk': self._get_disk_metrics(),
                'network': self._get_network_metrics(),
                'load': self._get_load_metrics(),
                'docker': self._get_docker_metrics()
            }
            return metrics
        except Exception as e:
            logger.error(f"获取系统指标失败: {e}")
            return {}

    def _get_cpu_metrics(self) -> Dict:
        """CPU指标"""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_count(),
            'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
        }

    def _get_memory_metrics(self) -> Dict:
        """内存指标"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free
        }

    def _get_disk_metrics(self) -> Dict:
        """磁盘指标"""
        disks = {}
        for partition in psutil.disk_partitions():
            if partition.fstype:
                usage = psutil.disk_usage(partition.mountpoint)
                disks[partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
        return disks

    def _get_network_metrics(self) -> Dict:
        """网络指标"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout
        }

    def _get_load_metrics(self) -> Dict:
        """负载指标"""
        load = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
        return {
            '1m': load[0],
            '5m': load[1],
            '15m': load[2]
        }

    def _get_docker_metrics(self) -> Dict:
        """Docker指标"""
        try:
            import docker
            client = docker.from_env()
            containers = client.containers.list()
            
            return {
                'total': len(containers),
                'running': len([c for c in containers if c.status == 'running']),
                'stopped': len([c for c in containers if c.status == 'exited']),
                'names': [c.name for c in containers]
            }
        except Exception as e:
            logger.warning(f"获取Docker指标失败: {e}")
            return {'error': str(e)}

    def check_thresholds(self, metrics: Dict) -> List[Dict]:
        """检查阈值并返回告警"""
        alerts = []

        # CPU检查
        cpu = metrics.get('cpu', {})
        if cpu.get('percent', 0) > self.alert_thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'warning',
                'message': f"CPU使用率过高: {cpu['percent']}%",
                'value': cpu['percent'],
                'threshold': self.alert_thresholds['cpu_percent']
            })

        # 内存检查
        memory = metrics.get('memory', {})
        if memory.get('percent', 0) > self.alert_thresholds['memory_percent']:
            alerts.append({
                'type': 'memory_high',
                'severity': 'warning',
                'message': f"内存使用率过高: {memory['percent']}%",
                'value': memory['percent'],
                'threshold': self.alert_thresholds['memory_percent']
            })

        # 磁盘检查
        disk = metrics.get('disk', {})
        for mount, usage in disk.items():
            if usage.get('percent', 0) > self.alert_thresholds['disk_percent']:
                alerts.append({
                    'type': 'disk_high',
                    'severity': 'critical',
                    'message': f"磁盘 {mount} 使用率过高: {usage['percent']}%",
                    'value': usage['percent'],
                    'threshold': self.alert_thresholds['disk_percent'],
                    'mount': mount
                })

        return alerts
```

#### 2.4 告警服务

```python
# backend/app/services/alert.py
import logging
from typing import List, Dict
from app.core.config import settings

logger = logging.getLogger(__name__)

class AlertService:
    """告警服务"""

    def __init__(self):
        self.qq_bot_enabled = settings.ALERT_QQ_BOT_ENABLED
        self.email_enabled = settings.ALERT_EMAIL_ENABLED

    async def send_alert(self, alert: Dict) -> bool:
        """发送告警"""
        try:
            logger.info(f"发送告警: {alert.get('type')}")

            # QQ Bot通知
            if self.qq_bot_enabled:
                await self._send_qq_alert(alert)

            # Email通知
            if self.email_enabled:
                await self._send_email_alert(alert)

            return True
        except Exception as e:
            logger.error(f"发送告警失败: {e}")
            return False

    async def _send_qq_alert(self, alert: Dict) -> bool:
        """发送QQ Bot告警"""
        try:
            # TODO: 集成QQ Bot API
            message = self._format_alert_message(alert)
            logger.info(f"QQ Bot告警: {message}")
            return True
        except Exception as e:
            logger.error(f"QQ Bot告警发送失败: {e}")
            return False

    async def _send_email_alert(self, alert: Dict) -> bool:
        """发送Email告警"""
        try:
            # TODO: 实现Email发送
            message = self._format_alert_message(alert)
            logger.info(f"Email告警: {message}")
            return True
        except Exception as e:
            logger.error(f"Email告警发送失败: {e}")
            return False

    def _format_alert_message(self, alert: Dict) -> str:
        """格式化告警消息"""
        severity_map = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'critical': '🚨'
        }
        icon = severity_map.get(alert.get('severity', 'info'), 'ℹ️')
        
        return f"""
{icon} {alert.get('message', '未知告警')}

类型: {alert.get('type')}
严重程度: {alert.get('severity')}
当前值: {alert.get('value')}
阈值: {alert.get('threshold')}
时间: {alert.get('timestamp', '未知')}
"""
```

#### 2.5 API路由

```python
# backend/app/api/v1/monitor.py
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.services.monitor import MonitorService

router = APIRouter()
monitor = MonitorService()

@router.get("/metrics")
async def get_system_metrics() -> Dict:
    """获取系统指标"""
    return await monitor.get_system_metrics()

@router.get("/health")
async def check_system_health() -> Dict:
    """检查系统健康状态"""
    metrics = await monitor.get_system_metrics()
    alerts = monitor.check_thresholds(metrics)
    
    return {
        "status": "healthy" if not alerts else "warning",
        "alerts": alerts,
        "metrics": metrics
    }
```

### 阶段3: 部署和测试（10分钟）

#### 3.1 构建和启动

```bash
cd /root/.openclaw/workspace/ops-agent

# 创建网络
docker network create ops-network

# 构建镜像
docker-compose build --no-cache

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 3.2 验证部署

```bash
# 健康检查
curl http://localhost:8001/health

# 获取系统指标
curl http://localhost:8001/api/v1/monitor/metrics

# 检查Prometheus metrics
curl http://localhost:8002/metrics
```

---

## 集成DSP Platform监控

### 1. 在Prometheus中添加目标

编辑Prometheus配置：

```yaml
scrape_configs:
  - job_name: 'ops-agent'
    static_configs:
      - targets: ['ops-agent:8002']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

重启Prometheus：

```bash
docker restart dsp-prometheus
```

### 2. 在Grafana中创建仪表板

- 导入Ops Agent仪表板
- 配置告警规则
- 设置通知渠道

---

## 自动化监控任务

使用Celery Beat执行周期性任务：

```python
# backend/app/tasks/monitor_tasks.py
from celery import Celery
from app.services.monitor import MonitorService
from app.services.alert import AlertService
import logging

logger = logging.getLogger(__name__)

celery_app = Celery('monitor_tasks')
celery_app.config_from_object('app.core.celery_config')

monitor = MonitorService()
alert_service = AlertService()

@celery_app.task
def collect_metrics():
    """采集系统指标"""
    metrics = asyncio.run(monitor.get_system_metrics())
    alerts = monitor.check_thresholds(metrics)
    
    for alert in alerts:
        asyncio.run(alert_service.send_alert(alert))
    
    return metrics

@celery_app.task
def check_service_health():
    """检查服务健康状态"""
    # TODO: 检查DSP Platform各服务状态
    pass

# Celery Beat配置
celery_app.conf.beat_schedule = {
    'collect-metrics': {
        'task': 'monitor_tasks.collect_metrics',
        'schedule': 60.0,  # 每60秒执行一次
    },
    'check-service-health': {
        'task': 'monitor_tasks.check_service_health',
        'schedule': 300.0,  # 每5分钟执行一次
    },
}
```

---

## 运维脚本

### 1. 系统健康检查脚本

```bash
# scripts/health-check.sh
#!/bin/bash
curl -s http://localhost:8001/api/v1/monitor/health | jq .
```

### 2. 服务重启脚本

```bash
# scripts/restart-service.sh
#!/bin/bash
docker-compose restart ops-agent
```

### 3. 日志清理脚本

```bash
# scripts/clean-logs.sh
#!/bin/bash
find /root/.openclaw/workspace/ops-agent/logs -name "*.log" -mtime +7 -delete
```

---

## 时间线

| 阶段 | 时间 | 任务 | 状态 |
|------|------|------|------|
| 阶段1 | 10分钟 | 基础设施准备 | ⏳ 待开始 |
| 阶段2 | 30分钟 | 核心模块开发 | ⏳ 待开始 |
| 阶段3 | 10分钟 | 部署和测试 | ⏳ 待开始 |
| 阶段4 | 20分钟 | 集成DSP Platform | ⏳ 待开始 |
| 阶段5 | 10分钟 | 配置告警和通知 | ⏳ 待开始 |
| **总计** | **80分钟** | **完整部署** | **⏳ 待开始** |

---

## 下一步

1. ✅ 创建项目目录结构
2. ✅ 初始化Docker配置
3. 🔄 开发核心监控模块
4. ⏳ 开发告警服务
5. ⏳ 开发自动修复模块
6. ⏳ 集成DSP Platform监控
7. ⏳ 配置Grafana仪表板
8. ⏳ 测试告警通知

---

**创建时间**: 2026-03-15 12:30
**预计完成**: 2026-03-15 13:50
**负责人**: Echo-2 (Agentic AI)
