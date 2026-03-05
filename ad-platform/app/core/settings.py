"""
配置管理
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    APP_NAME: str = "Ad Platform API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API 配置
    API_V1_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/ad_platform?charset=utf8mb4"

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600  # 缓存过期时间（秒）

    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 小时

    # 巨量引擎配置
    OCEAN_APP_ID: str = ""
    OCEAN_APP_SECRET: str = ""
    OCEAN_API_BASE_URL: str = "https://ad.oceanengine.com/open_api"

    # CORS 配置
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://10.3.0.2:5173",
    ]

    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_TIMES: int = 100  # 时间窗口内请求次数
    RATE_LIMIT_SECONDS: int = 60  # 时间窗口（秒）

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text

    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建配置实例
settings = Settings()
