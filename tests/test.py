import sys
from pathlib import Path

# اضافه کردن مسیر ریشه پروژه به sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.vectorstore import add_chunks, search

# 1. Load PDF
text = load_pdf("data/pdfs/Cornell University Library.pdf")

# 2. Chunk
chunks = chunk_text(text)

print("Chunks:", len(chunks))

# 3. Save to vector DB
add_chunks(chunks)

# 4. Test search
query = "شرایط دریافت وام مسکن چیست؟"

results = search(query)

print("\nTop Results:\n")
for r in results:
    print(r)
    print("-" * 50)