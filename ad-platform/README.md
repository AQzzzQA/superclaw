# Ad Platform API - 广告平台管理系统

完整的巨量引擎广告管理平台，支持广告计划、广告组、创意管理，以及数据报表和转化回传功能。

## 项目结构

```
ad-platform/
├── app/                      # 后端 API (FastAPI)
│   ├── api/                 # API 路由
│   │   ├── auth.py         # 用户认证
│   │   ├── oauth.py        # OAuth2 授权
│   │   ├── account.py      # 账户管理
│   │   ├── tenant.py       # 租户管理
│   │   ├── campaign.py     # 广告计划
│   │   ├── adgroup.py      # 广告组
│   │   ├── creative.py     # 创意管理
│   │   ├── report.py       # 数据报表
│   │   └── conversion.py   # 转化回传
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   ├── redis.py        # Redis 连接
│   │   ├── tenant.py       # 租户上下文
│   │   └── security.py     # 安全工具
│   ├── models/             # 数据模型
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── ocean_account.py
│   │   ├── campaign.py
│   │   ├── adgroup.py
│   │   ├── creative.py
│   │   └── report.py
│   ├── services/           # 业务服务
│   │   └── ocean/          # 巨量引擎服务
│   │       ├── client.py   # API 客户端（签名、HTTP）
│   │       ├── oauth.py    # OAuth2 认证
│   │       ├── campaign.py # 广告计划服务
│   │       ├── adgroup.py  # 广告组服务
│   │       ├── creative.py # 创意服务
│   │       ├── report.py   # 数据报表服务
│   │       └── conversion.py # 转化回传服务
│   └── main.py            # FastAPI 主入口
├── web/                    # 前端 (React + TypeScript)
│   ├── src/
│   │   ├── api/           # API 客户端
│   │   │   ├── index.ts
│   │   │   ├── auth.ts
│   │   │   ├── account.ts
│   │   │   ├── campaign.ts
│   │   │   ├── oauth.ts
│   │   │   ├── report.ts
│   │   │   └── conversion.ts
│   │   ├── App.tsx        # 主应用
│   │   └── main.tsx       # 入口
│   ├── package.json
│   └── vite.config.ts
├── alembic/                # 数据库迁移
├── requirements.txt        # Python 依赖
├── docker-compose.yml      # Docker 编排
└── README.md
```

## 功能特性

### ✅ 已完成功能

#### 后端 API
- **用户认证**：登录、注册、JWT Token 认证
- **租户管理**：多租户支持
- **账户管理**：巨量广告账户的创建、查询、更新、删除
- **OAuth2 授权**：巨量引擎授权流程
- **广告计划管理**：计划 CRUD、状态更新
- **广告组管理**：单元 CRUD、状态更新
- **创意管理**：创意 CRUD、状态更新
- **数据报表**：日报表查询、历史数据存储
- **转化回传**：转化数据上传、查询

#### 前端页面
- **仪表盘**：系统概览
- **登录页**：用户登录
- **账户管理**：巨量账户列表和操作
- **广告计划**：计划、广告组、创意管理
- **创意管理**：创意素材管理
- **数据报表**：数据可视化展示
- **转化回传**：转化数据管理

#### 基础设施
- **数据库**：MySQL + Alembic 迁移
- **缓存**：Redis
- **API 签名**：巨量引擎 MD5 签名
- **Docker 支持**：一键部署

## 快速开始

### 方式一：本地开发

#### 1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env
cp web/.env.example web/.env

# 编辑 .env 文件，填入巨量引擎配置
OCEAN_APP_ID=your_app_id
OCEAN_APP_SECRET=your_app_secret
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/ad_platform?charset=utf8mb4
REDIS_URL=redis://localhost:6379/0
```

#### 2. 启动后端

```bash
cd /root/.openclaw/workspace/ad-platform

# 安装依赖
pip install -r requirements.txt

# 执行数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. 启动前端

```bash
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 `http://localhost:5173` 查看前端页面

访问 `http://localhost:8000/docs` 查看 API 文档

### 方式二：Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## API 文档

### OAuth2 认证
- `GET /api/v1/oauth/authorize` - 获取授权 URL
- `POST /api/v1/oauth/callback` - 回调处理
- `POST /api/v1/oauth/refresh` - 刷新 Token

### 用户认证
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/register` - 用户注册
- `GET /api/v1/auth/me` - 获取当前用户信息

### 账户管理
- `POST /api/v1/account/create` - 创建账户
- `GET /api/v1/account/list` - 获取账户列表
- `GET /api/v1/account/{id}` - 获取账户详情
- `POST /api/v1/account/{id}/update` - 更新账户
- `POST /api/v1/account/{id}/delete` - 删除账户

### 广告计划
- `POST /api/v1/campaign/create` - 创建计划
- `GET /api/v1/campaign/list` - 获取计划列表
- `POST /api/v1/campaign/update` - 更新计划
- `POST /api/v1/campaign/update-status` - 更新状态
- `POST /api/v1/campaign/delete` - 删除计划

### 广告组
- `POST /api/v1/adgroup/create` - 创建广告组
- `GET /api/v1/adgroup/list` - 获取广告组列表
- `POST /api/v1/adgroup/update` - 更新广告组
- `POST /api/v1/adgroup/update-status` - 更新状态
- `POST /api/v1/adgroup/delete` - 删除广告组

### 创意
- `POST /api/v1/creative/create` - 创建创意
- `GET /api/v1/creative/list` - 获取创意列表
- `POST /api/v1/creative/update` - 更新创意
- `POST /api/v1/creative/update-status` - 更新状态
- `POST /api/v1/creative/delete` - 删除创意

### 数据报表
- `POST /api/v1/report/daily` - 获取日报表
- `GET /api/v1/report/history` - 获取历史报表

### 转化回传
- `POST /api/v1/conversion/upload` - 上传转化
- `POST /api/v1/conversion/query` - 查询转化

## 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

## 技术栈

### 后端
- FastAPI - Web 框架
- SQLAlchemy - ORM
- MySQL - 数据库
- Redis - 缓存
- Alembic - 数据库迁移
- PyJWT - JWT 认证
- httpx - HTTP 客户端

### 前端
- React 19 - UI 框架
- TypeScript - 类型系统
- Vite - 构建工具
- Ant Design 5 - UI 组件库
- React Router 7 - 路由管理
- Axios - HTTP 客户端

## 开发说明

1. 所有 API 需要在 Header 中传入 `Authorization: Bearer <token>`
2. 巨量引擎 API 有频率限制，建议使用 Redis 缓存
3. 生产环境需配置 CORS、限流、日志等
4. 转化回传需要真实转化数据，建议先在测试环境验证

## 参考文档

- [巨量引擎开放平台](https://open.oceanengine.com/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [React 官方文档](https://react.dev/)

## License

MIT
