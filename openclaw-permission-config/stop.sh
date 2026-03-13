#!/bin/bash

echo "🛑 停止OpenClaw权限配置服务..."
pkill -f "node server.js"
pkill -f "react-scripts start"
pkill -f "npm start"
echo "✅ 服务已停止"