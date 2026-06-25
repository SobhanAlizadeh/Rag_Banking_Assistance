# streamlit/chat_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(".envv")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ========== صفحه ورود ==========
def login_page():
    st.title("🔐 ورود به سامانه")
    
    with st.form("login_form"):
        submitted = st.form_submit_button("ورود")
        
        if submitted:
            
            try:
                response = requests.post(
                    f"{API_URL}/login",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                st.session_state.token = data.get("access_token")
                st.success("✅ ورود موفق")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطا در ارتباط با سرور: {e}")

# ========== صفحه چت ==========
def chat_page():
    st.title("🏦 دستیار بانکی")
    
    # دکمه خروج
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 خروج"):
            del st.session_state.token
            st.rerun()
        
    # تاریخچه پیام‌ها
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # ورودی کاربر
    if prompt := st.chat_input("سوال خود را بپرسید..."):
        # نمایش پیام کاربر
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # ارسال به API
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(
                f"{API_URL}/chat",
                json={"question": prompt},
                headers=headers,
                timeout=60  # افزایش timeout به ۶۰ ثانیه
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "پاسخی دریافت نشد.")
        except requests.exceptions.Timeout:
            answer = "⏳ زمان پاسخ‌دهی به پایان رسید. لطفاً دوباره تلاش کنید."
        except Exception as e:
            answer = f"❌ خطا در ارتباط با سرور: {e}"
        
        # نمایش پاسخ
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ========== اجرای اصلی ==========
def main():
    # تنظیمات صفحه
    st.set_page_config(page_title="بانک‌یار", layout="centered")
    
    # اگر توکن وجود نداشته باشد، صفحه ورود نشان داده شود
    if "token" not in st.session_state:
        login_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()