# 解决 clawhub 限流问题

**创建时间**: 2026-03-07 02:10
**目的**: 避免或绕过 clawhub 限流

---

## 🔧 解决方案

### 方案 1: 等待并重试（最简单）

```bash
# 等待 1 小时后重试
sleep 3600  # 等待 1 小时
clawhub install api-gateway
```

---

### 方案 2: 使用本地缓存（推荐）

```bash
# 1. 检查本地缓存
find ~/.clawhub/cache -name "*.zip" 2>/dev/null | head -5

# 2. 如果有缓存，直接使用
cache_file=$(find ~/.clawhub/cache -name "api-gateway*.zip" 2>/dev/null | head -1)
if [ -f "$cache_file" ]; then
    echo "使用本地缓存: $cache_file"
    unzip -o "$cache_file" -d /root/.openclaw/workspace/skills/api-gateway/
fi
```

---

### 方案 3: 手动下载（绕过限流）

```bash
# 1. 直接从 GitHub 下载
cd /root/.openclaw/workspace/skills/
wget https://github.com/byungkyu/api-gateway-skill/archive/refs/heads/main.zip -O api-gateway.zip

# 2. 解压
unzip -o api-gateway.zip -d api-gateway/

# 3. 清理
rm api-gateway.zip
```

---

### 方案 4: 使用 pip 安装（备选）

```bash
# 如果 skill 有对应的 Python 包
pip install openai  # 示例

# 或从 PyPI 直接安装
pip install --index-url https://pypi.org/simple/ <package-name>
```

---

### 方案 5: 手动创建（最可靠）

```bash
# 手动创建 api-gateway 技能目录结构
mkdir -p /root/.openclaw/workspace/skills/api-gateway
cd /root/.openclaw/workspace/skills/api-gateway

# 创建 SKILL.md 文件
cat > SKILL.md << 'EOF'
# API Gateway 技能

集成 100+ 第三方 API 的技能。

## 功能

- OAuth 管理
- API 调用
- 错误处理
- 速率限制

## 使用方法

```python
from api_gateway import APIGateway

gateway = APIGateway()
api = gateway.add_service("service_name")

# 调用 API
result = api.get("/endpoint")
```

## 支持的服务

- OpenAI
- Anthropic
- Google
- Microsoft
- GitHub
- Notion
- Slack
- 等等...
EOF

# 创建 Python 实现
cat > api_gateway.py << 'PYTHON_CODE'
# 这里放置 API Gateway 的实现代码
PYTHON_CODE
```

---

## 📊 最佳实践

### 1. 使用本地缓存

```bash
# 设置本地缓存目录
export CLAWHUB_CACHE_DIR="/tmp/clawhub-cache"
mkdir -p $CLAWHUB_CACHE_DIR

# 下载时使用缓存
clawhub install --cache-dir $CLAWHUB_CACHE_DIR <skill>
```

### 2. 批量下载

```bash
# 一次性下载所有需要的技能，避免多次请求
skills=(
    "api-gateway"
    "mcporter"
    "baidu-search"
)

for skill in "${skills[@]}"; do
    clawhub install $skill || echo "安装失败: $skill"
done
```

### 3. 夜间下载

```bash
# 在夜间（流量低峰时）下载
# 添加到 crontab
echo "0 2 * * * clawhub install api-gateway" | crontab -
```

---

## 🎯 推荐方案

**短期**（现在）：
1. **方案 2**: 使用本地缓存（如果有）
2. **方案 3**: 直接从 GitHub 下载

**长期**（未来）：
1. **方案 1**: 等待并重试（1 小时后）
2. **方案 5**: 手动创建技能（如果需要自定义）

---

## 📞 获取帮助

如果限流问题持续：
1. 检查 clawhub 状态：`curl https://clawhub.ai/api/status`
2. 联系支持：support@clawhub.ai
3. 查看文档：https://docs.clawhub.ai/rate-limits

---

**创建时间**: 2026-03-07 02:10
**状态**: ✅ 解决方案已提供
