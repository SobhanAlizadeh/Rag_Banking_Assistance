# streamlit/chat_app.py
import streamlit as st
import requests
import uuid
import os
import time
from dotenv import load_dotenv

load_dotenv(".envv")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="🏦 بانک‌یار - دستیار هوشمند بانکی",
    page_icon="🏦",
    layout="centered"
)

# ========== مدیریت Session ==========
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

# ========== صفحه ورود ==========
def login_page():
    st.title("🔐 ورود به سامانه")
    st.markdown("---")
    
    with st.form("login_form"):
        username = st.text_input("👤 نام کاربری", placeholder="نام کاربری خود را وارد کنید")
        password = st.text_input("🔑 رمز عبور", type="password", placeholder="رمز عبور خود را وارد کنید")
        submitted = st.form_submit_button("🚪 ورود", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("❌ لطفاً همه فیلدها را پر کنید")
            else:
                try:
                    with st.spinner("⏳ در حال اتصال به سرور..."):
                        response = requests.post(
                            f"{API_URL}/login",
                            json={"username": username, "password": password},
                            timeout=10
                        )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data.get("access_token")
                        st.session_state.username = username
                        st.success("✅ ورود موفق! در حال انتقال به صفحه چت...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ نام کاربری یا رمز عبور اشتباه است")
                except requests.exceptions.Timeout:
                    st.error("⏳ زمان اتصال به سرور به پایان رسید. لطفاً دوباره تلاش کنید.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 اتصال به سرور برقرار نشد. مطمئن شوید سرور در حال اجراست.")
                except Exception as e:
                    st.error(f"❌ خطا: {e}")

# ========== صفحه چت ==========
def chat_page():
    # هدر
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.title("🏦 بانک‌یار")
        st.caption(f"👤 کاربر: {st.session_state.username}")
    with col2:
        if st.button("🔄 جدید", help="شروع مکالمه جدید"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    with col3:
        if st.button("🚪 خروج"):
            # پاک کردن session
            del st.session_state.token
            del st.session_state.username
            del st.session_state.session_id
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    
    # ========== نمایش تاریخچه پیام‌ها ==========
    if not st.session_state.messages:
        st.info("💡 سوال خود را درباره بانکداری، وام، سرمایه‌گذاری و ... بپرسید.")
        st.caption("📌 این دستیار بر اساس اسناد بانکی شما پاسخ می‌دهد.")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # نمایش وضعیت کش اگر پیام از کش آمده باشد
            if msg.get("from_cache", False):
                st.caption(f"⚡ پاسخ از کش (زمان: {msg.get('processing_time', 0):.2f} ثانیه)")
            elif msg.get("processing_time") is not None:
                st.caption(f"🔄 پاسخ جدید (زمان: {msg.get('processing_time', 0):.2f} ثانیه)")
    
    # ========== ورودی کاربر ==========
    if prompt := st.chat_input("📝 سوال خود را بپرسید..."):
        # نمایش پیام کاربر
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # ذخیره پیام کاربر در history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "from_cache": False,
            "processing_time": None
        })
        
        # ========== ارسال به API ==========
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            
            # ارسال درخواست با time_start
            start_time = time.time()
            
            with st.spinner("🤔 در حال پردازش سوال شما..."):
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "question": prompt
                    },
                    headers=headers,
                    timeout=120
                )
            
            response.raise_for_status()
            data = response.json()
            
            # استخراج داده‌ها
            answer = data.get("answer", "پاسخی دریافت نشد.")
            from_cache = data.get("from_cache", False)
            processing_time = data.get("processing_time", 0.0)
            
            # نمایش پاسخ
            with st.chat_message("assistant"):
                st.markdown(answer)
                
                # نمایش وضعیت کش
                if from_cache:
                    st.caption(f"⚡ پاسخ از کش (زمان: {processing_time:.2f} ثانیه)")
                else:
                    st.caption(f"🔄 پاسخ جدید (زمان: {processing_time:.2f} ثانیه)")
            
            # ذخیره پاسخ در history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "from_cache": from_cache,
                "processing_time": processing_time
            })
            
        except requests.exceptions.Timeout:
            error_msg = "⏳ زمان پاسخ‌دهی به پایان رسید. لطفاً دوباره تلاش کنید."
            with st.chat_message("assistant"):
                st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "from_cache": False,
                "processing_time": None
            })
            
        except requests.exceptions.ConnectionError:
            error_msg = "🔌 اتصال به سرور برقرار نشد. مطمئن شوید سرور در حال اجراست."
            with st.chat_message("assistant"):
                st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "from_cache": False,
                "processing_time": None
            })
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = "🔐 نشست شما منقضی شده است. لطفاً دوباره وارد شوید."
                with st.chat_message("assistant"):
                    st.error(error_msg)
                # حذف توکن برای نمایش صفحه ورود
                del st.session_state.token
                st.rerun()
            else:
                error_msg = f"❌ خطای سرور: {e.response.status_code}"
                with st.chat_message("assistant"):
                    st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "from_cache": False,
                    "processing_time": None
                })
                
        except Exception as e:
            error_msg = f"❌ خطا در ارتباط با سرور: {e}"
            with st.chat_message("assistant"):
                st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "from_cache": False,
                "processing_time": None
            })

# ========== سایدبار با اطلاعات ==========
def render_sidebar():
    with st.sidebar:
        st.markdown("## ℹ️ اطلاعات")
        st.markdown(f"**شناسه نشست:**")
        st.code(st.session_state.session_id[:8] + "...", language="text")
        
        st.markdown("---")
        st.markdown("### 📊 وضعیت")
        
        # آمار پیام‌ها
        total_messages = len(st.session_state.messages)
        user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
        assistant_messages = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        cached_messages = sum(1 for m in st.session_state.messages if m.get("from_cache", False))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💬 کل پیام‌ها", total_messages)
        with col2:
            st.metric("⚡ از کش", cached_messages)
        
        st.markdown("---")
        st.markdown("### 🛠️ ابزارها")
        
        if st.button("🗑️ پاک کردن کش این نشست", use_container_width=True):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.delete(
                    f"{API_URL}/cache/session/{st.session_state.session_id}",
                    headers=headers
                )
                if response.status_code == 200:
                    st.success("✅ کش پاک شد!")
                else:
                    st.error("❌ خطا در پاک کردن کش")
            except Exception as e:
                st.error(f"❌ خطا: {e}")
        
        if st.button("📊 آمار کش سراسری", use_container_width=True):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.get(
                    f"{API_URL}/cache/stats",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    st.json(data)
                else:
                    st.error("❌ خطا در دریافت آمار")
            except Exception as e:
                st.error(f"❌ خطا: {e}")
        
        st.markdown("---")
        st.markdown("### 📌 نکات")
        st.info(
            "⚡ پاسخ‌های تکراری از **کش Redis** بازیابی می‌شوند.\n\n"
            "🔄 برای شروع مکالمه جدید، دکمه **جدید** را بزنید.\n\n"
            "🗑️ با **پاک کردن کش**، پاسخ‌های ذخیره‌شده حذف می‌شوند."
        )

# ========== اجرای اصلی ==========
def main():
    if "token" not in st.session_state or st.session_state.token is None:
        login_page()
    else:
        render_sidebar()
        chat_page()

if __name__ == "__main__":
    main()