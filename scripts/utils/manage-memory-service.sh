#!/bin/bash

# OpenClaw 记忆服务管理脚本

SERVICE_NAME="openclaw-memory"
PID_FILE="/var/run/${SERVICE_NAME}.pid"
LOG_FILE="/var/log/${SERVICE_NAME}.log"
WORKSPACE="/root/.openclaw/workspace"
PYTHON_SCRIPT="${WORKSPACE}/start-memory-service.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查服务状态
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "$PID"
            return 0
        else
            rm -f "$PID_FILE"
        fi
    fi
    return 1
}

# 启动服务
start() {
    log_info "启动 OpenClaw 记忆服务..."

    # 检查是否已运行
    if check_status > /dev/null; then
        log_warning "服务已在运行 (PID: $(check_status))"
        return 1
    fi

    # 创建日志目录
    mkdir -p /var/log

    # 设置环境变量
    cd "$WORKSPACE"
    export OPENCLAW_WORKSPACE="$WORKSPACE"
    export OPENVIKING_URL="http://localhost:1933"
    export OPENVIKING_ENABLE_FALLBACK="true"

    # 启动服务
    nohup python3 "$PYTHON_SCRIPT" > "$LOG_FILE" 2>&1 &
    PID=$!

    # 保存 PID
    echo "$PID" > "$PID_FILE"

    # 等待服务启动
    sleep 3

    # 验证服务状态
    if ps -p "$PID" > /dev/null 2>&1; then
        log_success "服务启动成功 (PID: $PID)"
        log_info "日志文件: $LOG_FILE"
        return 0
    else
        log_error "服务启动失败"
        log_info "查看日志: tail -f $LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止服务
stop() {
    log_info "停止 OpenClaw 记忆服务..."

    PID=$(check_status)
    if [ -z "$PID" ]; then
        log_warning "服务未运行"
        return 1
    fi

    # 发送 SIGTERM
    kill "$PID" 2>/dev/null

    # 等待进程结束
    for i in {1..30}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            rm -f "$PID_FILE"
            log_success "服务已停止"
            return 0
        fi
        sleep 1
    done

    # 如果还未停止，强制 kill
    log_warning "强制停止服务..."
    kill -9 "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    log_success "服务已强制停止"
}

# 重启服务
restart() {
    log_info "重启 OpenClaw 记忆服务..."
    stop
    sleep 2
    start
}

# 查看状态
status() {
    PID=$(check_status)
    if [ -n "$PID" ]; then
        log_success "服务正在运行 (PID: $PID)"

        # 显示最近日志
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "最近日志:"
            tail -10 "$LOG_FILE"
        fi
        return 0
    else
        log_warning "服务未运行"
        return 1
    fi
}

# 查看日志
logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        log_error "日志文件不存在: $LOG_FILE"
        return 1
    fi
}

# 健康检查
health() {
    PID=$(check_status)
    if [ -z "$PID" ]; then
        log_error "服务未运行"
        return 1
    fi

    log_info "检查服务健康状态..."

    # 测试 Python 模块
    cd "$WORKSPACE"
    python3 -c "
import sys
sys.path.insert(0, '.')
from openclaw_memory_integration import OpenClawMemoryIntegration
print('✅ 模块导入成功')
" 2>&1

    if [ $? -eq 0 ]; then
        log_success "服务健康检查通过"
        return 0
    else
        log_error "服务健康检查失败"
        return 1
    fi
}

# 清理旧记忆
cleanup() {
    log_info "清理旧记忆..."

    cd "$WORKSPACE"
    python3 -c "
import sys
sys.path.insert(0, '.')
import asyncio
from openclaw_memory_integration import OpenClawMemoryIntegration

async def cleanup():
    integration = OpenClawMemoryIntegration()
    deleted = await integration.cleanup_old_memories(days=30)
    print(f'删除了 {deleted} 个旧记忆')
    await integration.close()

asyncio.run(cleanup())
" 2>&1

    if [ $? -eq 0 ]; then
        log_success "清理完成"
    else
        log_error "清理失败"
        return 1
    fi
}

# 主函数
main() {
    case "$1" in
        start)
            start
            ;;
        stop)
            stop
            ;;
        restart)
            restart
            ;;
        status)
            status
            ;;
        logs)
            logs
            ;;
        health)
            health
            ;;
        cleanup)
            cleanup
            ;;
        *)
            echo "用法: $0 {start|stop|restart|status|logs|health|cleanup}"
            echo ""
            echo "命令:"
            echo "  start    - 启动服务"
            echo "  stop     - 停止服务"
            echo "  restart  - 重启服务"
            echo "  status   - 查看状态"
            echo "  logs     - 查看日志"
            echo "  health   - 健康检查"
            echo "  cleanup  - 清理旧记忆"
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"