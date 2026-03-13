# OpenClaw Permission Manager Backend

后端API服务器，用于OpenClaw权限配置可视化工具的管理功能。

## 功能特性

- 用户管理（QQ用户权限配置）
- 权限模板管理
- 配置文件管理
- JWT认证
- RESTful API

## 技术栈

- Node.js + Express
- TypeScript
- SQLite数据库
- JWT认证
- 中间件（CORS, Helmet, Morgan）

## 安装与运行

### 1. 安装依赖

```bash
npm install
```

### 2. 环境配置

复制 `.env.example` 到 `.env` 并配置：

```bash
cp .env.example .env
```

### 3. 初始化数据库

```bash
npm run init-db
```

### 4. 启动服务

```bash
# 开发模式
npm run dev

# 生产模式
npm run build
npm start
```

## API接口

### 认证接口

- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/profile` - 更新用户资料

### 用户管理接口

- `GET /api/users` - 获取用户列表
- `POST /api/users` - 创建用户
- `GET /api/users/:id` - 获取用户详情
- `PUT /api/users/:id` - 更新用户
- `DELETE /api/users/:id` - 删除用户
- `GET /api/users/qq/:qq_number` - 根据QQ号获取用户

### 权限模板接口

- `GET /api/permissions/templates` - 获取权限模板列表
- `POST /api/permissions/templates` - 创建权限模板
- `GET /api/permissions/templates/:id` - 获取模板详情
- `PUT /api/permissions/templates/:id` - 更新模板
- `DELETE /api/permissions/templates/:id` - 删除模板

### 配置管理接口

- `GET /api/permissions/configs` - 获取配置列表
- `POST /api/permissions/configs` - 创建配置
- `GET /api/permissions/configs/:id` - 获取配置详情
- `PUT /api/permissions/configs/:id` - 更新配置
- `DELETE /api/permissions/configs/:id` - 删除配置
- `GET /api/permissions/generate/:userId` - 生成用户配置

## 数据库结构

### users表
- id: 用户ID
- qq_number: QQ号码
- nickname: 昵称
- avatar_url: 头像URL
- role: 角色 (admin, user, readonly)
- permissions: 权限列表 (JSON)
- created_at: 创建时间
- updated_at: 更新时间

### permission_templates表
- id: 模板ID
- name: 模板名称
- description: 描述
- permissions: 权限列表 (JSON)
- is_system: 是否系统模板
- created_by: 创建者
- created_at: 创建时间
- updated_at: 更新时间

### openclaw_config表
- id: 配置ID
- config_name: 配置名称
- config_data: 配置数据 (JSON)
- version: 版本号
- created_by: 创建者
- created_at: 创建时间
- updated_at: 更新时间

## 部署

### 使用Docker

```bash
# 构建镜像
docker build -t openclaw-permission-manager-backend .

# 运行容器
docker run -p 3001:3001 openclaw-permission-manager-backend
```

### 使用PM2

```bash
npm install -g pm2
pm2 start ecosystem.config.js
```

## 开发工具

### 代码检查

```bash
npm run lint
npm run lint:fix
```

### 测试

```bash
npm test
npm run test:watch
```

## 许可证

MIT License