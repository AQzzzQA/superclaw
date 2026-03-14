# Changelog

All notable changes to the Ad Platform project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 自动化代码健康检查框架
- 问题跟踪机制 (TODO.md)
- 智能体自我增强任务 (HEARTBEAT.md)
- 代码规范配置 (.flake8, .black)

### Changed
- 增强了项目监控和维护能力

---

## [2.0.0] - 2026-03-01

### Added
- **Phase 3: V2.0 企业级功能**
  - 用户管理 API (CRUD)
  - 角色权限管理 API (RBAC)
  - 操作日志 API (审计)
  - 系统配置管理 API
  - Phase 2+3 单元测试
  - 集成测试

### Changed
- 从 MVP 升级为企业级平台
- 完整的权限管理体系

---

## [1.2.0] - 2026-03-01

### Added
- **Phase 2: V1.2 智能化功能**
  - Celery 异步任务队列
  - 转化回传异步化
  - 报表生成异步化
  - 数据导出异步化
  - 自动出价算法 (ROI 计算)
  - A/B 测试框架
  - 多种归因模型
  - 异步任务监控

### Changed
- 引入异步处理能力
- 提升系统性能和可扩展性

---

## [1.1.0] - 2026-02-28

### Added
- **Phase 1: V1.1 基础优化和核心功能**
  - 批量操作 API (启用/暂停、编辑)
  - 数据导出 API (Excel/CSV)
  - 批量上传转化 API
  - 统一响应格式
  - 自定义异常处理
  - 配置管理
  - 请求日志中间件
  - 请求 ID 中间件
  - 限流中间件
  - 错误处理中间件
  - 健康检查和监控
  - 数据可视化 (ECharts)
  - Zustand 状态管理
  - 单元测试

### Changed
- 优化代码结构和响应格式
- 完善中间件体系

---

## [1.0.0] - 2026-02-28

### Added
- **初始版本: MVP**
  - FastAPI 后端架构
  - React + TypeScript + Ant Design 前端
  - 用户认证 (JWT Token)
  - OAuth2 授权
  - 账户管理
  - 广告计划管理
  - 广告组管理
  - 创意管理
  - 数据报表
  - 转化回传
  - Docker 支持
  - 数据库迁移 (Alembic)

---

## Versioning

- **Major (X.0.0)**: 破坏性变更，架构重构
- **Minor (0.X.0)**: 新功能，向下兼容
- **Patch (0.0.X)**: Bug 修复，小改进
