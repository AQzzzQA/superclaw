# DSP Platform 外网IP+端口访问配置指南

**部署时间**: 2026-03-15
**适用场景**: 使用公网IP直接访问（无需域名）

---

## 访问架构

```
公网客户端 → 防火墙 → Nginx (80/443) → DSP Platform
           → 8000 (API)
           → 9090 (Prometheus)
           → 3002 (Grafana)
```

---

## 快速配置（3分钟）

### 步骤1：检查公网IP

```bash
# 获取公网IP
curl ifconfig.me

# 或
curl ip.sb
```

假设你的公网IP是：`1.2.3.4`

### 步骤2：配置防火墙开放端口

```bash
# CentOS/RHEL - firewalld
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --permanent --add-port=8000/tcp
firewall-cmd --permanent --add-port=9090/tcp
firewall-cmd --permanent --add-port=3002/tcp
firewall-cmd --permanent --add-port=5555/tcp
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --reload

# 验证
firewall-cmd --list-all

# Ubuntu/Debian - ufw
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw allow 9090/tcp
ufw allow 3002/tcp
ufw allow 5555/tcp
ufw allow 22/tcp
ufw enable

# 验证
ufw status
```

### 步骤3：修改Docker Compose端口映射

编辑 `/root/.openclaw/workspace/dsp-platform/docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    image: dsp-platform-backend:latest
    container_name: dsp-backend
    restart: unless-stopped
    ports:
      - "0.0.0.0:8000:8000"  # 绑定到所有网卡
    environment:
      - DATABASE_HOST=mysql
      - DATABASE_PORT=3306
      - DATABASE_USER=root
      - DATABASE_PASSWORD=DspSecurePassword2026
      - DATABASE_NAME=dsp_platform
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=RedisSecurePassword2026
    networks:
      - dsp-network
    depends_on:
      - mysql
      - redis
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/api/v1/system/health', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3

  mysql:
    image: mysql:8.0
    container_name: dsp-mysql
    restart: unless-stopped
    ports:
      - "0.0.0.0:3308:3306"
    environment:
      MYSQL_ROOT_PASSWORD: DspSecurePassword2026
      MYSQL_DATABASE: dsp_platform
    volumes:
      - dsp-mysql-data:/var/lib/mysql
    networks:
      - dsp-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.0-alpine
    container_name: dsp-redis
    restart: unless-stopped
    ports:
      - "0.0.0.0:6381:6379"
    volumes:
      - dsp-redis-data:/data
    networks:
      - dsp-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:1.25-alpine
    container_name: dsp-nginx
    restart: unless-stopped
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - dsp-network
    depends_on:
      - backend

  prometheus:
    image: prom/prometheus:latest
    container_name: dsp-prometheus
    restart: unless-stopped
    ports:
      - "0.0.0.0:9090:9090"
    volumes:
      - ./infrastructure/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - dsp-prometheus-data:/prometheus
    networks:
      - dsp-network

  grafana:
    image: grafana/grafana:latest
    container_name: dsp-grafana
    restart: unless-stopped
    ports:
      - "0.0.0.0:3002:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - dsp-grafana-data:/var/lib/grafana
    networks:
      - dsp-network

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: dsp-celery-worker
    restart: unless-stopped
    command: celery -A app.tasks.celery_app worker --loglevel=info
    environment:
      - DATABASE_HOST=mysql
      - DATABASE_PORT=3306
      - DATABASE_USER=root
      - DATABASE_PASSWORD=DspSecurePassword2026
      - DATABASE_NAME=dsp_platform
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=RedisSecurePassword2026
    networks:
      - dsp-network
    depends_on:
      - mysql
      - redis

  celery-beat:
    build:
      context: ./backend
      docker_name: dsp-celery-beat
      restart: unless-stopped
      command: celery -A app.tasks.celery_app beat --loglevel=info
      environment:
      - DATABASE_HOST=mysql
      - DATABASE_PORT=3306
      - DATABASE_USER=root
      - DATABASE_PASSWORD=DspSecurePassword2026
      - DATABASE_NAME=dsp_platform
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=RedisSecurePassword2026
    networks:
      - dsp-network
    depends_on:
      - mysql
      - redis

  flower:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: dsp-flower
    restart: unless-stopped
    command: celery -A app.tasks.celery_app flower --port=5555
    ports:
      - "0.0.0.0:5555:5555"
    environment:
      - DATABASE_HOST=mysql
      - DATABASE_PORT=3306
      - DATABASE_USER=root
      - DATABASE_PASSWORD=DspSecurePassword2026
      - DATABASE_NAME=dsp_platform
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=RedisSecurePassword2026
    networks:
      - dsp-network
    depends_on:
      - mysql
      - redis

networks:
  dsp-network:
    driver: bridge

volumes:
  dsp-mysql-data:
  dsp-redis-data:
  dsp-prometheus-data:
  dsp-grafana-data:
```

**关键修改**：
- 将所有端口映射从 `127.0.0.1:PORT:PORT` 改为 `0.0.0.0:PORT:PORT`
- 绑定到所有网卡，允许外网访问

### 步骤4：重启Docker服务

```bash
cd /root/.openclaw/workspace/dsp-platform

# 停止所有服务
docker-compose down

# 重新启动
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志（如果有问题）
docker-compose logs -f backend
```

### 步骤5：验证端口监听

```bash
# 检查端口是否在监听
netstat -tlnp | grep docker

# 或使用ss命令
ss -tlnp | grep docker

# 应该看到类似输出：
# tcp  0  0 0.0.0.0:8000    0.0.0.0:*    LISTEN  12345/docker-proxy
# tcp  0  0 0.0.0.0:9090    0.0.0.0:*    LISTEN  12346/docker-proxy
# tcp  0  0 0.0.0.0.0:3002   0.0.0.0:*    LISTEN  12347/docker-proxy
```

### 步骤6：外网访问测试

```bash
# 在本地机器上测试（替换为你的公网IP）
curl http://1.2.3.4:8000/api/v1/system/health

# 或在浏览器中访问
# http://1.2.3.4:8000/api/v1/system/health
# http://1.2.3.4:9090  (Prometheus)
# http://1.2.3.4:3002  (Grafana)
```

---

## 访问地址汇总

假设公网IP：`1.2.3.4`

| 服务 | 公网访问地址 | 说明 |
|------|--------------|------|
| **FastAPI后端** | http://1.2.3.4:8000 | API服务 |
| **Nginx反向代理** | http://1.2.3.4 | HTTP访问 |
| **Nginx HTTPS** | https://1.2.3.4 | HTTPS访问（需SSL证书） |
| **Prometheus** | http://1.2.3.4:9090 | 监控指标 |
| **Grafana** | http://1.2.3.4:3002 | 可视化面板 |
| **MySQL** | 1.2.3.4:3308 | 数据库（不推荐外网） |
| **Redis** | 1.2.3.4:6381 | 缓存（不推荐外网） |
| **Flower** | http://1.2.3.4:5555 | Celery监控 |
| **健康检查** | http://1.2.3.4:8000/api/v1/system/health | 服务状态 |

---

## 云服务器安全组配置

如果你使用的是云服务器（阿里云/腾讯云/AWS），需要在控制台配置安全组规则：

### 阿里云
```
入方向规则：
- 授权策略：允许
- 协议类型：TCP
- 端口范围：80/80, 443/443, 8000/8000, 9090/9090, 3002/3002, 5555/5555
- 授权对象：0.0.0.0/0（或指定IP段）

出方向规则：
- 授权策略：允许
- 协议类型：TCP
- 端口范围：1/65535
- 授权对象：0.0.0.0/0
```

### 腾讯云
```
入站规则：
- 类型：自定义
- 来源：0.0.0.0/0
- 协议端口：TCP:80, TCP:443, TCP:8000, TCP:9090, TCP:3002, TCP:5555
- 策略：允许

出站规则：
- 类型：自定义
- 目标：0.0.0.0/0
- 协议端口：TCP:1-65535
- 策略：允许
```

### AWS EC2
```
Inbound Rules：
- Type: Custom TCP
- Protocol: TCP
- Port: 80, 443, 8000, 9090, 3002, 5555
- Source: 0.0.0.0/0

Outbound Rules：
- Type: All traffic
- Protocol: All
- Port: All
- Destination: 0.0.0.0/0
```

---

## 安全加固

### 1. 限制访问IP（推荐）

修改 `/root/.openclaw/workspace/dsp-platform/docker-compose.yml`，使用防火墙限制：

```bash
# 只允许特定IP访问敏感服务
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="1.2.3.4" port protocol="tcp" port="9090" accept'
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="1.2.3.4" port protocol="tcp" port="3002" accept'
firewall-cmd --reload
```

### 2. 修改默认端口

使用非标准端口增加安全性：

```yaml
# 修改docker-compose.yml
backend:
  ports:
    - "0.0.0.0:18000:8000"  # 使用18000而不是8000

prometheus:
  ports:
    - "0.0.0.0:19090:9090"  # 使用19090而不是9090

grafana:
  ports:
    - "0.0.0.0:13002:3000"  # 使用13002而不是3000
```

### 3. 配置访问认证

#### Prometheus认证

编辑 `infrastructure/prometheus/prometheus.yml`：

```yaml
# 启用基本认证
basic_auth_users:
  admin: $2b$12$8XW2J4Y8Y8Y8Y8Y8Y8Y8Ye  # bcrypt加密的密码
```

#### Grafana认证

默认已启用，用户：`admin`，密码：`admin`（首次登录后需修改）

### 4. 使用fail2ban防止暴力破解

```bash
# 安装fail2ban
yum install fail2ban -y  # CentOS/RHEL
# 或
apt install fail2ban -y  # Ubuntu/Debian

# 创建配置
cat > /etc/fail2ban/jail.local << 'EOF'
[dsp-platform]
enabled = true
port = 8000,9090,3002
logpath = /var/log/nginx/access.log
maxretry = 5
bantime = 3600
findtime = 600
EOF

# 启动fail2ban
systemctl start fail2ban
systemctl enable fail2ban
```

### 5. 关闭不必要的外网端口

MySQL和Redis不应暴露到外网：

```yaml
# 修改docker-compose.yml，移除端口映射
mysql:
  ports: []  # 移除端口映射

redis:
  ports: []  # 移除端口映射
```

---

## 自签名SSL证书（可选）

虽然不使用域名，但也可以配置HTTPS（浏览器会警告）

### 生成自签名证书

```bash
# 创建证书目录
mkdir -p /root/.openclaw/workspace/dsp-platform/infrastructure/nginx/ssl

# 生成自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /root/.openclaw/workspace/dsp-platform/infrastructure/nginx/ssl/server.key \
  -out /root/.openclaw/workspace/dsp-platform/infrastructure/nginx/ssl/server.crt \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=DSPPlatform/CN=1.2.3.4"
```

### 配置Nginx使用SSL

编辑 `infrastructure/nginx/nginx.conf`：

```nginx
server {
    listen 80;
    server_name _;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

upstream backend {
    server backend:8000;
}
```

### 重启Nginx

```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose restart nginx
```

访问地址：`https://1.2.3.4`

---

## 监控外网访问

### 1. 查看访问日志

```bash
# Nginx访问日志
docker-compose logs -f nginx

# 应用日志
docker-compose logs -f backend
```

### 2. 统计访问量

```bash
# 统计独立IP访问
docker-compose logs nginx | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort | uniq | wc -l

# 统计访问最频繁的IP
docker-compose logs nginx | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort | uniq -c | sort -nr | head -10
```

---

## 故障排查

### 1. 无法从外网访问

```bash
# 检查服务是否运行
docker-compose ps

# 检查端口是否监听
netstat -tlnp | grep 8000

# 检查防火墙
firewall-cmd --list-all

# 检查云服务器安全组（在云控制台）

# 测试本地访问
curl http://localhost:8000/api/v1/system/health

# 测试内网访问
curl http://内网IP:8000/api/v1/system/health

# 检查路由
ip route show

# 检查iptables规则
iptables -L -n -v
```

### 2. 云服务器安全组未配置

- 登录云服务器控制台
- 找到安全组设置
- 添加入站规则（允许端口8000、9090、3002）
- 保存并等待生效（通常1-5分钟）

### 3. 防火墙阻止

```bash
# 临时关闭防火墙测试
systemctl stop firewalld  # CentOS/RHEL
# 或
ufw disable  # Ubuntu/Debian

# 如果可以访问，说明是防火墙问题，重新配置规则后重启
systemctl start firewalld
# 或
ufw enable
```

---

## 维护清单

### 每日
- [ ] 检查服务运行状态
- [ ] 查看访问日志（异常IP）
- [ ] 监控资源使用

### 每周
- [ ] 分析访问统计
- [ ] 检查安全日志
- [ ] 更新系统补丁

### 每月
- [ ] 审查访问权限
- [ ] 备份数据库
- [ ] 更新SSL证书（如使用）

---

## 快速命令参考

```bash
# 查看所有服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service-name]

# 重启服务
docker-compose restart [service-name]

# 停止所有服务
docker-compose down

# 启动所有服务
docker-compose up -d

# 查看端口占用
netstat -tlnp | grep [port]

# 检查防火墙
firewall-cmd --list-all
ufw status

# 测试健康检查
curl http://localhost:8000/api/v1/system/health
curl http://公网IP:8000/api/v1/system/health

# 查看Docker日志
docker logs dsp-backend
docker logs dsp-prometheus
docker logs dsp-grafana
```

---

## 注意事项

⚠️ **安全警告**：
1. 生产环境建议使用域名+SSL证书
2. 不要将MySQL和Redis暴露到外网
3. 限制Prometheus和Grafana的访问IP
4. 修改默认密码（Grafana等）
5. 定期更新系统安全补丁
6. 配置fail2ban防止暴力破解
7. 启用访问日志监控

📊 **性能考虑**：
1. 大量并发时考虑负载均衡
2. 使用CDN加速静态资源
3. 配置缓存减少数据库压力
4. 监控网络带宽使用

🔧 **运维建议**：
1. 建立监控告警机制
2. 定期备份数据库和配置
3. 制定应急响应计划
4. 文档化运维流程

---

**配置完成时间**: 2026-03-15
**下次更新**: 根据实际使用情况调整

**快速测试命令**：
```bash
curl http://YOUR_PUBLIC_IP:8000/api/v1/system/health
```

替换 `YOUR_PUBLIC_IP` 为你的实际公网IP即可测试访问！
