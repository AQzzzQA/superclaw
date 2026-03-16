# 权限系统Bug修复方案

**项目**: https://github.com/AQzzzQA/permissions-system
**问题**: Docker部署页面空白 + 容器启动失败
**分析时间**: 2026-03-16 23:25

---

## 🔍 问题分析

### 问题1: 访问http://localhost:3000页面空白

#### 根本原因
1. **前端未正确构建**
   - `docker-compose.yml`中的`frontend`服务使用`vite`命令启动开发服务器
   - 但没有指定`--host`参数，导致只监听`localhost`，无法从容器外部访问

2. **可能的原因**:
   - Vite开发服务器默认只绑定localhost
   - Docker网络无法访问localhost
   - 需要添加`--host 0.0.0.0`参数

#### 复现步骤
```bash
# 使用一键部署
docker-compose up -d

# 访问
curl http://localhost:3000
# 返回空白或404
```

### 问题2: Docker容器疑似没拉取或启动

#### 可能原因
1. **镜像构建失败**
   - Dockerfile配置问题
   - 依赖安装失败
   - 构建上下文路径错误

2. **服务依赖关系**
   - `backend`依赖`db`和`redis`
   - 如果`db`或`redis`启动慢，`backend`可能失败
   - 缺少健康检查

3. **网络配置**
   - 容器间网络通信失败
   - 端口映射冲突

---

## 🛠️ 修复方案

### 修复1: 前端服务配置

#### 方案A: 修改启动命令（推荐）
```yaml
# docker-compose.yml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:5173"  # Vite默认端口是5173，不是3000
    environment:
      - VITE_API_URL=http://localhost:8000
    command: npm run dev -- --host 0.0.0.0 --port 5173
    depends_on:
      - backend
```

**关键改动**:
- ✅ 添加`--host 0.0.0.0`（绑定所有网络接口）
- ✅ 明确指定端口`--port 5173`
- ✅ 修正端口映射`3000:5173`（映射到3000）

#### 方案B: 使用生产构建
```yaml
# docker-compose.yml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    command: npm run build && nginx -g 'daemon off;'
    depends_on:
      - backend
```

需要创建`Dockerfile`:
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 修复2: Docker Compose优化

```yaml
# docker-compose.yml (完整修复版)
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: permissions_db
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-permissions}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: permissions_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build: ./backend
    container_name: permissions_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-postgres}@db:5432/${DB_NAME:-permissions}
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY:-your-secret-key}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./backend/frontend
    container_name: permissions_frontend
    ports:
      - "3000:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    command: npm run dev -- --host 0.0.0.0 --port 5173

volumes:
  postgres_data:
```

**关键改进**:
1. ✅ 添加健康检查（`healthcheck`）
2. ✅ 修复依赖条件（`depends_on` + `condition`）
3. ✅ 所有服务添加`0.0.0.0`绑定
4. ✅ 明确端口映射
5. ✅ 环境变量默认值

### 修复3: 环境变量配置

#### 创建`.env`文件
```env
# .env
DB_USER=postgres
DB_PASSWORD=your_strong_password
DB_NAME=permissions
SECRET_KEY=your-secret-key-change-this
VITE_API_URL=http://localhost:8000
```

#### 确保`.env`不被Git跟踪
```bash
# .gitignore
.env
*.log
node_modules
__pycache__
```

---

## 🧪 验证步骤

### 1. 清理并重启
```bash
# 停止并删除容器
docker-compose down -v

# 清理构建缓存
docker system prune -f

# 重新构建并启动
docker-compose up --build -d

# 查看日志
docker-compose logs -f
```

### 2. 检查容器状态
```bash
# 查看所有容器
docker-compose ps

# 应该看到所有服务都是"Up"状态
```

### 3. 检查服务健康
```bash
# 检查后端
curl http://localhost:8000/docs
# 应该返回FastAPI文档页面

# 检查前端
curl http://localhost:3000
# 应该返回HTML内容
```

### 4. 查看日志
```bash
# 查看所有日志
docker-compose logs

# 查看特定服务日志
docker-compose logs frontend
docker-compose logs backend
docker-compose logs db
```

---

## 🐛 常见问题排查

### 问题: 前端仍然空白

#### 检查清单
```bash
# 1. 确认容器正在运行
docker-compose ps frontend

# 2. 查看前端日志
docker-compose logs frontend

# 3. 检查端口是否正确
netstat -tuln | grep 3000

# 4. 尝试直接访问容器
docker exec -it permissions_frontend sh
curl http://localhost:5173
```

#### 可能的解决方案
1. **端口冲突**: 修改端口映射
   ```yaml
   ports:
     - "3001:5173"  # 使用3001代替3000
   ```

2. **网络问题**: 检查防火墙
   ```bash
   sudo ufw allow 3000/tcp
   ```

3. **前端构建失败**: 检查依赖
   ```bash
   docker-compose run frontend npm install
   ```

### 问题: 容器启动失败

#### 检查清单
```bash
# 1. 查看容器退出状态
docker-compose ps -a

# 2. 查看错误日志
docker-compose logs <service_name>

# 3. 进入容器调试
docker run -it <image_name> sh
```

#### 常见错误及修复

**错误: "Database connection failed"**
- 原因: 数据库未就绪
- 修复: 等待数据库健康检查通过

**错误: "Module not found"**
- 原因: 依赖未安装
- 修复: 重新构建镜像

**错误: "Permission denied"**
- 原因: 文件权限问题
- 修复: 调整Dockerfile中的`USER`指令

---

## 📋 一键修复脚本

```bash
#!/bin/bash

echo "🔧 权限系统一键修复脚本"

# 停止所有容器
echo "🛑 停止容器..."
docker-compose down -v

# 清理缓存
echo "🧹 清理缓存..."
docker system prune -f

# 更新docker-compose.yml
echo "📝 更新配置..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: permissions_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: permissions
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: permissions_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build: ./backend
    container_name: permissions_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/permissions
      REDIS_URL: redis://redis:6379
      SECRET_KEY: your-secret-key
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    container_name: permissions_frontend
    ports:
      - "3000:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    command: npm run dev -- --host 0.0.0.0 --port 5173

volumes:
  postgres_data:
EOF

# 创建.env文件
echo "📄 创建环境变量..."
cat > .env << 'EOF'
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=permissions
SECRET_KEY=your-secret-key
VITE_API_URL=http://localhost:8000
EOF

# 重新构建并启动
echo "🚀 构建并启动..."
docker-compose up --build -d

# 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 10

# 检查状态
echo "📊 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 修复完成！"
echo "📌 访问地址："
echo "   前端: http://localhost:3000"
echo "   后端: http://localhost:8000/docs"
echo ""
echo "📝 查看日志: docker-compose logs -f"
```

使用方法:
```bash
chmod +x fix-permissions.sh
./fix-permissions.sh
```

---

## 📞 需要更多信息

如果问题仍然存在，请提供：

1. **Docker Compose日志**
   ```bash
   docker-compose logs > logs.txt
   ```

2. **容器状态**
   ```bash
   docker-compose ps
   ```

3. **浏览器控制台错误**
   - 打开浏览器开发者工具
   - 查看Console标签的错误信息

4. **网络信息**
   ```bash
   netstat -tuln | grep -E "3000|8000"
   ```

---

**修复人**: Echo-2
**修复时间**: 2026-03-16 23:25
**状态**: 🔍 分析完成，待验证
**建议**: 按照修复方案执行，然后提供日志反馈
