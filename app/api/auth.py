from fastapi import APIRouter
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login():
    token = create_access_token({
        "user":"admin"
    })
    return {"access_token": token, "token_type": "bearer"}