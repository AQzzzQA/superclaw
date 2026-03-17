# AGENTS.md - 子智能体团队

**更新时间**: 2026-03-17 18:50
**智能体数量**: 9个

---

## 🤖 智能体团队

### 1. 代码审查员 📋
**文件**: `AGENTS/Code-Reviewer.md`
**职责**:
- 检查代码质量和规范
- 运行flake8、black、mypy
- 代码风格统一
- 最佳实践检查

**技术栈**:
- flake8（代码规范）
- black（代码格式化）
- mypy（类型检查）
- pylint（代码质量）

---

### 2. 测试工程师 🧪
**文件**: `AGENTS/Test-Engineer.md`
**职责**:
- 编写和运行单元测试
- 测试覆盖率分析
- 集成测试
- E2E测试

**技术栈**:
- pytest（测试框架）
- pytest-cov（覆盖率）
- unittest（标准库）
- mock（模拟）

---

### 3. 文档编写员 📝
**文件**: `AGENTS/Documentation-Writer.md`
**职责**:
- 编写和维护项目文档
- API文档生成
- README更新
- 技术文档翻译

**技术栈**:
- Markdown
- Sphinx（文档生成）
- Swagger UI（API文档）
- GitBook

---

### 4. 安全审计员 🔒
**文件**: `AGENTS/Security-Auditor.md`
**职责**:
- 检查安全漏洞
- 依赖扫描
- 代码安全审查
- 漏洞修复建议

**技术栈**:
- safety（Python依赖扫描）
- bandit（安全漏洞检测）
- npm audit（前端依赖扫描）
- Snyk（漏洞扫描）

---

### 5. Manus专家 🧠
**文件**: `AGENTS/Manus-Expert.md`
**职责**:
- 调用Manus API处理复杂任务
- AI辅助开发
- 智能代码生成
- 复杂问题解决

**技术栈**:
- Manus API
- 大语言模型
- AI辅助编程

---

### 6. Backend-Expert（后端开发专家） ⚙️ 🆕
**文件**: `AGENTS/Backend-Expert.md`
**职责**:
- 后端API开发
- 数据库设计
- 认证和授权
- 异步任务处理
- 性能优化

**技术栈**:
- FastAPI（高性能Web框架）
- SQLAlchemy（ORM框架）
- Alembic（数据库迁移）
- Celery（任务队列）
- Redis（缓存）
- MySQL/PostgreSQL（数据库）
- Pydantic（数据验证）

**专业领域**:
- RESTful API设计
- 数据库优化
- 微服务架构
- 高并发处理
- API安全

---

### 7. FullStack-Expert（全栈开发专家）💻 🆕

---

### 8. Test-Engineer-UI（实操测试工程师）🧪 🆕
**文件**: `AGENTS/FullStack-Expert.md`
**职责**:
- 前端开发（React + TypeScript）
- 后端开发（Node.js/Python）
- 全栈集成
- 前后端联调
- 性能优化

**技术栈**:
- React（前端框架）
- TypeScript（类型安全）
- Ant Design/Material-UI（UI库）
- Next.js（React框架）
- Redux/Zustand（状态管理）
- Node.js/Express（后端）
- Prisma/Sequelize（ORM）
- PostgreSQL/MongoDB（数据库）
- Docker（容器化）

**专业领域**:
- 全栈架构设计
- 前后端分离
- 实时通讯（WebSocket）
- 前端性能优化
- 全栈测试

---

### 9. Frontend-Tester（前端测试专家）🧪 🆕
**文件**: `AGENTS/Frontend-Tester.md`
**职责**:
- 使用浏览器自动化工具测试前端应用
- 发现前端功能问题和UI/UX问题
- 协调后端开发修复API相关问题
- 向高级领导汇报无法独立解决的问题
- 生成详细测试报告

**技术栈**:
- Agent Browser（OpenClaw 内置浏览器自动化）
- Selenium WebDriver（备用方案）
- Playwright（备用方案）
- Puppeteer（备用方案）

**专业领域**:
- 自动化UI测试
- API集成测试
- 视觉回归测试
- 问题追踪和分级
- 跨智能体协作

---

## 🎯 智能体协作

### 典型项目流程

```
项目开始
    ↓
[Backend-Expert] 设计后端架构
    ↓
[Backend-Expert] 开发后端API
    ↓
[FullStack-Expert] 开发前端界面
    ↓
[Test-Engineer] 编写单元测试
    ↓
[Code-Reviewer] 代码审查
    ↓
[Security-Auditor] 安全审计
    ↓
[Documentation-Writer] 编写文档
    ↓
项目完成
```

### 协作场景

#### 场景1: 新项目开发
1. **Backend-Expert**: 设计数据库Schema和API接口
2. **Backend-Expert**: 实现后端核心功能
3. **FullStack-Expert**: 开发前端界面和组件
4. **Test-Engineer**: 编写单元测试和集成测试
5. **Code-Reviewer**: 审查代码质量
6. **Security-Auditor**: 进行安全审计
7. **Documentation-Writer**: 编写项目文档

#### 场景2: Bug修复
1. **Backend-Expert**: 定位和修复后端Bug
2. **FullStack-Expert**: 修复前端Bug
3. **Test-Engineer**: 编写回归测试
4. **Code-Reviewer**: 审查修复代码

#### 场景3: 性能优化
1. **Backend-Expert**: 优化后端性能（数据库查询、缓存）
2. **FullStack-Expert**: 优化前端性能（代码分割、懒加载）
3. **Test-Engineer**: 进行性能测试
4. **Documentation-Writer**: 更新性能优化文档

---

## 📋 智能体调用

### 调用方式

```python
# 调用Backend-Expert
invoke_agent("Backend-Expert", "设计用户认证API")

# 调用FullStack-Expert
invoke_agent("FullStack-Expert", "开发商品列表页面")

# 调用Code-Reviewer
invoke_agent("Code-Reviewer", "审查backend/app/api/v1/users.py")

# 调用Test-Engineer
invoke_agent("Test-Engineer", "为用户API编写单元测试")
```

### 自动触发

- 代码提交后自动触发Code-Reviewer
- PR创建后自动触发Security-Auditor
- 功能开发完成后自动触发Test-Engineer
- API更新后自动触发Documentation-Writer

---

## 🎓 智能体能力矩阵

| 智能体 | 代码审查 | 测试 | 文档 | 安全 | 后端 | 前端 | 浏览器测试 |
|---------|---------|------|------|------|------|------|-----------|
| Code-Reviewer | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| Test-Engineer | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Documentation-Writer | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| Security-Auditor | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Manus-Expert | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Backend-Expert | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| FullStack-Expert | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Frontend-Tester | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚀 未来扩展

### 计划添加的智能体

1. **DevOps-Expert**: CI/CD、容器化、自动化部署
2. **UI/UX-Designer**: 界面设计、用户体验优化
3. **Data-Scientist**: 数据分析、机器学习
4. **Mobile-Expert**: 移动端开发（iOS/Android）
5. **Performance-Expert**: 性能优化、负载测试

---

**更新时间**: 2026-03-17 18:50
**智能体总数**: 9个
**版本**: V3.0
**状态**: ✅ 完整团队已组建（含前端测试专家）
