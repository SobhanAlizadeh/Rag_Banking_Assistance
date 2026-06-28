# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from app.services.chat_service import chat_service
from app.api.deps import get_current_user
from app.cache.redis_client import get_cache_stats, clear_session_cache, redis_client
# from app.services.monitoring_service import monitoring
from app.memory.conversation import load_history

import json
import pandas as pd

router = APIRouter()

# ==========================================
# مدل‌های داده (Pydantic Models)
# ==========================================

class ChatRequest(BaseModel):
    """مدل درخواست چت"""
    session_id: str
    question: str

class ChatResponse(BaseModel):
    """مدل پاسخ چت"""
    answer: str
    sources: List[str] = []
    from_cache: bool = False
    processing_time: float = 0.0
    run_id: Optional[str] = None

class CacheStatsResponse(BaseModel):
    """مدل آمار کش"""
    total_keys: int
    global_keys: int
    session_keys: int

class MonitoringStatsResponse(BaseModel):
    """مدل آمار مانیتورینگ"""
    total_interactions: int
    avg_processing_time: float
    avg_answer_length: float
    cache_hit_rate: float

# ==========================================
# اندپوینت اصلی چت
# ==========================================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    دریافت پاسخ برای سوال کاربر
    
    - **session_id**: شناسه یکتا برای هر مکالمه
    - **question**: سوال کاربر
    """
    try:
        # استفاده از ChatService با یکپارچه‌سازی MLflow
        result = chat_service.ask(
            session_id=request.session_id,
            question=request.question
        )
                
        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            from_cache=result.get("from_cache", False),
            processing_time=result.get("processing_time", 0.0),
            run_id=result.get("run_id")
        )
        
    except Exception as e:
        print(f"❌ Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# اندپوینت‌های مدیریت کش (Cache)
# ==========================================

@router.get("/cache/stats", response_model=CacheStatsResponse)
async def cache_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    دریافت آمار کش Redis
    """
    stats = get_cache_stats()
    return CacheStatsResponse(
        total_keys=stats.get("total_keys", 0),
        global_keys=stats.get("global_keys", 0),
        session_keys=stats.get("session_keys", 0)
    )

@router.delete("/cache/session/{session_id}")
async def clear_session_cache_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    پاک کردن کش یک جلسه خاص
    
    - **session_id**: شناسه جلسه
    """
    deleted = clear_session_cache(session_id)
    return {
        "deleted_count": deleted,
        "message": f"{deleted} keys deleted for session {session_id}"
    }

@router.delete("/cache/all")
async def clear_all_cache(
    current_user: dict = Depends(get_current_user)
):
    """
    پاک کردن تمام کش سراسری (فقط ادمین)
    """
    keys = redis_client.keys("cache:answer:*")
    if keys:
        deleted = redis_client.delete(*keys)
        return {"deleted_count": deleted, "message": f"{deleted} keys deleted globally"}
    return {"deleted_count": 0, "message": "No cache keys found"}

# ==========================================
# اندپوینت‌های مانیتورینگ (Monitoring)
# ==========================================

@router.get("/monitoring/stats", response_model=MonitoringStatsResponse)
async def monitoring_stats(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    دریافت آمار کلی سیستم از ۱۰۰ تعامل اخیر
    
    - **limit**: تعداد تعاملات برای محاسبه آمار (پیش‌فرض ۱۰۰)
    """
    interactions = redis_client.keys("monitoring:interaction:*")
    
    if not interactions:
        return MonitoringStatsResponse(
            total_interactions=0,
            avg_processing_time=0.0,
            avg_answer_length=0.0,
            cache_hit_rate=0.0
        )
    
    # دریافت آخرین تعاملات
    recent_keys = interactions[-limit:]
    total_time = 0
    total_length = 0
    cache_hits = 0
    
    for key in recent_keys:
        data = redis_client.get(key)
        if data:
            try:
                interaction = json.loads(data)
                total_time += interaction.get("processing_time", 0)
                total_length += interaction.get("answer_length", 0)
                if interaction.get("from_cache"):
                    cache_hits += 1
            except json.JSONDecodeError:
                continue
    
    n = len(recent_keys)
    return MonitoringStatsResponse(
        total_interactions=len(interactions),
        avg_processing_time=round(total_time / n, 3) if n > 0 else 0.0,
        avg_answer_length=round(total_length / n, 1) if n > 0 else 0.0,
        cache_hit_rate=round((cache_hits / n) * 100, 1) if n > 0 else 0.0
    )

@router.get("/monitoring/interactions")
async def get_interactions(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    دریافت لیست تعاملات اخیر
    
    - **limit**: تعداد تعاملات
    - **offset**: نقطه شروع
    """
    interactions = redis_client.keys("monitoring:interaction:*")
    
    # مرتب‌سازی بر اساس زمان (جدیدترین اول)
    sorted_keys = sorted(interactions, reverse=True)
    
    # اعمال offset و limit
    paginated_keys = sorted_keys[offset:offset + limit]
    
    result = []
    for key in paginated_keys:
        data = redis_client.get(key)
        if data:
            try:
                interaction = json.loads(data)
                result.append(interaction)
            except json.JSONDecodeError:
                continue
    
    return {
        "total": len(interactions),
        "offset": offset,
        "limit": limit,
        "interactions": result
    }

# ==========================================
# اندپوینت‌های سلامت و اطلاعات
# ==========================================

@router.get("/health")
async def health_check():
    """
    بررسی سلامت سرویس
    """
    try:
        # تست اتصال به Redis
        redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "version": "1.0.0"
    }

@router.get("/info")
async def system_info(current_user: dict = Depends(get_current_user)):
    """
    دریافت اطلاعات سیستم
    """
    return {
        "system": {
            "name": "RAG Banking Assistant",
            "version": "1.0.0",
            "environment": "production"
        },
        "cache_stats": get_cache_stats(),
        "monitoring_enabled": True,
        "mlflow_enabled": True
    }

# ==========================================
# اندپوینت‌های آزمایشی (برای دیباگ)
# ==========================================

@router.get("/debug/prompt")
async def debug_prompt(
    question: str,
    session_id: str = "test-session",
    # current_user: dict = Depends(get_current_user)
):
    """
    دریافت پرامپت ساخته‌شده برای یک سوال (برای دیباگ)
    """
    from app.rag.pipeline import pipeline
    
    # دریافت تاریخچه و اسناد
    history = load_history(session_id)
    
    # ساخت پرامپت
    from app.llm.prompt_builder import build_prompt
    prompt = build_prompt(
        question=question,
        documents=[],
        history=history,
        system_prompt=pipeline.system_prompt
    )
    
    return {
        "prompt": prompt,
        "num_documents": len([]),
        "history_length": len(history)
    }

