# LemClaw - OpenClaw 授权网关 - 部署指南

## 🚀 快速部署

### 方式一：一键启动

```bash
cd openclaw-auth-gateway
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 OPENCLAW_GATEWAY_URL 和 GATEWAY_TOKEN

# 3. 启动服务器
python app.py
```

### 方式三：生产环境部署（推荐）

#### 使用 gunicorn

```bash
# 安装 gunicorn
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:8089 app:app
```

#### 使用 Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8089

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8089", "app:app"]
```

```bash
# 构建镜像
docker build -t openclaw-auth-gateway .

# 运行容器
docker run -d \
  -p 8089:8089 \
  -e OPENCLAW_GATEWAY_URL=http://host.docker.internal:8080 \
  -e GATEWAY_TOKEN=your-token \
  --name openclaw-auth-gateway \
  openclaw-auth-gateway
```

#### 使用 Docker Compose

```yaml
version: '3.8'

services:
  openclaw-auth-gateway:
    build: .
    ports:
      - "8089:8089"
    environment:
      - OPENCLAW_GATEWAY_URL=http://openclaw-gateway:8080
      - GATEWAY_TOKEN=${GATEWAY_TOKEN}
      - DATABASE_URL=sqlite:///auth_codes.db
      - HOST=0.0.0.0
      - PORT=8089
    depends_on:
      - openclaw-gateway
    restart: unless-stopped

  openclaw-gateway:
    image: openclaw/gateway:latest
    ports:
      - "8080:8080"
    volumes:
      - ./openclaw-data:/data
    restart: unless-stopped
```

```bash
docker-compose up -d
```

## 🔧 配置说明

### 必填配置

```bash
# OpenClaw Gateway URL
OPENCLAW_GATEWAY_URL=http://localhost:8080

# Gateway Token（重要！）
GATEWAY_TOKEN=your-gateway-token-here
```

### 可选配置

```bash
# 数据库配置（默认使用 SQLite）
DATABASE_URL=sqlite:///auth_codes.db
# DATABASE_URL=mysql+pymysql://user:password@localhost/openclaw_auth

# 服务器配置
HOST=0.0.0.0
PORT=8089
DEBUG=False

# 授权码配置
AUTH_CODE_LENGTH=32
DEFAULT_CODE_COUNT=50
```

## 📋 生成授权码

```bash
python generate_codes.py
```

这将生成 50 个授权码，保存到：
- `auth_codes.txt` (CSV 格式)
- `auth_codes.json` (JSON 格式)

## 🌐 Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8089;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 🔐 安全建议

1. **使用 HTTPS**
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       # ... other config
   }
   ```

2. **配置防火墙**
   ```bash
   # 只允许 80 和 443 端口
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```

3. **设置授权码过期时间**
   ```bash
   # 生成 30 天过期的授权码
   curl -X POST http://localhost:8089/api/admin/codes/generate \
     -H "Content-Type: application/json" \
     -d '{"count": 50, "expire_days": 30}'
   ```

4. **添加速率限制**
   ```python
   # 在 app.py 中添加
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(app, key_func=get_remote_address)

   @app.route('/api/chat', methods=['POST'])
   @limiter.limit("10 per minute")
   def chat():
       # ... existing code
   ```

## 📊 监控和日志

### 查看日志

```bash
# 查看服务器日志
tail -f server.log

# 查看 Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 健康检查

```bash
curl http://localhost:8089/health
```

### 使用统计

```bash
curl http://localhost:8089/api/admin/codes/list | jq '.codes[] | {client_name, message_count, last_used_at}'
```

## 🚦 验证部署

```bash
# 1. 检查服务器状态
curl http://localhost:8089/health

# 2. 生成测试授权码
python generate_codes.py

# 3. 测试验证接口
AUTH_CODE=$(head -1 auth_codes.txt | cut -d',' -f1)
curl -X POST http://localhost:8089/api/auth/verify \
  -H "Content-Type: application/json" \
  -d "{\"auth_code\": \"$AUTH_CODE\"}"

# 4. 测试聊天接口
curl -X POST http://localhost:8089/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"auth_code\": \"$AUTH_CODE\", \"message\": \"你好\"}"
```

## 🛠️ 故障排除

### 问题 1：无法连接到 OpenClaw Gateway

**解决**：
- 检查 `OPENCLAW_GATEWAY_URL` 是否正确
- 确保 OpenClaw Gateway 正在运行
- 检查防火墙设置

### 问题 2：授权码验证失败

**解决**：
- 确保授权码已生成
- 检查授权码状态是否为 `active`
- 查看服务器日志了解详情

### 问题 3：消息发送失败

**解决**：
- 检查 `GATEWAY_TOKEN` 是否正确
- 确保 OpenClaw Gateway 正常运行
- 查看服务器日志

## 📈 性能优化

1. **使用 Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8089 app:app
   ```

2. **使用 Redis 缓存**
   ```python
   # 添加 Redis 缓存
   import redis
   redis_client = redis.Redis(host='localhost', port=6379, db=0)

   # 缓存授权码验证结果
   def verify_auth_code(auth_code):
       cache_key = f"auth:{auth_code}"
       cached = redis_client.get(cache_key)
       if cached:
           return json.loads(cached)

       # ... verify logic
       redis_client.setex(cache_key, 300, json.dumps(result))
       return result
   ```

3. **使用数据库连接池**
   ```python
   from sqlalchemy.pool import QueuePool

   engine = create_engine(
       DATABASE_URL,
       poolclass=QueuePool,
       pool_size=10,
       max_overflow=20
   )
   ```

## 📝 备份和恢复

### 备份数据库

```bash
# SQLite
cp auth_codes.db auth_codes.db.backup

# MySQL
mysqldump -u user -p openclaw_auth > backup.sql
```

### 恢复数据库

```bash
# SQLite
cp auth_codes.db.backup auth_codes.db

# MySQL
mysql -u user -p openclaw_auth < backup.sql
```

---

**快速开始**：
```bash
git clone <repo-url>
cd openclaw-auth-gateway
./start.sh
python generate_codes.py
```
