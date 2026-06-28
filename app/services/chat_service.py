# app/services/chat_service.py
import mlflow
import time
from typing import Dict, Any, Optional
from app.rag.pipeline import pipeline
from app.core.config import settings


class ChatService:
    """
    سرویس چت با یکپارچه‌سازی MLflow برای ردیابی آزمایش‌ها
    (با Lazy Initialization برای جلوگیری از خطای اتصال در زمان import)
    """
    
    def __init__(self):
        """
        تنظیمات اولیه - بدون اتصال به MLflow در زمان ساخت
        """
        self._mlflow_initialized = False
        self.mlflow_enabled = settings.MLFLOW_ENABLED if hasattr(settings, "MLFLOW_ENABLED") else True
        self.tracking_uri = settings.MLFLOW_TRACKING_URI if hasattr(settings, "MLFLOW_TRACKING_URI") else "http://mlflow:5000"
        self.experiment_name = "RAG_Banking"
    
    def _init_mlflow(self):
        """
        مقداردهی اولیه MLflow در زمان اولین استفاده (Lazy Initialization)
        """
        if self._mlflow_initialized or not self.mlflow_enabled:
            return
        
        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            self._mlflow_initialized = True
            print(f"✅ MLflow initialized with tracking URI: {self.tracking_uri}")
        except Exception as e:
            print(f"⚠️ MLflow initialization failed: {e}")
            self.mlflow_enabled = False
            self._mlflow_initialized = False
    
    def ask(self, session_id: str, question: str) -> Dict[str, Any]:
        """
        پردازش سوال کاربر با ردیابی در MLflow
        """
        # مقداردهی اولیه MLflow در اولین استفاده
        self._init_mlflow()
        
        # ========== اجرای Pipeline ==========
        start_time = time.time()
        result = pipeline.execute(session_id, question)
        processing_time = time.time() - start_time
        
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        from_cache = result.get("from_cache", False)
        
        # ========== ثبت در MLflow (اگر فعال باشد) ==========
        if self.mlflow_enabled and self._mlflow_initialized:
            try:
                with mlflow.start_run(run_name=f"query-{question[:30]}") as run:
                    # ثبت پارامترها
                    mlflow.log_param("session_id", session_id)
                    mlflow.log_param("question", question)
                    mlflow.log_param("question_length", len(question))
                    
                    # ثبت متریک‌ها
                    mlflow.log_metric("processing_time_seconds", processing_time)
                    mlflow.log_metric("answer_length", len(answer))
                    mlflow.log_metric("num_sources", len(sources))
                    mlflow.log_metric("from_cache", 1 if from_cache else 0)
                    
                    # ثبت Tagها
                    mlflow.set_tag("model", "openai/gpt-oss-120b:free")
                    mlflow.set_tag("env", settings.ENV if hasattr(settings, "ENV") else "development")
                    mlflow.set_tag("cache_hit", "yes" if from_cache else "no")
                    
                    # ذخیره پاسخ به‌عنوان Artifact
                    with open("temp_answer.txt", "w", encoding="utf-8") as f:
                        f.write(f"Question: {question}\n\n")
                        f.write(f"Answer: {answer}\n\n")
                        f.write(f"Sources: {len(sources)} documents\n")
                        f.write(f"From Cache: {from_cache}\n")
                        f.write(f"Processing Time: {processing_time:.3f}s\n")
                    mlflow.log_artifact("temp_answer.txt")
                    
                    run_id = run.info.run_id
            except Exception as e:
                print(f"⚠️ MLflow logging failed: {e}")
                run_id = None
        else:
            run_id = None
        
        # ========== نتیجه نهایی ==========
        return {
            "answer": answer,
            "sources": sources,
            "from_cache": from_cache,
            "processing_time": processing_time,
            "run_id": run_id
        }
    
    def ask_without_mlflow(self, session_id: str, question: str) -> Dict[str, Any]:
        """
        نسخه بدون MLflow برای محیط‌های سبک یا تست
        """
        start_time = time.time()
        result = pipeline.execute(session_id, question)
        processing_time = time.time() - start_time
        
        return {
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
            "from_cache": result.get("from_cache", False),
            "processing_time": processing_time
        }


# ========== نمونه سراسری سرویس ==========
chat_service = ChatService()


# ========== تابع کمکی برای استفاده در API ==========
def get_chat_service() -> ChatService:
    """دریافت نمونه ChatService (برای استفاده در Dependency Injection)"""
    return chat_service