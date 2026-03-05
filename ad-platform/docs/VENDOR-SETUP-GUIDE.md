# 巨量引擎对接 - 开发者账号注册指南

## 一、开发者账号注册

### 1.1 巨量引擎开发者平台

**注册地址**: https://dev.oceanengine.com/

### 1.2 注册流程

1. **访问开发者平台**
   - 打开 https://dev.oceanengine.com/
   - 点击"注册"按钮

2. **填写注册信息**
   - 手机号验证（中国大陆手机号）
   - 邮箱验证
   - 设置密码
   - 企业信息（营业执照、公司名称等）

3. **完成实名认证**
   - 上传营业执照
   - 法人身份证正反面
   - 企业对公账户信息
   - 审核周期：1-3个工作日

4. **创建应用**
   - 登录后进入"应用管理"
   - 点击"创建应用"
   - 填写应用名称、应用描述
   - 选择应用类型（广告管理、数据分析等）

5. **获取 API 凭证**
   - 进入"API凭证"页面
   - 记录以下信息：
     - App ID
     - App Secret
     - Access Token

---

## 二、巨量广告账号开通

### 2.1 开通广告账号

**广告平台**: https://www.oceanengine.com/

### 2.2 开通流程

1. **企业认证**
   - 提交企业资质认证
   - 等待审核（1-3个工作日）

2. **充值**
   - 绑定企业对公账户
   - 充值广告费用（首充建议 5000 元以上）

3. **获取广告主 ID**
   - 在账户设置中查看广告主 ID
   - 格式如：`100000001`

4. **获取授权 Token**
   - 在开发者平台创建授权应用
   - 使用授权流程获取 access_token

---

## 三、API 接入配置

### 3.1 API 基础信息

**API 文档**: https://dev.oceanengine.com/doc/index.html?key=2967975365575320&type=1&id=699667

**API 环境地址**:
- 沙箱环境: `https://api-sandbox.oceanengine.com/`
- 正式环境: `https://ad.oceanengine.com/`

### 3.2 API 凭证配置

在项目配置文件中添加：

```python
# app/core/settings.py

OCEAN_ENGINE = {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "access_token": "your_access_token",
    "advertiser_id": "your_advertiser_id",
    "api_base_url": "https://ad.oceanengine.com/",
}
```

### 3.3 API 权限申请

在开发者平台申请以下权限：
- 广告计划管理
- 创意管理
- 数据报表
- 定向管理
- 出价管理

---

## 四、测试账号申请

### 4.1 沙箱环境测试

1. **申请沙箱环境**
   - 在开发者平台申请沙箱权限
   - 审核通过后获得沙箱账号

2. **测试流程**
   - 使用沙箱环境进行 API 调用测试
   - 验证所有接口功能
   - 测试完成后切换到正式环境

### 4.2 测试数据准备

准备以下测试数据：
- 测试广告计划（至少 2 个）
- 测试创意素材（至少 3 张图片）
- 测试定向配置
- 测试出价策略

---

## 五、开发辅助工具

### 5.1 API 调试工具

**Postman Collection**: 使用官方提供的 Postman 集合

**下载地址**: https://dev.oceanengine.com/doc/index.html?key=2967975365575320&type=1&id=699667

### 5.2 SDK 下载

**官方 SDK**:
- Python SDK: https://github.com/bytedance/pangolin-sdk-python
- Java SDK: https://github.com/bytedance/pangolin-sdk-java

### 5.3 文档资源

- **API 文档**: https://dev.oceanengine.com/doc/index.html?key=2967975365575320&type=1&id=699667
- **接入指南**: https://dev.oceanengine.com/doc/index.html?key=2967975365575320&type=1&id=699667
- **常见问题**: https://dev.oceanengine.com/doc/index.html?key=2967975365575320&type=1&id=699667

---

## 六、对接关键步骤

### 6.1 授权流程

1. **获取授权码**
   - 重定向用户到授权页面
   - 用户授权后获取 authorization_code

2. **换取 Access Token**
   - 使用 authorization_code 换取 access_token
   - access_token 有效期：30 天

3. **刷新 Token**
   - 使用 refresh_token 刷新 access_token

### 6.2 API 调用流程

1. **签名生成**
   - 使用 app_secret 生成签名
   - 将签名添加到请求头

2. **发送请求**
   - 调用 API 接口
   - 处理响应结果

3. **错误处理**
   - 解析错误码
   - 重试机制
   - 日志记录

---

## 七、注意事项

### 7.1 速率限制

- API 调用频率限制：10 次/秒
- 建议：使用令牌桶算法控制调用频率

### 7.2 数据更新延迟

- 广告数据更新延迟：15-30 分钟
- 报表数据更新延迟：1-2 小时
- 建议：设置合理的轮询间隔

### 7.3 审核流程

- 广告计划审核：1-2 小时
- 创意审核：1-2 小时
- 建议：提前准备素材，预留审核时间

### 7.4 费用说明

- API 调用：免费
- 广告投放：按实际消耗计费
- 建议设置预算上限

---

## 八、对接检查清单

### 8.1 开发前准备

- [ ] 注册巨量引擎开发者账号
- [ ] 完成企业实名认证
- [ ] 开通广告账号
- [ ] 充值测试金额
- [ ] 创建应用获取 API 凭证

### 8.2 开发中检查

- [ ] 配置 API 基础信息
- [ ] 实现授权流程
- [ ] 实现签名生成
- [ ] 实现错误处理
- [ ] 测试所有 API 接口

### 8.3 上线前检查

- [ ] 切换到正式环境
- [ ] 更新 API 凭证
- [ ] 设置预算上限
- [ ] 配置监控告警
- [ ] 完成压力测试

---

## 九、联系方式

### 9.1 官方支持

- **技术支持邮箱**: dev-support@oceanengine.com
- **客服电话**: 400-100-xxxx
- **在线客服**: 开发者平台内

### 9.2 开发者社区

- **开发者论坛**: https://dev.oceanengine.com/
- **技术交流群**: QQ群 xxxxxxxx

---

## 十、快速开始

### 第一步：注册账号（30 分钟）
1. 访问 https://dev.oceanengine.com/
2. 填写注册信息
3. 完成企业认证

### 第二步：创建应用（10 分钟）
1. 登录开发者平台
2. 创建新应用
3. 获取 API 凭证

### 第三步：测试接入（1 小时）
1. 申请沙箱环境
2. 配置 API 连接
3. 测试核心接口

### 第四步：正式对接（2 小时）
1. 切换正式环境
2. 测试完整流程
3. 准备上线

---

**总耗时**: 约 4 小时（不含审核等待时间）

**建议提前准备**，避免影响开发进度！

---

**文档更新**: 2026-03-01
**版本**: V1.0
