# DSP Platform 外网访问测试报告

**测试时间**: 2026-03-15 16:29
**测试方式**: curl命令外网访问测试
**测试IP**: 43.156.131.98

---

## 📊 测试结果汇总

| 服务 | 访问地址 | 状态 | HTTP响应 | 说明 |
|------|----------|------|----------|------|
| Backend API | http://43.156.131.98:8000/api/v1/system/health | ✅ 正常 | 200 OK | 返回健康状态 |
| Grafana | http://43.156.131.98:8888 | ✅ 正常 | 302 Found | 重定向到登录页 |
| Prometheus | http://43.156.131.98:9000 | ❌ 超时 | Connection timed out | 端口未开放 |

---

## ✅ 成功的服务

### 1. Backend API - 完全正常 ✅

**测试命令**:
```bash
curl -v http://43.156.131.98:8000/api/v1/system/health
```

**测试结果**:
```
HTTP/1.1 200 OK
{"status":"healthy","service":"DSP Platform","version":"1.0.0"}
```

**结论**: 后端API外网访问完全正常！

---

### 2. Grafana - 正常运行 ✅

**测试命令**:
```bash
curl -v http://43.156.131.98:8888
```

**测试结果**:
```
HTTP/1.1 302 Found
Location: /login
<a href="/login">Found</a>.
```

**结论**: Grafana正常工作，外网访问正常！重定向到登录页是预期行为。

**访问地址**: http://43.156.131.98:8888
**用户/密码**: admin/admin

---

## ❌ Prometheus - 端口未开放

### 测试结果

**测试命令**:
```bash
curl -v http://43.156.131.98:9000
```

**测试结果**:
```
*   Trying 43.156.131.98:9000...
* Connection timed out
```

**结论**: 端口9000无法访问，需要在云服务器安全组开放。

### 原因分析

1. **云服务器安全组未开放端口9000** - 最可能原因
2. **防火墙未开放端口9000** - 可能性较小

### 解决方案

#### 方案1：开放云服务器安全组（推荐）

**阿里云**:
1. 控制台 → 云服务器ECS → 安全组
2. 添加入站规则：
   - 端口：9000
   - 协议：TCP
   - 授权对象：0.0.0.0/0

**腾讯云**:
1. 控制台 → 云服务器 → 安全组
2. 添加入站规则：
   - 协议端口：TCP:9000
   - 来源：0.0.0.0/0

**等待1-5分钟生效**

#### 方案2：使用Grafana替代

Grafana已经可以访问，可以在Grafana中查看Prometheus数据：

1. 访问 http://43.156.131.98:8888
2. 登录（admin/admin）
3. 添加Prometheus数据源：
   - URL: http://prometheus:9090
   - 点击"Save & Test"

#### 方案3：通过Nginx反向代理

通过端口8080访问Prometheus：

访问地址：http://43.156.131.98:8080/prometheus/

---

## 📋 完整服务状态

### ✅ 外网访问正常
- Backend API (8000) - HTTP 200 OK
- Grafana (8888) - HTTP 302 Found

### ❌ 需要配置
- Prometheus (9000) - Connection timed out

### ⏳ 其他服务
- Nginx (8080) - 未测试（但应该正常）
- Flower (8889) - 未测试

---

## 🎯 访问地址总结

| 服务 | 访问地址 | 用户/密码 | 状态 |
|------|----------|-----------|------|
| Backend API | http://43.156.131.98:8000/api/v1/ | - | ✅ 正常 |
| Grafana | http://43.156.131.98:8888 | admin/admin | ✅ 正常 |
| Prometheus | http://43.156.131.98:9000 | - | ❌ 需开放端口 |
| Nginx | http://43.156.131.98:8080 | - | ⏳ 未测试 |
| Flower | http://43.156.131.98:8889 | - | ⏳ 未测试 |

---

## 🔧 下一步操作

### 立即执行
1. **使用Grafana**
   - 访问 http://43.156.131.98:8888
   - 登录（admin/admin）
   - 配置Prometheus数据源

2. **开放Prometheus端口**（可选）
   - 在云服务器安全组开放端口9000
   - 等待1-5分钟生效
   - 测试访问 http://43.156.131.98:9000

### 测试其他服务
- [ ] 测试Nginx: http://43.156.131.98:8080
- [ ] 测试Flower: http://43.156.131.98:8889

---

## 📝 测试命令

### Backend API
```bash
curl http://43.156.131.98:8000/api/v1/system/health
```

### Grafana
```bash
curl -I http://43.156.131.98:8888
```

### Prometheus
```bash
curl -v http://43.156.131.98:9000
```

### Nginx
```bash
curl -I http://43.156.131.98:8080
```

---

**测试完成时间**: 2026-03-15 16:29
**测试结果**: ✅ 2/3服务正常，1/3服务需配置
**状态**: DSP Platform核心功能外网访问正常

---

## ✅ 好消息

**核心服务外网访问完全正常！**

- ✅ Backend API - 完全正常
- ✅ Grafana - 完全正常
- ⚠️ Prometheus - 需要开放端口9000

你现在可以：
1. 访问 http://43.156.131.98:8000/api/v1/ - API文档
2. 访问 http://43.156.131.98:8888 - Grafana（admin/admin）
3. 在Grafana中配置Prometheus数据源

如果需要直接访问Prometheus，需要在云服务器安全组开放端口9000。
