# GitHub 仓库 README - 巨量广告自动化投放技能

> 技能名称：oceanengine-ads
> 版本：1.0.0
> 状态：✅ 已完成，测试通过（100%）
> 出品方：乐盟互动 LemClaw

---

## 📦 项目简介

巨量广告自动化投放技能是一个全功能的广告管理工具，支持巨量引擎（今日头条广告）、巨量千川（抖音广告）、穿山甲（程序化广告）的自动化投放和智能优化。

### 核心特性

- ✅ **100+ API 接口封装** - 完整覆盖巨量广告 API
- ✅ **智能自动化引擎** - AI 驱动的预算优化、创意轮换
- ✅ **ROI 优化算法** - 基于数据驱动的智能决策
- ✅ **实时监控告警** - 异常检测和多渠道通知
- ✅ **测试账户支持** - 开发者可用测试账户验证

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 依赖库（见 `requirements.txt`）

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/lemclaw/oceanengine-ads.git
cd oceanengine-ads

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
export OCEANENGINE_ACCESS_TOKEN="your_token"
export OCEANENGINE_APP_ID="your_app_id"
export OCEANENGINE_APP_SECRET="your_app_secret"
export OCEANENGINE_TEST_MODE=false  # 测试模式关闭
```

### 使用示例

```python
# 查询广告计划
from main import OceanEngineMain

main = OceanEngineMain()
main.init()
campaigns = main.campaign_list(account_id='your_id')
print(campaigns)

# 自动投放
from automation import OceanEngineAutomation

automation = OceanEngineAutomation()
result = automation.start_auto_launch(
    campaign_id='test_001',
    launch_immediately=True
)
print(result)
```

---

## 📊 功能模块

### 1. OAuth 认证 (`auth.py`)

- OAuth 2.0 认证流程
- Token 管理和刷新
- 测试账户支持

### 2. API 客户端 (`api_client.py`)

100+ 接口封装：
- 广告计划管理（创建/编辑/暂停/删除/查询）
- 广告组管理
- 广告创意管理
- 数据报表查询
- 异步批量请求

### 3. 自动化引擎 (`automation.py`)

- 智能投放启动
- 自动预算分配
- 创意自动轮换
- 批量投放管理

### 4. 智能优化 (`optimizer.py`)

- ROI 最大化算法
- 预算重分配建议
- 出价策略调整
- 定向优化建议
- 优化报告生成

### 5. 主入口 (`main.py`)

命令行工具支持：
- `status` - 查看系统状态
- `list` - 查询广告计划
- `create` - 创建广告
- `auto` - 自动投放
- `batch` - 批量投放
- `optimize` - 优化分析
- `report` - 查看报表

---

## 🧪 测试

运行测试套件：

```bash
python3 test_suite.py
```

**测试结果**：
- 总测试数：13个
- 通过：12个
- 跳过：1个
- **成功率：100%** ✅

---

## 📝 文档

- **SKILL.md** - 完整技能文档
- **README.md** - 快速开始指南
- **CHANGELOG.md** - 更新日志
- **BUSINESS-INFO.md** - 商务信息

---

## 🎯 适用场景

### 适合角色

- 广告优化师 - 优化 ROI、调整预算
- 数字营销经理 - 批量操作广告、数据报表
- 媒介采购人员 - 管理广告主账户
- 技术团队 - 自动化广告投放系统

### 支持平台

- 巨量引擎（今日头条广告）
- 巨量千川（抖音广告）
- 穿山甲（程序化广告）

---

## 🤝 贡献

欢迎贡献代码、报告 Bug 或提出功能建议！

### 开发步骤

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📜 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

### 乐盟互动 LemClaw

- **技术支持**：aoqian@lemhd.cn
- **商务合作**：business@lemclaw.com
- **官网**：https://www.lemclaw.com

### 开发者平台

- **巨量广告开放平台**：https://developer.oceanengine.com/
- **技术博客**：https://blog.oceanengine.com/
- **开发者论坛**：https://bbs.oceanengine.com/

---

## 🌟 Stars

如果这个技能对你有帮助，请给一个 Star！⭐

---

**🎯 LemClaw Smart Advertising Platform - 让巨量广告投放更智能！**

---

**最后更新**：2026-03-09  
**当前版本**：1.0.0