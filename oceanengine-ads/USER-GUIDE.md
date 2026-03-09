# 巨量广告技能 - 用户使用指南

> 技能名称：oceanengine-ads
> 版本：1.0.0
> 使用方式：本地 / GitHub

---

## 🎯 如何使用

### 方式1：本地直接使用（推荐）

```bash
# 进入技能目录
cd /root/.openclaw/workspace/skills/oceanengine-ads

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OCEANENGINE_ACCESS_TOKEN="your_token"
export OCEANENGINE_APP_ID="your_app_id"
export OCEANENGINE_APP_SECRET="your_app_secret"
export OCEANENGINE_TEST_MODE=false

# 测试连接
python3 -c "from auth import OceanEngineAuth; auth = OceanEngineAuth(); print(auth.test_connection())"

# 使用命令行工具
python3 main.py status
python3 main.py optimize <account_id>
```

---

### 方式2：通过 GitHub 克隆（推荐用于团队协作）

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/oceanengine-ads.git
cd oceanengine-ads

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OCEANENGINE_ACCESS_TOKEN="your_token"
export OCEANENGINE_APP_ID="your_app_id"
export OCEANENGINE_APP_SECRET="your_app_secret"
export OCEANENGINE_TEST_MODE=false

# 测试连接
python3 -c "from auth import OceanEngineAuth; auth = OceanEngineAuth(); print(auth.test_connection())"

# 使用技能
python3 main.py status
python3 main.py optimize <account_id>
```

### 方式3：通过已安装的技能

```bash
# 已安装 adspirer-ads-agent（巨量广告代理）
# 进入技能目录
cd /root/.openclaw/workspace/skills/adspirer-ads-agent

# 使用技能
python3 -c "
from main import OceanEngineMain
main = OceanEngineMain()
main.init()
main.optimize(account_id='your_id')
"
```

---

## 📊 技能快速开始

### 查询系统状态
```python3 main.py status
```

### 创建广告计划
```python3 main.py create <account_id> <name> <budget> <campaign_id> <campaign_id>
```

### 自动投放
```python3 main.py auto <campaign_id>
```

### 优化分析
```python3 main.py optimize <account_id>
```

### 生成报告
```python3 main.py report <account_id>
```

---

## 📋 文档资源

### 完整文档
```
/root/.openclaw/workspace/skills/oceanengine-ads/SKILL.md        # 技能主文档
/root/.openclaw/workspace/skills/oceanengine-ads/README.md          # 快速开始指南
/root/.openclaw/workspace/skills/oceanengine-ads/CHANGELOG.md       # 更新日志
/root/.openclaw/workspace/skills/oceanengine-ads/FINAL-REPORT.md     # 最终报告
/root/.openclaw/workspace/skills/oceanengine-ads/BUSINESS-INFO.md     # 商务信息
/root/.openclaw/workspace/skills/oceanengine-ads/FINAL-DELIVERY-SUCCESS.md # 最终交付总结
/root/.openclaw/workspace/skills/oceanengine-ads/FINAL-COMPLETION.md     # 最终完成总结
```

---

## 🤝 技术支持

### 巨量广告开放平台
- **巨量广告**：https://developer.oceanengine.com/
- **技术博客**：https://blog.oceanengine.com/
- **开发者论坛**：https://bbs.oceanengine.com/

### 乐盟互动 LemClaw
- **技术支持**：aoqian@lemhd.cn
- **商务合作**：business@lemclaw.com
- **官网**：https://www.lemclaw.com

---

## 🚀 立即可使用！

### 选择适合你当前场景的方式
1. **本地使用** - 推荐个人用户或小团队
2. **GitHub 克隆** - 推荐团队协作
3. **已安装技能** - 使用 `adspirer-ads-agent`（巨量广告代理）

---

**🎯 LemClaw Smart Advertising Platform - 让巨量广告投放更智能！**

---

**需要我帮你做其他事情吗？** 🚀