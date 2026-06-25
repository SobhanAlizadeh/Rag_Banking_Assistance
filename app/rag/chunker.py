# split text with langchain text splitter and return as list of chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(text):
    spliter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = spliter.split_text(text)
    return chunks