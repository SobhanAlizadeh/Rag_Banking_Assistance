# RAG Banking Assistant

A polished Retrieval-Augmented Generation (RAG) assistant designed for banking-related questions. The system combines FastAPI for the backend, Streamlit for a simple chat interface, Chroma for vector search, and OpenRouter for generating accurate answers from context.

## ✨ Key Features
- Secure chat API with authentication
- PDF ingestion and intelligent chunking
- Semantic search over stored knowledge chunks
- Friendly Streamlit-based user interface
- MLflow integration for tracking experiments and runs

## 🧱 Project Structure
- `app/` — core application logic, auth, RAG modules, schemas, and services
- `api/` — API routes
- `streamlit/` — web-based chat UI
- `scripts/` — document ingestion script
- `tests/` — API, auth, and RAG test coverage
- `docker-compose.yml` — local deployment stack

## 🚀 Getting Started

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment variables
```bash
cp .envv.example .envv
```
Update the file with your API keys and secrets.

### 4) Ingest sample documents
```bash
python scripts/ingest.py
```

## ▶️ Run the Application

### Backend API
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Streamlit UI
```bash
streamlit run streamlit/chat_app.py
```

### Full stack with Docker Compose
```bash
docker compose up --build
```

## 📊 MLflow
Start MLflow locally with:

```bash
docker compose up -d mlflow
```

Then open:
```text
http://localhost:5000
```

If you prefer running it directly on your machine:
```bash
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow_artifacts
```

## ✅ Testing
```bash
pytest tests/
```

---
## 👨‍💻 About the Author
Created by [Sobhan Alizadeh](https://github.com/SobhanAlizadeh)

- GitHub: [https://github.com/SobhanAlizadeh](https://github.com/SobhanAlizadeh)
- LinkedIn: [https://www.linkedin.com/in/sobhan-alizadeh/](https://www.linkedin.com/in/sobhan-alizadeh/)

