# SuperClaw 架构设计

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                   Web 层（前端）                      │
│  - React + TypeScript + Ant Design                    │
│  - 实时任务看板                                     │
│  - 监控仪表盘                                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────────┐
│               API 网关层（Nginx）                    │
│  - 反向代理                                         │
│  - SSL 终止                                          │
│  - 负载均衡                                         │
│  - 限流与熔断                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│            应用层（FastAPI）                          │
│  - RESTful API                                       │
│  - WebSocket 支持                                    │
│  - 认证与授权                                        │
└────┬───────────────────┬───────────────────┬───────────┘
     │                   │                   │
┌────▼────┐        ┌────▼────┐       ┌────▼────┐
│编排引擎  │        │ 记忆系统  │       │ 监控系统  │
├─────────┤        ├─────────┤       ├─────────┤
│任务管理  │        │向量存储  │       │指标收集  │
│工作流引擎│        │全文搜索  │       │告警规则  │
│智能体调度│        │TTL 管理 │       │报表生成  │
└────┬────┘        └────┬────┘       └────┬────┘
     │                   │                   │
┌────▼───────────────────▼───────────────────▼────────┐
│              LemClaw 集成层                          │
│  - 模型池管理                                       │
│  - API 路由                                        │
│  - 请求聚合                                         │
│  - 成本追踪                                         │
└────┬───────────────────────────────────────────────────────┘
     │
┌────▼──────────────────────┬───────────────────────────┐
│   专业智能体池           │      基础设施层         │
├───────────────────────────┼───────────────────────────┤
│ • 代码审查员           │  • PostgreSQL (数据）     │
│ • 测试工程师           │  • Redis (缓存）         │
│ • 数据分析师           │  • MinIO (文件存储）      │
│ • 内容创作者           │  • Prometheus (监控）     │
│ • 安全审计员           │  • Grafana (可视化）      │
└───────────────────────────┴───────────────────────────┘
```

---

## 🔄 核心组件

### 1. 智能体编排引擎

#### 任务管理器 (TaskManager)
```python
class TaskManager:
    def create_task(self, task_data):
        """创建新任务"""
    
    def get_task(self, task_id):
        """获取任务详情"""
    
    def update_task_status(self, task_id, status):
        """更新任务状态"""
    
    def list_tasks(self, filters):
        """查询任务列表"""
```

#### 工作流引擎 (WorkflowEngine)
```python
class WorkflowEngine:
    def create_workflow(self, steps):
        """创建工作流"""
    
    def execute_workflow(self, workflow_id):
        """执行工作流"""
    
    def pause_workflow(self, workflow_id):
        """暂停工作流"""
    
    def resume_workflow(self, workflow_id):
        """恢复工作流"""
```

#### 智能体调度器 (AgentScheduler)
```python
class AgentScheduler:
    def schedule_task(self, task):
        """调度任务到智能体"""
    
    def parallel_execute(self, tasks):
        """并行执行任务"""
    
    def serial_execute(self, tasks):
        """串行执行任务"""
```

---

### 2. 记忆系统

#### 向量存储 (VectorStore)
```python
class VectorStore:
    def store_memory(self, memory_data):
        """存储记忆向量"""
    
    def search_similar(self, query, top_k=5):
        """相似度搜索"""
    
    def delete_memory(self, memory_id):
        """删除记忆"""
```

#### 全文搜索 (FullTextSearch)
```python
class FullTextSearch:
    def index_memory(self, memory_data):
        """建立全文索引"""
    
    def search(self, query):
        """全文搜索"""
    
    def update_index(self):
        """更新索引"""
```

---

### 3. LemClaw 集成层

#### 模型路由器 (ModelRouter)
```python
class ModelRouter:
    def select_model(self, task_type, budget):
        """选择最优模型"""
    
    def balance_load(self):
        """负载均衡"""
    
    def failover(self, model_id):
        """故障转移"""
```

#### 成本追踪器 (CostTracker)
```python
class CostTracker:
    def track_usage(self, model_id, tokens):
        """追踪使用量"""
    
    def calculate_cost(self, usage_data):
        """计算成本"""
    
    def get_bill(self, period):
        """生成账单"""
```

---

### 4. 监控系统

#### 指标收集器 (MetricsCollector)
```python
class MetricsCollector:
    def collect_task_metrics(self, task_id):
        """收集任务指标"""
    
    def collect_system_metrics(self):
        """收集系统指标"""
    
    def collect_agent_metrics(self, agent_id):
        """收集智能体指标"""
```

#### 告警引擎 (AlertEngine)
```python
class AlertEngine:
    def evaluate_rules(self, metrics):
        """评估告警规则"""
    
    def send_alert(self, alert_data):
        """发送告警"""
    
    def manage_escalation(self, alert_id):
        """管理告警升级"""
```

---

## 🗄️ 数据库设计

### 核心表结构

#### tasks 表（任务表）
```sql
CREATE TABLE tasks (
    id BIGSERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    parameters JSONB,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration DECIMAL(10, 2),
    priority VARCHAR(20),
    parent_task_id BIGINT REFERENCES tasks(id)
);
```

#### workflows 表（工作流表）
```sql
CREATE TABLE workflows (
    id BIGSERIAL PRIMARY KEY,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    steps JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

#### memories 表（记忆表）
```sql
CREATE TABLE memories (
    id BIGSERIAL PRIMARY KEY,
    memory_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT[],
    importance VARCHAR(20),
    vector_embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ttl_seconds INTEGER
);
```

#### agents 表（智能体表）
```sql
CREATE TABLE agents (
    id BIGSERIAL PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    capabilities JSONB,
    status VARCHAR(20),
    last_active_at TIMESTAMP
);
```

---

## 🔐 安全架构

### 认证与授权

```
┌──────────────┐
│   客户端      │
└──────┬───────┘
       │ JWT Token
┌──────▼────────┐
│  API 网关     │
└──────┬────────┘
       │ 验证 Token
┌──────▼────────┐
│  认证服务     │
└──────┬────────┘
       │ 用户信息
┌──────▼────────┐
│  数据库       │
└───────────────┘
```

#### 权限模型

```python
class Permission:
    CREATE_TASK = "create_task"
    READ_TASK = "read_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    MANAGE_AGENTS = "manage_agents"
    VIEW_LOGS = "view_logs"

class Role:
    ADMIN = "admin"           # 所有权限
    USER = "user"             # 基本权限
    VIEWER = "viewer"          # 只读权限
```

---

### 数据加密

- **传输加密**：TLS 1.3
- **存储加密**：AES-256（敏感数据）
- **Token 加密**：SHA-256 哈希
- **密钥管理**：使用环境变量

---

## 📊 性能优化

### 缓存策略

```python
class CacheManager:
    def cache_task_result(self, task_id, result, ttl=3600):
        """缓存任务结果"""
    
    def get_cached_result(self, task_id):
        """获取缓存结果"""
    
    def invalidate_cache(self, pattern):
        """失效缓存"""
```

---

### 数据库优化

- **索引优化**：为常用查询字段创建索引
- **连接池**：使用连接池减少连接开销
- **查询优化**：使用 EXPLAIN 分析查询性能
- **分区表**：按时间分区大表

---

## 🔄 高可用设计

### 负载均衡

```
┌─────────────┐
│   客户端    │
└──────┬─────┘
       │
┌──────▼────────────────────────────┐
│      Nginx 负载均衡器          │
└────┬────────┬────────┬────────┘
     │        │        │
┌────▼──┐ ┌─▼────┐ ┌─▼────┐
│实例 1  │ │实例 2 │ │实例 3 │
└───────┘ └───────┘ └───────┘
```

---

### 故障转移

```python
class FailoverManager:
    def health_check(self, instance_id):
        """健康检查"""
    
    def trigger_failover(self, failed_instance):
        """触发故障转移"""
    
    def restore_instance(self, instance_id):
        """恢复实例"""
```

---

## 📚 文档索引

- [快速入门](getting-started.md)
- [API 参考](api-reference.md)
- [部署指南](deployment.md)
- [智能体开发](agent-development.md)
- [LemClaw 集成](lemclaw-integration.md)

---

**最后更新**: 2026-03-08
