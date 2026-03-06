#!/bin/bash

# LemClaw - OpenClaw 授权网关启动脚本

echo "🚀 LemClaw - OpenClaw 授权网关启动脚本"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  未找到 .env 文件，从 .env.example 复制..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo "⚠️  请编辑 .env 文件，设置 OPENCLAW_GATEWAY_URL 和 GATEWAY_TOKEN"
    echo ""
    echo "编辑完成后，重新运行此脚本"
    exit 0
fi

# 启动服务器
echo ""
echo "🔧 启动服务器..."
echo "📍 服务地址: http://localhost:8089"
echo "📄 前端页面: http://localhost:8089/index.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 后台运行服务器
nohup python3 app.py > server.log 2>&1 &
SERVER_PID=$!

echo "✅ 服务器已启动 (PID: $SERVER_PID)"
echo ""
echo "📋 日志文件: server.log"
echo "🔍 查看日志: tail -f server.log"
echo "⏹️  停止服务器: kill $SERVER_PID"

# 等待服务器启动
sleep 3

# 检查服务器状态
if ps -p $SERVER_PID > /dev/null; then
    echo ""
    echo "✅ 服务器运行正常！"
    echo ""
    echo "现在可以运行以下命令生成授权码："
    echo "  python3 generate_codes.py"
else
    echo ""
    echo "❌ 服务器启动失败，请查看 server.log 了解详情"
    exit 1
fi
