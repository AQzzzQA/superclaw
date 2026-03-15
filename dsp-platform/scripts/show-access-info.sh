#!/bin/bash

# DSP Platform 外网访问配置完成报告
# 时间: 2026-03-15

echo "================================"
echo "  DSP Platform 外网访问配置完成"
echo "================================"
echo ""

# 获取公网IP
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "未知")

echo "✅ 配置已完成！"
echo ""
echo "公网IP: $PUBLIC_IP"
echo ""

echo "📋 端口监听状态："
echo "================================"
netstat -tlnp 2>/dev/null | grep -E ":(8000|9090|3002|5555)" | while read line; do
    port=$(echo $line | awk '{print $4}' | grep -oP ':\K\d+')
    echo "  端口 $port: ✅ 已监听"
done
echo ""

echo "🚀 外网访问地址："
echo "================================"
echo "  后端API:    http://$PUBLIC_IP:8000/api/v1/"
echo "  Nginx:      http://$PUBLIC_IP"
echo "  Prometheus: http://$PUBLIC_IP:9090"
echo "  Grafana:    http://$PUBLIC_IP:3002"
echo "  Flower:     http://$PUBLIC_IP:5555"
echo "  健康检查:   http://$PUBLIC_IP:8000/api/v1/system/health"
echo ""

echo "🧪 测试命令："
echo "================================"
echo "  curl http://$PUBLIC_IP:8000/api/v1/system/health"
echo ""

echo "📊 服务状态："
echo "================================"
docker ps --filter "name=dsp-" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null
echo ""

echo "⚠️  云服务器安全组配置："
echo "================================"
echo "如果你使用的是云服务器，需要在云控制台配置安全组规则"
echo ""
echo "开放端口："
echo "  - 端口 80    (HTTP)"
echo "  - 端口 8000  (后端API)"
echo "  - 端口 9090  (Prometheus)"
echo "  - 端口 3002  (Grafana)"
echo "  - 端口 5555  (Flower)"
echo ""
echo "授权对象：0.0.0.0/0"
echo "配置完成后，等待1-5分钟生效"
echo ""

echo "================================"
echo "📝 常用命令："
echo "================================"
echo "  查看服务状态: cd /root/.openclaw/workspace/dsp-platform && docker-compose ps"
echo "  查看服务日志: docker-compose logs -f [service-name]"
echo "  重启服务:     docker-compose restart [service-name]"
echo "  停止所有服务: docker-compose down"
echo "  启动所有服务: docker-compose up -d"
echo "  查看端口监听: netstat -tlnp | grep docker"
echo "================================"
echo ""
