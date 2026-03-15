#!/bin/bash

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "请使用root权限运行此脚本"
        exit 1
    fi
}

# 获取公网IP
get_public_ip() {
    PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ip.sb 2>/dev/null || echo "")
    if [ -z "$PUBLIC_IP" ]; then
        print_error "无法获取公网IP"
        exit 1
    fi
    print_info "公网IP: $PUBLIC_IP"
}

# 检测操作系统
detect_os() {
    if [ -f /etc/redhat-release ] || [ -f /etc/opencloudos-release ]; then
        OS="centos"
        FIREWALL_CMD="firewall-cmd"
    elif [ -f /etc/debian_version ]; then
        OS="ubuntu"
        FIREWALL_CMD="ufw"
    else
        print_error "不支持的操作系统"
        exit 1
    fi
    print_info "检测到操作系统: $OS"
}

# 配置防火墙
configure_firewall() {
    print_info "配置防火墙..."

    if [ "$OS" = "centos" ]; then
        # CentOS/RHEL - firewalld
        systemctl start firewalld 2>/dev/null || true
        systemctl enable firewalld 2>/dev/null || true

        $FIREWALL_CMD --permanent --add-port=80/tcp 2>/dev/null || print_warn "端口80已开放"
        $FIREWALL_CMD --permanent --add-port=443/tcp 2>/dev/null || print_warn "端口443已开放"
        $FIREWALL_CMD --permanent --add-port=8000/tcp 2>/dev/null || print_warn "端口8000已开放"
        $FIREWALL_CMD --permanent --add-port=9090/tcp 2>/dev/null || print_warn "端口9090已开放"
        $FIREWALL_CMD --permanent --add-port=3002/tcp 2>/dev/null || print_warn "端口3002已开放"
        $FIREWALL_CMD --permanent --add-port=5555/tcp 2>/dev/null || print_warn "端口5555已开放"
        $FIREWALL_CMD --permanent --add-port=22/tcp 2>/dev/null || print_warn "端口22已开放"
        $FIREWALL_CMD --reload 2>/dev/null || true

    else
        # Ubuntu/Debian - ufw
        ufw --force enable 2>/dev/null || true

        ufw allow 80/tcp 2>/dev/null || print_warn "端口80已开放"
        ufw allow 443/tcp 2>/dev/null || print_warn "端口443已开放"
        ufw allow 8000/tcp 2>/dev/null || print_warn "端口8000已开放"
        ufw allow 9090/tcp 2>/dev/null || print_warn "端口9090已开放"
        ufw allow 3002/tcp 2>/dev/null || print_warn "端口3002已开放"
        ufw allow 5555/tcp 2>/dev/null || print_warn "端口5555已开放"
        ufw allow 22/tcp 2>/dev/null || print_warn "端口22已开放"
    fi

    print_info "防火墙配置完成"
}

# 修改Docker Compose端口映射
modify_docker_compose() {
    print_info "修改Docker Compose端口映射..."

    DOCKER_COMPOSE="/root/.openclaw/workspace/dsp-platform/docker-compose.yml"

    if [ ! -f "$DOCKER_COMPOSE" ]; then
        print_error "未找到docker-compose.yml文件: $DOCKER_COMPOSE"
        exit 1
    fi

    # 备份原文件
    cp $DOCKER_COMPOSE ${DOCKER_COMPOSE}.backup.$(date +%Y%m%d_%H%M%S)
    print_info "已备份原文件到 ${DOCKER_COMPOSE}.backup"

    # 修改端口映射（将127.0.0.1:PORT改为0.0.0.0:PORT）
    sed -i 's/- "127.0.0.1:80:/- "0.0.0.0:80:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:443:/- "0.0.0.0:443:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:8000:/- "0.0.0.0:8000:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:3308:/- "0.0.0.0:3308:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:6381:/- "0.0.0.0:6381:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:9090:/- "0.0.0.0:9090:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:3002:/- "0.0.0.0:3002:/g' $DOCKER_COMPOSE
    sed -i 's/- "127.0.0.1:5555:/- "0.0.0.0:5555:/g' $DOCKER_COMPOSE

    # 对于没有指定127.0.0.1的端口，确保使用0.0.0.0
    sed -i 's/- "8000:8000"/- "0.0.0.0:8000:8000"/g' $DOCKER_COMPOSE
    sed -i 's/- "3308:3306"/- "0.0.0.0:3308:3306"/g' $DOCKER_COMPOSE
    sed -i 's/- "6381:6379"/- "0.0.0.0:6381:6379"/g' $DOCKER_COMPOSE
    sed -i 's/- "9090:9090"/- "0.0.0.0:9090:9090"/g' $DOCKER_COMPOSE
    sed -i 's/- "3002:3000"/- "0.0.0.0:3002:3000"/g' $DOCKER_COMPOSE
    sed -i 's/- "5555:5555"/- "0.0.0.0:5555:5555"/g' $DOCKER_COMPOSE

    print_info "Docker Compose端口映射已修改"
}

# 重启Docker服务
restart_docker_services() {
    print_info "重启Docker服务..."

    cd /root/.openclaw/workspace/dsp-platform

    # 停止所有服务
    print_info "停止所有服务..."
    docker-compose down

    # 等待容器完全停止
    sleep 5

    # 重新启动所有服务
    print_info "重新启动所有服务..."
    docker-compose up -d

    # 等待服务启动
    sleep 10

    print_info "Docker服务已重启"
}

# 验证端口监听
verify_ports() {
    print_info "验证端口监听..."

    PORTS=(80 443 8000 3308 6381 9090 3002 5555)
    LISTENING_PORTS=()

    for port in "${PORTS[@]}"; do
        if netstat -tln 2>/dev/null | grep -q ":$port " || ss -tln 2>/dev/null | grep -q ":$port "; then
            LISTENING_PORTS+=("$port")
            print_info "端口 $port 已监听 ✅"
        else
            print_warn "端口 $port 未监听 ⚠️"
        fi
    done

    if [ ${#LISTENING_PORTS[@]} -eq 0 ]; then
        print_error "没有端口在监听"
        return 1
    fi

    return 0
}

# 显示服务状态
show_services_status() {
    print_info "检查服务状态..."

    cd /root/.openclaw/workspace/dsp-platform

    echo ""
    echo "================================"
    echo "Docker 服务状态"
    echo "================================"
    docker-compose ps
    echo "================================"
}

# 测试本地访问
test_local_access() {
    print_info "测试本地访问..."

    # 测试后端API
    if curl -s http://localhost:8000/api/v1/system/health > /dev/null 2>&1; then
        print_info "后端API访问正常 ✅"
    else
        print_warn "后端API访问异常 ⚠️"
    fi

    # 测试Prometheus
    if curl -s http://localhost:9090 > /dev/null 2>&1; then
        print_info "Prometheus访问正常 ✅"
    else
        print_warn "Prometheus访问异常 ⚠️"
    fi

    # 测试Grafana
    if curl -s http://localhost:3002 > /dev/null 2>&1; then
        print_info "Grafana访问正常 ✅"
    else
        print_warn "Grafana访问异常 ⚠️"
    fi
}

# 显示访问信息
show_access_info() {
    echo ""
    echo "================================"
    echo -e "${GREEN}外网访问配置完成！${NC}"
    echo "================================"
    echo ""
    echo "公网IP: $PUBLIC_IP"
    echo ""
    echo "访问地址："
    echo "  🌐 后端API:    http://$PUBLIC_IP:8000/api/v1/"
    echo "  🌐 Nginx:      http://$PUBLIC_IP"
    echo "  🌐 Nginx HTTPS: https://$PUBLIC_IP"
    echo "  📊 Prometheus: http://$PUBLIC_IP:9090"
    echo "  📈 Grafana:    http://$PUBLIC_IP:3002"
    echo "  🌺 Flower:     http://$PUBLIC_IP:5555"
    echo "  🔍 健康检查:   http://$PUBLIC_IP:8000/api/v1/system/health"
    echo ""
    echo "测试命令："
    echo "  curl http://$PUBLIC_IP:8000/api/v1/system/health"
    echo ""
    echo "管理命令："
    echo "  查看服务状态: cd /root/.openclaw/workspace/dsp-platform && docker-compose ps"
    echo "  查看服务日志: docker-compose logs -f [service-name]"
    echo "  重启服务:     docker-compose restart [service-name]"
    echo "  停止所有服务: docker-compose down"
    echo "  启动所有服务: docker-compose up -d"
    echo ""
    echo "================================"
}

# 显示云服务器安全组提示
show_security_group_warning() {
    echo ""
    echo "================================"
    echo -e "${YELLOW}⚠️  云服务器安全组配置${NC}"
    echo "================================"
    echo ""
    echo "如果你使用的是云服务器（阿里云/腾讯云/AWS等），"
    echo "需要在云控制台配置安全组规则，开放以下端口："
    echo ""
    echo "  端口 80    - HTTP访问"
    echo "  端口 443   - HTTPS访问"
    echo "  端口 8000  - 后端API"
    echo "  端口 9090  - Prometheus"
    echo "  端口 3002  - Grafana"
    echo "  端口 5555  - Flower"
    echo ""
    echo "授权对象：0.0.0.0/0（或指定你的IP）"
    echo ""
    echo "配置完成后，等待1-5分钟生效"
    echo ""
    echo "================================"
}

# 主函数
main() {
    echo ""
    echo "================================"
    echo "  DSP Platform 外网IP访问配置"
    echo "================================"
    echo ""

    check_root
    get_public_ip
    detect_os

    echo ""
    echo "配置概要："
    echo "  公网IP: $PUBLIC_IP"
    echo "  操作系统: $OS"
    echo ""

    read -p "是否继续配置? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消配置"
        exit 0
    fi

    configure_firewall
    modify_docker_compose
    restart_docker_services
    verify_ports
    show_services_status
    test_local_access
    show_access_info
    show_security_group_warning

    echo ""
    print_info "配置完成！"
    print_info "请配置云服务器安全组后，从外网测试访问"
    echo ""
}

# 运行主函数
main "$@"
