# DSP全媒体广告平台 - 快速开始指南

## 项目状态

✅ **前端架构和开发已完成**

## 快速启动

### 1. 进入项目目录
```bash
cd /root/.openclaw/workspace/dsp-platform/frontend
```

### 2. 安装依赖
```bash
npm install
```

### 3. 启动开发服务器
```bash
npm run dev
```

开发服务器将在 http://localhost:3000 启动

### 4. 访问应用
- 打开浏览器访问 http://localhost:3000
- 登录页面：输入任意用户名和密码即可登录（演示模式）

## 项目特点

### 24个完整路由
- 账户管理（2个）
- 广告计划（3个）
- 广告组（3个）
- 广告创意（2个）
- 数据监控（1个）
- 效果报表（3个）
- 数据分析（3个）
- 系统设置（3个）
- 其他（4个）

### 15个可复用组件
- 通用组件：6个
- 图表组件：4个
- 表单组件：4个
- 布局组件：1个

### 技术栈
- React 18 + TypeScript + Vite
- Ant Design 5.x
- Redux Toolkit + RTK Query
- ECharts + Socket.IO

## 核心功能

### 1. 账户管理
- 支持抖音、快手、B站、微博、小红书
- 账户授权和同步
- 余额监控

### 2. 广告投放
- 计划管理
- 广告组管理
- 精细化定向
- 创意上传

### 3. 数据监控
- WebSocket实时推送
- 多维度数据展示
- 自动刷新

### 4. 效果分析
- 日报/周报
- 自定义报表
- 计划/创意/人群分析

## 开发说明

### 环境变量
开发环境配置在 `.env.development`：
```
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### API代理
Vite配置了API代理，将 `/api` 请求转发到后端服务器

### WebSocket
实时数据通过WebSocket推送，使用Socket.IO客户端

## 可用命令

```bash
# 开发
npm run dev

# 构建
npm run build

# 预览构建
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run lint:fix
```

## 文档

- **README.md** - 详细项目文档
- **PROJECT_OVERVIEW.md** - 项目概览

## 下一步

1. 启动后端API服务
2. 配置真实的API地址
3. 连接数据库
4. 测试所有功能
5. 部署到生产环境

## 注意事项

- 当前使用模拟数据，需要连接真实后端API
- WebSocket连接需要后端支持Socket.IO
- 部分功能需要后端接口完善
- 建议在Chrome浏览器中开发

## 技术支持

如有问题，请参考：
- Ant Design文档：https://ant.design/
- React文档：https://react.dev/
- TypeScript文档：https://www.typescriptlang.org/
- Vite文档：https://vitejs.dev/
