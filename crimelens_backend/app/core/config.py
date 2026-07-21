from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CrimeCop AI"
    MONGO_URL: str = "mongodb://localhost:27017/crimecop"
    REDIS_URL: Optional[str] = None
    JWT_SECRET: str = "cybernexus_super_secure_key_123!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # AI Engine settings
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
