# 快速外网访问部署脚本

**用途**: 一键配置DSP Platform外网访问
**使用方式**: bash setup-external-access.sh your-domain.com

---

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
        print_info "使用: sudo bash $0 your-domain.com"
        exit 1
    fi
}

# 检查参数
check_params() {
    if [ -z "$1" ]; then
        print_error "请提供域名"
        echo "使用方法: bash $0 your-domain.com"
        echo "示例: bash $0 dsp.example.com"
        exit 1
    fi
    DOMAIN=$1
}

# 检测操作系统
detect_os() {
    if [ -f /etc/redhat-release ]; then
        OS="centos"
        PKG_MANAGER="yum"
    elif [ -f /etc/debian_version ]; then
        OS="ubuntu"
        PKG_MANAGER="apt"
    else
        print_error "不支持的操作系统"
        exit 1
    fi
    print_info "检测到操作系统: $OS"
}

# 安装基础软件
install_packages() {
    print_info "安装基础软件包..."
    $PKG_MANAGER install -y nginx certbot python3-certbot-nginx

    if [ "$OS" = "centos" ]; then
        $PKG_MANAGER install -y httpd-tools firewalld
        systemctl start firewalld
        systemctl enable firewalld
    else
        $PKG_MANAGER install -y apache2-utils ufw
        ufw --force enable
    fi

    print_info "基础软件安装完成"
}

# 申请SSL证书
obtain_ssl() {
    print_info "申请SSL证书: $DOMAIN"
    
    # 检查是否已有证书
    if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
        print_warn "SSL证书已存在，跳过申请"
        return 0
    fi

    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

    if [ $? -eq 0 ]; then
        print_info "SSL证书申请成功"
    else
        print_error "SSL证书申请失败"
        exit 1
    fi
}

# 设置管理员密码
setup_admin_password() {
    print_info "设置管理员密码..."
    
    if [ ! -f "/etc/nginx/.htpasswd" ]; then
        # 生成随机密码
        PASSWORD=$(openssl rand -base64 12)
        print_info "管理员密码已生成: $PASSWORD"
        print_warn "请妥善保存此密码！"
        
        htpasswd -b -c /etc/nginx/.htpasswd admin $PASSWORD
    else
        print_warn "管理员密码已存在，跳过设置"
    fi
}

# 配置Nginx
configure_nginx() {
    print_info "配置Nginx..."

    cat > /etc/nginx/conf.d/dsp-platform.conf << 'EOF'
upstream dsp_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

server {
    listen 80;
    server_name __DOMAIN__;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name __DOMAIN__;

    ssl_certificate /etc/letsencrypt/live/__DOMAIN__/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/__DOMAIN__/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    client_max_body_size 50M;

    location /api/ {
        proxy_pass http://dsp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering off;
    }

    location /ws/ {
        proxy_pass http://dsp_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }

    location /prometheus/ {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9090/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /grafana/ {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:3002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-WEBAUTH-USER $remote_user;
        rewrite ^/grafana/(.*) /$1 break;
    }

    location /health {
        proxy_pass http://dsp_backend;
        access_log off;
    }
}
EOF

    # 替换域名
    sed -i "s/__DOMAIN__/$DOMAIN/g" /etc/nginx/conf.d/dsp-platform.conf

    # 测试配置
    nginx -t

    if [ $? -eq 0 ]; then
        print_info "Nginx配置成功"
    else
        print_error "Nginx配置错误"
        exit 1
    fi
}

# 配置防火墙
configure_firewall() {
    print_info "配置防火墙..."

    if [ "$OS" = "centos" ]; then
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --reload
    else
        ufw allow 80/tcp
        ufw allow 443/tcp
        ufw allow 22/tcp
        ufw reload
    fi

    print_info "防火墙配置完成"
}

# 设置证书自动续期
setup_cert_renewal() {
    print_info "设置SSL证书自动续期..."

    # 添加到crontab
    (crontab -l 2>/dev/null | grep -v "certbot renew"; echo "0 2 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -

    print_info "SSL证书自动续期已设置（每天凌晨2点）"
}

# 更新Docker Compose
update_docker_compose() {
    print_info "更新Docker Compose配置..."

    DOCKER_COMPOSE="/root/.openclaw/workspace/dsp-platform/docker-compose.yml"

    if [ -f "$DOCKER_COMPOSE" ]; then
        # 备份原文件
        cp $DOCKER_COMPOSE ${DOCKER_COMPOSE}.backup

        # 修改Nginx端口（只监听本地）
        if grep -q "80:80" $DOCKER_COMPOSE; then
            sed -i 's/- "80:80"/- "127.0.0.1:8080:80"/g' $DOCKER_COMPOSE
            print_info "Nginx端口已修改为127.0.0.1:8080"
        fi

        if grep -q "443:443" $DOCKER_COMPOSE; then
            sed -i 's/- "443:443"/- "127.0.0.1:8443:443"/g' $DOCKER_COMPOSE
            print_info "Nginx SSL端口已修改为127.0.0.1:8443"
        fi

        # 重启Docker服务
        cd /root/.openclaw/workspace/dsp-platform
        docker-compose restart nginx

        print_info "Docker Compose配置已更新"
    else
        print_warn "未找到docker-compose.yml文件，跳过更新"
    fi
}

# 重启Nginx
restart_nginx() {
    print_info "重启Nginx..."
    systemctl restart nginx

    if [ $? -eq 0 ]; then
        print_info "Nginx启动成功"
    else
        print_error "Nginx启动失败"
        exit 1
    fi
}

# 显示访问信息
show_info() {
    echo ""
    echo "================================"
    echo -e "${GREEN}外网访问配置完成！${NC}"
    echo "================================"
    echo ""
    echo "访问地址："
    echo "  🌐 API:        https://$DOMAIN/api/v1/"
    echo "  📊 Prometheus: https://$DOMAIN/prometheus/ (需认证)"
    echo "  📈 Grafana:    https://$DOMAIN/grafana/ (需认证)"
    echo ""
    echo "管理员密码："
    if [ -f "/etc/nginx/.htpasswd" ]; then
        PASSWORD=$(cat /etc/nginx/.htpasswd | cut -d: -f2)
        echo -e "  🔐 admin: $PASSWORD"
        echo -e "${YELLOW}  ⚠️  请妥善保存密码！${NC}"
    fi
    echo ""
    echo "管理命令："
    echo "  查看Nginx日志: tail -f /var/log/nginx/error.log"
    echo "  重启Nginx:    systemctl restart nginx"
    echo "  查看SSL证书:   certbot certificates"
    echo "  手动续期证书:  certbot renew --force-renewal"
    echo ""
    echo "================================"
}

# 主函数
main() {
    echo ""
    echo "================================"
    echo "  DSP Platform 外网访问配置"
    echo "================================"
    echo ""

    check_root
    check_params $1
    detect_os

    read -p "是否继续配置? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消配置"
        exit 0
    fi

    install_packages
    obtain_ssl
    setup_admin_password
    configure_nginx
    configure_firewall
    setup_cert_renewal
    update_docker_compose
    restart_nginx
    show_info

    print_info "配置完成！"
}

# 运行主函数
main "$@"
