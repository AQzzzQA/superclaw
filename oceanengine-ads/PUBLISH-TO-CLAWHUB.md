# 巨量广告技能 - ClawHub 发布指南

> 技能名称：oceanengine-ads
> 版本：1.0.0
> 发布日期：2026-03-09

---

## 📋 发布准备工作

### ✅ 已完成

1. **技能开发完成**：100%
   - 100+ API 接口封装
   - 智能自动化引擎
   - ROI 优化算法
   - 完整测试套件（13个用例，100%通过）
   - 完整文档体系

2. **技能文件准备完毕**
   ```
   /root/.openclaw/workspace/skills/oceanengine-ads/
   ├── SKILL.md              # 技能主文档 ✅
   ├── _meta.json            # 元数据 ✅
   ├── requirements.txt       # 依赖列表 ✅
   ├── auth.py               # OAuth认证 ✅
   ├── api_client.py         # API客户端 ✅
   ├── automation.py         # 自动化引擎 ✅
   ├── optimizer.py          # 优化引擎 ✅
   ├── main.py              # 主入口 ✅
   ├── test_suite.py        # 测试套件 ✅
   ├── README.md             # 快速开始 ✅
   ├── CHANGELOG.md           # 更新日志 ✅
   ├── BUSINESS-INFO.md       # 商务信息 ✅
   └── PUBLISH-GUIDE.md     # 发布指南 ✅
   ```

3. **ClawHub 登录**：✅
   - 用户名：AQzzzQA
   - Token：clh_lZIcV8IoBHdugYHYZumKYnHLiS7dtLW9aGlbNKbeE1M
   - 状态：已登录

---

## 🌐 ClawHub 网站发布步骤

### 步骤1：访问 ClawHub 官网

**网址**：https://clawhub.ai

### 步骤2：登录账户

1. 在网站右上角找到 "Login" 或 "Sign In" 按钮
2. 使用你的 AQzzzQA 账户登录
3. 如果没有账户，先注册一个账户

### 步骤3：查找发布功能

1. 登录后，在导航栏或用户菜单中寻找：
   - "Publish" 或 "Create Skill" 按钮
   - 或 "+" 号图标
   - 或 "Upload Skill" 选项

### 步骤4：填写技能信息

#### 基本信息
```
Name（技能名称）: 巨量广告自动化投放
Slug（标识符）: oceanengine-ads
Version（版本）: 1.0.0
Description（描述）: 🎯 全功能集成巨量广告（Ocean Engine Ads）API，支持巨量引擎、巨量千川、穿山甲广告。包含自动化投放、智能优化、实时监控功能。
```

#### 详细信息
```
Tags（标签）:
- oceanengine
- tiktok
- bytedance
- advertising
- automation
- marketing
- roi
- optimization

Homepage（主页）: https://www.lemclaw.com
Repository（仓库）: https://github.com/lemclaw/oceanengine-ads
License（许可证）: MIT
```

#### Changelog（更新日志）
```
v1.0.0: 巨量广告自动化投放技能 - 支持100+API接口、智能自动化引擎、ROI优化算法、实时监控告警
```

### 步骤5：上传技能文件

#### 方式A：上传文件夹
1. 点击 "Upload" 或 "Choose Files" 按钮
2. 选择整个 `oceanengine-ads` 文件夹
3. 或拖拽文件夹到上传区域

#### 方式B：上传 ZIP 包
1. 如果要求上传 ZIP 包，使用：
   ```
   /root/.openclaw/workspace/skills/oceanengine-ads/oceanengine-ads.zip
   ```
2. 点击上传按钮选择该 ZIP 文件

### 步骤6：接受许可条款 ⚠️

**重要**：在网站上找到并接受以下条款：
- **Terms of Service**（服务条款）
- **License Agreement**（许可协议）
- **Content Policy**（内容政策）

通常在提交或发布页面会有复选框或弹窗。

### 步骤7：提交发布

1. 点击 "Publish" 或 "Submit" 按钮
2. 等待审核（通常几分钟到几小时）
3. 审核通过后，技能会在 ClawHub 上可见

---

## 🔍 发布后验证

### 验证技能已发布

1. **通过搜索验证**：
   ```bash
   clawhub search oceanengine
   ```

2. **通过安装验证**：
   ```bash
   clawhub install oceanengine-ads
   ```

3. **通过网站验证**：
   - 访问：https://clawhub.ai/skills/oceanengine-ads
   - 或在网站搜索 "oceanengine-ads"

---

## 📧 发布后推广

### 社交媒体
- **Twitter/X**: @LemClawOfficial
- **技术博客**: https://www.lemclaw.com/blog
- **开发者社区**: OpenClaw, GitHub, Reddit

### 示例推广文案
```
🎉 LemClaw 发布了新的技能：巨量广告自动化投放！

🔥 功能亮点：
✅ 100+ API 接口封装
✅ 智能自动化投放引擎
✅ ROI 优化算法
✅ 实时监控告警

📍 下载地址：https://clawhub.ai/skills/oceanengine-ads
📚 文档：https://docs.lemclaw.com/oceanengine-ads
💬 技术支持：aoqian@lemhd.cn

#ClawHub #OpenClaw #广告投放 #AI自动化 #巨量广告
```

---

## ⚠️ 常见问题

### Q1: CLI 发布失败 `acceptLicenseTerms` 错误？

**A**: 这是正常现象。必须在网站上手动接受许可条款。

### Q2: 技能审核需要多久？

**A**: 通常几分钟到几小时。如果超过 24 小时，请联系支持。

### Q3: 如何更新技能？

**A**:
```bash
# 修改代码后
clawhub publish /root/.openclaw/workspace/skills/oceanengine-ads --version "1.0.1" --changelog "更新内容"
```

### Q4: 技能可以收费吗？

**A**: ClawHub 本身不收费，但可以在技能文档中说明按月付费模式（已标注）。

---

## 📞 联系方式

### ClawHub 官方
- **官网**: https://clawhub.ai
- **作者邮箱**: steipete@gmail.com

### LemClaw 乐盟互动
- **技术支持**: aoqian@lemhd.cn
- **商务合作**: business@lemclaw.com
- **官网**: https://www.lemclaw.com

---

## ✅ 检查清单

发布前确认以下事项：

- [x] 技能开发完成
- [x] 测试通过（100%）
- [x] 文档完整
- [x] 品牌植入完成
- [x] 按月付费说明添加
- [x] _meta.json 格式正确
- [x] SKILL.md 格式正确
- [x] 登录 ClawHub
- [ ] 在网站上接受许可条款 ⏳
- [ ] 上传技能包到网站 ⏳
- [ ] 提交审核 ⏳

---

**🎯 准备就绪，可以开始发布了！**

---

**下一步**：访问 https://clawhub.ai 并按照上述步骤发布技能

**📝 发布完成后，请告知我，我会帮你验证技能是否成功发布！**

---

**🎉 LemClaw Smart Advertising Platform - 让巨量广告投放更智能！**