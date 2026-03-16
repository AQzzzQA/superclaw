# OpenClaw 权限管理系统 - 部署与使用说明

## 📋 目录

1. [系统概述](#系统概述)
2. [快速部署](#快速部署)
3. [常见问题修复](#常见问题修复)
4. [验证清单](#验证清单)
5. [技术支持](#技术支持)

---

## 系统概述

OpenClaw权限管理系统是一个完整的RBAC权限管理解决方案，已修复所有已知问题，可直接部署使用。

### ✅ 已解决的问题

| 问题 | 状态 | 说明 |
|------|------|------|
| 页面空白 | ✅ 已修复 | 前端使用生产构建，正常显示 |
| 菜单报错 | ✅ 已修复 | 数据库连接和API响应正常 |
| 容器启动失败 | ✅ 已修复 | 健康检查和依赖配置正确 |

---

## 快速部署

### 方法1: 一键部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/AQzzzQA/permissions-system.git
cd permissions-system

# 2. 配置环境
cp .env.example .env
nano .env
```

**必须修改的配置**:
```env
# 数据库密码（设置强密码）
DB_PASSWORD=YourStrongPassword123!

# JWT密钥（必须修改！）
JWT_SECRET=your_very_long_random_secret_key_2024

# 超级管理员
SUPERADMIN_EMAIL=admin@yourcompany.com
SUPERADMIN_PASSWORD=AdminStrongPassword123!
```

```bash
# 3. 启动服务
docker-compose up -d

# 4. 查看日志（可选）
docker-compose logs -f
```

**访问地址**:
- 前端: http://localhost:3000
- 后端: http://localhost:8001/health

---

## 常见问题修复

### 问题1: 访问 http://localhost:3000 页面空白

**原因**: 前端容器未启动或配置错误

**解决方案**:

```bash
# 检查容器状态
docker-compose ps

# 如果前端容器未运行，重启
docker-compose restart frontend

# 查看日志
docker-compose logs frontend
```

**验证**:
```bash
curl -s http://localhost:3000 | head -5
# 应该返回HTML内容
```

---

### 问题2: 登录后菜单点击报错

**原因**: 数据库连接或API响应问题

**解决方案**:

```bash
# 1. 检查后端日志
docker-compose logs backend

# 2. 验证数据库连接
docker exec -it permissions_db psql -U postgres -c "SELECT version();"

# 3. 检查环境变量
cat .env | grep DB_HOST
# 应该是: DB_HOST=db（不是localhost）

# 4. 如果配置错误，修改后重启
nano .env
docker-compose restart backend
```

**验证**:
```bash
curl -s http://localhost:8001/health
# 应该返回: {"status":"ok"}
```

---

### 问题3: Docker容器启动失败

**原因**: 依赖关系或健康检查问题

**解决方案**:

```bash
# 1. 查看容器状态
docker-compose ps

# 2. 查看错误日志
docker-compose logs

# 3. 清理并重新构建
docker-compose down -v
docker system prune -f
docker-compose up --build -d

# 4. 等待40秒让服务完全启动
sleep 40

# 5. 验证状态
docker-compose ps
```

**预期结果**:
```
NAME                      STATUS
permissions_db            Up (healthy)
permissions_redis         Up (healthy)
permissions_backend       Up (healthy)
permissions_frontend      Up (healthy)
```

---

## 验证清单

部署完成后，请按以下顺序验证：

### ✅ 1. 容器状态
```bash
docker-compose ps
```
**预期**: 所有服务状态为 "Up"

### ✅ 2. 健康检查
```bash
docker inspect permissions_backend --format='{{.State.Health.Status}}'
```
**预期**: 返回 "healthy"

### ✅ 3. 前端访问
```bash
curl -s http://localhost:3000 | head -5
```
**预期**: 返回HTML内容

### ✅ 4. 后端API
```bash
curl -s http://localhost:8001/health
```
**预期**: 返回 `{"status":"ok"}`

### ✅ 5. 登录功能
- 访问 http://localhost:3000
- 使用超级管理员账号登录
**预期**: 登录成功

### ✅ 6. 菜单功能
- 点击左侧菜单
**预期**: 页面正常跳转，无报错

---

## 技术支持

### 获取帮助

1. **查看详细文档**
   - 客户使用指南: `PERMISSIONS-SYSTEM-CUSTOMER-GUIDE.md`
   - 问题修复说明: `PERMISSIONS-SYSTEM-FIX-EXPLAINED.md`
   - 完整测试报告: `PERMISSIONS-SYSTEM-TEST-REPORT.md`

2. **收集问题信息**
   ```bash
   docker-compose logs > debug-logs.txt
   docker-compose ps > container-status.txt
   cat .env > env-config.txt
   ```

3. **提交问题**
   - GitHub Issues: https://github.com/AQzzzQA/permissions-system/issues

---

## ⚠️ 重要提示

### 部署前必读

1. **必须修改默认密码**
   - 数据库密码
   - JWT密钥
   - 超级管理员密码

2. **数据库配置**
   - `DB_HOST` 必须设置为 `db`（容器名）
   - 不要使用 `localhost`

3. **CORS配置**
   - `CORS_ORIGIN` 必须匹配前端访问地址

### 部署后检查

1. ✅ 所有容器状态为 "Up"
2. ✅ 健康检查通过
3. ✅ 前端可访问
4. ✅ 后端API响应正常
5. ✅ 登录功能正常
6. ✅ 菜单功能正常

---

**系统状态**: ✅ 所有问题已解决，可投入使用
**文档版本**: v1.0
**更新日期**: 2026-03-16
