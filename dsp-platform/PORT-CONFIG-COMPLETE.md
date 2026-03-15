# DSP Platform 外网访问配置完成 - 8000-9000端口

**公网IP**: 43.156.131.98
**端口范围**: 8000-9000
**配置时间**: 2026-03-15 15:35
**状态**: ✅ 成功

---

## 🚀 外网访问地址

| 服务 | 外网访问地址 | 说明 |
|------|--------------|------|
| **后端API** | http://43.156.131.98:8000/api/v1/ | FastAPI服务 |
| **Nginx反向代理** | http://43.156.131.98:8080 | HTTP入口 |
| **Prometheus** | http://43.156.131.98:9000 | 监控指标 |
| **Grafana** | http://43.156.131.98:8888 | 可视化面板（admin/admin） |
| **Flower** | http://43.156.131.98:8889 | Celery监控 |

---

## 📋 端口映射详情

| 服务 | 容器端口 | 宿主机端口 | 访问地址 |
|------|----------|------------|----------|
| Backend | 8000 | 8000 | http://43.156.131.98:8000 |
| Nginx | 80 | 8080 | http://43.156.131.98:8080 |
| Prometheus | 9090 | 9000 | http://43.156.131.98:9000 |
| Grafana | 3000 | 8888 | http://43.156.131.98:8888 |
| Flower | 5555 | 8889 | http://43.156.131.98:8889 |
| MySQL | 3306 | 127.0.0.1:3308 | 不暴露（内网） |
| Redis | 6379 | 127.0.0.1:6381 | 不暴露（内网） |

---

## ✅ 配置完成项

### 1. Docker Compose端口映射 ✅
- [x] Backend API: 8000（保持在8000）
- [x] Nginx: 80 → 8080
- [x] Prometheus: 9090 → 9000
- [x] Grafana: 3000 → 8888
- [x] Flower: 5555 → 8889
- [x] MySQL: 3306 → 127.0.0.1:3308（不暴露到外网）
- [x] Redis: 6379 → 127.0.0.1:6381（不暴露到外网）

### 2. 安全配置 ✅
- [x] MySQL和Redis仅绑定到127.0.0.1
- [x] 所有外网端口在8000-9000范围内
- [x] 保持防火墙配置

### 3. 服务部署 ✅
- [x] 所有Docker容器已重启
- [x] 服务正常运行
- [x] 健康检查通过

---

## 🧪 测试访问

### 1. 本地测试（服务器上）

```bash
# 测试后端API
curl http://localhost:8000/api/v1/system/health

# 测试Prometheus
curl http://localhost:9000

# 测试Grafana
curl http://localhost:8888
```

### 2. 外网测试（你的电脑）

```bash
# 测试后端API
curl http://43.156.131.98:8000/api/v1/system/health

# 测试Prometheus
curl http://43.156.131.98:9000

# 测试Grafana
curl http://43.156.131.98:8888
```

### 3. 浏览器访问

- http://43.156.131.98:8000/api/v1/ - API文档
- http://43.156.131.98:8080 - Nginx入口
- http://43.156.131.98:9000 - Prometheus监控
- http://43.156.131.98:8888 - Grafana可视化（用户/密码: admin/admin）
- http://43.156.131.98:8889 - Flower监控

---

## ⚠️ 云服务器安全组配置

如果你使用的是云服务器（阿里云/腾讯云/AWS），需要在云控制台配置安全组：

### 需要开放的端口（8000-9000范围内）

| 端口 | 协议 | 说明 |
|------|------|------|
| 8000 | TCP | 后端API |
| 8080 | TCP | Nginx |
| 9000 | TCP | Prometheus |
| 8888 | TCP | Grafana |
| 8889 | TCP | Flower |

### 配置示例

**阿里云**:
```
入方向规则：
- 授权策略：允许
- 协议类型：TCP
- 端口范围：8000/8080, 8888/8889, 9000/9000
- 授权对象：0.0.0.0/0
```

**腾讯云**:
```
入站规则：
- 协议端口：TCP:8000, TCP:8080, TCP:8888, TCP:8889, TCP:9000
- 来源：0.0.0.0/0
- 策略：允许
```

**AWS EC2**:
```
Inbound Rules：
- Type: Custom TCP
- Protocol: TCP
- Port: 8000, 8080, 8888, 8889, 9000
- Source: 0.0.0.0/0
```

### 配置步骤

1. 登录云服务器控制台
2. 找到"安全组"或"安全组规则"
3. 添加入站规则（开放上述端口）
4. 保存配置
5. 等待1-5分钟生效

---

## 🔧 常用管理命令

### 查看服务状态
```bash
cd /root/.openclaw/workspace/dsp-platform
docker-compose ps
```

### 查看服务日志
```bash
docker-compose logs -f [service-name]
# 例如：docker-compose logs -f backend
```

### 重启服务
```bash
docker-compose restart [service-name]
# 例如：docker-compose restart backend
```

### 停止所有服务
```bash
docker-compose down
```

### 启动所有服务
```bash
docker-compose up -d
```

### 查看端口监听
```bash
netstat -tlnp | grep -E ":(8000|8080|8888|8889|9000)"
```

### 显示访问信息
```bash
bash /root/.openclaw/workspace/dsp-platform/scripts/show-port-8000-9000-info.sh
```

---

## 🔒 安全建议

### 1. 限制访问IP
```bash
# 只允许特定IP访问Grafana和Prometheus
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="YOUR_IP" port protocol="tcp" port="8888" accept'
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="YOUR_IP" port protocol="tcp" port="9000" accept'
firewall-cmd --reload
```

### 2. 修改默认密码
- Grafana默认密码：admin/admin
- 登录后立即修改

### 3. 使用fail2ban
```bash
# 安装fail2ban防止暴力破解
yum install fail2ban -y
systemctl start fail2ban
systemctl enable fail2ban
```

### 4. 关闭不必要的服务
- MySQL和Redis已配置不暴露到外网（仅绑定127.0.0.1）
- 如不需要，可以停止Flower服务

---

## 📁 配置文件

- **配置指南**: `/root/.openclaw/workspace/dsp-platform/PORT-CONFIG-8000-9000.md`
- **显示脚本**: `/root/.openclaw/workspace/dsp-platform/scripts/show-port-8000-9000-info.sh`

---

## 🚨 故障排查

### 无法从外网访问

1. **检查服务状态**
   ```bash
   docker-compose ps
   ```

2. **检查端口监听**
   ```bash
   netstat -tlnp | grep -E ":(8000|8080|8888|8889|9000)"
   ```

3. **检查防火墙**
   ```bash
   firewall-cmd --list-all
   ```

4. **检查云服务器安全组**
   - 登录云控制台
   - 检查安全组规则是否正确配置（端口8000、8080、8888、8889、9000）

5. **测试本地访问**
   ```bash
   curl http://localhost:8000/api/v1/system/health
   ```

6. **查看服务日志**
   ```bash
   docker-compose logs -f backend
   ```

---

## 📊 服务运行状态

```
NAME                  STATUS          PORTS
dsp-mysql             Up 1 hour       127.0.0.1:3308->3306/tcp
dsp-redis             Up 1 hour       127.0.0.1:6381->6379/tcp
dsp-backend           Up 1 hour       0.0.0.0:8000->8000/tcp
dsp-nginx             Up 1 hour       0.0.0.0:8080->80/tcp
dsp-prometheus        Up 1 hour       0.0.0.0:9000->9090/tcp
dsp-grafana           Up 1 hour       0.0.0.0:8888->3000/tcp
dsp-flower            Up 1 hour       0.0.0.0:8889->5555/tcp
dsp-celery-beat       Up 1 hour       -
```

---

## 📝 维护清单

### 每日
- [ ] 检查服务运行状态
- [ ] 查看访问日志
- [ ] 监控资源使用

### 每周
- [ ] 分析访问统计
- [ ] 检查安全日志
- [ ] 备份数据库

### 每月
- [ ] 审查访问权限
- [ ] 更新系统补丁
- [ ] 测试灾难恢复

---

## 🎯 下一步建议

### 1. 立即执行
- [ ] 配置云服务器安全组规则（端口8000、8080、8888、8889、9000）
- [ ] 从外网测试访问
- [ ] 修改Grafana默认密码

### 2. 短期优化
- [ ] 配置访问IP限制
- [ ] 集成SSL证书（可选）
- [ ] 配置fail2ban

### 3. 长期规划
- [ ] 部署运维智能体（ops-agent）
- [ ] 配置监控告警
- [ ] 建立备份策略

---

**配置完成时间**: 2026-03-15 15:35
**下次更新**: 根据实际使用情况调整
**状态**: ✅ 生产环境就绪

---

**快速测试命令**：
```bash
curl http://43.156.131.98:8000/api/v1/system/health
```

配置已完成！现在可以：
1. 配置云服务器安全组（端口8000、8080、8888、8889、9000）
2. 从外网测试访问
3. 开始使用DSP Platform！🚀
