# Git 仓库创建步骤

> 技能名称：oceanengine-ads
> 版本：1.0.0
> 准备日期：2026-03-09

---

## 📋 准备工作

### 1. 创建 GitHub 账户

如果你还没有 GitHub 账户：
1. 访问：https://github.com/signup
2. 使用 AQzzzQA 或你的邮箱注册
3. 验证邮箱

### 2. 创建 GitHub 仓库

1. 登录 GitHub：https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   ```
   Repository name: oceanengine-ads
   Description: 🎯 巨量广告自动化投放技能 - LemClaw Skills
   Public/Private: Public（推荐）
   Initialize with: README（可选）
   ```
4. 点击 "Create repository"

---

## 🚀 提交代码

### 步骤1：初始化 Git 仓库

```bash
cd /root/.openclaw/workspace/skills/oceanengine-ads

# 初始化 Git
git init

# 配置用户信息
git config user.name "AQzzzQA"
git config user.email "aoqian@lemhd.cn"
```

### 步骤2：添加所有文件

```bash
# 添加所有文件
git add .

# 查看要提交的文件
git status
```

### 步骤3：首次提交

```bash
# 提交所有更改
git commit -m "feat: 巨量广告自动化投放技能 v1.0.0

- 100+ API 接口封装
- 智能自动化投放引擎
- ROI 优化算法
- 完整测试套件（100%通过）
- 乐盟互动品牌植入
- 按月付费说明"
```

---

## 📤 推送到 GitHub

### 步骤1：添加远程仓库

```bash
# 添加 GitHub 仓库远程地址
# 替换 <your-username> 为你的 GitHub 用户名
git remote add origin https://github.com/<your-username>/oceanengine-ads.git
```

### 步骤2：推送到 GitHub

```bash
# 推送主分支
git push -u origin main

# 或推送所有分支
git push --all origin
```

### 如果提示输入用户名和密码

GitHub 可能会提示输入：
- **Username**: 你的 GitHub 用户名（如 AQzzzQA）
- **Password**: 使用 **Personal Access Token**（不是账户密码）
  1. 访问：https://github.com/settings/tokens
  2. 点击 "Generate new token" (classic)
  3. 选择权限：
     - ☑️ repo（完整仓库访问权限）
  4. 生成 Token（如：`ghp_xxxxxxxxxxxxxxxxxxxxxxxx`）
  5. 复制 Token 并粘贴到密码字段

---

## ✅ 验证成功

### 在 GitHub 上查看

1. 访问：https://github.com/<your-username>/oceanengine-ads
2. 检查：
   - ✅ README.md 文件
   - ✅ 代码文件（auth.py, api_client.py 等）
   - ✅ LICENSE 文件
   - ✅ 提交历史

### 仓库信息

```
Repository Name: oceanengine-ads
Description: 🎯 巨量广告自动化投放技能 - LemClaw Skills
License: MIT
Language: Python
Topics: oceanengine, tiktok, bytedance, advertising, automation, optimization
```

---

## 🔗 仓库地址

### GitHub URL（创建后）

```
https://github.com/<your-username>/oceanengine-ads
```

### Clone URL（供他人使用）

```bash
git clone https://github.com/<your-username>/oceanengine-ads.git
```

---

## 📝 仓库配置建议

### 添加 Topics（标签）

在仓库 Settings → Topics 中添加：
```
oceanengine, tiktok, bytedance, advertising, automation, optimization, lemclaw, 巨量广告
```

### 设置 Branch Protection（推荐）

Settings → Branches → Add rule：
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

### 添加 License（已完成）

文件已创建：`LICENSE` (MIT License)

---

## 🎯 下一步

### 1. 在 GitHub 上分享

- 分享仓库链接到社交平台
- 提交到 OpenClaw 社区
- 在开发者论坛中分享

### 2. 创建 Releases

```bash
# 创建 Git 标签
git tag -a v1.0.0 -m "v1.0.0 release"

# 推送标签到 GitHub
git push origin v1.0.0
```

然后在 GitHub 网站创建 Release：
1. 进入 Releases 页面
2. 点击 "Draft a new release"
3. 选择标签：`v1.0.0`
4. 填写 Release 标题和说明
5. 点击 "Publish release"

---

## 📞 联系方式

### 乐盟互动 LemClaw

- **技术支持**：aoqian@lemhd.cn
- **商务合作**：business@lemclaw.com
- **官网**：https://www.lemclaw.com

---

**🎯 准备就绪，可以开始创建 GitHub 仓库了！**

---

**下一步**：
1. 在 GitHub 创建仓库
2. 按照 Git 命令推送代码
3. 验证仓库成功

**完成后告诉我，我会帮你准备推广材料！** 🚀