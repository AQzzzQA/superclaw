#!/bin/bash

# OpenClaw 权限配置可视化工具 - 快速启动脚本
# 快速部署并启动服务

echo "🚀 OpenClaw 权限配置可视化工具 - 快速启动"
echo "============================================"

# 设置工作目录
WORK_DIR="/root/.openclaw/workspace/openclaw-permission-config"

cd "$WORK_DIR"

# 检查是否存在node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    pnpm install
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend && pnpm install && cd ..
fi

# 创建必要目录
mkdir -p logs config/backups config/templates

# 检查服务是否运行
if pgrep -f "node server.js" > /dev/null; then
    echo "⚠️  服务已运行，先停止现有服务..."
    pkill -f "node server.js"
    sleep 2
fi

# 启动后端服务
echo "🚀 启动后端服务..."
nohup node server.js > logs/server.log 2>&1 &
sleep 3

# 检查服务状态
if curl -s http://localhost:8080/api/health > /dev/null; then
    echo "✅ 后端服务启动成功: http://localhost:8080"
    echo "✅ API健康检查: http://localhost:8080/api/health"
else
    echo "❌ 后端服务启动失败，请检查日志: logs/server.log"
    exit 1
fi

# 询问是否启动前端
read -p "是否启动前端开发服务器? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动前端开发服务器..."
    cd frontend
    nohup npm start > ../logs/frontend.log 2>&1 &
    cd ..
    sleep 5
    echo "✅ 前端服务启动成功: http://localhost:3000"
fi

echo ""
echo "============================================"
echo "🎉 快速启动完成！"
echo "============================================"
echo ""
echo "🌐 访问地址:"
echo "  后端API: http://localhost:8080/api/health"
echo "  前端界面: http://localhost:3000"
echo ""
echo "📁 日志文件:"
echo "  后端日志: logs/server.log"
echo "  前端日志: logs/frontend.log"
echo ""
echo "🛑 停止服务:"
echo "  pkill -f 'node server.js'"
echo "  pkill -f 'react-scripts start'"
echo ""
echo "🔍 查看日志:"
echo "  tail -f logs/server.log"
echo "  tail -f logs/frontend.log"
echo ""