# 大模型对话系统 - 快速启动指南

**创建时间**: 2026-03-06 21:30
**目的**: 5 分钟快速启动

---

## 🚀 一键启动（推荐）

### 方法 1: 使用 OpenClaw Gateway（最快）

```bash
# 1. 在当前服务器执行
cd /root/.openclaw/workspace/big-model-chat

# 2. 读取快速指南
cat QUICK_START.md

# 3. 执行一键启动脚本
bash quick-start.sh
```

---

## 🚀 方法 2: 传统方式

### 步骤 1: 启动依赖服务

```bash
# 启动 Redis
redis-server --daemonize yes --port 6379 &

# 启动 MySQL
mysqld --daemonize &

# 启动 Celery Worker
celery -A celery worker.celery \
    --loglevel=info \
    --concurrency=4 \
    --maxtasks-per-child=100 \
    --detach
```

### 步骤 2: 启动 Web 服务

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📊 验证服务

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试 API
curl http://localhost:8000/api/health

# 查看日志
tail -f logs/app.log
```

---

## 🔄 停止服务

```bash
# 使用停止脚本
./stop.sh
```

---

## 📋 故障排除

### 问题 1: 端口被占用
```bash
# 查看进程
netstat -tlnp | grep :8000

# 查杀进程
lsof -i :8000 -t
```

### 问题 2: 数据库连接失败
```bash
# 检查 MySQL
mysqladmin ping

# 检查 Redis
redis-cli ping

# 查看错误日志
tail -f logs/app.log | grep ERROR
```

### 问题 3: 模型调用失败
```bash
# 检查配置
cat .env | grep API

# 查看日志
tail -f logs/app.log | grep API
```

---

## 📞 联系方式

需要帮助？：
1. 查看 QUICK_START.md
2. 查看 README.md
3. 查看 phase1-preparation.md
4. 查看 PHASE1-PLAN.md
5. 查看故障排除文档（待创建）

---

**创建时间**: 2026-03-06 21:30
**状态**: ✅ 快速启动指南已创建
**下一步**: 执行 Phase 1 准备或快速启动
