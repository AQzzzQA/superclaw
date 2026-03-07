# SuperClaw 开发者指南

> **版本**: v1.0.0
> **创建时间**: 2026-03-08
> **作者**: AQzzzQA

---

## 📋 目录

- [快速开始](#快速开始)
- [开发环境](#开发环境)
- [项目结构](#项目结构)
- [开发流程](#开发流程)
- [测试指南](#测试指南)
- [部署指南](#部署指南)
- [贡献指南](#贡献指南)

---

## 快速开始

### 前置要求

- **Rust**: 1.70 或更高版本
- **Node.js**: 22.22.0 或更高版本
- **Python**: 3.11 或更高版本（用于 LemClaw Gateway）
- **Git**: 最新版本

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/AQzzzQA/superclaw.git
cd superclaw

# 安装 Rust 依赖
cd superclaw
cargo build --release

# 安装前端依赖
cd frontend
npm install
```

### 启动开发服务器

```bash
# 终端 1: 启动 SuperClaw 后端
cd superclaw
cargo run

# 终端 2: 启动前端开发服务器
cd frontend
npm run dev

# 终端 3: 启动 LemClaw Gateway
cd LemClaw
pip install -r requirements.txt
python3 app.py
```

---

## 开发环境

### 推荐工具

- **IDE**: VS Code（推荐）或 IntelliJ IDEA + Rust 插件
- **Rust**: rust-analyzer + Rust 扩展
- **前端**: Volar + Vue DevTools
- **Git**: GitKraken 或 SourceTree

### VS Code 扩展

```json
{
  "recommendations": [
    "rust-lang.rust-analyzer",
    "Vue.volar",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens"
  ]
}
```

---

## 项目结构

```
superclaw/
├── Cargo.toml              # Rust 项目配置
├── src/
│   ├── main.rs             # 主入口
│   ├── gateway/            # 双网关
│   │   ├── mod.rs
│   │   ├── websocket.rs   # WebSocket Gateway
│   │   └── http.rs       # HTTP Gateway
│   ├── skills/             # Echo Skills
│   │   ├── mod.rs
│   │   └── echo.rs       # 扫描、修复、生成
│   ├── api/                # API 路由
│   │   ├── mod.rs
│   │   └── skills.rs      # Skills API
│   ├── agents/             # 智能体编排
│   ├── security/           # 安全模块
│   └── models/            # 数据模型
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   ├── main.js        # 入口文件
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面组件
│   │   ├── composables/   # 组合式函数
│   │   └── assets/        # 静态资源
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docs/                  # 文档目录
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DEVELOPER.md
│   └── SECURITY.md
├── tests/                 # 测试文件
│   ├── integration/         # 集成测试
│   └── unit/              # 单元测试
└── .env.example           # 环境变量示例
```

---

## 开发流程

### 1. 代码规范

#### Rust 代码规范

- ✅ 使用 `cargo fmt` 格式化代码
- ✅ 使用 `cargo clippy` 检查代码
- ✅ 遵循 Rust 命名规范（snake_case）
- ✅ 添加文档注释（`///`）
- ✅ 使用 `Result<T, E>` 处理错误

示例：
```rust
/// 发送消息到智能体
///
/// # Arguments
///
/// * `auth_code` - 授权码
/// * `message` - 消息内容
///
/// # Returns
///
/// 返回智能体响应
pub async fn send_message(
    auth_code: &str,
    message: &str,
) -> Result<AgentResponse, Box<dyn std::error::Error>> {
    // 实现...
}
```

#### Vue 代码规范

- ✅ 使用 `<script setup>` 语法
- ✅ 使用 Composition API
- ✅ 组件名使用 PascalCase
- ✅ 文件名使用 PascalCase
- ✅ 添加组件注释
- ✅ 使用 ESLint + Prettier

示例：
```vue
<!--
  组件名称: ChatView
  描述: 对话界面组件
-->
<script setup>
import { ref } from 'vue'

const message = ref('')
</script>

<template>
  <div class="chat-view">{{ message }}</div>
</template>

<style scoped>
.chat-view {
  /* 样式 */
}
</style>
```

### 2. Git 工作流

#### 分支策略

```
main          - 生产分支
├── develop    - 开发分支
├── feature/*  - 功能分支
└── hotfix/*   - 修复分支
```

#### 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**：
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式调整
- `refactor` - 重构
- `perf` - 性能优化
- `test` - 测试相关

示例：
```
feat(gateway): 添加 WebSocket 连接管理

实现连接池管理，支持自动重连和心跳检测。
```

### 3. 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **开发功能**
   - 编写代码
   - 添加测试
   - 更新文档

3. **提交代码**
   ```bash
   cargo fmt
   cargo clippy
   git add .
   git commit -m "feat(scope): description"
   ```

4. **推送到远程**
   ```bash
   git push origin feature/new-feature-name
   ```

5. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 等待 Code Review
   - 合并到 main 分支

---

## 测试指南

### 单元测试

#### Rust 测试

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test test_name

# 显示测试输出
cargo test -- --nocapture

# 生成覆盖率报告
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
```

示例：
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_send_message() {
        let result = send_message("code", "message");
        assert!(result.is_ok());
    }
}
```

#### Vue 测试

```bash
# 安装测试依赖
npm install --save-dev vitest @vue/test-utils

# 运行测试
npm run test

# 监视模式
npm run test:watch
```

示例：
```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)

const increment = () => {
  count.value++
}
</script>

<template>
  <button @click="increment">{{ count }}</button>
</template>

<script setup>
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatView from '@/views/Chat.vue'

describe('ChatView', () => {
  it('increments count', async () => {
    const wrapper = mount(ChatView)
    await wrapper.find('button').trigger('click')
    expect(wrapper.vm.count).toBe(1)
  })
})
</script>
```

### 集成测试

```bash
# 启动测试环境
cargo run

# 运行集成测试
tests/integration/test_gateway.sh

# 使用 Supertest 测试 API
tests/integration/test_api.sh
```

---

## 部署指南

### Docker 部署

#### 构建镜像

```dockerfile
# Dockerfile
FROM rust:1.70-slim as builder

WORKDIR /app

COPY . .
RUN cargo build --release

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /app/target/release/superclaw .
COPY --from=builder /app/frontend/dist ./frontend

EXPOSE 3000

CMD ["./superclaw"]
```

```bash
# 构建镜像
docker build -t superclaw:latest .

# 运行容器
docker run -p 3000:3000 superclaw:latest
```

### 生产环境配置

```bash
# 环境变量
export RUST_LOG=info
export OPENCLAW_GATEWAY_URL=https://api.openclaw.com
export LEMLAW_GATEWAY_URL=https://api.lemclaw.com
export DATABASE_URL=postgresql://user:pass@db/superclaw
export REDIS_URL=redis://redis:6379/0

# 运行生产服务器
cargo run --release
```

---

## 贡献指南

### 如何贡献

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 本仓库
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **编写代码**
   - 遵循代码规范
   - 添加测试
   - 更新文档

4. **提交更改**
   ```bash
   git commit -m "feat: add amazing feature"
   ```

5. **推送到 Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 详细描述更改内容
   - 等待 Code Review

### Pull Request 检查清单

- [ ] 代码通过 `cargo fmt` 格式化
- [ ] 代码通过 `cargo clippy` 检查
- [ ] 所有测试通过
- [ ] 添加了单元测试
- [ ] 更新了相关文档
- [ ] 遵循提交规范
- [ ] PR 描述清晰完整

---

## 性能优化

### Rust 优化技巧

1. **使用异步 I/O**
   ```rust
   use tokio::fs;

   async fn read_file(path: &str) -> Result<String, io::Error> {
       tokio::fs::read_to_string(path).await
   }
   ```

2. **避免不必要的克隆**
   ```rust
   // ❌ 不推荐
   let result = process(&input.clone());

   // ✅ 推荐
   let result = process(&input);
   ```

3. **使用引用传递**
   ```rust
   fn process(input: &str) -> String {
       // 使用引用避免克隆
   }
   ```

### Vue 优化技巧

1. **使用 v-once**
   ```vue
   <div v-once>{{ staticData }}</div>
   ```

2. **合理使用 computed**
   ```vue
   <script setup>
   import { computed } from 'vue'

   const filteredList = computed(() => {
     return list.value.filter(item => item.active)
   })
   </script>
   ```

3. **虚拟滚动（大数据列表）**
   ```vue
   <template>
     <RecycleScroller
       :items="largeList"
       :item-size="50"
     >
       <template #default="{ item }">
         <div>{{ item }}</div>
       </template>
     </RecycleScroller>
   </template>
   ```

---

## 调试技巧

### Rust 调试

```bash
# 使用 dbg! 宏
dbg!(&variable);

# 使用日志
log::info!("Variable value: {}", variable);
log::error!("Error occurred: {:?}", error);

# 使用 RUST_BACKTRACE
RUST_BACKTRACE=1 cargo run
```

### Vue 调试

```javascript
// 使用 Vue DevTools
console.log('Variable value:', variable);

// 使用 debugger
debugger;
```

---

## 常见问题

### Q: 如何添加新的 API 端点？

A: 在 `src/api/mod.rs` 中定义路由，然后在 `src/main.rs` 中注册。

### Q: 如何添加新的 Echo Skill？

A: 在 `src/skills/echo.rs` 中实现新功能，然后在 `src/api/skills.rs` 中添加 API 端点。

### Q: 如何调试 WebSocket 连接？

A: 使用浏览器开发者工具的 Network → WS 标签页查看 WebSocket 消息。

### Q: 如何配置生产环境？

A: 创建 `.env.production` 文件，设置生产环境变量，然后使用 `cargo run --release` 启动。

---

## 资源链接

- [Rust 官方文档](https://doc.rust-lang.org/)
- [Vue 3 官方文档](https://vuejs.org/)
- [Naive UI 文档](https://www.naiveui.com/)
- [OpenClaw 文档](https://docs.openclaw.ai/)

---

**创建时间**: 2026-03-08
**版本**: v1.0.0
**作者**: AQzzzQA 🚀
