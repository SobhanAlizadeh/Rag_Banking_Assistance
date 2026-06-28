# main.py (در ریشه پروژه)
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.auth import router as auth_router      # ✅ مسیر درست
from app.api.routes import router as chat_router    # ✅ مسیر درست
from prometheus_fastapi_instrumentator import Instrumentator

security_scheme = HTTPBearer()

app = FastAPI(
    title="Banking Assistant",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True,
)

# instrument کردن اپ
instrumentator.instrument(app).expose(app, endpoint="/metrics")

app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}