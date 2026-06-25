# app/api/deps.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.services.chat_service import ChatService

# ایجاد یک نمونه از HTTPBearer
security = HTTPBearer()

def get_chat_service():
    return ChatService()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    دریافت و اعتبارسنجی توکن از هدر Authorization
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    return payload