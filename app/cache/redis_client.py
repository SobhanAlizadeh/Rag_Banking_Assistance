# app/cache/redis_client.py
import redis
import json
import hashlib
from typing import Optional, Any
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

# ========== توابع کش عمومی ==========

def cache_get(key: str) -> Optional[str]:
    """دریافت مقدار از کش"""
    return redis_client.get(key)

def cache_set(key: str, value: str, ttl: int = 3600) -> None:
    """ذخیره مقدار در کش با TTL (پیش‌فرض ۱ ساعت)"""
    redis_client.setex(key, ttl, value)

def cache_delete(key: str) -> None:
    """حذف یک کلید از کش"""
    redis_client.delete(key)

def cache_exists(key: str) -> bool:
    """بررسی وجود کلید در کش"""
    return redis_client.exists(key) > 0

# ========== توابع مخصوص کش پاسخ‌ها ==========

def get_cached_answer(question: str, session_id: Optional[str] = None) -> Optional[str]:
    """
    دریافت پاسخ کش‌شده برای یک سوال
    
    اگر session_id نداشته باشد، کش سراسری است.
    اگر session_id داشته باشد، کش مختص آن session است.
    """
    key = _build_cache_key(question, session_id)
    data = cache_get(key)
    
    if data is None:
        return None
    
    try:
        result = json.loads(data)
        return result.get("answer")
    except json.JSONDecodeError:
        return None

def set_cached_answer(question: str, answer: str, session_id: Optional[str] = None, ttl: int = 3600) -> None:
    """
    ذخیره پاسخ در کش
    
    ttl: زمان انقضا به ثانیه (پیش‌فرض ۱ ساعت)
    """
    key = _build_cache_key(question, session_id)
    data = json.dumps({
        "answer": answer,
        "timestamp": redis_client.time()[0]  # زمان فعلی به ثانیه
    })
    cache_set(key, data, ttl)

def _build_cache_key(question: str, session_id: Optional[str] = None) -> str:
    """
    ساخت کلید یکتا برای کش
    
    با استفاده از hash سوال، کلید کوتاه و یکتا می‌شود
    """
    # نرمال‌سازی سوال (حذف فاصله‌های اضافی و کوچک‌سازی)
    normalized = " ".join(question.lower().split())
    
    # ساخت hash از سوال
    question_hash = hashlib.md5(normalized.encode()).hexdigest()[:16]
    
    if session_id:
        return f"cache:answer:{session_id}:{question_hash}"
    else:
        return f"cache:answer:global:{question_hash}"

def clear_session_cache(session_id: str) -> int:
    """
    پاک کردن تمام کش‌های مربوط به یک session
    
    Returns: تعداد کلیدهای پاک‌شده
    """
    pattern = f"cache:answer:{session_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        return redis_client.delete(*keys)
    return 0

def get_cache_stats() -> dict:
    """
    دریافت آمار کش (تعداد کلیدها و ...)
    """
    all_keys = redis_client.keys("cache:answer:*")
    return {
        "total_keys": len(all_keys),
        "global_keys": len(redis_client.keys("cache:answer:global:*")),
        "session_keys": len(all_keys) - len(redis_client.keys("cache:answer:global:*"))
    }