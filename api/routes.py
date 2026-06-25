# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.rag.vectorstore import rag_chat
from app.api.deps import get_chat_service, get_current_user
from app.services.chat_service import ChatService


router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list = []

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),  # ← محافظت شده
    #for use mlflow for metrics and tracking you must uncomment the following line
    # chat_service: ChatService = Depends(get_chat_service)
):
    try:
        chat=ChatService()
        chat.ask(request.question)
        answer, sources = rag_chat(request.question) #for use mlflow comment this
        # answer,source=ChatService().ask(request.question) # uncomment this
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))