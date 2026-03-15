# DSP Platform 外网访问运维配置指南

**部署时间**: 2026-03-15
**适用场景**: 生产环境外网访问

---

## 前置要求

### 1. 服务器要求
- [ ] 公网IP服务器（推荐配置：4C8G，SSD 50GB）
- [ ] 域名已备案（如：dsp.yourdomain.com）
- [ ] SSL证书（推荐 Let's Encrypt 免费）

### 2. 网络配置
- [ ] 防火墙开放端口：80, 443, 22
- [ ] 安全组规则配置（云服务器）
- [ ] DNS解析指向服务器IP

---

## 快速配置（5分钟）

### 步骤1：配置域名DNS解析

到域名DNS管理平台添加A记录：

```
主机记录: dsp
记录类型: A
记录值: 你的服务器公网IP
TTL: 600
```

等待DNS生效（5-10分钟）

### 步骤2：安装Nginx（服务器级）

```bash
# 安装Nginx
yum install nginx -y  # CentOS/RHEL
# 或
apt install nginx -y   # Ubuntu/Debian

# 启动Nginx
systemctl start nginx
systemctl enable nginx
```

### 步骤3：申请SSL证书

```bash
# 安装certbot
yum install certbot python3-certbot-nginx -y  # CentOS/RHEL
# 或
apt install certbot python3-certbot-nginx -y   # Ubuntu/Debian

# 申请证书（自动配置Nginx）
certbot --nginx -d dsp.yourdomain.com

# 按提示操作，证书将自动安装到 /etc/letsencrypt/live/dsp.yourdomain.com/
```

### 步骤4：配置反向代理

创建Nginx配置文件 `/etc/nginx/conf.d/dsp-platform.conf`：

```nginx
upstream dsp_backend {
    server localhost:8080;
    keepalive 32;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name dsp.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name dsp.yourdomain.com;

    # SSL证书
    ssl_certificate /etc/letsencrypt/live/dsp.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dsp.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 安全头部
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 客户端配置
    client_max_body_size 50M;
    client_body_timeout 60s;
    client_header_timeout 60s;

    # API代理
    location /api/ {
        proxy_pass http://dsp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # WebSocket支持
    location /ws/ {
        proxy_pass http://dsp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }

    # 监控服务（需要密码保护）
    location /prometheus/ {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://localhost:9090/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /grafana/ {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://localhost:3002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Grafana需要特殊配置
        proxy_set_header X-WEBAUTH-USER $remote_user;
        rewrite ^/grafana/(.*) /$1 break;
    }

    # 健康检查
    location /health {
        proxy_pass http://dsp_backend;
        access_log off;
    }
}
```

### 步骤5：创建认证文件

```bash
# 安装htpasswd工具
yum install httpd-tools -y  # CentOS/RHEL
# 或
apt install apache2-utils -y # Ubuntu/Debian

# 创建管理员密码（替换your_password）
htpasswd -c /etc/nginx/.htpasswd admin

# 重启Nginx
systemctl restart nginx
```

### 步骤6：更新Docker Compose配置

编辑 `/root/.openclaw/workspace/dsp-platform/docker-compose.yml`，修改Nginx端口：

```yaml
  nginx:
    image: nginx:1.25-alpine
    container_name: dsp-nginx
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:80"  # 只监听本地，通过服务器Nginx代理
      - "127.0.0.1:8443:443"  # 内部SSL（可选）
    networks:
      - dsp-network
```

重启Docker服务：

```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose restart nginx
```

### 步骤7：配置防火墙

```bash
# firewalld (CentOS/RHEL)
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload

# ufw (Ubuntu/Debian)
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

### 步骤8：设置证书自动续期

```bash
# 添加自动续期任务
crontab -e

# 添加以下行（每天凌晨2点检查续期）
0 2 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

---

## 访问地址配置完成

### 公网访问地址

| 服务 | 公网地址 | 认证 |
|------|----------|------|
| **API** | https://dsp.yourdomain.com/api/v1/ | - |
| **前端** | https://dsp.yourdomain.com | - |
| **Prometheus** | https://dsp.yourdomain.com/prometheus/ | admin/密码 |
| **Grafana** | https://dsp.yourdomain.com/grafana/ | admin/密码 |

### 内部访问地址（仅限服务器）

| 服务 | 地址 |
|------|------|
| Docker Nginx | http://localhost:8080 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3002 |

---

## 安全加固

### 1. 限制访问IP（可选）

如果只允许特定IP访问Prometheus/Grafana：

```nginx
location /prometheus/ {
    # 只允许特定IP访问
    allow 1.2.3.4;    # 替换为你的IP
    allow 192.168.1.0/24;
    deny all;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;

    proxy_pass http://localhost:9090/;
    # ... 其他配置
}
```

### 2. 限流保护

在 `http {}` 块中添加：

```nginx
http {
    # 限流配置
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=1000r/s;

    # 在 server 块中应用
    server {
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            # ...
        }

        location / {
            limit_req zone=general_limit burst=50 nodelay;
            # ...
        }
    }
}
```

### 3. 禁用目录列表

在 `http {}` 或 `server {}` 块中：

```nginx
server {
    autoindex off;
    # ...
}
```

### 4. 配置fail2ban（防止暴力破解）

```bash
# 安装fail2ban
yum install fail2ban -y  # CentOS/RHEL
# 或
apt install fail2ban -y  # Ubuntu/Debian

# 创建Nginx防护规则
cat > /etc/fail2ban/jail.local << 'EOF'
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 3600

[nginx-noscript]
enabled = true
filter = nginx-noscript
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6
bantime = 86400
EOF

systemctl start fail2ban
systemctl enable fail2ban
```

---

## 性能优化

### 1. 启用Gzip压缩

在 `http {}` 块中：

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript
           application/json application/javascript application/xml+rss
           application/rss+xml font/truetype font/opentype
           application/vnd.ms-fontobject image/svg+xml;
```

### 2. 配置缓存

```nginx
# 静态资源缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 3. 启用HTTP/2

Nginx配置中已启用：
```nginx
listen 443 ssl http2;
```

---

## 监控和日志

### 1. Nginx访问日志

```bash
# 查看实时日志
tail -f /var/log/nginx/access.log

# 统计访问量
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head

# 查看错误日志
tail -f /var/log/nginx/error.log
```

### 2. 监控SSL证书过期

```bash
# 检查证书过期时间
certbot certificates

# 添加监控脚本
cat > /usr/local/bin/check-cert-expiry.sh << 'EOF'
#!/bin/bash
EXPIRY=$(openssl x509 -enddate -noout -in /etc/letsencrypt/live/dsp.yourdomain.com/cert.pem | cut -d= -f2)
DAYS=$(( ($(date -d "$EXPIRY" +%s) - $(date +%s)) / 86400 ))
if [ $DAYS -lt 7 ]; then
    echo "警告：SSL证书将在 $DAYS 天后过期"
fi
EOF

chmod +x /usr/local/bin/check-cert-expiry.sh

# 添加到crontab（每天检查一次）
0 8 * * * /usr/local/bin/check-cert-expiry.sh
```

---

## 故障排查

### 1. 无法访问

```bash
# 检查Nginx状态
systemctl status nginx

# 检查配置
nginx -t

# 查看日志
tail -f /var/log/nginx/error.log

# 检查防火墙
firewall-cmd --list-all  # CentOS/RHEL
ufw status              # Ubuntu/Debian

# 检查端口监听
netstat -tlnp | grep nginx
```

### 2. SSL证书问题

```bash
# 手动续期
certbot renew --force-renewal

# 重新安装证书
certbot --nginx -d dsp.yourdomain.com --force-renewal
```

### 3. DNS解析问题

```bash
# 检查DNS解析
dig dsp.yourdomain.com
nslookup dsp.yourdomain.com

# 检查本地DNS缓存（清除缓存）
# Windows: ipconfig /flushdns
# Linux: sudo systemctl restart systemd-resolved
```

---

## 备份和恢复

### 1. 备份Nginx配置

```bash
# 创建备份脚本
cat > /usr/local/bin/backup-nginx.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/nginx"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp -r /etc/nginx $BACKUP_DIR/nginx_$DATE
tar -czf $BACKUP_DIR/nginx_$DATE.tar.gz $BACKUP_DIR/nginx_$DATE
rm -rf $BACKUP_DIR/nginx_$DATE

# 保留最近7天的备份
find $BACKUP_DIR -name "nginx_*.tar.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-nginx.sh

# 添加到crontab（每天凌晨3点备份）
0 3 * * * /usr/local/bin/backup-nginx.sh
```

### 2. 恢复配置

```bash
# 解压备份
tar -xzf /backups/nginx/nginx_20260315_030000.tar.gz -C /tmp

# 恢复配置
cp -r /tmp/nginx_20260315_030000/* /etc/nginx/

# 重启Nginx
systemctl restart nginx
```

---

## 维护清单

### 每日
- [ ] 检查Nginx日志（错误日志）
- [ ] 监控服务器资源使用
- [ ] 检查SSL证书状态

### 每周
- [ ] 分析访问日志
- [ ] 检查安全日志（fail2ban）
- [ ] 查看备份完整性

### 每月
- [ ] 更新系统安全补丁
- [ ] 审查访问权限
- [ ] 测试灾难恢复流程

---

## 紧急联系方式

- 服务器IP：_________
- 域名：_________
- SSL证书路径：/etc/letsencrypt/live/dsp.yourdomain.com/
- Nginx配置路径：/etc/nginx/conf.d/dsp-platform.conf
- 管理员密码文件：/etc/nginx/.htpasswd

---

**配置完成后，访问地址**：
- 🌐 生产环境：https://dsp.yourdomain.com
- 📊 监控面板：https://dsp.yourdomain.com/grafana/（需登录）
- 📈 指标监控：https://dsp.yourdomain.com/prometheus/（需登录）

**配置时间**: 2026-03-15
**下次更新**: 根据实际使用情况调整
