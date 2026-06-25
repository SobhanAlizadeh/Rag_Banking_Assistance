# app/main.py
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.auth import router as auth_router
from api.routes import router as chat_router
from prometheus_fastapi_instrumentator import Instrumentator

# تعریف طرح امنیتی برای مستندات
security_scheme = HTTPBearer()

app = FastAPI(
    title="Banking Assistant",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True  # توکن پس از رفرش صفحه باقی بماند
    }
)

# افزودن میان‌افزار متریک

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# ثبت روترها
app.include_router(auth_router)
app.include_router(chat_router)

# (اختیاری) مسیر تست
@app.get("/ping")
def ping():
    return {"status": "ok"}