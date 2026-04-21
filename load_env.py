from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    BACKEND_API_BASE_URL: str
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
