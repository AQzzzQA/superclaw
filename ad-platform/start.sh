#!/bin/bash

# Ad Platform 启动脚本

echo "====================================="
echo "  Ad Platform 启动脚本"
echo "====================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：.env 文件不存在，请先创建并配置环境变量"
    cp .env.example .env
    echo "已创建 .env 文件，请编辑并填入正确的配置"
    exit 1
fi

# 执行数据库迁移
echo "执行数据库迁移..."
alembic upgrade head

# 启动服务
echo "启动服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
