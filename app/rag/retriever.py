# app/rag/retriever.py
from app.rag.vectorstore import search

def retrieve_documents(query: str, k: int = 3):
    """
    بازیابی اسناد مرتبط از پایگاه داده برداری
    
    Args:
        query (str): سوال کاربر
        k (int): تعداد اسناد مورد نظر
    
    Returns:
        list: لیست متن‌های بازیابی‌شده
    """
    # تابع search در vectorstore قبلاً تعریف شده است
    docs = search(query, k=k)
    
    # اگر هیچ نتیجه‌ای نبود، یک لیست خالی برگردان
    if not docs:
        return []
    
    return docs