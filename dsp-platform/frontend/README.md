# DSP全媒体广告平台 - 前端项目

## 项目简介

DSP全媒体广告平台是一个功能完善的广告投放管理系统，支持抖音、快手、B站、微博、小红书等国内主流媒体的广告投放管理。

## 技术栈

### 核心框架
- **React 18**: 用户界面框架
- **TypeScript**: 类型安全
- **Vite**: 构建工具

### UI组件库
- **Ant Design 5.x**: 企业级UI组件库
- **@ant-design/icons**: 图标组件

### 状态管理
- **Redux Toolkit**: 状态管理
- **RTK Query**: 数据获取和缓存

### 图表库
- **ECharts**: 专业数据可视化
- **echarts-for-react**: React集成

### 实时通信
- **Socket.IO Client**: WebSocket客户端
- **socket.io**: 实时数据推送

### 其他工具
- **dayjs**: 日期处理
- **axios**: HTTP客户端
- **react-use**: React Hooks工具集

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── components/         # 可复用组件
│   │   ├── layout/        # 布局组件
│   │   │   └── MainLayout.tsx
│   │   ├── common/        # 通用组件
│   │   │   ├── PageHeader.tsx
│   │   │   ├── DataTable.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   ├── LoadingOverlay.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   └── FilterBar.tsx
│   │   ├── charts/        # 图表组件
│   │   │   ├── LineChart.tsx
│   │   │   ├── BarChart.tsx
│   │   │   ├── PieChart.tsx
│   │   │   └── RealtimeChart.tsx
│   │   └── forms/         # 表单组件
│   │       ├── CampaignForm.tsx
│   │       ├── AdGroupForm.tsx
│   │       ├── CreativeForm.tsx
│   │       └── TargetingForm.tsx
│   ├── pages/             # 页面组件
│   │   ├── auth/          # 认证页面
│   │   │   └── Login.tsx
│   │   ├── dashboard/     # 仪表盘
│   │   │   └── Dashboard.tsx
│   │   ├── account/       # 账户管理
│   │   │   ├── AccountList.tsx
│   │   │   └── AccountAuthorize.tsx
│   │   ├── campaign/      # 广告计划
│   │   │   ├── CampaignList.tsx
│   │   │   ├── CampaignCreate.tsx
│   │   │   └── CampaignEdit.tsx
│   │   ├── adgroup/       # 广告组
│   │   │   ├── AdGroupList.tsx
│   │   │   ├── AdGroupCreate.tsx
│   │   │   └── AdGroupEdit.tsx
│   │   ├── creative/      # 广告创意
│   │   │   ├── CreativeList.tsx
│   │   │   └── CreativeUpload.tsx
│   │   ├── monitor/       # 数据监控
│   │   │   └── DataMonitor.tsx
│   │   ├── report/        # 效果报表
│   │   │   ├── ReportDaily.tsx
│   │   │   ├── ReportWeekly.tsx
│   │   │   └── ReportCustom.tsx
│   │   ├── analysis/      # 数据分析
│   │   │   ├── CampaignAnalysis.tsx
│   │   │   ├── CreativeAnalysis.tsx
│   │   │   └── AudienceAnalysis.tsx
│   │   └── settings/      # 系统设置
│   │       ├── UserSettings.tsx
│   │       ├── SystemSettings.tsx
│   │       └── PermissionManagement.tsx
│   ├── store/             # Redux状态管理
│   │   ├── store.ts       # Store配置
│   │   ├── services/      # API服务（RTK Query）
│   │   │   ├── api.ts
│   │   │   ├── accountApi.ts
│   │   │   ├── campaignApi.ts
│   │   │   ├── adGroupApi.ts
│   │   │   └── creativeApi.ts
│   │   └── slices/        # Redux Slices
│   │       ├── authSlice.ts
│   │       ├── campaignSlice.ts
│   │       ├── adGroupSlice.ts
│   │       ├── creativeSlice.ts
│   │       └── monitorSlice.ts
│   ├── hooks/             # 自定义Hooks
│   │   ├── useWebSocket.ts
│   │   ├── usePagination.ts
│   │   └── useTableSelection.ts
│   ├── types/             # TypeScript类型定义
│   │   └── index.ts
│   ├── utils/             # 工具函数
│   │   └── format.ts
│   ├── styles/            # 全局样式
│   │   └── global.css
│   ├── App.tsx            # 应用根组件
│   ├── main.tsx           # 应用入口
│   └── vite-env.d.ts      # Vite类型声明
├── index.html             # HTML模板
├── package.json           # 项目依赖
├── tsconfig.json          # TypeScript配置
├── vite.config.ts         # Vite配置
└── README.md             # 项目说明
```

## 路由设计

### 公开路由
- `/login` - 登录页面

### 主应用路由（共24个）
1. `/dashboard` - 数据总览仪表盘

2. **账户管理**（2个路由）
   - `/accounts` - 账户列表
   - `/accounts/authorize` - 账户授权

3. **广告计划**（3个路由）
   - `/campaigns` - 计划列表
   - `/campaigns/create` - 新建计划
   - `/campaigns/:id/edit` - 编辑计划

4. **广告组**（3个路由）
   - `/ad-groups` - 广告组列表
   - `/ad-groups/create` - 新建广告组
   - `/ad-groups/:id/edit` - 编辑广告组

5. **广告创意**（2个路由）
   - `/creatives` - 创意列表
   - `/creatives/upload` - 上传创意

6. **数据监控**（1个路由）
   - `/monitor` - 实时数据监控

7. **效果报表**（3个路由）
   - `/reports/daily` - 日报表
   - `/reports/weekly` - 周报表
   - `/reports/custom` - 自定义报表

8. **数据分析**（3个路由）
   - `/analysis/campaign` - 计划分析
   - `/analysis/creative` - 创意分析
   - `/analysis/audience` - 人群分析

9. **系统设置**（3个路由）
   - `/settings/user` - 用户设置
   - `/settings/system` - 系统设置
   - `/settings/permissions` - 权限管理

## 核心功能

### 1. 账户管理
- 多账户列表展示
- 账户授权管理（抖音、快手、B站、微博、小红书）
- 账户状态同步
- 账户余额监控

### 2. 广告计划管理
- 计划列表查询和筛选
- 新建广告计划
- 编辑计划信息
- 批量启停操作
- 计划数据概览

### 3. 广告组管理
- 广告组列表管理
- 精细化定向设置（年龄、性别、地域、兴趣、设备等）
- 出价和预算配置
- 实时性能监控

### 4. 广告创意管理
- 创意素材上传（图片、视频）
- 创意预览
- 创意效果分析
- 批量管理

### 5. 数据监控
- WebSocket实时数据推送
- 多维度数据展示（曝光、点击、消耗、转化）
- 实时图表更新
- 自动刷新控制

### 6. 效果报表
- 日报表、周报表
- 自定义报表生成
- 数据导出功能
- 多维度分析

### 7. 数据分析
- 计划表现分析
- 创意效果分析
- 人群画像分析
- 平台对比分析

## 组件设计

### 通用组件
- **PageHeader**: 页面头部组件，包含标题、操作按钮
- **DataTable**: 数据表格组件，支持分页、排序、筛选
- **StatusBadge**: 状态标签组件
- **LoadingOverlay**: 加载遮罩组件
- **EmptyState**: 空状态组件
- **FilterBar**: 筛选栏组件

### 图表组件
- **LineChart**: 折线图（支持面积图）
- **BarChart**: 柱状图（支持横向）
- **PieChart**: 饼图（支持玫瑰图）
- **RealtimeChart**: 实时折线图

### 表单组件
- **CampaignForm**: 广告计划表单
- **AdGroupForm**: 广告组表单
- **CreativeForm**: 广告创意表单
- **TargetingForm**: 定向设置表单

## 状态管理

### Redux Slices
- **authSlice**: 用户认证状态
- **campaignSlice**: 广告计划筛选和选择
- **adGroupSlice**: 广告组筛选和选择
- **creativeSlice**: 创意筛选和选择
- **monitorSlice**: 监控页面状态

### RTK Query APIs
- **accountApi**: 账户相关API
- **campaignApi**: 广告计划相关API
- **adGroupApi**: 广告组相关API
- **creativeApi**: 创意相关API

## 自定义Hooks

- **useWebSocket**: WebSocket连接管理
- **usePagination**: 分页状态管理
- **useTableSelection**: 表格选择管理

## 工具函数

- **formatNumber**: 数字格式化
- **formatCurrency**: 金额格式化
- **formatPercent**: 百分比格式化
- **formatDateTime**: 日期时间格式化
- **formatDate**: 日期格式化
- **formatTime**: 时间格式化
- **formatRelativeTime**: 相对时间格式化
- **formatFileSize**: 文件大小格式化
- **formatDuration**: 时长格式化

## 开发指南

### 环境要求
- Node.js >= 18
- npm >= 9

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

开发服务器将在 http://localhost:3000 启动

### 构建生产版本
```bash
npm run build
```

### 预览生产构建
```bash
npm run preview
```

### 代码检查
```bash
npm run lint
```

### 代码格式化
```bash
npm run lint:fix
```

## 配置说明

### API代理配置
在 `vite.config.ts` 中配置了API代理：
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### WebSocket配置
在 `useWebSocket.ts` 中配置WebSocket连接：
```typescript
const socket = io('http://localhost:8000', {
  transports: ['websocket', 'polling'],
  reconnection: true,
})
```

## 类型定义

所有TypeScript类型定义在 `src/types/index.ts` 中，包括：
- Account: 账户信息
- Campaign: 广告计划
- AdGroup: 广告组
- Creative: 广告创意
- RealTimeData: 实时数据
- ReportData: 报表数据
- User: 用户信息

## 样式规范

- 使用Ant Design主题系统
- 全局样式在 `src/styles/global.css`
- 组件内联样式使用style对象
- 推荐使用CSS Modules或styled-components进行复杂样式管理

## 性能优化

1. 使用React.memo和useMemo优化组件渲染
2. RTK Query自动缓存API响应
3. 虚拟滚动处理大数据表格
4. 图片懒加载
5. 代码分割和懒加载

## 浏览器兼容性

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 许可证

MIT License

## 作者

Echo-2 - Agentic AI
