# Ad Platform 开发者快速入门

**版本**: v2.0
**更新时间**: 2026-03-01

---

## 🚀 5分钟快速开始

### 1. 获取 API 密钥
访问 [Ad Platform 控制台](https://platform.example.com)，在"开发者中心"获取 API 密钥。

### 2. 发起第一个请求
```bash
curl -X GET "https://api.example.com/api/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 3. 获取授权 URL
```bash
curl -X GET "https://api.example.com/api/v1/oauth/authorize?redirect_uri=https://example.com/callback" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 4. 创建第一个广告计划
```bash
curl -X POST "https://api.example.com/api/v1/campaign/create" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaignId": 100001,
    "campaignName": "测试计划",
    "objectiveType": "产品推广",
    "预算": 1000
  }'
```

---

## 📚 SDK 集成

### JavaScript/TypeScript
```bash
npm install @ad-platform/sdk
```

```typescript
import { AdPlatformClient } from '@ad-platform/sdk'

const client = new AdPlatformClient({
  apiKey: 'YOUR_API_KEY'
})

// 创建广告计划
const campaign = await client.campaign.create({
  campaignName: '测试计划',
  objectiveType: '产品推广',
  budget: 1000
})
```

### Python
```bash
pip install adplatform-sdk
```

```python
from adplatform import AdPlatformClient

client = AdPlatformClient(api_key='YOUR_API_KEY')

# 创建广告计划
campaign = client.campaign.create(
  campaign_name='测试计划',
  objective_type='产品推广',
  budget=1000
)
```

---

## 🔧 开发工具

### API 测试工具
- Postman Collection: [下载链接](https://example.com/postman-collection)
- Swagger UI: https://api.example.com/docs
- OpenAPI 规范: https://api.example.com/openapi.json

### 监控面板
- 任务监控: https://monitor.example.com/flower
- 性能监控: https://monitor.example.com/grafana
- 日志查看: https://logs.example.com

---

## 💡 示例代码

### 完整示例
见 `/examples` 目录：
- JavaScript 示例
- Python 示例
- Java 示例
- PHP 示例

---

## 🆘 获取帮助
- 文档: https://docs.example.com
- 论坛: https://forum.example.com
- 支持: support@example.com

---

**祝你对接顺利！** 🎉
