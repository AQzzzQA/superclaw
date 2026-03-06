#!/bin/bash

# LemClaw - OpenClaw 授权网关停止脚本

echo "🛑 LemClaw - OpenClaw 授权网关停止脚本"
echo "================================"

# 查找并停止服务器进程
PIDS=$(ps aux | grep "python3 app.py" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✅ 没有运行中的服务器进程"
    exit 0
fi

echo "找到以下进程："
echo "$PIDS"
echo ""

# 停止进程
for PID in $PIDS; do
    kill $PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ 已停止进程 $PID"
    else
        echo "❌ 停止进程 $PID 失败"
    fi
done

# 等待进程完全停止
sleep 2

# 再次检查
PIDS=$(ps aux | grep "python3 app.py" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo ""
    echo "✅ 所有进程已成功停止"
else
    echo ""
    echo "⚠️  仍有进程运行中："
    echo "$PIDS"
    echo "请手动停止: kill -9 $PIDS"
fi
