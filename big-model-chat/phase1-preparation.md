# 大模型对话系统 - 准备工作

**创建时间**: 2026-03-06 21:25
**目的**: 为自研大模型进行基础准备

---

## 🎯 阶段 1: 环境搭建（1 周）

### 1. 硬件准备

```bash
# 创建项目目录
cd ~/big-model-chat
mkdir -p {api,atabase,services,models,static,logs,tests,docs}

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 创建依赖文件
cat > requirements.txt << 'EOF'
# Web 框架
fastapi>=0.104.1
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
python-multipart>=0.0.5
sqlalchemy>=2.0.0
redis>=5.0.0
celery>=5.3.0
python-dotenv>=1.0.0

# AI 工具
openai>=1.3.0
tiktoken>=0.5.1
anthropic>=0.18.0
cohere>=4.41.0

# 数据验证
pydantic-settings>=2.0.0
email-validator>=2.1.0
pymysql-connector>=8.0.34
# 后台任务
celery[redis]>=2.5.0
flower>=2.0.1

# 监控和日志
prometheus-client>=0.18.0
sentry-sdk>=1.39.0
loguru>=0.7.0
python-json-logger>=2.0.0
EOF

# 创建环境变量
cat > .env.example << 'EOF'
# 服务配置
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=INFO

# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost/big_model_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# OpenClaw Gateway 配置
OPENCLAW_URL=http://localhost:18789
OPENCLAW_TOKEN=your_token_here

# 模型配置（示例）
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
COHERE_API_KEY=sk-...
# 模型选择
DEFAULT_MODEL=gpt-4
MODE=fast-api  # fast-api | direct | proxy
EOF

# 创建启动脚本
cat > start.sh << 'EOF'
#!/bin/bash

echo "=========================================="
echo "大模型对话系统启动"
echo "=========================================="
echo ""

# 加载环境变量
export \$(cat .env | grep -v '^')

# 启动 Redis
echo "🔥 启动 Redis..."
redis-server --daemonize yes --port 6379 &
REDIS_PID=$!
sleep 2

# 启动 MySQL
echo "🔥 启动 MySQL..."
mysqld --daemonize &
MYSQL_PID=$!
sleep 2

# 启动 Celery Worker
echo "🚀 启动 Celery Worker..."
celery -A celery worker.celery \
    --loglevel=info \
    --concurrency=4 \
    --maxtasks-per-child=100 \
    --loglevel=info \
    --pidfile /tmp/celery.pid \
    --detach

echo "✅ 后端服务已启动！"
echo ""
echo "启动 Web 服务..."
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
EOF

chmod +x start.sh

# 创建停止脚本
cat > stop.sh << 'EOF'
#!/bin/bash

echo "=========================================="
echo "大模型对话系统停止"
echo "=========================================="
echo ""

# 停止服务
echo "🛑 停止 Web 服务..."
pkill -f "uvicorn.*main:app"

# 停止 Celery
echo "🚀 停止 Celery Worker..."
if [ -f /tmp/celery.pid ]; then
    kill $(cat /tmp/celery.pid)
fi

# 停止 Redis
echo "🔥 停止 Redis..."
if [ ! -z "$REDIS_PID" ]; then
    redis-cli shutdown
fi

# 停止 MySQL
echo "🔥 停止 MySQL..."
kill -9 $MYSQL_PID 2>/dev/null

echo "✅ 所有服务已停止！"
EOF

chmod +x stop.sh

# 创建监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash

echo "=========================================="
echo "大模型对话系统监控"
echo "=========================================="
echo ""

echo ""
echo "🌐 网络状态："
echo "=========================================="
curl -s http://localhost:8000/health || echo "❌ 服务未运行"

echo ""
echo "🔥 数据库状态："
echo "=========================================="
redis-cli ping
mysqladmin -e "SELECT 1" 2>/dev/null

echo ""
echo "📊 系统资源："
echo "=========================================="
echo "CPU: $(nproc)"
echo "内存: $(free -h | grep Mem | awk '{print $2"/" / " /" ($3/$2" * 100)" / " /")'
echo "磁盘: $(df -h / | tail -n 1 | awk '{print $5"/" / " /" ($3/$5" * 100)" / " /")'

echo ""
echo "📊 服务进程："
echo "=========================================="
ps aux | grep -E "(uvicorn|celery|redis|mysql)" | head -5

echo ""
echo "=========================================="
EOF

chmod +x monitor.sh
EOF
echo "✅ 准备工作脚本已创建！"
EOF
