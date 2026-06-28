# app/memory/conversation.py
import json
from typing import List, Dict, Any
from app.cache.redis_client import redis_client

# تنظیمات
MEMORY_TTL = 60 * 60 * 24  # ۲۴ ساعت
MAX_HISTORY = 10  # حداکثر تعداد پیام‌های ذخیره‌شده

def load_history(session_id: str) -> List[Dict[str, str]]:
    """
    دریافت تاریخچه گفتگو از Redis
    """
    key = f"history:{session_id}"
    data = redis_client.get(key)
    
    if data is None:
        return []
    
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        # اگر داده خراب بود، تاریخچه را پاک کن
        redis_client.delete(key)
        return []

def save_history(session_id: str, history: List[Dict[str, str]]) -> None:
    """
    ذخیره تاریخچه گفتگو در Redis با TTL
    """
    key = f"history:{session_id}"
    redis_client.setex(
        key,
        MEMORY_TTL,
        json.dumps(history)
    )

def append_message(session_id: str, role: str, content: str) -> None:
    """
    اضافه کردن یک پیام جدید به تاریخچه
    """
    history = load_history(session_id)
    
    # اضافه کردن پیام جدید
    history.append({
        "role": role,
        "content": content
    })
    
    # محدود کردن تعداد پیام‌ها
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    
    save_history(session_id, history)

def get_conversation_text(history: List[Dict[str, str]]) -> str:
    """
    تبدیل تاریخچه به متن برای قرار دادن در پرامپت
    """
    conversation = ""
    for msg in history:
        role = "کاربر" if msg["role"] == "user" else "دستیار"
        conversation += f"{role}: {msg['content']}\n\n"
    
    return conversation.strip()