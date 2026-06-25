from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.vectorstore import add_chunks

PDF_PATH = "data/pdfs/Cornell University Library.pdf"

def main():

    print("Loading PDF...")

    text = load_pdf(PDF_PATH)

    print(f"Characters: {len(text):,}")

    print("Chunking...")

    chunks = chunk_text(text)

    print(f"Chunks: {len(chunks):,}")

    print("Building vector database...")

    add_chunks(chunks)

    print("Done ✅")


if __name__ == "__main__":
    main()