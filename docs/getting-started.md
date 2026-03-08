# SuperClaw 快速入门指南

## 🎯 5 分钟快速开始

### 1. 安装 SuperClaw

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

SuperClaw 将在 `http://localhost:8000` 启动。

---

### 2. 创建第一个任务

#### 2.1 通过 Web 界面

1. 打开浏览器访问 `http://localhost:8000`
2. 点击"创建任务"
3. 选择智能体类型（如：代码审查员）
4. 输入任务参数
5. 点击"执行"

#### 2.2 通过 API

```python
import requests

# 创建任务
response = requests.post(
    "http://localhost:8000/api/v1/tasks",
    json={
        "task_name": "代码审查",
        "agent_type": "code_reviewer",
        "parameters": {
            "code_path": "/path/to/code"
        }
    }
)

print(response.json())
```

---

## 🚀 核心功能演示

### 示例 1：并行执行多个任务

```python
from superclaw import AgentOrchestrator

# 初始化
orchestrator = AgentOrchestrator()

# 创建并行任务
tasks = [
    orchestrator.create_task("代码审查", agent="code_reviewer"),
    orchestrator.create_task("测试覆盖", agent="test_engineer"),
    orchestrator.create_task("文档生成", agent="doc_writer")
]

# 并行执行
results = orchestrator.run_parallel(tasks)

# 查看结果
for result in results:
    print(f"{result.task_name}: {result.status} - {result.duration}s")
```

---

### 示例 2：串行工作流

```python
# 创建工作流
workflow = orchestrator.create_workflow([
    {"task": "代码审查", "agent": "code_reviewer"},
    {"task": "运行测试", "agent": "test_engineer", "depends_on": ["代码审查"]},
    {"task": "生成报告", "agent": "data_analyst", "depends_on": ["运行测试"]}
])

# 执行工作流
result = workflow.run()
print(result.summary)
```

---

### 示例 3：存储和检索记忆

```python
# 存储记忆
orchestrator.memory.store(
    content="修复边界条件 bug 的经验",
    tags=["bug_fix", "boundary_conditions"],
    importance="high"
)

# 检索记忆
memories = orchestrator.memory.search(
    query="边界条件",
    tags=["bug_fix"],
    limit=5
)

for mem in memories:
    print(f"{mem.content} (相关性: {mem.relevance})")
```

---

## 🧪 测试与验证

### 单元测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_orchestrator.py

# 查看覆盖率
pytest --cov=superclaw --cov-report=html
```

---

### 集成测试

```bash
# 启动测试环境
docker-compose -f docker-compose.test.yml up -d

# 运行集成测试
pytest tests/integration/

# 清理测试环境
docker-compose -f docker-compose.test.yml down
```

---

## 🔧 配置说明

### 环境变量

创建 `.env` 文件：

```bash
# 必需配置
DB_HOST=localhost
DB_NAME=superclaw
DB_USER=superclaw
DB_PASSWORD=your_password

# 可选配置
REDIS_HOST=localhost
REDIS_PORT=6379

# LemClaw 配置
LEMCLAW_API_URL=https://api.lemclaw.com
LEMCLAW_API_KEY=your_api_key

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/superclaw.log
```

---

## 📊 监控与调试

### 查看日志

```bash
# 实时日志
tail -f logs/superclaw.log

# 搜索错误
grep "ERROR" logs/superclaw.log

# 查看最近 100 行
tail -n 100 logs/superclaw.log
```

---

### 健康检查

```bash
# 基础健康检查
curl http://localhost:8000/health

# 详细健康检查
curl http://localhost:8000/health/detailed
```

---

## 💡 最佳实践

### 1. 任务设计

- ✅ **明确目标**：清晰定义每个任务的期望输出
- ✅ **合理拆分**：将大任务拆分成小任务，提高并行度
- ✅ **设置超时**：为每个任务设置合理的超时时间
- ✅ **错误处理**：定义任务失败后的处理策略

### 2. 记忆管理

- ✅ **结构化存储**：使用标签和分类，便于检索
- ✅ **定期清理**：删除过期或不相关的记忆
- ✅ **版本控制**：重要记忆保留多个版本

### 3. 性能优化

- ✅ **批量操作**：减少 API 调用次数
- ✅ **缓存结果**：缓存常用查询结果
- ✅ **异步执行**：使用异步处理提升响应速度

---

## 📚 下一步

- [阅读完整 API 文档](api-reference.md)
- [了解部署指南](deployment.md)
- [查看架构设计](architecture.md)
- [加入社区讨论](https://github.com/AQzzzQA/superclaw/discussions)

---

## 🆘 需要帮助？

- **文档**: https://docs.superclaw.ai
- **GitHub Issues**: https://github.com/AQzzzQA/superclaw/issues
- **Discord**: https://discord.gg/superclaw

---

**祝您使用愉快！** 🚀

**最后更新**: 2026-03-08
