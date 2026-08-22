from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ilova sozlamalari — qiymatlar `.env` fayldan yoki muhit o'zgaruvchilaridan o'qiladi."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    PROJECT_NAME: str = "iticket.uz API"
    ACCESS_TOKEN_TIMELIMIT: int = 10
    ACCESS_TOKEN_SECRET_KEY: str = "change-me"

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
