# app/rag/retriever.py
from app.rag.vectorstore import search

def retrieve_documents(query: str, k: int = 3):

    return search(query, k=k)
    