from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Ad Platform API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./ad_platform.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Ocean Engine (巨量引擎)
    OCEAN_APP_ID: str = ""
    OCEAN_APP_SECRET: str = ""
    OCEAN_REDIRECT_URI: str = "http://localhost:5173/oauth/callback"
    OCEAN_API_BASE: str = "https://api.oceanengine.com/open_api/v3.0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
