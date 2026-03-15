# Prometheus连接被拒绝问题

**问题**: 外网访问 http://43.156.131.98:8999 时显示"连接被拒绝"
**时间**: 2026-03-15 16:55
**状态**: ⚠️ 严重问题

---

## 问题描述

从外网访问 http://43.156.131.98:8999 时：
- **错误**: 连接被拒绝 (Connection Refused)
- **说明**: 端口8999无法访问

---

## 排查结果

### 1. 端口监听检查 ❌

```bash
netstat -tlnp | grep 8999
# 结果：无输出
```

**结论**: 端口8999未在监听！

### 2. Docker容器状态 ⚠️

```
dsp-prometheus - Up 2 minutes - 0.0.0.0:8999->9090/tcp
```

**结论**: 容器运行中，端口映射已配置。

### 3. Prometheus日志 ✅

```
ts=2026-03-15T08:52:00.000Z caller=main.go:1025 level=info msg="Starting Prometheus" ...
ts=2026-03-15T08:52:00.000Z caller=web.go:535 level=info msg="Listening" address=[::]:9090
ts=2026-03-15T08:52:00.000Z caller=main.go:1029 level=info msg="Server is ready to receive web requests."
```

**结论**: Prometheus启动正常，监听容器内端口9090。

---

## 🔍 问题分析

### 根本原因：docker-proxy未正常工作

Docker容器显示端口映射 `0.0.0.0:8999->9090/tcp`，但netstat检查发现端口8999未监听。

**可能的原因**：
1. Docker网络问题
2. docker-proxy进程异常
3. 端口映射配置问题
4. 防火墙规则干扰

---

## 🔧 解决方案

### 方案1：重新启动Prometheus容器

```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose stop prometheus
docker-compose rm -f prometheus
docker-compose up -d prometheus
```

### 方案2：检查Docker网络

```bash
# 检查Docker网络
docker network ls
docker network inspect dsp-platform_dsp-network

# 重启Docker网络
docker-compose down
docker-compose up -d
```

### 方案3：检查防火墙规则

```bash
# 检查防火墙状态
firewall-cmd --list-all

# 开放端口8999
firewall-cmd --permanent --add-port=8999/tcp
firewall-cmd --reload

# 检查端口是否开放
firewall-cmd --list-ports
```

### 方案4：检查Docker服务

```bash
# 检查Docker服务状态
systemctl status docker

# 重启Docker服务
systemctl restart docker

# 重新启动DSP Platform
cd /root/.openclaw/workspace/dsp-platform
docker-compose up -d
```

---

## 🧪 执行方案1（最快）

```bash
# 停止并删除Prometheus容器
cd /root/.openclaw/workspace/dsp-platform
docker-compose stop prometheus
docker-compose rm -f prometheus

# 重新启动Prometheus
docker-compose up -d prometheus

# 等待5秒
sleep 5

# 检查端口监听
netstat -tlnp | grep 8999

# 测试访问
curl http://localhost:8999
```

---

## 📋 待办事项

### 立即执行
- [ ] 重新启动Prometheus容器
- [ ] 验证端口8999监听
- [ ] 测试本地访问
- [ ] 测试外网访问

### 短期目标
- [ ] 诊断Docker网络问题
- [ ] 检查防火墙规则
- [ ] 验证所有服务正常

### 长期目标
- [ ] 添加端口健康检查
- [ ] 配置服务监控告警
- [ ] 优化Docker网络配置

---

## 📊 当前服务状态

### 正常运行 ✅
- Backend (8000) - 外网访问正常
- Grafana (8888) - 外网访问正常
- MySQL (3308) - 内网访问正常
- Redis (6381) - 内网访问正常
- Nginx (8080) - 预计正常

### 异常服务 ⚠️
- Prometheus (8999) - 连接被拒绝
- 端口8999未监听

---

## 🔧 命令参考

### 检查端口监听
```bash
netstat -tlnp | grep 8999
# 或
ss -tlnp | grep 8999
```

### 检查Docker端口映射
```bash
docker ps --filter "name=dsp-prometheus"
```

### 测试本地访问
```bash
curl http://localhost:8999
```

### 测试外网访问
```bash
curl http://43.156.131.98:8999
```

---

## 📁 相关文档

- `docker-compose.yml` - Docker Compose配置
- `infrastructure/prometheus/prometheus.yml` - Prometheus配置

---

**报告时间**: 2026-03-15 16:55
**优先级**: 🔴 高
**状态**: ⚠️ 端口8999未监听，需要重新启动服务
**建议**: 执行方案1重新启动Prometheus容器
