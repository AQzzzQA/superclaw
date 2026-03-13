#!/bin/bash

# OpenClaw 权限配置可视化工具 - 部署脚本
# 作者: Echo-2
# 版本: 1.0.0

set -e

echo "🚀 OpenClaw 权限配置可视化工具部署脚本"
echo "📅 部署时间: $(date)"
echo "🔧 脚本版本: 1.0.0"
echo "=================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Node.js版本
check_nodejs() {
    log_info "检查Node.js版本..."
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js未安装，请先安装Node.js 16+"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 16 ]; then
        log_error "Node.js版本过低，需要16+版本，当前版本: $(node -v)"
        exit 1
    fi
    
    log_success "Node.js版本检查通过: $(node -v)"
}

# 检查pnpm
check_pnpm() {
    log_info "检查pnpm..."
    
    if ! command -v pnpm &> /dev/null; then
        log_warning "pnpm未安装，尝试安装..."
        npm install -g pnpm
    fi
    
    log_success "pnpm版本: $(pnpm -v)"
}

# 安装依赖
install_dependencies() {
    log_info "安装项目依赖..."
    
    if [ ! -d "node_modules" ]; then
        log_info "安装后端依赖..."
        pnpm install
    else
        log_info "后端依赖已存在，跳过安装"
    fi
    
    if [ ! -d "frontend/node_modules" ]; then
        log_info "安装前端依赖..."
        cd frontend && pnpm install && cd ..
    else
        log_info "前端依赖已存在，跳过安装"
    fi
    
    log_success "依赖安装完成"
}

# 创建必要目录
create_directories() {
    log_info "创建必要目录..."
    
    mkdir -p logs
    mkdir -p config/backups
    mkdir -p config/templates
    
    log_success "目录创建完成"
}

# 初始化配置文件
init_config() {
    log_info "初始化配置文件..."
    
    if [ ! -f "config/templates.json" ]; then
        log_info "创建默认模板文件..."
        cat > config/templates.json << 'EOF'
[
  {
    "id": "admin-full",
    "name": "完整管理员",
    "description": "拥有所有权限，包括配置管理、用户管理、系统控制等",
    "icon": "crown",
    "color": "#ff4757",
    "category": "administration",
    "permissions": ["*"],
    "role": "admin",
    "is_system": true,
    "created_at": "2026-03-13T00:00:00Z",
    "updated_at": "2026-03-13T00:00:00Z"
  },
  {
    "id": "manager-limited",
    "name": "有限管理员",
    "description": "可以管理用户和配置，但不能修改核心系统设置",
    "icon": "user-shield",
    "color": "#ffa502",
    "category": "administration",
    "permissions": [
      "config:read",
      "config:write",
      "users:read",
      "users:write",
      "templates:read",
      "templates:write"
    ],
    "role": "advanced",
    "is_system": true,
    "created_at": "2026-03-13T00:00:00Z",
    "updated_at": "2026-03-13T00:00:00Z"
  },
  {
    "id": "editor",
    "name": "编辑者",
    "description": "可以查看和编辑配置，但不能管理用户",
    "icon": "edit",
    "color": "#3742fa",
    "category": "content",
    "permissions": [
      "config:read",
      "config:write",
      "templates:read"
    ],
    "role": "normal",
    "is_system": true,
    "created_at": "2026-03-13T00:00:00Z",
    "updated_at": "2026-03-13T00:00:00Z"
  },
  {
    "id": "viewer",
    "name": "观察者",
    "description": "只能查看配置和日志，不能进行修改",
    "icon": "eye",
    "color": "#2ed573",
    "category": "content",
    "permissions": [
      "config:read",
      "logs:read"
    ],
    "role": "readonly",
    "is_system": true,
    "created_at": "2026-03-13T00:00:00Z",
    "updated_at": "2026-03-13T00:00:00Z"
  }
]
EOF
    fi
    
    log_success "配置文件初始化完成"
}

# 检查系统资源
check_resources() {
    log_info "检查系统资源..."
    
    # 检查内存
    TOTAL_MEM=$(free -m | awk 'NR==2{printf "%.1f", $2/1024}')
    AVAILABLE_MEM=$(free -m | awk 'NR==2{printf "%.1f", $7/1024}')
    
    log_info "系统内存: ${TOTAL_MEM}GB 可用: ${AVAILABLE_MEM}GB"
    
    if (( $(echo "$AVAILABLE_MEM < 2.0" | bc -l) )); then
        log_warning "可用内存不足2GB，可能影响性能"
    fi
    
    # 检查磁盘空间
    DISK_USAGE=$(df -h . | awk 'NR==2{print $5}' | sed 's/%//')
    DISK_AVAILABLE=$(df -h . | awk 'NR==2{print $4}')
    
    log_info "磁盘使用率: ${DISK_USAGE}% 可用: ${DISK_AVAILABLE}"
    
    if [ "$DISK_USAGE" -gt 90 ]; then
        log_warning "磁盘使用率过高，建议清理空间"
    fi
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    # 检查服务是否已经运行
    if pgrep -f "node server.js" > /dev/null; then
        log_warning "服务已经在运行，请先停止现有服务"
        read -p "是否要重启服务? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pkill -f "node server.js"
        else
            exit 0
        fi
    fi
    
    # 启动后端服务
    log_info "启动后端服务..."
    nohup node server.js > logs/server.log 2>&1 &
    sleep 3
    
    # 检查后端服务是否启动成功
    if curl -s http://localhost:8080/api/health > /dev/null; then
        log_success "后端服务启动成功: http://localhost:8080"
    else
        log_error "后端服务启动失败，请检查日志: logs/server.log"
        exit 1
    fi
    
    # 启动前端服务（如果需要）
    read -p "是否同时启动前端开发服务器? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "启动前端开发服务器..."
        cd frontend && nohup npm start > ../logs/frontend.log 2>&1 &
        cd ..
        sleep 5
        log_success "前端服务启动成功: http://localhost:3000"
    fi
    
    log_success "所有服务启动完成"
}

# 创建启动脚本
create_startup_scripts() {
    log_info "创建启动脚本..."
    
    # 创建启动脚本
    cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 启动OpenClaw权限配置服务..."
cd /root/.openclaw/workspace/openclaw-permission-config
nohup node server.js > logs/server.log 2>&1 &
echo "✅ 服务已启动: http://localhost:8080"
EOF
    
    # 创建停止脚本
    cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 停止OpenClaw权限配置服务..."
pkill -f "node server.js"
pkill -f "react-scripts start"
echo "✅ 服务已停止"
EOF
    
    # 重启脚本
    cat > restart.sh << 'EOF'
#!/bin/bash
echo "🔄 重启OpenClaw权限配置服务..."
./stop.sh
sleep 2
./start.sh
EOF
    
    chmod +x start.sh stop.sh restart.sh
    log_success "启动脚本创建完成"
}

# 显示部署完成信息
show_deployment_info() {
    echo ""
    echo "=================================="
    echo "🎉 部署完成！"
    echo "=================================="
    echo ""
    echo "📋 服务信息:"
    echo "  后端地址: http://localhost:8080"
    echo "  后端API: http://localhost:8080/api/health"
    echo "  前端地址: http://localhost:3000"
    echo ""
    echo "📁 项目结构:"
    echo "  后端代码: src/"
    echo "  前端代码: frontend/src/"
    echo "  日志文件: logs/"
    echo "  配置文件: config/"
    echo ""
    echo "🛠️  管理命令:"
    echo "  启动服务: ./start.sh"
    echo "  停止服务: ./stop.sh"
    echo "  重启服务: ./restart.sh"
    echo ""
    echo "📖 使用说明:"
    echo "  1. 访问 http://localhost:3000 打开管理界面"
    echo "  2. 使用管理员账户登录"
    echo "  3. 管理QQ用户权限和配置"
    echo ""
    echo "⚠️  注意事项:"
    echo "  - 确保端口8080和3000未被占用"
    echo "  - 建议在生产环境中使用nginx代理"
    echo "  - 定期备份数据和配置文件"
    echo ""
}

# 主函数
main() {
    log_info "开始部署OpenClaw权限配置可视化工具..."
    
    check_nodejs
    check_pnpm
    install_dependencies
    create_directories
    init_config
    check_resources
    create_startup_scripts
    
    read -p "是否立即启动服务? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_services
    fi
    
    show_deployment_info
}

# 运行主函数
main "$@"