# DSP国内全媒体广告平台

## 项目简介

DSP（Demand Side Platform）国内全媒体广告平台是一个面向广告主的全渠道广告投放管理平台，支持抖音、快手、微信朋友圈、百度信息流、腾讯广告等多个媒体渠道的广告投放、数据监控、效果分析和智能优化。

## 技术栈

### 后端
- **Web框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: MySQL 8.0+
- **缓存**: Redis 7.0+
- **任务队列**: Celery 5.3+
- **API风格**: RESTful API + WebSocket
- **认证**: JWT + OAuth2.0

### 前端
- **框架**: React 18+
- **UI组件**: Ant Design 5+
- **状态管理**: Redux Toolkit
- **构建工具**: Vite

### 部署
- **容器**: Docker + Docker Compose
- **反向代理**: Nginx
- **进程管理**: Supervisor

## 项目结构

```
dsp-platform/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── campaigns.py
│   │   │   │   ├── creatives.py
│   │   │   │   ├── audiences.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── billing.py
│   │   │   │   └── notifications.py
│   │   │   └── websocket/
│   │   │       └── realtime.py
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模式
│   │   ├── services/        # 业务逻辑
│   │   ├── tasks/           # Celery任务
│   │   ├── core/            # 核心配置
│   │   └── utils/           # 工具函数
│   ├── docs/                # 文档
│   │   ├── architecture.md   # 架构文档
│   │   ├── api-endpoints.md # API端点清单
│   │   ├── database.md      # 数据库Schema
│   │   └── celery-tasks.md  # Celery任务设计
│   ├── tests/               # 测试
│   └── scripts/             # 脚本
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── pages/           # 页面
│   │   ├── services/        # API服务
│   │   └── utils/           # 工具函数
│   └── public/              # 静态资源
├── deployment/              # 部署配置
│   ├── docker/              # Docker配置
│   └── k8s/                 # Kubernetes配置
└── infrastructure/          # 基础设施配置
    ├── nginx/               # Nginx配置
    ├── redis/               # Redis配置
    └── mysql/               # MySQL配置
```

## 核心功能

### 1. 广告投放管理
- 广告计划创建、编辑、删除
- 创意素材上传与管理
- 受众定向配置
- 投放策略设置

### 2. 数据回传
- 实时曝光、点击、转化数据接收
- 批量数据处理
- 数据清洗与标准化
- 异常数据检测

### 3. 报表分析
- 实时报表生成
- 自定义报表配置
- 多维度数据分析
- 报表导出（Excel/PDF/CSV）

### 4. 计费管理
- 账户充值
- 消费统计
- 发票管理
- 预算控制

### 5. 实时监控
- WebSocket实时数据推送
- 广告计划状态监控
- 性能指标实时更新
- 告警通知

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+
- Docker & Docker Compose

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库、Redis等

# 初始化数据库
python scripts/init_db.py

# 启动FastAPI服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 启动Celery Worker（另一个终端）
celery -A app.tasks.worker worker --loglevel=info

# 启动Celery Beat（另一个终端）
celery -A app.tasks.worker beat --loglevel=info
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置API地址等

# 启动开发服务器
npm run dev
```

### Docker部署

```bash
# 使用Docker Compose一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

详细API文档请参考: [backend/docs/api-endpoints.md](backend/docs/api-endpoints.md)

## 数据库设计

数据库Schema设计文档: [backend/docs/database-schema.md](backend/docs/database-schema.md)

### 数据库表清单（21张表）

#### 用户相关（3张）
- users - 用户表
- roles - 角色表
- user_roles - 用户角色关联表

#### 广告相关（6张）
- campaigns - 广告计划表
- creatives - 创意素材表
- audiences - 受众定向表
- strategies - 投放策略表
- campaign_audiences - 广告计划受众关联表
- campaign_creatives - 广告计划创意关联表

#### 数据相关（3张）
- impressions - 曝光数据表
- clicks - 点击数据表
- conversions - 转化数据表

#### 报表相关（3张）
- reports - 报表配置表
- report_data - 报表数据表
- report_schedules - 报表定时任务表

#### 计费相关（3张）
- accounts - 账户表
- transactions - 交易记录表
- invoices - 发票表

#### 系统表（3张）
- platforms - 媒体平台表
- platform_accounts - 平台账户表
- notifications - 系统通知表

## Celery任务设计

Celery任务队列设计文档: [backend/docs/celery-tasks.md](backend/docs/celery-tasks.md)

### 任务分类

1. **数据回传任务** - 实时数据接收、批量处理、数据清洗
2. **报表生成任务** - 实时计算、自定义报表、报表导出
3. **数据同步任务** - 平台数据同步、账户信息同步
4. **通知任务** - 邮件、短信、推送通知
5. **定时任务** - 数据归档、预算检查、数据统计

## 架构设计

详细架构文档: [backend/docs/architecture.md](backend/docs/architecture.md)

### 核心架构特点

- **高性能**: FastAPI异步框架 + Redis缓存 + 数据库优化
- **高可用**: 集群部署 + 主从复制 + 自动故障转移
- **实时性**: WebSocket推送 + 异步任务队列
- **安全性**: JWT认证 + OAuth2.0 + 数据加密
- **可扩展**: 微服务架构 + 插件化设计
- **易维护**: 完整的日志 + 监控 + 文档

## 性能指标

### 目标指标
- **API响应时间**: P95 < 200ms, P99 < 500ms
- **并发支持**: 10,000+ QPS
- **系统可用性**: 99.9%
- **数据处理**: 支持千万级数据量
- **实时推送**: 延迟 < 1s

## 开发规范

### 代码规范
- 遵循PEP 8规范
- 使用类型注解
- 编写docstring
- 代码审查制度

### Git规范
- 分支管理策略
- Commit message规范
- Pull Request流程

### API规范
- RESTful风格
- 统一响应格式
- 错误码规范
- 版本控制

## 测试

```bash
# 运行后端测试
cd backend
pytest tests/ --cov=app --cov-report=html

# 运行前端测试
cd frontend
npm run test
```

## 部署

### 开发环境
- 单机部署
- 本地数据库
- 本地缓存

### 测试环境
- Docker容器化
- 测试数据库
- 模拟数据

### 生产环境
- 多节点集群
- 数据库主从
- Redis集群
- 负载均衡

## 监控与运维

### 系统监控
- 应用性能监控（APM）
- 日志收集与分析
- 指标监控
- 告警机制

### 健康检查
- 服务健康检查
- 数据库健康检查
- 缓存健康检查
- 依赖服务检查

## 技术亮点

1. **高性能**: FastAPI异步框架 + Redis缓存 + 数据库优化
2. **高可用**: 集群部署 + 主从复制 + 自动故障转移
3. **实时性**: WebSocket推送 + 异步任务队列
4. **安全性**: JWT认证 + OAuth2.0 + 数据加密
5. **可扩展**: 微服务架构 + 插件化设计
6. **易维护**: 完整的日志 + 监控 + 文档

## 支持的媒体平台

- 抖音巨量引擎
- 快手广告
- 微信朋友圈广告
- 百度信息流
- 腾讯广告
- 今日头条
- Bilibili广告
- 微博广告

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

项目维护者: Echo-2
创建时间: 2026-03-15

---

**当前版本**: 1.0
**最后更新**: 2026-03-15
**维护者**: Echo-2
