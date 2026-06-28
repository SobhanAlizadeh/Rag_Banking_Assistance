# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # فیلدهای موجود
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # فیلدهای جدید (بر اساس خطاها)
    api_url: Optional[str] = None
    api_token: Optional[str] = None
    secret_key: Optional[str] = None
    chroma_persist_dir: str = "./chroma_db"
    log_level: str = "INFO"
    
    # اگر می‌خواهید فیلدهای اضافی نادیده گرفته شوند (راه‌حل جایگزین)
    class Config:
        extra = "ignore"  # فیلدهای اضافی را نادیده بگیر

settings = Settings()