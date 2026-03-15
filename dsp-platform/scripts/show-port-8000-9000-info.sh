#!/bin/bash

# DSP Platform 外网访问信息显示 - 8000-9000端口配置
# 时间: 2026-03-15 15:35

echo "================================"
echo "  DSP Platform 外网访问配置完成"
echo "  端口范围: 8000-9000"
echo "================================"
echo ""

echo "✅ 配置已完成！"
echo ""
echo "公网IP: 43.156.131.98"
echo ""

echo "📋 端口监听状态："
echo "================================"
netstat -tln 2>/dev/null | grep -E ":(8000|8080|8888|8889|9000)" | while read line; do
    port=$(echo $line | awk '{print $4}' | grep -oP ':\K\d+')
    echo "  端口 $port: ✅ 已监听"
done
echo ""

echo "🚀 外网访问地址："
echo "================================"
echo "  后端API:    http://43.156.131.98:8000/api/v1/"
echo "  Nginx:      http://43.156.131.98:8080"
echo "  Prometheus: http://43.156.131.98:9000"
echo "  Grafana:    http://43.156.131.98:8888"
echo "  Flower:     http://43.156.131.98:8889"
echo "  健康检查:   http://43.156.131.98:8000/api/v1/system/health"
echo ""

echo "🧪 测试命令："
echo "================================"
echo "  curl http://43.156.131.98:8000/api/v1/system/health"
echo ""

echo "📊 服务状态："
echo "================================"
docker ps --filter "name=dsp-" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null
echo ""

echo "⚠️  云服务器安全组配置："
echo "================================"
echo "如果你使用的是云服务器，需要在云控制台配置安全组规则"
echo ""
echo "开放端口（8000-9000范围内）："
echo "  - 端口 8000  (后端API)"
echo "  - 端口 8080  (Nginx)"
echo "  - 端口 8888  (Grafana)"
echo "  - 端口 8889  (Flower)"
echo "  - 端口 9000  (Prometheus)"
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
