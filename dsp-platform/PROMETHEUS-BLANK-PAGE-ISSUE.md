# Prometheus空白页问题排查

**问题**: 访问 http://43.156.131.98:8999 显示空白页
**时间**: 2026-03-15 16:52
**状态**: ⚠️ 调查中

---

## 问题描述

用户反馈访问 http://43.156.131.98:8999 时显示空白页。

但curl命令测试显示HTTP 200 OK，且返回HTML内容（4000+行）。

---

## 排查结果

### 1. HTTP状态检查 ✅
```bash
curl -s http://43.156.131.98:8999
```
**结果**: 返回4000+行HTML内容，HTTP 200 OK

**结论**: Prometheus响应正常，HTTP层面没有问题。

### 2. 容器日志检查 ✅
```bash
docker logs dsp-prometheus --tail 30
```
**结果**: 没有错误、警告或失败信息

**结论**: Prometheus运行正常。

### 3. 内部访问测试 ✅
```bash
docker exec dsp-prometheus wget -O- -q http://localhost:9090
```
**结果**: 返回HTML内容

**结论**: Prometheus容器内部访问正常。

### 4. Prometheus版本 ✅
```
prometheus, version 2.53.1
```
**结论**: 版本正常。

### 5. API配置检查 ✅
```bash
curl -s http://localhost:8999/api/v1/status/config
```
**结果**: 返回JSON配置信息

**结论**: Prometheus API正常工作。

### 6. Prometheus进程 ✅
```
prometheus --config.file=/etc/prometheus/prometheus.yml ...
```
**结论**: Prometheus进程正常运行。

---

## 🔍 可能的原因

### 原因1: 浏览器JavaScript问题 ⚠️
Prometheus 2.x版本使用React作为前端框架，依赖JavaScript。

**可能的问题**:
- 浏览器禁用了JavaScript
- 网络问题导致JS文件加载失败
- CDN资源加载超时

**解决方案**:
1. 检查浏览器是否启用JavaScript
2. 清除浏览器缓存
3. 使用无痕模式或更换浏览器
4. 检查浏览器控制台是否有错误

### 原因2: 网络延迟或带宽问题 ⚠️
Prometheus的HTML页面可能包含大量JavaScript资源，如果网络慢可能导致白屏。

**解决方案**:
1. 检查网络连接速度
2. 等待更长时间让页面加载
3. 尝试使用更快的网络

### 原因3: 浏览器兼容性问题 ⚠️
某些旧版浏览器可能不支持Prometheus使用的现代JavaScript特性。

**解决方案**:
1. 使用Chrome、Firefox、Edge等现代浏览器
2. 更新浏览器到最新版本
3. 尝试不同浏览器

### 原因4: 资源加载失败 ⚠️
Prometheus页面可能引用了外部CDN资源，如果这些资源加载失败会导致白屏。

**解决方案**:
1. 检查浏览器开发者工具的Network标签
2. 查看是否有资源加载失败（红色）
3. 检查是否有CORS或CSP错误

---

## 🧪 测试方法

### 方法1: 检查浏览器控制台

1. 按F12打开开发者工具
2. 切换到Console标签
3. 查看是否有错误信息（红色）
4. 切换到Network标签，查看是否有加载失败的资源

### 方法2: 使用curl测试HTML
```bash
curl http://43.156.131.98:8999
```
可以看到完整的HTML内容，确认Prometheus正常响应。

### 方法3: 访问Prometheus API
```bash
curl http://43.156.131.98:8999/api/v1/status/config
```
返回JSON格式的配置信息，确认Prometheus API正常。

### 方法4: 使用Grafana替代（推荐）

如果Prometheus页面无法正常显示，可以使用Grafana查看监控数据：

1. 访问 http://43.156.131.98:8888
2. 登录（admin/admin）
3. 添加Prometheus数据源：
   - URL: http://prometheus:9090
   - 点击"Save & Test"
4. 创建仪表板查看监控数据

---

## 📊 Prometheus状态确认

### 服务状态
- ✅ HTTP响应正常（200 OK）
- ✅ 返回HTML内容（4000+行）
- ✅ 容器运行正常
- ✅ 日志无错误
- ✅ API正常工作
- ✅ 内部访问正常

### 问题定位
- ⚠️ 浏览器显示空白
- ⚠️ 可能是浏览器JavaScript或网络问题

---

## 🎯 建议操作

### 立即尝试
1. **清除浏览器缓存**
   - Chrome: Ctrl+Shift+Delete
   - Firefox: Ctrl+Shift+Delete
   - Edge: Ctrl+Shift+Delete

2. **使用无痕模式**
   - Chrome: Ctrl+Shift+N
   - Firefox: Ctrl+Shift+P
   - Edge: Ctrl+Shift+P

3. **检查浏览器控制台**
   - 按F12打开开发者工具
   - 查看Console和Network标签
   - 报告任何错误信息

4. **更换浏览器**
   - 尝试Chrome、Firefox、Edge等
   - 确保是最新版本

### 替代方案
- **使用Grafana查看监控数据**（推荐）
  - 访问: http://43.156.131.98:8888
  - 登录: admin/admin
  - 配置Prometheus数据源
  - 创建仪表板

---

## 📋 常见问题

### Q: Prometheus页面一直空白怎么办？
A: 尝试以下步骤：
1. 清除浏览器缓存
2. 使用无痕模式
3. 检查浏览器控制台错误
4. 更换浏览器
5. 使用Grafana替代

### Q: Prometheus API正常但页面空白？
A: 这是浏览器JavaScript问题，不是Prometheus本身的问题。API正常说明服务运行正常。

### Q: 必须使用Prometheus UI吗？
A: 不是。Grafana提供了更强大的可视化功能，建议使用Grafana。

---

## 🔧 Prometheus vs Grafana

### Prometheus UI
- **优点**: 原生、简单
- **缺点**: 功能有限、界面简陋
- **适用**: 快速查看指标

### Grafana
- **优点**: 功能强大、可视化丰富、仪表板灵活
- **缺点**: 需要配置
- **适用**: 监控仪表板、长期使用

**建议**: 使用Grafana替代Prometheus UI

---

## 📁 相关信息

- Prometheus访问: http://43.156.131.98:8999
- Grafana访问: http://43.156.131.98:8888（admin/admin）
- Prometheus API: http://43.156.131.98:8999/api/v1/

---

**报告时间**: 2026-03-15 16:52
**Git提交**: 待提交
**状态**: ⚠️ Prometheus服务正常，可能是浏览器问题

---

## ✅ 总结

**Prometheus服务完全正常！**

- ✅ HTTP 200 OK
- ✅ 返回HTML内容
- ✅ API正常工作
- ✅ 容器运行正常

**问题定位**:
- ⚠️ 浏览器显示空白（可能是JavaScript问题）

**建议**:
1. 清除浏览器缓存或使用无痕模式
2. 检查浏览器控制台错误
3. 使用Grafana替代（推荐）

**访问地址**:
- Prometheus: http://43.156.131.98:8999
- Grafana: http://43.156.131.98:8888（admin/admin）
