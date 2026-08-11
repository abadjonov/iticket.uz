from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ilova sozlamalari — qiymatlar `.env` fayldan yoki muhit o'zgaruvchilaridan o'qiladi."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "iticket.uz API"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    HOST: str = "localhost"
    PORT: int = 8000

    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """Async SQLAlchemy (asyncpg) uchun ulanish satri."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
