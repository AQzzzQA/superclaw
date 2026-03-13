# 安装指南

## 系统要求

- Node.js 18.0 或更高版本
- npm 8.0 或更高版本
- 至少 2GB 可用内存
- 至少 1GB 可用磁盘空间

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd openclaw-permission-manager
```

### 2. 安装依赖

```bash
# 安装后端依赖
cd backend
npm install

# 安装前端依赖
cd ../frontend
npm install

# 返回根目录
cd ..
```

### 3. 环境配置

#### 后端环境配置

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件：

```env
PORT=3001
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=7d
DB_PATH=./data/permissions.db
MAX_UPLOAD_SIZE=10485760
UPLOAD_PATH=./uploads
```

#### 前端环境配置

```bash
cd frontend
cp .env.example .env
```

编辑 `.env` 文件：

```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_NAME=OpenClaw权限管理系统
REACT_APP_VERSION=1.0.0
```

### 4. 启动应用

#### 启动后端

```bash
cd backend
npm run dev
```

#### 启动前端

```bash
cd frontend
npm start
```

### 5. 访问应用

打开浏览器访问：`http://localhost:3000`

## 详细安装步骤

### 后端安装

1. **进入后端目录**
   ```bash
   cd backend
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **初始化数据库**
   ```bash
   npm run init-db
   ```

4. **启动开发服务器**
   ```bash
   npm run dev
   ```

### 前端安装

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm start
   ```

## 使用Docker部署

### 使用Docker Compose

1. **安装Docker和Docker Compose**

2. **克隆项目**
   ```bash
   git clone <repository-url>
   cd openclaw-permission-manager
   ```

3. **构建和启动服务**
   ```bash
   docker-compose up -d
   ```

4. **访问应用**
   - 前端：`http://localhost:3000`
   - 后端API：`http://localhost:3001`

### 单独运行Docker容器

#### 后端容器

```bash
# 构建镜像
docker build -t openclaw-permission-manager-backend ./backend

# 运行容器
docker run -p 3001:3001 \
  -e NODE_ENV=production \
  -e JWT_SECRET=your-production-secret-key \
  -v $(pwd)/backend/data:/app/data \
  openclaw-permission-manager-backend
```

#### 前端容器

```bash
# 构建镜像
docker build -t openclaw-permission-manager-frontend ./frontend

# 运行容器
docker run -p 3000:80 openclaw-permission-manager-frontend
```

## 生产环境部署

### 使用PM2

1. **安装PM2**
   ```bash
   npm install -g pm2
   ```

2. **启动后端**
   ```bash
   cd backend
   pm2 start ecosystem.config.js
   ```

3. **使用Nginx反向代理**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:3001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### 使用Systemd

创建服务文件 `/etc/systemd/system/openclaw-permission-manager.service`：

```ini
[Unit]
Description=OpenClaw Permission Manager Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/openclaw-permission-manager/backend
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start openclaw-permission-manager
sudo systemctl enable openclaw-permission-manager
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   lsof -i :3001
   lsof -i :3000
   
   # 修改端口
   # 后端：编辑 backend/.env 中的 PORT
   # 前端：修改 frontend/package.json 中的 start 脚本
   ```

2. **数据库错误**
   ```bash
   # 检查数据库文件权限
   chmod -R 755 backend/data/
   
   # 重新初始化数据库
   cd backend
   npm run init-db
   ```

3. **前端无法连接后端**
   - 检查后端是否正在运行
   - 检查网络连接
   - 验证API URL配置

### 日志查看

**Docker容器日志：**
```bash
docker logs openclaw-permission-manager-backend
docker logs openclaw-permission-manager-frontend
```

**PM2日志：**
```bash
pm2 logs
pm2 logs openclaw-permission-manager
```

### 性能优化

1. **使用缓存**
   ```bash
   # 启用Redis缓存
   npm install redis
   
   # 配置缓存
   ```
2. **数据库优化**
   ```bash
   # 定期备份数据库
   sqlite3 backend/data/permissions.db ".backup backup.db"
   
   # 添加索引
   sqlite3 backend/data/permissions.db "CREATE INDEX idx_users_role ON users(role);"
   ```

## 监控

### 健康检查

```bash
# 后端健康检查
curl http://localhost:3001/api/health

# 前端健康检查
curl http://localhost:3000
```

### 监控指标

- 内存使用率
- CPU使用率
- 响应时间
- 数据库连接数
- 错误率

## 备份与恢复

### 数据库备份

```bash
# 创建备份
sqlite3 backend/data/permissions.db ".backup backup_$(date +%Y%m%d_%H%M%S).db"

# 恢复备份
sqlite3 backend/data/permissions.db ".restore backup_20240101_120000.db"
```

### 配置备份

```bash
# 备份配置文件
tar -czf config_backup.tar.gz backend/.env frontend/.env

# 恢复配置
tar -xzf config_backup.tar.gz
```