# 巨量引擎广告平台对接指导书

## 目录
1. [系统概述](#系统概述)
2. [访问地址](#访问地址)
3. [网络资源与API文档](#网络资源与api文档)
4. [快速开始](#快速开始)
5. [功能模块使用指南](#功能模块使用指南)
6. [常见问题](#常见问题)
7. [技术支持](#技术支持)

---

## 系统概述

本广告平台管理系统是一套完整的巨量引擎广告管理解决方案，支持：

- **账户管理**：多账户管理，授权授权
- **广告计划**：计划创建、编辑、启用/停用
- **广告组**：单元管理，预算控制
- **创意管理**：素材上传、创意创建
- **数据报表**：日报表、实时数据查询
- **转化回传**：转化数据上报、查询

---

## 访问地址

### 生产环境
```
前端地址：http://43.156.131.98:5173
后端API：http://43.156.131.98:5000
API文档：http://43.156.131.98:5000/docs
```

### 健康检查
```bash
curl http://43.156.131.98:5000/health
```

---

## 网络资源与API文档

### 官方文档

1. **巨量引擎开放平台**
   - 网址：https://open.oceanengine.com/
   - 包含：产品介绍、接入指南、API文档、SDK下载

2. **API文档中心**
   - 网址：https://open.oceanengine.com/doc/index.html
   - 包含：所有API接口文档、参数说明、返回示例

3. **开发者社区**
   - 网址：https://www.oceanengine.com/
   - 包含：常见问题、技术讨论、更新公告

### 核心API接口

#### OAuth2 认证
- **授权URL生成**：GET `/oauth2/authorize/`
- **获取Access Token**：POST `/oauth2/access_token/`
- **刷新Token**：POST `/oauth2/refresh_token/`

#### 广告计划
- **创建计划**：POST `/2/campaign/create/`
- **查询计划**：GET `/2/campaign/get/`
- **更新计划**：POST `/2/campaign/update/`
- **删除计划**：POST `/2/campaign/delete/`

#### 广告组
- **创建广告组**：POST `/2/adgroup/create/`
- **查询广告组**：GET `/2/adgroup/get/`
- **更新广告组**：POST `/2/adgroup/update/`

#### 创意
- **创建创意**：POST `/2/creative/create/`
- **查询创意**：GET `/2/creative/get/`

#### 数据报表
- **获取日报表**：GET `/3/report/ad/get/`

#### 转化回传
- **上传转化**：POST `/2/conversion/upload/`
- **查询转化**：GET `/2/conversion/query/`

---

## 快速开始

### 步骤1：获取应用凭证

1. 注册巨量引擎开发者账号
2. 创建应用，获取：
   - `app_id`：应用ID
   - `app_secret`：应用密钥

### 步骤2：配置系统

修改后端配置文件 `.env`：
```bash
OCEAN_APP_ID=your_app_id
OCEAN_APP_SECRET=your_app_secret
OCEAN_REDIRECT_URI=http://43.156.131.98:5173/oauth/callback
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ad_platform
REDIS_URL=redis://localhost:6379/0
```

### 步骤3：OAuth2 授权

#### 方式一：系统内授权

1. 访问：http://43.156.131.98:5173
2. 点击左侧「账户管理」
3. 点击「添加账户」
4. 系统自动跳转到巨量引擎授权页
5. 授权成功后自动返回并保存账户信息

#### 方式二：手动授权

1. 访问授权URL：
   ```
   https://ad.oceanengine.com/openapi/oauth2/index.html?app_id={app_id}&redirect_uri={redirect_uri}
   ```

2. 扫码或登录巨量广告账号
3. 授权成功后跳转回系统，获取 `auth_code`

4. 使用 `auth_code` 换取 `access_token`：
   ```bash
   POST http://43.156.131.98:5000/api/v1/oauth/callback?auth_code={auth_code}
   ```

---

## 功能模块使用指南

### 1. 账户管理

#### 添加账户
1. 进入「账户管理」页面
2. 点击「添加账户」按钮
3. 填写表单：
   - 广告主ID：巨量广告账户ID
   - 广告主名称：自定义名称
   - 访问令牌：OAuth2 授权获取的 access_token
   - 刷新令牌：OAuth2 授权获取的 refresh_token
4. 点击「创建」保存

#### 管理账户
- **编辑**：修改账户信息
- **删除**：删除不再使用的账户
- **查看状态**：启用/禁用状态

#### Token 刷新
系统会自动检测 Token 过期，使用 refresh_token 自动刷新。

---

### 2. 广告计划管理

#### 创建计划
1. 进入「广告计划」页面
2. 点击「创建计划」按钮
3. 填写表单：
   - 计划名称：自定义名称
   - 广告主ID：选择已授权的账户
   - 预算模式：1-日预算，2-总预算
   - 预算金额：单位：分
   - 投放时间：选择开始和结束时间
   - 推广目标：选择推广目标类型
4. 点击「创建」提交

#### 管理计划
- **启用/停用**：控制计划投放状态
- **编辑**：修改计划信息
- **删除**：删除已结束的计划

---

### 3. 广告组管理

#### 创建广告组
1. 进入「广告组」页面
2. 点击「创建广告组」按钮
3. 填写表单：
   - 广告组名称：自定义名称
   - 所属计划：选择已创建的广告计划
   - 预算控制：设置预算上限
   - 定向设置：设置人群定向、地域定向等
4. 点击「创建」提交

---

### 4. 创意管理

#### 上传创意
1. 进入「创意管理」页面
2. 点击「上传创意」按钮
3. 选择创意类型：
   - 视频：支持 MP4 格式
   - 图片：支持 JPG、PNG 格式
4. 上传素材文件
5. 填写创意信息：
   - 创意名称
   - 创意类型
   - 创意素材模式
6. 点击「创建」提交

---

### 5. 数据报表

#### 查看日报表
1. 进入「数据报表」页面
2. 选择日期范围
3. 点击「查询」按钮
4. 查看报表数据：
   - 消耗：广告花费
   - 曝光：广告展示次数
   - 点击：广告点击次数
   - 点击率(CTR)：点击/曝光
   - 千次曝光费用(CPM)
   - 平均点击成本(CPC)
   - 转化数：转化完成次数

#### 数据导出
- 点击「导出」按钮下载 Excel 或 CSV 格式报表

---

### 6. 转化回传

#### 上传转化数据
1. 进入「转化回传」页面
2. 点击「上传转化」按钮
3. 填写表单：
   - 点击ID：广告点击追踪ID
   - 转化时间：转化发生时间
   - 转化类型：注册、下单、支付等
4. 点击「上传」提交

#### 查询转化记录
- 查看已上传的转化数据
- 查看转化状态：成功、处理中、失败

---

## API 调用示例

### 1. 创建广告计划

```bash
curl -X POST "http://43.156.131.98:5000/api/v1/campaign/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "advertiser_id": "100000001",
    "campaign_name": "测试计划",
    "budget_mode": 1,
    "budget": 100000,
    "start_time": "2026-02-28T00:00:00Z",
    "end_time": "2026-03-31T23:59:59Z",
    "objectives": ["LIFESPAN_PROMOTION"]
  }'
```

### 2. 查询计划列表

```bash
curl -X GET "http://43.156.131.98:5000/api/v1/campaign/list" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "advertiser_id": "100000001",
    "page": 1,
    "page_size": 10
  }'
```

### 3. 上传转化数据

```bash
curl -X POST "http://43.156.131.98:5000/api/v1/conversion/upload" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "advertiser_id": "100000001",
    "conversions": [
      {
        "click_id": "click_123456",
        "conversion_time": "2026-02-28T12:00:00Z",
        "conversion_type": "register"
      }
    ]
  }'
```

### 4. 获取日报表

```bash
curl -X POST "http://43.156.131.98:5000/api/v1/report/daily" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "advertiser_id": "100000001",
    "start_date": "2026-02-20",
    "end_date": "2026-02-28",
    "page": 1,
    "page_size": 20
  }'
```

---

## 常见问题

### Q1：如何获取 app_id 和 app_secret？

**A：**
1. 注册巨量引擎开发者账号
2. 登录 https://open.oceanengine.com/
3. 创建应用，系统会自动分配 app_id 和 app_secret

### Q2：授权 URL 无效？

**A：**
- 检查 redirect_uri 是否与后台配置一致
- 确保域名已在巨量引擎白名单中

### Q3：Token 过期如何处理？

**A：**
- 系统会自动使用 refresh_token 刷新
- 如刷新失败，需要重新授权

### Q4：数据报表有延迟吗？

**A：**
- 是的，巨量引擎数据通常有 1-2 小时延迟
- 可通过「实时数据」接口查询最新数据

### Q5：如何调试 API 请求？

**A：**
1. 使用 API 文档页面测试：http://43.156.131.98:5000/docs
2. 查看后端日志
3. 使用浏览器 F12 开发者工具查看请求详情

### Q6：素材上传失败？

**A：**
- 检查素材格式和大小限制
- 视频时长不超过 30 秒
- 图片大小不超过 5MB

---

## 技术支持

### 联系方式
- 系统管理员：[联系方式]
- 技术支持邮箱：[邮箱地址]
- 工单系统：[工单链接]

### 问题反馈

遇到问题时，请提供以下信息：
1. 操作步骤
2. 错误截图
3. 浏览器版本
4. 错误时间

### 系统更新

系统会定期更新优化，更新内容包括：
- 功能增强
- 性能优化
- Bug 修复
- 安全加固

---

## 附录

### A. API 签名说明

巨量引擎 API 需要对所有请求进行 MD5 签名，签名算法：

1. 将所有请求参数按字典序排序
2. 拼接成字符串：`key1=value1&key2=value2`
3. 在末尾追加 `app_secret`
4. 计算 MD5 哈希值
5. 将哈希值作为 `signature` 参数

### B. 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 40001 | 参数错误 | 检查请求参数 |
| 40002 | Token 无效 | 刷新 Token 或重新授权 |
| 40003 | 权限不足 | 检查应用权限 |
| 40004 | 账户余额不足 | 充值广告账户 |
| 40005 | 广告计划不存在 | 检查计划 ID |

### C. 数据字段说明

#### 广告计划
- `campaign_id`：计划ID（巨量引擎返回）
- `campaign_name`：计划名称
- `budget`：预算（单位：分）
- `status`：状态（enable-启用，disable-停用）

#### 报表数据
- `cost`：消耗（单位：分）
- `show`：曝光次数
- `click`：点击次数
- `ctr`：点击率（百分比）
- `cpm`：千次曝光费用（单位：分）
- `cpc`：平均点击成本（单位：分）
- `convert`：转化数

---

## 更新日志

### v1.0.0 (2026-02-28)
- 初始版本发布
- 支持账户管理
- 支持广告计划管理
- 支持数据报表
- 支持转化回传

---

**本文档持续更新中，请关注最新版本**
