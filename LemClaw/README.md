# LemClaw Gateway 🦞

> **LemClaw Gateway** - HTTP Gateway for SuperClaw
>
> 基于 Flask 的高性能 HTTP 网关，集成认证、授权、速率限制等企业级特性

---

## 📋 项目简介

LemClaw Gateway 是 SuperClaw 平台的 HTTP 网关组件，提供：

- ✅ **双网关兼容** - 与 OpenClaw Gateway 无缝集成
- ✅ **授权系统** - 基于授权码的安全认证
- ✅ **速率限制** - Redis 驱动的请求限流
- ✅ **IP 白名单** - 灵活的访问控制
- ✅ **浏览器集成** - agent-browser 自动化支持
- ✅ **监控面板** - 实时性能监控

---

## 🏗️ 技术栈

| 组件 | 技术选型 |
|------|---------|
| **Web 框架** | Flask + Flask-CORS |
| **数据库** | SQLite（授权码） + Redis（缓存） |
| **AI 集成** | OpenClaw CLI + Manus API |
| **浏览器** | agent-browser |
| **部署** | Nginx + Gunicorn |

---

## 📂 项目结构

```
lemclaw-gateway/
├── app.py                # Flask 应用入口
├── browser_bot.py        # 浏览器机器人
├── generate_codes.py     # 授权码生成
├── rate_limit.py        # 速率限制
├── ip_whitelist.py      # IP 白名单
├── requirements.txt     # Python 依赖
├── .env.example       # 环境变量示例
└── nginx.conf.example  # Nginx 配置示例
```

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Redis 7.0+
- SQLite 3.38+

### 安装

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/lemclaw-gateway.git
cd lemclaw-gateway

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写配置

# 初始化数据库
python3 generate_codes.py

# 启动服务
python3 app.py
```

### 配置

编辑 `.env` 文件：

```bash
# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL=http://localhost:18789
GATEWAY_TOKEN=your_token_here

# LemClaw Gateway 配置
LEMLCLAW_GATEWAY_URL=http://localhost:8089
LEMLCLAW_AUTH_TOKEN=your_token_here

# 数据库配置
DATABASE_URL=sqlite:///lemclaw/lemclaw.db
REDIS_URL=redis://localhost:6379/0

# 速率限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# IP 白名单（可选）
IP_WHITELIST_ENABLED=true
IP_WHITELIST=127.0.0.1,192.168.1.0/24
```

---

## 📚 API 文档

### 健康检查

```http
GET /health
```

**响应**：
```json
{
  "status": "healthy",
  "gateway": "connected",
  "timestamp": "2026-03-08T01:00:00Z"
}
```

### 消息发送

```http
POST /api/agent
Authorization: Bearer {auth_token}
Content-Type: application/json

{
  "auth_code": "your_auth_code",
  "message": "Hello, SuperClaw!"
}
```

**响应**：
```json
{
  "success": true,
  "reply": "AI回复内容",
  "timestamp": "2026-03-08T01:00:00Z"
}
```

---

## 🔧 开发

### 运行开发服务器

```bash
# 启动 Flask 开发服务器
python3 app.py

# 使用 Gunicorn（生产）
gunicorn -w 4 -b 0.0.0.0:8089 app:app
```

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-flask

# 运行测试
pytest tests/
```

---

## 📊 监控

### 启动监控脚本

```bash
# 启动监控面板
./monitor.sh
```

### 查看日志

```bash
# 实时日志
tail -f logs/lemclaw/app.log

# 错误日志
grep ERROR logs/lemclaw/app.log
```

---

## 🚀 部署

### 使用 Nginx

```bash
# 配置 Nginx
cp nginx.conf.example /etc/nginx/sites-available/lemclaw
ln -s /etc/nginx/sites-available/lemclaw /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### 使用 Gunicorn + Supervisor

```bash
# 创建 Supervisor 配置
cat > /etc/supervisor/conf.d/lemclaw.conf << EOF
[program:lemclaw]
command=/usr/bin/gunicorn -w 4 -b 0.0.0.0:8089 app:app
directory=/path/to/lemclaw-gateway
user=www-data
autostart=true
autorestart=true
EOF

# 启动服务
supervisorctl update
supervisorctl start lemclaw
```

---

## 🤝 贡献

欢迎提交 PR！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🌟 相关项目

- [SuperClaw](https://github.com/AQzzzQA/superclaw) - Super Claw AI Platform
- [OpenClaw](https://github.com/openclaw/openclaw) - OpenClaw 平台
- [LemClaw](https://github.com/LemClaw/LemClaw) - LemClaw 项目

---

**创建时间**: 2026-03-08
**版本**: v1.0.0
**作者**: AQzzzQA 🚀
