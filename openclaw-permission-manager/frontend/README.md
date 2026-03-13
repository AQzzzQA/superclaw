# OpenClaw Permission Manager Frontend

前端React应用，用于OpenClaw权限配置可视化工具。

## 功能特性

- 用户管理界面
- 权限模板管理
- 配置文件管理
- 权限配置导出
- 响应式设计

## 技术栈

- React 18
- TypeScript
- Ant Design 5
- React Router
- Axios

## 安装与运行

### 1. 安装依赖

```bash
npm install
```

### 2. 环境配置

复制 `.env.example` 到 `.env` 并配置：

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
npm start
```

### 4. 构建生产版本

```bash
npm run build
```

## 项目结构

```
src/
├── components/          # 公共组件
│   └── Header.tsx      # 顶部导航栏
├── pages/              # 页面组件
│   ├── Dashboard.tsx   # 仪表板
│   ├── UserManagement.tsx  # 用户管理
│   ├── PermissionTemplates.tsx  # 权限模板管理
│   ├── ConfigManagement.tsx    # 配置管理
│   └── LoginPage.tsx   # 登录页面
├── services/           # API服务
│   ├── api.ts          # API配置
│   ├── authService.ts  # 认证服务
│   ├── userService.ts  # 用户服务
│   ├── permissionService.ts  # 权限服务
│   └── configService.ts    # 配置服务
├── types/              # TypeScript类型定义
│   └── index.ts
├── App.tsx             # 主应用组件
└── index.tsx           # 入口文件
```

## 主要功能

### 仪表板
- 用户统计信息
- 最近用户列表
- 系统状态

### 用户管理
- 用户列表查看
- 添加/编辑/删除用户
- 角色分配
- 权限管理

### 权限模板管理
- 权限模板列表
- 创建/编辑权限模板
- 模板预览
- 模板复制

### 配置管理
- 配置文件管理
- 生成用户配置
- 配置预览和导出
- JSON格式查看

## 开发工具

### 代码检查

```bash
npm run lint
```

### 测试

```bash
npm test
```

## 部署

### 构建生产版本

```bash
npm run build
```

### 使用Nginx部署

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/build;
        try_files $uri $uri/ /index.html;
    }
}
```

## 兼容性

- 浏览器: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- React 18+
- TypeScript 4.5+

## 许可证

MIT License