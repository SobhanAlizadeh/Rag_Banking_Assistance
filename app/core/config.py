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
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://mlflow:5000"
    MLFLOW_ENABLED: bool = True  # ← اضافه شد
    ENV: str = "development"

    # API
    API_URL: Optional[str] = None
    API_TOKEN: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    
    # RAG
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"

    # اگر می‌خواهید فیلدهای اضافی نادیده گرفته شوند (راه‌حل جایگزین)
    class Config:
        env_file = ".envv"
        extra = "ignore"  # فیلدهای اضافی را نادیده بگیر

settings = Settings()