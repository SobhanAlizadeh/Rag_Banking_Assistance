import pytest
from app.rag.vectorstore import rag_chat

def test_rag_chat():
    answer, sources = rag_chat("شرایط وام مسکن چیست؟")
    assert isinstance(answer, str)
    assert isinstance(sources, list)