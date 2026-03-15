#!/bin/bash

# DSP平台部署脚本
# 用途: 快速部署DSP平台到各环境

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数: 打印信息
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数: 检查依赖
check_dependencies() {
    info "检查依赖..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    info "依赖检查通过"
}

# 函数: 初始化环境
init_environment() {
    local env=$1
    
    info "初始化 $env 环境..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.$env" ]; then
            cp ".env.$env" .env
            info "已从 .env.$env 创建 .env 文件"
        else
            warn "未找到 .env.$env 文件，使用 .env.example"
            cp .env.example .env
            warn "请编辑 .env 文件，配置正确的环境变量"
            read -p "按Enter继续..."
        fi
    fi
    
    info "环境初始化完成"
}

# 函数: 生成SSL证书
generate_ssl_cert() {
    local domain=$1
    
    info "生成SSL证书..."
    
    if [ -z "$domain" ]; then
        error "域名不能为空"
        exit 1
    fi
    
    # 首次获取证书
    docker-compose run --rm certbot certonly \
        --webroot \
        --webroot-path /var/www/certbot \
        -d "$domain" \
        -d "www.$domain" \
        --email admin@$domain \
        --agree-tos \
        --non-interactive
    
    info "SSL证书生成完成"
}

# 函数: 创建htpasswd文件
create_htpasswd() {
    info "创建htpasswd文件..."
    
    if ! command -v htpasswd &> /dev/null; then
        warn "htpasswd未安装，跳过"
        return
    fi
    
    if [ ! -f "nginx/.htpasswd" ]; then
        read -p "输入监控服务用户名 [admin]: " username
        username=${username:-admin}
        
        htpasswd -c nginx/.htpasswd "$username"
        
        info "htpasswd文件创建完成"
    else
        info "htpasswd文件已存在，跳过"
    fi
}

# 函数: 启动服务
start_services() {
    local compose_file=$1
    
    info "启动服务..."
    
    if [ -n "$compose_file" ]; then
        docker-compose -f "$compose_file" up -d
    else
        docker-compose up -d
    fi
    
    info "等待服务启动..."
    sleep 10
    
    info "服务启动完成"
    
    # 显示服务状态
    docker-compose ps
}

# 函数: 停止服务
stop_services() {
    info "停止服务..."
    docker-compose down
    info "服务已停止"
}

# 函数: 查看日志
view_logs() {
    local service=$1
    
    if [ -n "$service" ]; then
        docker-compose logs -f "$service"
    else
        docker-compose logs -f
    fi
}

# 函数: 备份数据
backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    
    info "备份数据到 $backup_dir ..."
    
    mkdir -p "$backup_dir"
    
    # 备份数据库
    docker-compose exec -T dsp-mysql mysqldump \
        -u root \
        -p"${MYSQL_ROOT_PASSWORD}" \
        dsp_db > "$backup_dir/mysql_backup.sql"
    
    # 备份配置
    tar -czf "$backup_dir/config_backup.tar.gz" .env nginx/ prometheus/ grafana/ alertmanager/
    
    # 备份Redis数据（如果需要）
    docker-compose exec dsp-redis redis-cli --rdb - > "$backup_dir/redis_backup.rdb"
    
    info "数据备份完成: $backup_dir"
}

# 函数: 健康检查
health_check() {
    info "执行健康检查..."
    
    # 检查容器状态
    local unhealthy=$(docker-compose ps | grep -c "Exit" || true)
    
    if [ "$unhealthy" -gt 0 ]; then
        error "发现 $unhealthy 个异常容器"
        return 1
    fi
    
    # 检查API健康端点
    if curl -f -s http://localhost/api/v1/health > /dev/null; then
        info "API健康检查通过"
    else
        error "API健康检查失败"
        return 1
    fi
    
    info "所有健康检查通过"
}

# 函数: 清理资源
cleanup_resources() {
    info "清理未使用的资源..."
    
    docker-compose down -v
    docker system prune -f
    
    info "清理完成"
}

# 函数: 显示帮助
show_help() {
    cat << EOF
DSP平台部署脚本

用法: ./deploy.sh [命令] [选项]

命令:
    init [env]           初始化环境 (staging/production)
    start [compose-file] 启动服务
    stop                 停止服务
    restart [compose-file] 重启服务
    logs [service]       查看日志
    status               查看服务状态
    ssl [domain]         生成SSL证书
    htpasswd            创建htpasswd文件
    backup              备份数据
    health              健康检查
    cleanup             清理未使用的资源
    update              更新服务
    help                显示帮助

示例:
    ./deploy.sh init staging
    ./deploy.sh ssl your-domain.com
    ./deploy.sh start
    ./deploy.sh logs dsp-backend
    ./deploy.sh health
    ./deploy.sh backup

EOF
}

# 主函数
main() {
    local command=$1
    shift || true
    
    case "$command" in
        init)
            check_dependencies
            init_environment "$@"
            ;;
        ssl)
            check_dependencies
            generate_ssl_cert "$@"
            ;;
        htpasswd)
            create_htpasswd
            ;;
        start)
            check_dependencies
            start_services "$@"
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            check_dependencies
            start_services "$@"
            ;;
        logs)
            view_logs "$@"
            ;;
        status)
            docker-compose ps
            ;;
        backup)
            backup_data
            ;;
        health)
            health_check
            ;;
        cleanup)
            cleanup_resources
            ;;
        update)
            info "更新服务..."
            docker-compose pull
            docker-compose up -d
            info "服务更新完成"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
