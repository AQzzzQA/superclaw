# 安全测试检查点

## 概述

本文档定义DSP平台的安全测试检查点，确保在开发、测试和部署阶段都符合安全要求。

---

## 1. 代码开发阶段

### 1.1 输入验证检查点

- [ ] 所有用户输入都经过验证和清洗
- [ ] 使用ORM参数化查询（禁止字符串拼接SQL）
- [ ] 前端表单包含客户端验证
- [ ] 后端验证所有API输入
- [ ] 限制输入长度和格式
- [ ] 文件上传类型白名单验证
- [ ] URL参数验证（防止SSRF）

**测试方法**：
```python
# 测试输入验证
def test_sql_injection_protection():
    malicious_input = "1' OR '1'='1"
    response = client.get(f"/api/v1/users/{malicious_input}")
    assert response.status_code == 400 or response.status_code == 404

def test_xss_protection():
    malicious_input = "<script>alert('XSS')</script>"
    response = client.post("/api/v1/campaigns", json={
        "name": malicious_input,
        "description": malicious_input
    })
    data = response.json()
    assert "<script>" not in str(data)
```

### 1.2 身份认证检查点

- [ ] 密码使用bcrypt哈希存储
- [ ] 密码强度验证（12位+大小写数字特殊字符）
- [ ] 登录失败限制（5次锁定30分钟）
- [ ] JWT Token有效期限制（15分钟）
- [ ] Refresh Token有效期限制（7天）
- [ ] Token黑名单机制
- [ ] 敏感操作需要重新认证
- [ ] MFA支持（推荐）

**测试方法**：
```python
# 测试登录失败限制
def test_login_rate_limit():
    for i in range(6):
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "wrong_password"
        })
    assert response.status_code == 429

# 测试Token过期
def test_token_expiration():
    expired_token = create_expired_token()
    response = client.get(
        "/api/v1/campaigns",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
```

### 1.3 访问控制检查点

- [ ] 实施RBAC权限系统
- [ ] 资源级访问控制（用户只能访问自己的数据）
- [ ] API端点权限检查
- [ ] 水平权限绕过防护（用户A不能访问用户B数据）
- [ ] 垂直权限提升防护（普通用户不能访问管理员功能）
- [ ] API密钥权限限制

**测试方法**：
```python
# 测试水平权限绕过
def test_horizontal_privilege_escalation():
    # 用户A创建数据
    user_a = create_user("user_a@example.com")
    campaign = client.post(
        "/api/v1/campaigns",
        json={"name": "Test Campaign"},
        headers={"Authorization": f"Bearer {user_a.token}"}
    ).json()

    # 用户B尝试访问用户A的数据
    user_b = create_user("user_b@example.com")
    response = client.get(
        f"/api/v1/campaigns/{campaign['id']}",
        headers={"Authorization": f"Bearer {user_b.token}"}
    )

    assert response.status_code == 403

# 测试垂直权限提升
def test_vertical_privilege_escalation():
    user = create_user("user@example.com", role="user")
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {user.token}"}
    )
    assert response.status_code == 403
```

---

## 2. 单元测试阶段

### 2.1 安全函数测试

```python
# tests/test_security_functions.py
import pytest
from app.utils.security import (
    verify_password,
    hash_password,
    create_access_token,
    verify_api_signature
)

class TestSecurityFunctions:
    """安全功能单元测试"""

    def test_password_hashing(self):
        """测试密码哈希"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        # 验证哈希与原密码不同
        assert hashed != password

        # 验证可以正确验证
        assert verify_password(password, hashed)

        # 验证错误密码失败
        assert not verify_password("WrongPassword", hashed)

    def test_token_creation_and_verification(self):
        """测试JWT Token创建和验证"""
        data = {"sub": "123", "role": "admin"}
        token = create_access_token(data)

        # Token不应为空
        assert token is not None
        assert len(token) > 0

        # 验证Token
        payload = verify_access_token(token)
        assert payload["sub"] == "123"
        assert payload["role"] == "admin"

    def test_api_signature_verification(self):
        """测试API签名验证"""
        api_key = "test_api_key"
        api_secret = "test_secret"
        timestamp = int(datetime.utcnow().timestamp())
        payload = f"{timestamp}test_data"
        signature = hmac.new(
            api_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        # 验证正确签名
        assert verify_api_signature(api_key, timestamp, signature, b"test_data")

        # 验证错误签名
        wrong_signature = "wrong_signature"
        assert not verify_api_signature(api_key, timestamp, wrong_signature, b"test_data")

    def test_data_masking(self):
        """测试数据脱敏"""
        from app.utils.data_masker import masker

        # 测试邮箱脱敏
        email = "admin@example.com"
        masked = masker.mask_email(email)
        assert "@" in masked
        assert "example.com" in masked
        assert "admin" not in masked

        # 测试手机脱敏
        phone = "13812345678"
        masked = masker.mask_phone(phone)
        assert phone[:3] in masked
        assert phone[-4:] in masked
        assert "1234" not in masked
```

---

## 3. 集成测试阶段

### 3.1 端到端安全测试

```python
# tests/test_security_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestSecurityIntegration:
    """安全集成测试"""

    async def test_full_auth_flow(self, client: AsyncClient):
        """测试完整认证流程"""
        # 1. 注册
        register_response = await client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "StrongPassword123!"
        })
        assert register_response.status_code == 201

        # 2. 登录
        login_response = await client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "StrongPassword123!"
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data

        # 3. 使用Token访问受保护资源
        access_token = token_data["access_token"]
        protected_response = await client.get(
            "/api/v1/campaigns",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert protected_response.status_code == 200

        # 4. 登出
        logout_response = await client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert logout_response.status_code == 200

        # 5. 验证Token已失效
        failed_response = await client.get(
            "/api/v1/campaigns",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert failed_response.status_code == 401

    async def test_api_key_authentication(self, client: AsyncClient):
        """测试API密钥认证"""
        # 创建API密钥
        api_key = create_test_api_key()

        # 使用API密钥访问
        response = await client.get(
            "/api/v1/campaigns",
            headers={"X-API-Key": api_key}
        )

        assert response.status_code == 200

        # 无效API密钥
        response = await client.get(
            "/api/v1/campaigns",
            headers={"X-API-Key": "invalid_key"}
        )

        assert response.status_code == 401

    async def test_webhook_signature_verification(self, client: AsyncClient):
        """测试Webhook签名验证"""
        # 创建Webhook
        webhook = create_test_webhook()

        # 计算签名
        timestamp = int(datetime.utcnow().timestamp())
        payload = json.dumps({"event": "campaign.created"})
        signature = compute_signature(webhook.secret, timestamp, payload)

        # 发送有效的Webhook
        response = await client.post(
            f"/webhooks/{webhook.id}",
            headers={
                "X-Webhook-Timestamp": str(timestamp),
                "X-Webhook-Signature": signature
            },
            data=payload
        )
        assert response.status_code == 200

        # 发送无效签名的Webhook
        response = await client.post(
            f"/webhooks/{webhook.id}",
            headers={
                "X-Webhook-Timestamp": str(timestamp),
                "X-Webhook-Signature": "invalid_signature"
            },
            data=payload
        )
        assert response.status_code == 401
```

---

## 4. 安全扫描阶段

### 4.1 自动化安全扫描

#### Safety扫描（Python依赖）

```bash
# 运行扫描
safety check

# CI/CD集成
safety check --json --output safety-report.json

# 失败阈值
safety check --continue-on-error --ignore 43672
```

**检查点**：
- [ ] 无高危漏洞（CVSS >= 7.0）
- [ ] 无已知的恶意依赖
- [ ] 依赖版本在支持期内

#### Bandit扫描（代码安全）

```bash
# 基本扫描
bandit -r ./backend

# 输出JSON报告
bandit -r ./backend -f json -o bandit-report.json

# CI/CD集成
bandit -r ./backend -f json -o bandit-report.json || true
```

**检查点**：
- [ ] 无高危问题（High + Error）
- [ ] 禁用使用`exec()`、`eval()`
- [ ] 禁用使用不安全的pickle
- [ ] 禁用使用shell=True

#### npm audit（Node.js依赖）

```bash
# 扫描依赖
npm audit

# 自动修复
npm audit fix

# 仅扫描
npm audit --audit-level moderate

# JSON输出
npm audit --json
```

**检查点**：
- [ ] 无高危漏洞（High + Critical）
- [ ] 依赖版本与package.json一致
- [ ] package-lock.json已提交

---

## 5. 渗透测试阶段

### 5.1 手工渗透测试检查点

#### 认证测试

- [ ] 弱密码测试
  - 尝试弱密码（123456, password, admin等）
  - 尝试默认凭证
  - 测试密码复杂度验证

- [ ] 暴力破解防护
  - 尝试多次失败登录
  - 验证账户锁定机制
  - 测试锁定时间

- [ ] 会话管理
  - 测试会话固定攻击
  - 测试会话超时
  - 验证会话并发限制

- [ ] Token安全
  - 测试Token暴力破解
  - 测试Token重放攻击
  - 验证Token过期
  - 测试Token黑名单

#### 授权测试

- [ ] 水平权限绕过
  - 用户A尝试访问用户B的数据
  - 修改URL中的ID
  - 修改请求体中的user_id

- [ ] 垂直权限提升
  - 普通用户尝试访问管理员端点
  - 修改请求中的role字段
  - 测试参数篡改

- [ ] API访问控制
  - 尝试绕过权限检查
  - 测试API密钥权限
  - 测试速率限制绕过

#### 输入验证测试

- [ ] SQL注入
  - GET参数注入
  - POST参数注入
  - Cookie注入
  - Header注入

- [ ] XSS攻击
  - 反射型XSS
  - 存储型XSS
  - DOM型XSS

- [ ] 其他注入
  - 命令注入
  - NoSQL注入
  - 路径遍历
  - 文件包含

#### API安全测试

- [ ] API密钥安全
  - 暴力破解测试
  - 签名绕过测试
  - 时间戳操纵测试

- [ ] Webhook安全
  - 签名验证测试
  - 重放攻击测试
  - 恶意payload测试

---

## 6. 部署前检查

### 6.1 生产环境检查清单

```bash
# 运行安全检查脚本
python scripts/security-checklist.py
```

**必查项**：
- [ ] DEBUG = False
- [ ] JWT_SECRET_KEY已更换
- [ ] 数据库密码强度足够
- [ ] Redis密码已设置
- [ ] HTTPS强制启用
- [ ] CORS配置正确
- [ ] 安全响应头已配置
- [ ] 日志脱敏已启用
- [ ] 敏感数据已加密
- [ ] .env在.gitignore中

**环境变量验证**：
```bash
# 验证关键环境变量
echo $JWT_SECRET_KEY | wc -c  # 应该 >= 64
echo $DATABASE_PASSWORD | wc -c  # 应该 >= 12
echo $REDIS_PASSWORD  # 不应该为空
```

### 6.2 安全配置验证

```bash
# 1. 检查数据库用户权限
mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='dsp_app';"

# 2. 检查Redis配置
redis-cli CONFIG GET requirepass

# 3. 检查SSL证书
openssl x509 -in /path/to/cert.pem -noout -dates

# 4. 检查防火墙规则
iptables -L -n

# 5. 检查文件权限
ls -la .env
ls -la /var/log/dsp/
```

---

## 7. 持续监控检查

### 7.1 运行时安全监控

**Prometheus指标**：
- [ ] 登录失败率监控
- [ ] API认证失败监控
- [ ] SQL注入尝试监控
- [ ] XSS尝试监控
- [ ] 敏感数据访问监控
- [ ] 异常IP访问监控

**告警规则**：
```yaml
# 1分钟内登录失败超过10次
- alert: HighFailedLoginRate
  expr: rate(login_attempts_total{status="failure"}[1m]) > 10

# 5分钟内SQL注入尝试 > 0
- alert: SQLInjectionAttempt
  expr: increase(sql_injection_attempts[5m]) > 0

# 1小时内敏感数据访问异常
- alert: UnusualDataAccess
  expr: rate(sensitive_data_access[1h]) > 100
```

### 7.2 日志审计

**每日检查**：
- [ ] 审计异常登录
- [ ] 检查权限变更
- [ ] 审查敏感数据访问
- [ ] 分析失败认证

**每周检查**：
- [ ] 审查安全事件
- [ ] 分析攻击趋势
- [ ] 检查依赖更新
- [ ] 审查访问日志

---

## 8. 合规性检查

### 8.1 等保2.0三级检查

**检查点**：
- [ ] 身份鉴别（双因子认证、复杂密码、会话管理）
- [ ] 访问控制（最小权限、权限分离、访问审计）
- [ ] 安全审计（日志记录、审计分析、异常检测）
- [ ] 数据完整性（数据校验、防篡改、备份加密）
- [ ] 数据保密性（敏感数据加密、传输加密）
- [ ] 个人信息保护（数据脱敏、访问控制、数据最小化）

### 8.2 GDPR合规检查

**检查点**：
- [ ] 用户同意管理
- [ ] 数据访问权
- [ ] 数据删除权
- [ ] 数据可移植权
- [ ] 隐私政策
- [ ] 数据泄露通知
- [ ] DPIA（数据保护影响评估）

---

## 9. 测试报告模板

```markdown
# DSP平台安全测试报告

**测试日期**: 2026-03-15
**测试环境**: Staging
**测试人员**: 安全测试团队

## 测试摘要

| 测试类型 | 测试项 | 通过 | 失败 | 风险等级 |
|---------|--------|------|------|---------|
| 单元测试 | 安全函数 | 10 | 0 | 低 |
| 集成测试 | 认证流程 | 5 | 0 | 低 |
| 安全扫描 | 依赖漏洞 | 20 | 2 | 高 |
| 渗透测试 | 授权控制 | 15 | 1 | 高 |

**总体评分**: 85/100

## 测试详情

### 1. 单元测试
✅ 通过 - 所有安全函数测试通过

### 2. 集成测试
✅ 通过 - 认证流程完整测试通过

### 3. 安全扫描
❌ 失败 - 发现2个高危依赖漏洞
- PyJWT 2.4.0 -> 需要升级到 2.6.0
- SQLAlchemy 1.4.0 -> 需要升级到 2.0.0

### 4. 渗透测试
❌ 失败 - 发现1个权限提升漏洞
- 用户可以通过修改user_id访问其他用户数据

## 修复建议

1. 立即升级PyJWT和SQLAlchemy
2. 修复权限提升漏洞（添加用户ID验证）
3. 增加API速率限制

## 下次测试计划
2026-03-22
```

---

## 附录

### A. 安全测试工具安装

```bash
# Python安全工具
pip install safety bandit pytest-cov

# Node.js安全工具
npm install -g npm audit

# 安全扫描工具
sudo apt install nmap sqlmap

# Web应用扫描
docker run -p 8080:8080 -it owasp/zap2docker-stable zap-webswing.sh
```

### B. 快速测试命令

```bash
# 完整安全测试套件
./scripts/run-security-tests.sh

# 依赖扫描
safety check && bandit -r ./backend

# 渗透测试
./scripts/pentest.sh

# 生产环境检查
./scripts/security-checklist.py
```

**测试通过标准**：
- 所有单元测试通过 ✅
- 无高危依赖漏洞 ✅
- 渗透测试无高危问题 ✅
- 生产环境检查通过 ✅

---

**文档版本**: 1.0.0
**最后更新**: 2026-03-15
**维护人**: 安全团队
