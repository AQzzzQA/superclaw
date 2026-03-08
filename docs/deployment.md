# SuperClaw 部署指南

## 🚀 快速开始

### 1. 环境要求

#### 必需组件
| 组件 | 版本要求 | 说明 |
|------|----------|------|
| **Python** | 3.11+ | 核心运行环境 |
| **Redis** | 7.0+ | 缓存和任务队列 |
| **PostgreSQL** | 14+ | 数据存储 |
| **Nginx** | 1.18+ | 反向代理（可选） |

#### 推荐配置
| 场景 | CPU | 内存 | 磁盘 |
|------|-----|------|--------|
| **开发环境** | 2 核 | 4 GB | 20 GB |
| **测试环境** | 4 核 | 8 GB | 50 GB |
| **生产环境** | 8 核 | 16 GB | 100 GB |

---

### 2. Docker 部署（推荐）

#### 2.1 拉取镜像

```bash
# 拉取最新镜像
docker pull superclaw/superclaw:latest

# 或者从源码构建
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw
docker build -t superclaw/superclaw .
```

---

#### 2.2 配置环境变量

创建 `.env` 文件：

```bash
# 数据库配置
DB_HOST=postgres
DB_PORT=5432
DB_NAME=superclaw
DB_USER=superclaw
DB_PASSWORD=your_secure_password

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# LemClaw 配置
LEMCLAW_API_URL=https://api.lemclaw.com
LEMCLAW_API_KEY=your_lemclaw_api_key

# 安全配置
SECRET_KEY=your_secret_key_min_32_chars
ALLOWED_HOSTS=api.superclaw.ai,superclaw.ai

# 监控配置
ENABLE_MONITORING=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

---

#### 2.3 使用 Docker Compose 启动

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build
```

---

### 3. 传统部署

#### 3.1 安装依赖

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

#### 3.2 数据库初始化

```bash
# 创建数据库
createdb superclaw

# 运行迁移
python scripts/migrate.py

# 初始化数据
python scripts/init_db.py
```

---

#### 3.3 启动服务

```bash
# 开发环境
python main.py --dev --port 8000

# 生产环境（使用 Gunicorn）
gunicorn -w 4 -b 0.0.0.0:8000 superclaw.app:app
```

---

### 4. Nginx 配置

创建 `/etc/nginx/sites-available/superclaw.conf`：

```nginx
upstream superclaw {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name api.superclaw.ai;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.superclaw.ai;

    ssl_certificate /etc/letsencrypt/live/api.superclaw.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.superclaw.ai/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    client_max_body_size 10M;

    location / {
        proxy_pass http://superclaw;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /health {
        proxy_pass http://superclaw/health;
        access_log off;
    }

    # 静态文件缓存
    location /static {
        alias /var/www/superclaw/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/superclaw.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### 5. SSL 证书配置

#### 使用 Let's Encrypt（免费）

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d api.superclaw.ai

# 自动续期
sudo certbot renew --dry-run
```

---

### 6. 监控与日志

#### 6.1 日志配置

配置 `/etc/rsyslog.d/50-superclaw.conf`：

```bash
# 应用日志
if $programname == 'superclaw' then {
    *.* /var/log/superclaw/app.log
    stop
}

# 错误日志
if $programname == 'superclaw' then {
    if ($msg contains 'ERROR') or ($msg contains 'CRITICAL') then {
        *.* /var/log/superclaw/error.log
    }
}
```

#### 6.2 Prometheus 监控

配置 `/etc/prometheus/prometheus.yml`：

```yaml
scrape_configs:
  - job_name: 'superclaw'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 15s
```

启动 Prometheus：

```bash
docker run -d \
    -p 9090:9090 \
    -v /etc/prometheus:/etc/prometheus \
    prom/prometheus
```

---

### 7. 高可用部署

#### 7.1 负载均衡

```yaml
# docker-compose.yml
version: '3.8'

services:
  superclaw-1:
    image: superclaw/superclaw:latest
    environment:
      - INSTANCE_ID=1
    depends_on:
      - postgres
      - redis
  
  superclaw-2:
    image: superclaw/superclaw:latest
    environment:
      - INSTANCE_ID=2
    depends_on:
      - postgres
      - redis
  
  postgres:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=superclaw
      - POSTGRES_USER=superclaw
      - POSTGRES_PASSWORD=your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - superclaw-1
      - superclaw-2

volumes:
  postgres_data:
  redis_data:
```

---

#### 7.2 数据库主从复制

主库配置 (`postgres-master.conf`)：

```ini
wal_level = replica
max_wal_senders = 3
wal_keep_size = 16MB
```

从库配置 (`postgres-replica.conf`)：

```ini
hot_standby = on
standby_mode = replica
primary_conninfo = 'host=master port=5432 user=replicator password=replicator_password'
```

---

### 8. 备份与恢复

#### 8.1 自动备份

创建备份脚本 `/usr/local/bin/backup-superclaw.sh`：

```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/superclaw"
DB_NAME="superclaw"
DB_USER="superclaw"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 数据库备份
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/superclaw_db_$DATE.sql.gz

# 文件备份
tar -czf $BACKUP_DIR/superclaw_files_$DATE.tar.gz /var/www/superclaw

# 保留最近 7 天的备份
find $BACKUP_DIR -name "superclaw_*" -mtime +7 -delete

# 上传到 S3（可选）
# aws s3 cp $BACKUP_DIR/superclaw_db_$DATE.sql.gz s3://superclaw-backups/
```

设置定时任务：

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /usr/local/bin/backup-superclaw.sh
```

---

#### 8.2 灾难恢复

```bash
# 停止服务
docker-compose down

# 恢复数据库
gunzip -c /backup/superclaw/superclaw_db_20260308_020000.sql.gz | psql -U superclaw superclaw

# 恢复文件
tar -xzf /backup/superclaw/superclaw_files_20260308_020000.tar.gz -C /

# 启动服务
docker-compose up -d
```

---

### 9. 性能优化

#### 9.1 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_memory_tags ON memory USING GIN(tags);

-- 配置连接池
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
```

---

#### 9.2 Redis 优化

```bash
# 编辑 redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

---

### 10. 安全加固

#### 10.1 防火墙配置

```bash
# 只开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 9000/tcp  # Prometheus（内网访问）
sudo ufw enable
```

---

#### 10.2 Fail2Ban

```bash
# 安装 Fail2Ban
sudo apt-get install fail2ban

# 配置 /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

---

## 🧪 测试部署

### 压力测试

```bash
# 安装 Apache Bench
sudo apt-get install apache2-utils

# 并发 100，总共 1000 请求
ab -n 1000 -c 100 https://api.superclaw.ai/health
```

---

### 健康检查

```bash
# 基础健康检查
curl https://api.superclaw.ai/health

# 详细健康检查
curl https://api.superclaw.ai/health/detailed
```

---

## 📞 故障排查

### 常见问题

#### 问题 1：服务无法启动

```bash
# 查看日志
docker-compose logs -f

# 检查端口占用
netstat -tlnp | grep :8000

# 检查数据库连接
psql -U superclaw -h localhost -d superclaw
```

---

#### 问题 2：数据库连接失败

```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 检查连接数
psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# 查看日志
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

---

#### 问题 3：内存不足

```bash
# 查看内存使用
free -h

# 查看进程内存占用
ps aux --sort=-%mem | head

# 增加 swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📞 支持与联系

- **部署文档**: https://docs.superclaw.ai/deployment
- **技术支持**: support@superclaw.ai
- **GitHub Issues**: https://github.com/AQzzzQA/superclaw/issues

---

**最后更新**: 2026-03-08
