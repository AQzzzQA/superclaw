# OpenClaw Permission Manager

一个专为QQ用户权限配置设计的可视化管理系统，提供完整的用户管理、权限模板管理和配置文件管理功能。

## 🚀 功能特性

- **用户管理**: QQ用户权限配置、角色分配、权限设置
- **权限模板管理**: 系统预设和自定义权限模板
- **配置管理**: 生成和管理OpenClaw配置文件
- **Web界面**: 基于React+TypeScript+Ant Design的现代化界面
- **RESTful API**: 完整的后端API支持
- **JWT认证**: 安全的身份验证系统
- **Docker支持**: 容器化部署方案

## 🏗️ 技术栈

### 后端
- **Node.js** + **Express** - Web框架
- **TypeScript** - 类型安全的JavaScript
- **SQLite** - 轻量级数据库
- **JWT** - 身份验证
- **bcryptjs** - 密码加密

### 前端
- **React 18** - 用户界面框架
- **TypeScript** - 类型安全
- **Ant Design 5** - UI组件库
- **React Router** - 路由管理
- **Axios** - HTTP客户端

### 部署
- **Docker** - 容器化
- **Docker Compose** - 容器编排
- **Nginx** - 反向代理
- **PM2** - 进程管理

## 📦 安装

### 快速开始

```bash
# 克隆项目
git clone <repository-url>
cd openclaw-permission-manager

# 使用开发脚本启动
./scripts/start-dev.sh
```

### 手动安装

```bash
# 安装后端依赖
cd backend
npm install

# 安装前端依赖
cd ../frontend
npm install

# 配置环境变量
cd ..
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 初始化数据库
cd backend
npm run init-db

# 启动服务
cd ../backend && npm run dev &
cd ../frontend && npm start &
```

## 🚀 使用

### 访问地址
- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:3001

### 默认账户
- **管理员QQ**: `admin`
- **角色**: 管理员
- **权限**: 所有权限

### 主要功能

1. **仪表板**: 用户统计、系统状态
2. **用户管理**: 添加/编辑/删除用户，设置权限
3. **权限模板**: 创建和管理权限模板
4. **配置管理**: 生成和导出配置文件

## 📋 系统要求

- **Node.js**: 18.0 或更高版本
- **npm**: 8.0 或更高版本
- **内存**: 至少 2GB
- **磁盘**: 至少 1GB

## 🔧 配置

### 环境变量

#### 后端 (.env)
```env
PORT=3001
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=7d
DB_PATH=./data/permissions.db
MAX_UPLOAD_SIZE=10485760
UPLOAD_PATH=./uploads
```

#### 前端 (.env)
```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_NAME=OpenClaw权限管理系统
REACT_APP_VERSION=1.0.0
```

### 数据库配置

系统使用SQLite数据库，数据文件位于 `backend/data/permissions.db`。

## 🐳 Docker部署

### 使用Docker Compose

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs
```

### 单独部署

```bash
# 构建后端镜像
docker build -t openclaw-permission-manager-backend ./backend

# 构建前端镜像
docker build -t openclaw-permission-manager-frontend ./frontend

# 运行后端容器
docker run -p 3001:3001 openclaw-permission-manager-backend

# 运行前端容器
docker run -p 3000:80 openclaw-permission-manager-frontend
```

## 📖 文档

- [API文档](docs/api/README.md) - 完整的API接口说明
- [安装指南](docs/installation/README.md) - 详细的安装步骤
- [使用指南](docs/usage/README.md) - 系统使用说明

## 🔒 安全说明

- 所有密码使用bcryptjs加密存储
- JWT token用于身份验证
- RESTful API支持CORS跨域请求
- 所有输入数据都经过验证

## 🚀 开发

### 开发环境

```bash
# 启动开发服务器
./scripts/start-dev.sh

# 或者手动启动
cd backend && npm run dev &
cd frontend && npm start &
```

### 代码检查

```bash
# 后端代码检查
cd backend && npm run lint

# 前端代码检查
cd frontend && npm run lint
```

### 测试

```bash
# 后端测试
cd backend && npm test

# 前端测试
cd frontend && npm test
```

## 📊 监控

### 健康检查

```bash
# 后端健康检查
curl http://localhost:3001/api/health

# 前端健康检查
curl http://localhost:3000
```

### 日志查看

```bash
# Docker日志
docker logs openclaw-permission-manager-backend
docker logs openclaw-permission-manager-frontend

# PM2日志
pm2 logs
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请提交Issue或联系项目维护者。

---

**OpenClaw Permission Manager** - 让QQ用户权限配置变得简单高效！