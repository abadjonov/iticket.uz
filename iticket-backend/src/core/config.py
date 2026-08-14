from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
	app_name: str = "iticket-backend"
	debug: bool = True
	database_url: AnyUrl = "sqlite+aiosqlite:///./dev.db"
	secret_key: str = "changeme"
	access_token_expire_minutes: int = 60 * 24

	smtp_host: str | None = None
	smtp_port: int | None = None
	smtp_user: str | None = None
	smtp_password: str | None = None

	class Config:
		env_file = ".env"


settings = Settings()

