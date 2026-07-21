import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "CrimeLens AI"
    ENV: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Database
    MONGODB_URL: str = "mongodb://localhost:27017/crimelens"
    DB_NAME: str = "crimelens"

    # Security
    JWT_SECRET_KEY: str = "9a6c5df9df1a073fdeee80e8ef186c52bb023d6a2f8c5b6b19280d0d8299feee"
    JWT_REFRESH_SECRET_KEY: str = "0a6d54cf8a7ef20bcf8a48ef18a6a2cf2a8c5b6b12980d0d2989feee0011bb22"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # AI Services
    GEMINI_API_KEY: Optional[str] = ""

    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]

    # Rate Limiting
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
