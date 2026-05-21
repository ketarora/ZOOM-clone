"""
app/core/config.py
Centralised settings loaded from .env via pydantic-settings
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────
    APP_NAME: str = "ZoomConnect"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production

    # ── Security ─────────────────────────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 h

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./zoomconnect.db"

    # ── CORS ─────────────────────────────────────────────────────
    CORS_ORIGINS: str = "*"

    # ── Derived ──────────────────────────────────────────────────
    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — call this everywhere instead of instantiating."""
    return Settings()
