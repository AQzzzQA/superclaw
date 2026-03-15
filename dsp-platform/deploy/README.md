# DSP广告平台部署指南

## 目录结构

```
deploy/
├── docker-compose.yml          # Docker Compose编排文件
├── .env.example               # 环境变量示例
├── init-scripts/
│   └── init.sql              # MySQL初始化脚本
├── nginx/
│   ├── nginx.conf            # Nginx主配置
│   └── conf.d/
│       └── dsp-platform.conf # 虚拟主机配置
├── prometheus/
│   ├── prometheus.yml        # Prometheus配置
│   └── alerts.yml            # 告警规则
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml
│   │   └── dashboards/
│   │       └── dashboard.yml
│   └── dashboards/
│       └── dsp-platform-overview.json
├── alertmanager/
│   └── alertmanager.yml      # AlertManager配置
├── elasticsearch/
│   └── elasticsearch.yml     # Elasticsearch配置
├── logstash/
│   └── logstash.conf         # Logstash配置
├── kibana/
│   └── kibana.yml            # Kibana配置
├── certbot/
│   ├── conf/                 # SSL证书目录（自动生成）
│   └── www/                  # ACME挑战目录
└── .github/workflows/
    └── ci-cd.yml             # GitHub Actions CI/CD配置
```

## 快速开始

### 1. 环境准备

```bash
# 安装Docker和Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose插件
sudo apt-get install docker-compose-plugin
```

### 2. 配置环境变量

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑环境变量（根据实际情况修改）
vim .env
```

### 3. 生成SSL证书

```bash
# 首次获取SSL证书（需要域名指向服务器）
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot -d your-domain.com -d www.your-domain.com

# 测试证书续期
docker-compose run --rm certbot renew --dry-run
```

### 4. 创建htpasswd文件（用于监控服务认证）

```bash
# 安装htpasswd工具
sudo apt-get install apache2-utils

# 生成密码文件
htpasswd -c nginx/.htpasswd admin

# 添加更多用户（可选）
htpasswd nginx/.htpasswd user2
```

### 5. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止服务并删除数据卷（谨慎使用）
docker-compose down -v
```

## 服务访问

| 服务 | URL | 认证 |
|------|-----|------|
| 主应用 | https://your-domain.com | 无 |
| API | https://your-domain.com/api | 无 |
| Prometheus | https://prometheus.your-domain.com | htpasswd |
| Grafana | https://grafana.your-domain.com | admin/password |
| AlertManager | https://alertmanager.your-domain.com | htpasswd |
| Kibana | https://kibana.your-domain.com | htpasswd |

## 监控配置

### Prometheus告警规则

告警规则分为以下类别：

1. **基础设施告警** (`infrastructure_alerts`)
   - CPU使用率 > 80%
   - 内存使用率 > 85%
   - 磁盘使用率 > 85%

2. **应用告警** (`application_alerts`)
   - 服务宕机
   - HTTP错误率 > 5%
   - HTTP响应时间 P95 > 1s

3. **数据库告警** (`database_alerts`)
   - MySQL连接数 > 80%
   - MySQL慢查询 > 10/s
   - Redis内存使用率 > 80%

4. **容器告警** (`container_alerts`)
   - 容器CPU使用率 > 80%
   - 容器内存使用率 > 85%
   - 容器频繁重启（1小时内>5次）

5. **业务告警** (`business_alerts`)
   - 请求量异常下降
   - API错误率 > 1%
   - 广告投放失败率高
   - 预算消耗 > 80%
   - 结算失败

### Grafana仪表板

预配置的仪表板包括：

- **DSP Platform Overview**: 系统总览
  - CPU/内存/磁盘使用率
  - HTTP请求率和响应时间
  - 网络流量
  - 数据库状态

更多仪表板可以从Grafana官网导入。

### 告警通知

支持多种告警通知渠道：

1. **邮件通知**: 自动发送到配置的邮箱
2. **钉钉通知**: 通过Webhook发送
3. **企业微信通知**: 通过Webhook发送

配置方法：在 `.env` 文件中配置相应的参数。

## CI/CD流程

### GitHub Actions工作流

工作流包含以下阶段：

1. **代码质量检查** (`lint`)
   - Python: Black, isort, Flake8, mypy
   - JavaScript/TypeScript: ESLint, Prettier

2. **安全扫描** (`security`)
   - Trivy漏洞扫描
   - Snyk依赖扫描

3. **单元测试** (`test`)
   - 后端测试（pytest）
   - 前端测试（Jest）
   - 代码覆盖率报告

4. **构建镜像** (`build`)
   - 构建Docker镜像
   - 推送到GitHub Container Registry

5. **部署到Staging** (`deploy-staging`)
   - 触发条件: develop分支
   - 自动部署到测试环境
   - 烟雾测试
   - Slack通知

6. **部署到Production** (`deploy-production`)
   - 触发条件: main分支
   - 蓝绿部署
   - 数据库备份
   - 集成测试
   - 回滚机制

7. **性能测试** (`performance`)
   - k6负载测试
   - 性能基准对比

### 部署步骤

#### Staging环境部署

```bash
# 推送到develop分支
git checkout develop
git add .
git commit -m "feat: new feature"
git push origin develop

# GitHub Actions自动触发部署
```

#### Production环境部署

```bash
# 推送到main分支
git checkout main
git merge develop
git push origin main

# GitHub Actions自动触发部署
```

#### 手动部署

```bash
# 连接到服务器
ssh user@server

# 进入项目目录
cd /opt/dsp-platform

# 拉取最新代码
git pull origin main

# 更新环境变量
cp deploy/.env.production .env

# 拉取最新镜像
docker-compose -f deploy/docker-compose.yml pull

# 重启服务
docker-compose -f deploy/docker-compose.yml up -d

# 运行数据库迁移
docker-compose -f deploy/docker-compose.yml exec -T dsp-backend alembic upgrade head
```

## 日志管理

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f dsp-backend
docker-compose logs -f dsp-frontend
docker-compose logs -f dsp-nginx

# 查看最近100行日志
docker-compose logs --tail=100 dsp-backend
```

### Kibana日志分析

访问 Kibana (`https://kibana.your-domain.com`) 进行日志分析：

1. 创建索引模式: `dsp-logs-*`
2. 选择时间字段: `@timestamp`
3. 创建可视化图表和仪表板

## 备份和恢复

### 数据库备份

```bash
# 手动备份
docker-compose exec dsp-mysql mysqldump -u root -p dsp_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 自动备份（添加到crontab）
0 2 * * * cd /opt/dsp-platform && docker-compose exec -T dsp-mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} dsp_db > backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql
```

### 数据恢复

```bash
# 恢复数据库
docker-compose exec -T dsp-mysql mysql -u root -p dsp_db < backup_20260315_020000.sql
```

### 配置备份

```bash
# 备份配置文件
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz .env nginx/ prometheus/ grafana/ alertmanager/
```

## 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker-compose logs [service-name]

# 检查容器状态
docker-compose ps

# 检查资源使用情况
docker stats

# 重启特定服务
docker-compose restart [service-name]
```

### SSL证书问题

```bash
# 检查证书有效期
docker-compose run --rm certbot certificates

# 手动续期
docker-compose run --rm certbot renew

# 重新生成证书
docker-compose run --rm certbot certonly --force-renewal --webroot --webroot-path /var/www/certbot -d your-domain.com
```

### 性能问题

```bash
# 查看容器资源使用情况
docker stats

# 查看数据库连接数
docker-compose exec dsp-mysql mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected'"

# 查看Redis连接数
docker-compose exec dsp-redis redis-cli INFO clients

# 查看Nginx状态
curl http://localhost/nginx_status
```

### 告警过多

```bash
# 编辑告警规则
vim prometheus/alerts.yml

# 重新加载Prometheus配置
docker-compose restart dsp-prometheus

# 或使用API热重载
curl -X POST http://localhost:9090/-/reload
```

## 安全加固

### 1. 修改默认密码

```bash
# 修改所有默认密码
vim .env

# 重启相关服务
docker-compose up -d dsp-grafana dsp-mysql dsp-redis
```

### 2. 配置防火墙

```bash
# 仅开放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 3. 启用fail2ban

```bash
# 安装fail2ban
sudo apt-get install fail2ban

# 创建配置文件
sudo vim /etc/fail2ban/jail.local

# 添加SSH保护
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

# 重启fail2ban
sudo systemctl restart fail2ban
```

### 4. 定期更新

```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 更新Docker镜像
docker-compose pull
docker-compose up -d
```

## 监控和维护

### 健康检查

```bash
# 检查所有服务健康状态
docker-compose ps

# 手动健康检查
curl https://your-domain.com/health
curl https://your-domain.com/api/v1/health
```

### 资源监控

访问 Grafana 仪表板查看：

- CPU使用率
- 内存使用率
- 磁盘空间
- 网络流量
- 容器状态

### 性能优化

1. **数据库优化**
   - 定期清理慢查询日志
   - 优化索引
   - 调整缓存大小

2. **Redis优化**
   - 配置持久化
   - 调整最大内存限制
   - 使用集群模式（大规模）

3. **Nginx优化**
   - 启用缓存
   - 配置负载均衡
   - 优化keepalive

## 联系方式

如有问题，请联系运维团队或查看项目文档。
