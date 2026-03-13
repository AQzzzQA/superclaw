# OpenClaw 权限配置可视化工具 - 使用说明

## 🎯 快速开始

### 1. 一键启动
```bash
cd /root/.openclaw/workspace/openclaw-permission-config
./quick-start.sh
```

### 2. 手动启动
```bash
# 安装依赖
pnpm install

# 启动后端
npm start

# 在另一个终端启动前端
cd frontend && npm start
```

## 🌐 访问地址
- **后端API**: http://localhost:8080/api/health
- **前端界面**: http://localhost:3000
- **API文档**: http://localhost:8080/api/docs

## 📋 核心功能

### 1. 用户管理
- 📊 查看所有QQ用户列表
- ➕ 添加新用户
- ✏️ 编辑用户信息和权限
- 🗑️ 删除用户（不能删除超级管理员）
- 📥 批量导入用户

### 2. 权限配置
- 🔒 4种基本权限级别：超级管理员、高级用户、普通用户、只读用户
- 🌳 可视化权限树，精确控制权限分配
- ⚡ 实时权限验证和冲突检查
- 🎨 不同角色对应的权限颜色标识

### 3. 模板管理
- 📄 4个预置权限模板（完整管理员、有限管理员、编辑者、观察者）
- 🎨 自定义权限模板创建
- 📋 模板复制和编辑
- 📤 导入/导出模板

### 4. 配置导出
- 💾 生成标准openclaw.json配置文件
- 🔍 配置完整性验证
- 📋 备份和恢复配置
- 🌍 支持JSON和YAML格式导出

## 🛠️ 管理命令

### 服务管理
```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh

# 重启服务
./restart.sh

# 查看日志
tail -f logs/server.log
tail -f logs/frontend.log
```

### 系统检查
```bash
# 检查服务状态
curl http://localhost:8080/api/health

# 查看用户列表
curl http://localhost:8080/api/users

# 查看配置状态
curl http://localhost:8080/api/config/status
```

## 🔧 权限级别说明

### 超级管理员
- **权限**: 所有权限（*）
- **颜色**: 🔴 红色
- **图标**: 👑
- **描述**: 拥有系统所有权限，不能被删除

### 高级用户
- **权限**: 配置读写、用户管理、模板管理
- **颜色**: 🟠 橙色
- **图标**: 🛡️
- **描述**: 可以管理用户和配置，但不能修改核心系统

### 普通用户
- **权限**: 配置读取、用户查看、模板查看
- **颜色**: 🔵 蓝色
- **图标**: ✏️
- **描述**: 可以查看和编辑配置，但不能管理用户

### 只读用户
- **权限**: 配置读取
- **颜色**: 🟢 绿色
- **图标**: 👁️
- **描述**: 只能查看配置信息，不能进行修改

## 🎨 界面特色

### 仪表板
- 📈 实时统计信息展示
- 🚀 快捷操作入口
- 📋 最近活动记录
- ⚠️ 系统状态提醒

### 用户管理
- 🔍 实时搜索过滤
- 📤 批量导入/导出
- 🎯 权限级别快速切换
- 📊 用户权限分布图表

### 权限配置
- 🌳 树形权限结构
- ✅ 实时权限验证
- 🔄 权限冲突检测
- 📝 权限变更历史

## 📊 安全特性

### 1. 权限保护
- 超级管理员权限不能被修改或删除
- 关键操作需要二次确认
- 权限变更实时记录

### 2. 配置安全
- 自动配置备份
- 配置完整性验证
- 变更日志追踪

### 3. 系统监控
- 实时服务状态监控
- 异常操作报警
- 性能指标监控

## 🚀 高级功能

### API接口
所有功能都提供RESTful API接口：
- `GET /api/users` - 获取用户列表
- `POST /api/users` - 添加用户
- `PUT /api/users/:id` - 更新用户
- `DELETE /api/users/:id` - 删除用户
- `GET /api/permissions/levels` - 获取权限级别
- `POST /api/config/generate` - 生成配置文件
- `POST /api/templates` - 创建模板

### 扩展功能
- 🔌 支持自定义权限模板
- 🌐 支持多语言（当前：中文）
- 📱 响应式设计，支持移动端
- 🎨 主题定制（暗色模式支持）

## 💡 使用建议

### 1. 权限分配建议
- 超级管理员：只有系统管理员
- 高级用户：管理员助理、技术支持
- 普通用户：日常使用用户
- 只读用户：审计人员、查看员

### 2. 安全建议
- 定期检查权限配置
- 定期备份配置文件
- 监控异常登录行为
- 定期更新用户权限

### 3. 性能建议
- 限制批量导入数量
- 定期清理日志文件
- 定期检查磁盘空间

## 🔍 故障排除

### 常见问题

#### 1. 服务无法启动
```bash
# 检查端口占用
netstat -tulpn | grep 8080

# 检查日志
tail -f logs/server.log

# 重启服务
./restart.sh
```

#### 2. 前端无法访问
```bash
# 检查前端服务
netstat -tulpn | grep 3000

# 查看前端日志
tail -f logs/frontend.log

# 重启前端
cd frontend && npm start
```

#### 3. 权限配置问题
```bash
# 检查配置文件
curl http://localhost:8080/api/config/status

# 重新生成配置
curl -X POST http://localhost:8080/api/config/validate \
  -H "Content-Type: application/json" \
  -d '{"config": {...}}'
```

## 📞 技术支持

### 日志分析
```bash
# 后端日志
tail -f logs/server.log

# 前端日志
tail -f logs/frontend.log

# 错误日志
grep ERROR logs/server.log
```

### 系统信息
```bash
# Node.js版本
node -v

# pnpm版本
pnpm -v

# 系统资源
free -h
df -h
```

---

**版本**: 1.0.0  
**更新时间**: 2026-03-13  
**作者**: Echo-2  
**许可证**: MIT