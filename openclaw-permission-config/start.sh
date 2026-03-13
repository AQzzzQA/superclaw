#!/bin/bash

echo "🚀 启动OpenClaw权限配置服务..."
cd /root/.openclaw/workspace/openclaw-permission-config

# 停止已运行的服务
pkill -f "node server.js"
sleep 2

# 启动服务在端口8899
export PORT=8899
nohup node server.js > logs/server.log 2>&1 &
sleep 3

# 检查服务是否启动成功
if curl -s http://localhost:8899/api/health > /dev/null; then
    echo "✅ 后端服务启动成功: http://localhost:8899"
    echo "✅ API健康检查: http://localhost:8899/api/health"
    echo "✅ 前端地址: http://localhost:8899"
else
    echo "❌ 服务启动失败，请检查日志: logs/server.log"
    exit 1
fi

echo "🎉 所有服务启动完成！"