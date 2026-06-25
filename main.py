# main.py (در ریشه پروژه)
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.auth import router as auth_router      # ✅ مسیر درست
from api.routes import router as chat_router    # ✅ مسیر درست
from prometheus_fastapi_instrumentator import Instrumentator

security_scheme = HTTPBearer()

app = FastAPI(
    title="Banking Assistant",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}