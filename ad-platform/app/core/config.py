from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Ad Platform API"
    APP_VERSION: str = "2.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./ad_platform.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Ocean Engine (巨量引擎)
    OCEAN_APP_ID: str = ""
    OCEAN_APP_SECRET: str = ""
    OCEAN_REDIRECT_URI: str = (
        "http://localhost:5173/oauth/callback"
    )  # fmt: skip
    OCEAN_API_BASE: str = "https://api.oceanengine.com/open_api/v3.0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Memory Service (OpenViking Integration)
    MEMORY_SERVER_URL: str = os.getenv("MEMORY_SERVER_URL", "http://localhost:1933")
    MEMORY_API_KEY: Optional[str] = os.getenv("MEMORY_API_KEY")
    MEMORY_TIMEOUT: int = int(os.getenv("MEMORY_TIMEOUT", "60"))
    MEMORY_MAX_RETRIES: int = int(os.getenv("MEMORY_MAX_RETRIES", "3"))
    MEMORY_CACHE_SIZE: int = int(os.getenv("MEMORY_CACHE_SIZE", "1000"))
    MEMORY_DEFAULT_LAYER: str = os.getenv("MEMORY_DEFAULT_LAYER", "L1")
    MEMORY_OPTIMIZATION_THRESHOLD: float = float(
        os.getenv("MEMORY_OPTIMIZATION_THRESHOLD", "0.8")
    )  # fmt: skip

    # Performance
    WORKER_COUNT: int = int(os.getenv("WORKER_COUNT", "4"))
    WORKER_TIMEOUT: int = int(os.getenv("WORKER_TIMEOUT", "30"))
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "100"))

    # Monitoring
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    METRICS_PORT: int = int(
        os.getenv("METRICS_PORT", "8090")
    )  # fmt: skip

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
