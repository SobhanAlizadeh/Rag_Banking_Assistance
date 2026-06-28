# app/llm/prompt_builder.py
from typing import List, Dict, Optional

SYSTEM_PROMPT = """شما یک دستیار بانکی حرفه‌ای و دقیق هستید.

قوانین مهم:
1. فقط بر اساس اطلاعات موجود در "متن‌های مرجع" پاسخ دهید.
2. اگر پاسخ در متن‌های مرجع وجود ندارد، صادقانه بگویید: "اطلاعات کافی در اسناد موجود نیست."
3. از دانش عمومی خود استفاده نکنید.
4. پاسخ‌ها را به زبان فارسی روان و ساده بنویسید.
5. اگر کاربر به سوال قبلی اشاره کرد (مثل "دوباره توضیح بده")، به تاریخچه گفتگو توجه کنید.
"""

def build_prompt(
    question: str,
    documents: List[str],
    history: List[Dict[str, str]],
    system_prompt: Optional[str] = None
) -> str:
    """
    ساخت پرامپت کامل با تاریخچه گفتگو و اسناد بازیابی‌شده
    """
    # ۱. سیستم پرامپت
    system = system_prompt or SYSTEM_PROMPT
    
    # ۲. تاریخچه گفتگو
    conversation = ""
    for msg in history:
        role = "کاربر" if msg["role"] == "user" else "دستیار"
        conversation += f"{role}: {msg['content']}\n\n"
    
    if not conversation:
        conversation = "هیچ گفتگوی قبلی وجود ندارد."
    
    # ۳. متن‌های مرجع (Context)
    if documents:
        context = "\n\n---\n\n".join(documents)
    else:
        context = "هیچ سند مرتبطی یافت نشد."
    
    # ۴. ساخت پرامپت نهایی با ترتیب استاندارد
    prompt = f"""{system}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 تاریخچه گفتگو:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{conversation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 متن‌های مرجع:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ سوال کاربر:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{question}

پاسخ شما:"""

    return prompt

def build_prompt_for_test(
    question: str,
    documents: List[str],
    history: List[Dict[str, str]]
) -> str:
    """
    نسخه ساده‌شده برای تست (بدون سیستم پرامپت)
    """
    conversation = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in history
    ])
    
    context = "\n\n".join(documents)
    
    return f"""Conversation History:
{conversation}

Retrieved Context:
{context}

Current Question:
{question}

Answer:"""