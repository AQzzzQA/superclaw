# SuperClaw - Multi-stage Dockerfile
# 支持 Rust 后端和前端构建

# ==========================================
# Stage 1: Rust 后端
# ==========================================

FROM rust:1.70-slim as builder

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖清单
COPY Cargo.toml Cargo.lock ./

# 构建依赖
RUN cargo build --release

# ==========================================
# Stage 2: 生产镜像
# ==========================================

FROM debian:bookworm-slim as runtime

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制编译后的二进制文件
COPY --from=builder /app/target/release/superclaw /usr/local/bin/superclaw

# 创建非 root 用户
RUN useradd -m -u 1000 superclaw && \
    mkdir -p /app/data /app/logs && \
    chown -R superclaw:superclaw /app

# 切换到非 root 用户
USER superclaw

# 复制配置文件（如果有）
COPY .env.example /app/.env.example
RUN chown superclaw:superclaw /app/.env.example

# 创建日志目录
RUN mkdir -p /app/logs && \
    chown superclaw:superclaw /app/logs

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# 环境变量
ENV RUST_LOG=info
ENV DATABASE_URL=sqlite:///app/data/superclaw.db
ENV REDIS_URL=redis://redis:6379/0

# 启动命令
CMD ["superclaw"]
