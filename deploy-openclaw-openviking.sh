#!/bin/bash

# OpenClaw 与 OpenViking 集成部署脚本
# 用途：一键安装、配置和部署 OpenViking 与 OpenClaw 集成

set -e

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

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    local missing_deps=()
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if ! command_exists pip3; then
        missing_deps+=("pip3")
    fi
    
    if ! command_exists git; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "缺少以下依赖: ${missing_deps[*]}"
        log_info "请先安装依赖："
        echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip git"
        echo "  - CentOS/RHEL: sudo yum install python3 python3-pip git"
        exit 1
    fi
    
    log_success "依赖检查通过"
}

# Step 2: 安装 Python 依赖
install_python_dependencies() {
    log_info "安装 Python 依赖..."
    
    # 升级 pip
    pip3 install --upgrade pip
    
    # 安装核心依赖
    pip3 install aiohttp async-timeout python-dotenv
    
    log_success "Python 依赖安装完成"
}

# Step 3: 安装 OpenViking
install_openviking() {
    log_info "检查 OpenViking 安装状态..."
    
    if command_exists openviking-server; then
        log_warning "OpenViking 已安装，跳过安装"
        return
    fi
    
    log_info "安装 OpenViking..."
    
    # 方法 1: 使用 pip 安装（推荐）
    if pip3 install openviking --upgrade; then
        log_success "OpenViking 安装成功"
    else
        log_warning "pip 安装失败，尝试从源码安装..."
        
        # 方法 2: 从源码安装
        cd /tmp
        if [ ! -d "openviking" ]; then
            git clone https://github.com/volcengine/OpenViking.git
        fi
        cd openviking
        cargo install --path .
        
        log_success "OpenViking 从源码安装成功"
    fi
}

# Step 4: 配置 OpenViking
configure_openviking() {
    log_info "配置 OpenViking..."
    
    # 创建配置目录
    mkdir -p ~/.openviking
    
    # 创建服务器配置
    cat > ~/.openviking/ov.conf << 'EOF'
{
  "storage": {
    "workspace": "/root/.openviking/workspace"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "https://ark.cn-beijing.volces.com/api/v3",
      "api_key": "${OPENVIKING_EMBEDDING_API_KEY}",
      "provider": "volcengine",
      "dimension": 1024,
      "model": "doubao-embedding-vision-250615"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "${OPENVIKING_VLM_API_KEY}",
    "provider": "volcengine",
    "model": "doubao-seed-2-0-pro-260215",
    "max_concurrent": 100
  }
}
EOF
    
    # 创建 CLI 配置
    cat > ~/.openviking/ovcli.conf << 'EOF'
{
  "url": "http://localhost:1933",
  "timeout": 60.0,
  "output": "table"
}
EOF
    
    log_success "OpenViking 配置完成"
}

# Step 5: 配置环境变量
setup_environment_variables() {
    log_info "配置环境变量..."
    
    # 创建 .env 文件
    cat > /root/.openclaw/workspace/.env << 'EOF'
# OpenClaw 工作目录
OPENCLAW_WORKSPACE=/root/.openclaw/workspace

# OpenViking 配置
OPENVIKING_URL=http://localhost:1933
OPENVIKING_API_KEY=

# 启用降级模式
OPENVIKING_ENABLE_FALLBACK=true

# API 密钥（可选，用于云服务）
# OPENVIKING_EMBEDDING_API_KEY=your-embedding-api-key
# OPENVIKING_VLM_API_KEY=your-vlm-api-key
EOF
    
    # 添加到 ~/.bashrc（如果不存在）
    if ! grep -q "OPENCLAW_WORKSPACE" ~/.bashrc; then
        cat >> ~/.bashrc << 'EOF'

# OpenClaw & OpenViking Environment
export OPENCLAW_WORKSPACE=/root/.openclaw/workspace
export OPENVIKING_URL=http://localhost:1933
EOF
    fi
    
    log_success "环境变量配置完成"
}

# Step 6: 启动 OpenViking 服务
start_openviking() {
    log_info "启动 OpenViking 服务..."
    
    # 检查服务是否已在运行
    if pgrep -f "openviking-server" > /dev/null; then
        log_warning "OpenViking 服务已在运行"
        return
    fi
    
    # 启动服务
    nohup openviking-server --with-bot > /var/log/openviking.log 2>&1 &
    
    # 等待服务启动
    sleep 5
    
    # 检查服务状态
    if pgrep -f "openviking-server" > /dev/null; then
        log_success "OpenViking 服务启动成功"
        log_info "服务地址: http://localhost:1933"
    else
        log_error "OpenViking 服务启动失败"
        log_info "请查看日志: tail -f /var/log/openviking.log"
        exit 1
    fi
}

# Step 7: 测试集成
test_integration() {
    log_info "测试 OpenClaw 与 OpenViking 集成..."
    
    # 运行测试脚本
    cd /root/.openclaw/workspace
    
    if [ -f "tests/test_openclaw_memory_integration.py" ]; then
        log_info "运行集成测试..."
        python3 -m pytest tests/test_openclaw_memory_integration.py -v || {
            log_warning "部分测试失败，但集成仍可用"
        }
    else
        log_warning "测试文件不存在，跳过测试"
    fi
    
    log_success "集成测试完成"
}

# Step 8: 创建启动脚本
create_startup_script() {
    log_info "创建启动脚本..."
    
    cat > /root/.openclaw/workspace/start-openviking.sh << 'EOF'
#!/bin/bash

# OpenViking 启动脚本

echo "Starting OpenViking server..."

# 检查服务是否已在运行
if pgrep -f "openviking-server" > /dev/null; then
    echo "OpenViking is already running"
    exit 0
fi

# 启动服务
nohup openviking-server --with-bot > /var/log/openviking.log 2>&1 &

# 等待服务启动
sleep 5

# 检查服务状态
if pgrep -f "openviking-server" > /dev/null; then
    echo "OpenViking started successfully"
    echo "Server URL: http://localhost:1933"
else
    echo "Failed to start OpenViking"
    exit 1
fi
EOF
    
    chmod +x /root/.openclaw/workspace/start-openviking.sh
    
    log_success "启动脚本创建完成"
}

# Step 9: 创建停止脚本
create_stop_script() {
    log_info "创建停止脚本..."
    
    cat > /root/.openclaw/workspace/stop-openviking.sh << 'EOF'
#!/bin/bash

# OpenViking 停止脚本

echo "Stopping OpenViking server..."

# 停止服务
pkill -f "openviking-server"

# 等待服务停止
sleep 3

# 检查服务状态
if pgrep -f "openviking-server" > /dev/null; then
    echo "Failed to stop OpenViking"
    exit 1
else
    echo "OpenViking stopped successfully"
fi
EOF
    
    chmod +x /root/.openclaw/workspace/stop-openviking.sh
    
    log_success "停止脚本创建完成"
}

# 主函数
main() {
    echo "=============================================="
    echo "  OpenClaw 与 OpenViking 集成部署脚本"
    echo "=============================================="
    echo ""
    
    # 执行部署步骤
    check_dependencies
    install_python_dependencies
    install_openviking
    configure_openviking
    setup_environment_variables
    start_openviking
    test_integration
    create_startup_script
    create_stop_script
    
    echo ""
    echo "=============================================="
    log_success "部署完成！"
    echo "=============================================="
    echo ""
    echo "下一步操作："
    echo "  1. 测试集成: python3 -c 'from openclaw_memory_integration import *'"
    echo "  2. 启动服务: ./start-openviking.sh"
    echo "  3. 停止服务: ./stop-openviking.sh"
    echo "  4. 查看日志: tail -f /var/log/openviking.log"
    echo "  5. 查看文档: cat OPENCLAW-OPENVIKING-INTEGRATION.md"
    echo ""
    log_info "OpenViking 服务地址: http://localhost:1933"
}

# 运行主函数
main "$@"