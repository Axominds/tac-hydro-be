from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # Core Django settings
    SECRET_KEY: str
    DEBUG: bool = False

    # Hosts
    ALLOWED_HOSTS: list[str]

    # CORS
    CORS_ALLOW_ALL_ORIGINS: bool = False
    CORS_ALLOWED_ORIGINS: list[str]

    # Database (optional override - if not set, sqlite is used)
    DATABASE_URL: str = ""

    # Email
    EMAIL_HOST: str = "smtp.zoho.com"
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = ""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


env = Settings()
print(env)
