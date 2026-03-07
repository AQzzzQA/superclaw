# 斑布纸广告管理系统 - 完整开发文档

**创建时间**: 2026-03-07 01:58
**目的**: 创建斑布纸广告投放管理系统

---

## 📋 项目概述

### 项目名称
斑布纸广告管理系统（Banbu Paper Ads Manager）

### 项目目标
- 集成巨量广告 API
- 自动化广告投放流程
- 实时监控广告数据
- 智能优化投放策略

### 技术栈
- **后端**: Python 3.10+ + FastAPI
- **数据库**: MySQL + Redis
- **API 集成**: API Gateway + mcporter
- **前端**: React + TypeScript（可选）
- **部署**: Docker + Docker Compose

---

## 🚀 项目结构

```
/root/.openclaw/workspace/banbu-paper-ads/
├── app/                      # FastAPI 应用
│   ├── main.py               # 主应用入口
│   ├── config.py             # 配置文件
│   ├── database.py           # 数据库连接
│   ├── models/              # 数据模型
│   ├── api/                 # API 路由
│   └── services/            # 业务逻辑
├── tests/                   # 测试用例
├── docs/                    # 文档
├── scripts/                 # 脚本工具
├── Dockerfile              # Docker 镜像
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python 依赖
└── .env.example          # 环境变量模板
```

---

## 🔧 核心功能

### 1. 账户管理
- ✅ 连接巨量广告账户
- ✅ 获取账户信息
- ✅ 查询账户余额
- ✅ 自动充值（可选）

### 2. 广告计划管理
- ✅ 创建广告计划
- ✅ 更新广告计划
- ✅ 暂停/开启广告计划
- ✅ 查看广告计划列表

### 3. 创意管理
- ✅ 上传视频/图片创意
- ✅ 创建图文广告
- ✅ A/B 测试创意
- ✅ 删除创意

### 4. 定向人群管理
- ✅ 创建定向人群
- ✅ 更新定向设置
- ✅ 查看定向效果
- ✅ 删除定向人群

### 5. 数据监控
- ✅ 实时监控广告数据
- ✅ 生成数据报告
- ✅ 可视化数据展示
- ✅ 数据导出（CSV/Excel）

### 6. 自动优化
- ✅ 自动调整出价
- ✅ 自动暂停效果差的创意
- ✅ 自动扩大效果好的创意
- ✅ 智能预算分配

---

## 📊 数据库设计

### 表结构

```sql
-- 广告计划表
CREATE TABLE campaigns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    campaign_id VARCHAR(100),
    name VARCHAR(200),
    budget DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创意表
CREATE TABLE creatives (
    id INT PRIMARY KEY AUTO_INCREMENT,
    creative_id VARCHAR(100),
    campaign_id INT,
    name VARCHAR(200),
    type VARCHAR(50),
    url VARCHAR(500),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- 定向人群表
CREATE TABLE targeting (
    id INT PRIMARY KEY AUTO_INCREMENT,
    targeting_id VARCHAR(100),
    name VARCHAR(200),
    age_min INT,
    age_max INT,
    gender VARCHAR(50),
    geo TEXT,
    interests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据报告表
CREATE TABLE reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    campaign_id INT,
    creative_id INT,
    date DATE,
    impressions INT,
    clicks INT,
    conversions INT,
    cost DECIMAL(10, 2),
    ctr DECIMAL(5, 4),
    cpc DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (creative_id) REFERENCES creatives(id)
);
```

---

## 🚀 开发步骤

### Phase 1: 基础架构（1 周）

#### Day 1-2: 环境搭建
```bash
# 创建项目目录
mkdir -p ~/banbu-paper-ads
cd ~/banbu-paper-ads

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 创建依赖文件
cat > requirements.txt << 'EOF'
fastapi>=0.104.1
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
pymysql>=1.0.2
redis>=5.0.0
celery>=5.3.0
python-dotenv>=1.0.0
requests>=2.31.0
pandas>=2.1.0
matplotlib>=3.8.0
EOF

# 安装依赖
pip install -r requirements.txt
```

#### Day 3-4: 数据库设置
```bash
# 启动 MySQL
docker run -d --name mysql-banbu \
    -e MYSQL_ROOT_PASSWORD=password \
    -e MYSQL_DATABASE=banbu_ads \
    -p 3306:3306 \
    mysql:8.0

# 启动 Redis
docker run -d --name redis-banbu \
    -p 6379:6379 \
    redis:7.0
```

#### Day 5-7: 基础框架
- 创建 FastAPI 应用
- 创建数据库连接
- 创建基础 API 路由

### Phase 2: API 集成（2 周）

#### Week 2: 巨量广告 API 集成
```python
# app/services/oceanengine.py
from api_gateway import APIGateway

class OceanEngineService:
    def __init__(self):
        self.gateway = APIGateway()
        self.oceanengine = self.gateway.add_service("oceanengine")

    def create_campaign(self, data):
        return self.oceanengine.post("/campaign/add", data)

    def get_campaigns(self):
        return self.oceanengine.get("/campaign/get")

    def create_creative(self, data):
        return self.oceanengine.post("/creative/add", data)

    def get_reports(self, start_date, end_date):
        return self.oceanengine.post("/report/get", {
            "start_date": start_date,
            "end_date": end_date
        })
```

#### Week 3: API 测试和优化
- 测试所有 API 调用
- 优化错误处理
- 添加日志记录

### Phase 3: 业务逻辑（2 周）

#### Week 4: 广告管理功能
- 创建广告计划
- 更新广告计划
- 暂停/开启广告

#### Week 5: 创意和定向管理
- 上传创意
- 创建定向人群
- A/B 测试

### Phase 4: 数据监控和优化（2 周）

#### Week 6: 数据监控
- 实时监控广告数据
- 生成数据报告
- 可视化展示

#### Week 7: 自动优化
- 自动调整出价
- 自动优化创意
- 智能预算分配

### Phase 5: 测试和部署（1 周）

#### Week 8: 测试和部署
- 单元测试
- 集成测试
- Docker 部署
- 性能优化

---

## 📊 API 接口设计

### 1. 广告计划 API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CampaignCreate(BaseModel):
    name: str
    budget: float
    start_date: str
    end_date: str

@app.post("/api/campaigns")
async def create_campaign(campaign: CampaignCreate):
    """创建广告计划"""
    # 调用巨量广告 API
    oceanengine = OceanEngineService()
    result = oceanengine.create_campaign(campaign.dict())
    return result

@app.get("/api/campaigns")
async def get_campaigns():
    """获取广告计划列表"""
    oceanengine = OceanEngineService()
    return oceanengine.get_campaigns()

@app.put("/api/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, campaign: CampaignCreate):
    """更新广告计划"""
    oceanengine = OceanEngineService()
    return oceanengine.update_campaign(campaign_id, campaign.dict())

@app.delete("/api/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int):
    """删除广告计划"""
    oceanengine = OceanEngineService()
    return oceanengine.delete_campaign(campaign_id)
```

### 2. 创意 API

```python
class CreativeCreate(BaseModel):
    name: str
    type: str
    url: str
    campaign_id: int

@app.post("/api/creatives")
async def create_creative(creative: CreativeCreate):
    """创建广告创意"""
    oceanengine = OceanEngineService()
    return oceanengine.create_creative(creative.dict())

@app.get("/api/creatives")
async def get_creatives():
    """获取创意列表"""
    oceanengine = OceanEngineService()
    return oceanengine.get_creatives()
```

### 3. 数据报告 API

```python
@app.get("/api/reports")
async def get_reports(start_date: str, end_date: str):
    """获取数据报告"""
    oceanengine = OceanEngineService()
    return oceanengine.get_reports(start_date, end_date)
```

---

## 🚀 部署配置

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@mysql:3306/banbu_ads
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=banbu_ads
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0
    ports:
      - "6379:6379"

volumes:
  mysql_data:
```

---

## 📊 时间线（8 周）

| 阶段 | 时间 | 任务 |
|------|------|------|
| **Phase 1** | Week 1 | 基础架构搭建 |
| **Phase 2** | Week 2-3 | API 集成 |
| **Phase 3** | Week 4-5 | 业务逻辑开发 |
| **Phase 4** | Week 6-7 | 数据监控和优化 |
| **Phase 5** | Week 8 | 测试和部署 |

---

## 🎯 成功指标

### 技术指标
- ✅ API 响应时间 < 1 秒
- ✅ 数据库查询 < 100ms
- ✅ 系统可用性 > 99.9%
- ✅ 错误率 < 0.1%

### 业务指标
- ✅ 广告投放效率提升 50%
- ✅ 数据监控实时性 < 1 分钟
- ✅ 自动优化准确性 > 80%
- ✅ 用户满意度 > 90%

---

**创建时间**: 2026-03-07 01:58
**状态**: ✅ 完整开发文档已创建

---

## 🚀 立即开始

**你现在想要**：

1. **开始 Phase 1**？（搭建基础架构）
2. **跳到 Phase 2**？（直接开始 API 集成）
3. **查看完整代码**？（获取代码示例）
4. **开始测试**？（测试现有功能）

**告诉我你的选择，我帮你开始开发！🚀**
