#!/bin/bash

# 权限系统一键修复脚本
# 用途: 修复Docker部署空白页面和容器启动问题
# 作者: Echo-2
# 时间: 2026-03-16

set -e

echo "🔧 权限系统一键修复脚本"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ 错误: 请在项目根目录运行此脚本${NC}"
    echo "   当前目录: $(pwd)"
    exit 1
fi

# 停止所有容器
echo -e "${YELLOW}🛑 停止容器...${NC}"
docker-compose down -v || true

# 清理缓存
echo -e "${YELLOW}🧹 清理Docker缓存...${NC}"
docker system prune -f --volumes || true

echo ""

# 备份原配置
if [ -f "docker-compose.yml" ]; then
    echo -e "${YELLOW}📦 备份原配置...${NC}"
    cp docker-compose.yml docker-compose.yml.backup
fi

# 创建修复后的docker-compose.yml
echo -e "${YELLOW}📝 创建修复后的配置...${NC}"
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: permissions_db
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-permissions}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: permissions_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build: ./backend
    container_name: permissions_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-postgres}@db:5432/${DB_NAME:-permissions}
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY:-your-secret-key}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    container_name: permissions_frontend
    ports:
      - "3000:5173"
    environment:
      VITE_API_URL: ${VITE_API_URL:-http://localhost:8000}
    depends_on:
      - backend
    command: npm run dev -- --host 0.0.0.0 --port 5173

volumes:
  postgres_data:
EOF

# 创建.env文件（如果不存在）
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📄 创建环境变量文件...${NC}"
    cat > .env << 'EOF'
# 数据库配置
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=permissions

# 后端配置
SECRET_KEY=your-secret-key-change-this-in-production

# 前端配置
VITE_API_URL=http://localhost:8000
EOF
fi

echo ""

# 重新构建并启动
echo -e "${YELLOW}🚀 重新构建并启动容器...${NC}"
docker-compose up --build -d

echo ""

# 等待服务启动
echo -e "${YELLOW}⏳ 等待服务启动（10秒）...${NC}"
for i in {10..1}; do
    echo -ne "   $i 秒...\r"
    sleep 1
done
echo ""

# 检查服务状态
echo -e "${GREEN}📊 检查服务状态:${NC}"
docker-compose ps

echo ""

# 检查容器健康状态
echo -e "${GREEN}🏥 检查健康状态:${NC}"
for container in db redis backend frontend; do
    status=$(docker-compose ps -q $container | xargs docker inspect --format='{{.State.Health.Status}}' 2>/dev/null || echo "no-healthcheck")
    if [ "$status" = "healthy" ] || [ "$container" = "frontend" ]; then
        echo -e "   ${GREEN}✓${NC} $container: 运行正常"
    else
        echo -e "   ${RED}✗${NC} $container: $status"
    fi
done

echo ""

# 测试服务连接
echo -e "${GREEN}🔍 测试服务连接:${NC}"

# 测试后端
echo -n "   测试后端API (http://localhost:8000)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200"; then
    echo -e " ${GREEN}✓ 正常${NC}"
else
    echo -e " ${RED}✗ 失败${NC}"
fi

# 测试前端
echo -n "   测试前端 (http://localhost:3000)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo -e " ${GREEN}✓ 正常${NC}"
else
    echo -e " ${RED}✗ 失败（可能需要更多时间启动）${NC}"
fi

echo ""

# 显示访问地址
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ 修复完成！${NC}"
echo ""
echo -e "📌 访问地址:"
echo -e "   ${GREEN}前端:${NC}   http://localhost:3000"
echo -e "   ${GREEN}后端:${NC}   http://localhost:8000/docs"
echo -e "   ${GREEN}数据库:${NC}  postgresql://postgres:postgres@localhost:5432/permissions"
echo ""
echo -e "📝 常用命令:"
echo "   查看日志: ${YELLOW}docker-compose logs -f${NC}"
echo "   查看状态: ${YELLOW}docker-compose ps${NC}"
echo "   停止服务: ${YELLOW}docker-compose down${NC}"
echo "   重启服务: ${YELLOW}docker-compose restart${NC}"
echo ""
echo -e "⚠️  注意事项:"
echo "   1. 如果前端仍然空白，请等待1-2分钟后刷新"
echo "   2. 查看完整日志: ${YELLOW}docker-compose logs frontend${NC}"
echo "   3. 原配置已备份到: ${YELLOW}docker-compose.yml.backup${NC}"
echo ""
echo -e "🔧 如果问题仍然存在，请运行:"
echo -e "   ${YELLOW}docker-compose logs > debug-logs.txt${NC}"
echo "   然后发送 ${YELLOW}debug-logs.txt${NC} 进行分析"
echo ""
