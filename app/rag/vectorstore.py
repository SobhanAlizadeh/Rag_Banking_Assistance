import chromadb
from app.rag.embedding import get_embedding
from app.rag.generator import generate_answer

client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection("bank_rag")

def add_chunks(chunks):

    existing = collection.count()

    for i, chunk in enumerate(chunks):

        emb = get_embedding(chunk)

        collection.add(
            ids=[f"chunk_{existing+i}"],
            documents=[chunk],
            embeddings=[emb],
            metadatas=[
        {
            "source": "bank.pdf",
            "chunk_id": i
        }
        ]
        )

def search(query, k=3):
    query_emb = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=k
    )
    return results['documents'][0]

def rag_chat(question):
    docs = search(question)
    context = "\n".join(docs)
    answer = generate_answer(context, question)
    return answer, docs  # هم پاسخ و هم مستندات را برگردان