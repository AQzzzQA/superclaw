#!/bin/bash

# LemClaw 服务监控脚本

SERVER_DIR="/root/.openclaw/workspace/LemClaw"
LOG_FILE="$SERVER_DIR/server.log"
PID_FILE="$SERVER_DIR/app.pid"

echo "📊 LemClaw 服务监控"
echo "======================"

# 检查进程
PID=$(ps aux | grep "python3 app.py" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "❌ 服务未运行"
    echo "🔄 正在重启..."

    cd "$SERVER_DIR"
    nohup python3 app.py > server.log 2>&1 &
    sleep 3

    # 再次检查
    NEW_PID=$(ps aux | grep "python3 app.py" | grep -v grep | awk '{print $2}')
    if [ -n "$NEW_PID" ]; then
        echo "✅ 服务已重启 (PID: $NEW_PID)"
    else
        echo "❌ 重启失败"
        exit 1
    fi
else
    echo "✅ 服务运行中 (PID: $PID)"

    # 测试健康检查
    HEALTH=$(curl -s http://localhost:8089/health --max-time 5)
    if [ $? -eq 0 ]; then
        echo "✅ 健康检查通过"
    else
        echo "❌ 健康检查失败"
    fi
fi

echo ""
echo "📋 服务信息："
echo "  - 进程 ID: $PID"
echo "  - 日志文件: $LOG_FILE"
echo "  - 访问地址: http://43.156.131.98:8089/"
echo ""
echo "🔍 查看日志："
echo "  tail -f $LOG_FILE"
echo ""
echo "🛑 停止服务："
echo "  pkill -f 'python3 app.py'"
