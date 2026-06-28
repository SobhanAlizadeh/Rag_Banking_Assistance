# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.rag.pipeline import run_pipeline
from app.api.deps import get_current_user
from app.cache.redis_client import get_cache_stats, clear_session_cache

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list = []
    from_cache: bool = False  # 🆕 نشان می‌دهد آیا پاسخ از کش آمده
    processing_time: float = 0.0  # 🆕 زمان پردازش

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        result = run_pipeline(
            session_id=request.session_id,
            question=request.question
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            from_cache=result.get("from_cache", False),
            processing_time=result.get("processing_time", 0.0)
        )
        
    except Exception as e:
        print(f"❌ Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== اندپوینت‌های مدیریت کش ==========

@router.get("/cache/stats")
async def cache_stats(current_user: dict = Depends(get_current_user)):
    """دریافت آمار کش"""
    return get_cache_stats()

@router.delete("/cache/session/{session_id}")
async def clear_session_cache_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """پاک کردن کش یک session خاص"""
    deleted = clear_session_cache(session_id)
    return {"deleted_count": deleted, "message": f"{deleted} keys deleted"}

@router.delete("/cache/all")
async def clear_all_cache(current_user: dict = Depends(get_current_user)):
    """پاک کردن تمام کش (فقط ادمین)"""
    from app.cache.redis_client import redis_client
    keys = redis_client.keys("cache:answer:*")
    if keys:
        deleted = redis_client.delete(*keys)
        return {"deleted_count": deleted}
    return {"deleted_count": 0}