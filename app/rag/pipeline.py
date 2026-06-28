# app/rag/pipeline.py
import logging
from typing import Dict, Any, List
from app.memory.conversation import load_history, append_message
from app.rag.retriever import retrieve_documents
from app.llm.prompt_builder import build_prompt, SYSTEM_PROMPT  # ← import SYSTEM_PROMPT
from app.llm.generator import generate_answer
from app.cache.redis_client import get_cached_answer, set_cached_answer
import time

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Pipeline کامل RAG با پشتیبانی از حافظه گفتگو و کش
    """
    
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT  # ← حالا تعریف شده است
        self.cache_ttl = 3600  # ۱ ساعت
    
    def execute(self, session_id: str, question: str) -> Dict[str, Any]:
        """
        اجرای کامل Pipeline با کش
        """
        start_time = time.time()
        
        # ========== مرحله ۰: بررسی کش ==========
        cached_answer = get_cached_answer(question, session_id)
        if cached_answer:
            print(f"⚡ پاسخ از کش برای: {question[:30]}...")
            append_message(session_id, "user", question)
            append_message(session_id, "assistant", cached_answer)
            
            return {
                "answer": cached_answer,
                "sources": [],
                "from_cache": True,
                "processing_time": time.time() - start_time
            }
        
        # ========== مرحله ۱: دریافت تاریخچه ==========
        history = load_history(session_id)
        
        # ========== مرحله ۲: بازیابی اسناد ==========
        documents = retrieve_documents(question)
        
        # ========== مرحله ۳: ساخت پرامپت ==========
        prompt = build_prompt(
            question=question,
            documents=documents,
            history=history,
            system_prompt=self.system_prompt
        )
        
        # ========== مرحله ۴: تولید پاسخ ==========
        answer = generate_answer(prompt)
        
        # ========== مرحله ۵: ذخیره در کش ==========
        set_cached_answer(question, answer, session_id, self.cache_ttl)
        
        # ========== مرحله ۶: ذخیره در تاریخچه ==========
        append_message(session_id, "user", question)
        append_message(session_id, "assistant", answer)
        
        # ========== مرحله ۷: برگرداندن نتیجه ==========
        return {
            "answer": answer,
            "sources": documents,
            "from_cache": False,
            "processing_time": time.time() - start_time
        }
    def _get_history(self, session_id: str) -> List[Dict[str, str]]:
        """دریافت تاریخچه مکالمه"""
        try:
            history = load_history(session_id)
            return history
        except Exception as e:
            logger.warning(f"Could not load history: {e}")
            return []
    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """دریافت تاریخچه کامل برای نمایش (عمومی)"""
        return self._get_history(session_id)

# نمونه سراسری Pipeline
pipeline = RAGPipeline()

def run_pipeline(session_id: str, question: str) -> Dict[str, Any]:
    return pipeline.execute(session_id, question)