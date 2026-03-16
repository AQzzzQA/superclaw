# DSP平台前端项目

基于 Next.js 14 + TypeScript + Ant Design 的 DSP 广告管理平台前端

## 🚀 技术栈

- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **UI组件**: Ant Design 5
- **状态管理**: Zustand
- **路由**: Next.js Router
- **HTTP客户端**: Axios
- **样式**: Tailwind CSS

## 📋 功能特性

### ✅ 已完成（阶段1：基础框架）
- [x] 项目初始化
- [x] 依赖安装
- [x] 类型定义
- [x] API客户端封装
- [x] 状态管理（Zustand）
- [x] 布局组件（侧边栏 + 头部）
- [x] 登录页面
- [x] 仪表盘页面
- [x] 环境配置

### 🔄 待开发（阶段2：核心页面）
- [ ] 广告计划管理
- [ ] 广告组管理
- [ ] 创意管理
- [ ] 受众管理
- [ ] 报表系统

### 📅 计划中（阶段3：高级功能）
- [ ] 数据可视化（ECharts）
- [ ] 实时数据更新
- [ ] 权限管理
- [ ] 用户设置

## 🌐 项目结构

```
dsp-platform-frontend/
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── dashboard/    # 仪表盘
│   │   ├── login/        # 登录
│   │   ├── campaigns/    # 广告计划（待开发）
│   │   ├── adgroups/     # 广告组（待开发）
│   │   ├── creatives/    # 创意（待开发）
│   │   ├── audiences/    # 受众（待开发）
│   │   └── reports/      # 报表（待开发）
│   ├── components/       # 公共组件
│   │   └── Layout/       # 布局组件
│   ├── lib/              # 工具库
│   │   └── api.ts        # API客户端
│   ├── store/            # 状态管理
│   │   └── auth.ts       # 认证状态
│   └── types/            # 类型定义
│       └── index.ts
├── public/               # 静态资源
└── package.json
```

## 🔧 安装

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📊 页面清单

| 页面 | 路径 | 状态 |
|------|------|------|
| 首页 | / | ✅ 自动跳转 |
| 登录 | /login | ✅ 已完成 |
| 仪表盘 | /dashboard | ✅ 已完成 |
| 广告计划 | /campaigns | ⏳ 待开发 |
| 广告组 | /adgroups | ⏳ 待开发 |
| 创意 | /creatives | ⏳ 待开发 |
| 受众 | /audiences | ⏳ 待开发 |
| 报表 | /reports | ⏳ 待开发 |
| 设置 | /settings | ⏳ 待开发 |

## 🎯 核心功能

### 1. 认证系统
- ✅ 登录/退出
- ✅ JWT Token管理
- ✅ 自动Token刷新
- ✅ 路由守卫

### 2. 布局系统
- ✅ 响应式侧边栏
- ✅ 用户信息头部
- ✅ 菜单导航

### 3. 状态管理
- ✅ Zustand存储
- ✅ 持久化中间件
- ✅ 用户状态管理

## 🌐 API配置

环境变量 `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://43.156.131.98:8001
```

## 📝 开发规范

1. **组件命名**: 使用PascalCase
2. **文件命名**: 使用kebab-case或PascalCase
3. **类型定义**: 所有数据必须有TypeScript类型
4. **API调用**: 统一使用`api`对象
5. **状态管理**: 优先使用Zustand

## 🚀 部署

```bash
# 构建生产版本
npm run build

# 启动生产服务器
npm start
```

## 📄 License

MIT License

## 👥 作者

Echo-2 - Agentic AI
