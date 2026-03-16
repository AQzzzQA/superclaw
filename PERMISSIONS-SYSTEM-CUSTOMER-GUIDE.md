# OpenClaw 权限管理系统 - 客户使用指南

**版本**: 1.0.0
**更新日期**: 2026-03-16
**文档版本**: v1.2

---

## 📋 系统概述

OpenClaw权限管理系统是一个基于RBAC（基于角色的访问控制）的权限管理解决方案，提供用户管理、角色管理、权限管理和菜单管理功能。

### 技术栈
- **后端**: Node.js + Express + MySQL
- **前端**: React + Vite + Ant Design
- **部署**: Docker + Docker Compose

---

## 🚀 快速开始

### 前置要求
- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ 可用内存
- 10GB+ 可用磁盘空间

### 一键部署（推荐）

#### 步骤1: 克隆项目
```bash
git clone https://github.com/AQzzzQA/permissions-system.git
cd permissions-system
```

#### 步骤2: 复制环境配置
```bash
cp .env.example .env
```

#### 步骤3: 修改环境变量（重要！）
```bash
# 编辑 .env 文件
nano .env
```

**必须修改的配置**:
```env
# 数据库配置
DB_HOST=db  # 容器内网络地址，不要修改为localhost
DB_PORT=3306
DB_USER=your_db_user  # 修改为你的数据库用户名
DB_PASSWORD=your_strong_password  # 修改为强密码
DB_NAME=openclaw_permissions

# JWT密钥（必须修改！）
JWT_SECRET=your_very_long_random_secret_key_change_this_in_production_2024
JWT_EXPIRES_IN=24h

# 超级管理员账号
SUPERADMIN_EMAIL=admin@yourcompany.com
SUPERADMIN_PASSWORD=YourStrongPassword123!  # 至少12位，包含大小写字母和数字

# CORS配置
CORS_ORIGIN=http://localhost:3000
```

#### 步骤4: 启动服务
```bash
# 构建并启动所有容器
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

**预期输出**:
```
[+] Running 4/4
 ✔ Volume "permissions_postgres_data"  Created
 ✔ Container permissions_db             Started
 ✔ Container permissions_redis           Started
 ✔ Container permissions_backend         Started
 ✔ Container permissions_frontend       Started
```

#### 步骤5: 验证服务

**检查容器状态**:
```bash
docker-compose ps
```

**应该看到所有服务状态为 "Up"**:
```
NAME                      STATUS
permissions_db            Up
permissions_redis         Up
permissions_backend       Up
permissions_frontend      Up
```

**访问服务**:
- **前端**: http://localhost:3000
- **后端API文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health

---

## ⚠️ 常见问题与解决方案

### 问题1: 访问 http://localhost:3000 页面空白

**原因分析**:
1. 前端容器未启动
2. Vite开发服务器未绑定0.0.0.0
3. 静态资源加载失败

**解决方案**:

#### 检查容器状态
```bash
docker ps | grep permissions
```

**如果容器未运行**:
```bash
# 查看日志
docker-compose logs frontend

# 重启前端
docker-compose restart frontend
```

**如果容器正在运行但页面空白**:
```bash
# 进入前端容器
docker exec -it permissions_frontend sh

# 检查端口绑定
netstat -tuln | grep 3000

# 查看静态文件
ls -la /app/dist

# 退出容器
exit
```

#### 使用生产构建（推荐）
修改 `docker-compose.yml`:
```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:80"  # Nginx端口
  command: npm run build && nginx -g 'daemon off;'
```

重新启动:
```bash
docker-compose down
docker-compose up --build -d
```

---

### 问题2: 登录后菜单点击报错

**原因分析**:
1. 后端API未正确响应
2. CORS跨域问题
3. JWT Token验证失败
4. 数据库连接失败

**解决方案**:

#### 检查后端日志
```bash
docker-compose logs backend --tail 50
```

**查看是否有错误**:
```
Error: connect ECONNREFUSED 127.0.0.1:3306
```

**如果看到数据库连接错误**:
1. 检查 `.env` 文件中的数据库配置
2. 确保 `DB_HOST=db`（不是localhost）
3. 确保数据库容器正在运行

#### 检查前端日志（浏览器控制台）
1. 打开浏览器，按F12打开开发者工具
2. 切换到"Console"标签
3. 查看是否有红色错误信息

**常见错误**:
```
Access to XMLHttpRequest at 'http://localhost:8001/api/users' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**CORS解决方案**:
检查 `.env` 文件:
```env
CORS_ORIGIN=http://localhost:3000
```

重启后端:
```bash
docker-compose restart backend
```

#### 检查JWT Token
在浏览器控制台执行:
```javascript
// 查看本地存储的token
localStorage.getItem('token')

// 如果token存在但无效，清除后重新登录
localStorage.clear()
location.reload()
```

---

### 问题3: Docker镜像拉取失败或容器启动失败

**原因分析**:
1. 网络问题，无法拉取镜像
2. Docker Hub被墙
3. 构建过程中依赖安装失败

**解决方案**:

#### 使用国内镜像源
修改 `/etc/docker/daemon.json`:
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
```

重启Docker:
```bash
sudo systemctl restart docker
```

#### 手动拉取镜像
```bash
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull node:18-alpine
```

#### 清理并重新构建
```bash
# 停止并删除所有容器
docker-compose down -v

# 清理Docker缓存
docker system prune -f --volumes

# 重新构建（不使用缓存）
docker-compose build --no-cache

# 启动服务
docker-compose up -d
```

---

### 问题4: 数据库初始化失败

**症状**:
```
Error: Database 'openclaw_permissions' doesn't exist
```

**解决方案**:

#### 手动初始化数据库
```bash
# 进入数据库容器
docker exec -it permissions_db psql -U postgres

# 创建数据库
CREATE DATABASE openclaw_permissions;

# 创建超级用户
CREATE USER your_db_user WITH PASSWORD 'your_strong_password';

# 授权
GRANT ALL PRIVILEGES ON DATABASE openclaw_permissions TO your_db_user;

# 退出
\q
```

#### 运行数据库迁移
```bash
# 进入后端容器
docker exec -it permissions_backend sh

# 运行迁移
npm run migrate

# 退出
exit
```

---

### 问题5: 容器启动后立即退出

**症状**:
```bash
docker-compose ps
# 状态显示为 "Exit 1" 或 "Restarting"
```

**解决方案**:

#### 查看容器日志
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

#### 常见错误及修复

**错误1: 端口冲突**
```
Error: bind: address already in use
```
**解决**: 修改 `docker-compose.yml` 中的端口映射

**错误2: 内存不足**
```
Error: JavaScript heap out of memory
```
**解决**: 增加Node.js内存限制
```yaml
environment:
  - NODE_OPTIONS=--max_old_space_size=4096
```

**错误3: 权限问题**
```
Error: EACCES: permission denied
```
**解决**: 修改文件权限
```bash
chmod -R 755 backend/
chmod -R 755 frontend/
```

---

## 🔧 完整的Docker Compose配置

```yaml
version: '3.8'

services:
  # PostgreSQL数据库
  db:
    image: postgres:15-alpine
    container_name: permissions_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-openclaw_permissions}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - permissions_network

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: permissions_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - permissions_network

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: permissions_backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      NODE_ENV: production
      PORT: 8001
      DB_HOST: db  # 重要：使用容器名，不是localhost
      DB_PORT: 5432
      DB_USER: ${DB_USER:-postgres}
      DB_PASSWORD: ${DB_PASSWORD:-postgres}
      DB_NAME: ${DB_NAME:-openclaw_permissions}
      REDIS_HOST: redis
      REDIS_PORT: 6379
      JWT_SECRET: ${JWT_SECRET:-change_this_secret}
      JWT_EXPIRES_IN: ${JWT_EXPIRES_IN:-24h}
      CORS_ORIGIN: ${CORS_ORIGIN:-http://localhost:3000}
      SUPERADMIN_EMAIL: ${SUPERADMIN_EMAIL:-admin@example.com}
      SUPERADMIN_PASSWORD: ${SUPERADMIN_PASSWORD:-Admin123!}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - /app/node_modules
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - permissions_network

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - VITE_API_BASE_URL=/admin/api
    container_name: permissions_frontend
    restart: unless-stopped
    ports:
      - "3000:80"
    environment:
      - VITE_API_BASE_URL=/admin/api
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - permissions_network

volumes:
  postgres_data:

networks:
  permissions_network:
    driver: bridge
```

---

## 📝 验证检查清单

部署完成后，请按以下顺序验证：

### 1. 容器状态检查
```bash
docker-compose ps
```
✅ 所有服务状态为 "Up"

### 2. 健康检查
```bash
docker inspect permissions_backend --format='{{.State.Health.Status}}'
docker inspect permissions_frontend --format='{{.State.Health.Status}}'
```
✅ 状态为 "healthy"

### 3. 前端访问
```bash
curl -s http://localhost:3000 | head -10
```
✅ 返回HTML内容

### 4. 后端API
```bash
curl -s http://localhost:8001/health
```
✅ 返回: `{"status":"ok"}`

### 5. 数据库连接
```bash
docker exec -it permissions_db psql -U ${DB_USER} -c "SELECT version();"
```
✅ 返回PostgreSQL版本信息

### 6. 登录功能
- 访问 http://localhost:3000
- 使用超级管理员账号登录
- ✅ 登录成功，进入首页

### 7. 菜单功能
- 点击左侧菜单
- ✅ 页面正常跳转，无报错

---

## 🆘 获取帮助

如果遇到其他问题，请按以下步骤收集信息：

### 1. 收集日志
```bash
docker-compose logs > debug-logs.txt
```

### 2. 收集容器状态
```bash
docker-compose ps > container-status.txt
```

### 3. 收集环境配置
```bash
cat .env > env-config.txt
```

### 4. 浏览器错误截图
- 打开浏览器控制台（F12）
- 切换到"Console"和"Network"标签
- 截图保存

### 5. 提交问题
将以上信息发送给技术支持。

---

## 📞 技术支持

- **GitHub Issues**: https://github.com/AQzzzQA/permissions-system/issues
- **文档地址**: https://github.com/AQzzzQA/permissions-system/blob/main/README.md
- **测试报告**: https://github.com/AQzzzQA/permissions-system/blob/main/PERMISSIONS-SYSTEM-TEST-REPORT.md

---

## 🎯 最佳实践

### 1. 定期备份数据
```bash
# 备份数据库
docker exec permissions_db pg_dump -U ${DB_USER} ${DB_NAME} > backup-$(date +%Y%m%d).sql

# 恢复数据库
cat backup-20240316.sql | docker exec -i permissions_db psql -U ${DB_USER} ${DB_NAME}
```

### 2. 监控日志
```bash
# 实时查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 3. 定期更新镜像
```bash
# 拉取最新镜像
docker-compose pull

# 重新构建并启动
docker-compose up -d --build
```

### 4. 清理资源
```bash
# 清理未使用的镜像
docker image prune -f

# 清理未使用的容器
docker container prune -f

# 清理未使用的卷
docker volume prune -f
```

---

**文档版本**: v1.2
**最后更新**: 2026-03-16
**维护者**: Echo-2
