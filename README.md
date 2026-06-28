<!-- ===================================================== -->
<!-- HEADER -->
<!-- ===================================================== -->

<p align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=220&section=header&text=RAG%20Banking%20Assistant&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Retrieval-Augmented%20Generation%20•%20FastAPI%20•%20ChromaDB%20•%20MLflow&descAlignY=62&descSize=16&descColor=a78bfa"/>
</p>

<h1 align="center">
🏦 RAG Banking Assistant
</h1>

<p align="center">
Production-ready Retrieval-Augmented Generation (RAG) system for banking documents powered by FastAPI, ChromaDB, MLflow and Docker.
</p>

<p align="center">

<a href="https://python.org">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</a>

<a href="https://fastapi.tiangolo.com">
<img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
</a>

<a href="https://streamlit.io">
<img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
</a>

<a href="https://trychroma.com">
<img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-7C3AED?style=for-the-badge"/>
</a>

<a href="https://mlflow.org">
<img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
</a>

<a href="https://docker.com">
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</a>

<img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>

</p>

---

## 📌 Overview

**RAG Banking Assistant** is a production-ready Retrieval-Augmented Generation system designed for banking knowledge bases.

Instead of relying solely on an LLM, the assistant retrieves relevant banking documents from a vector database before generating answers, ensuring higher accuracy, transparency, and grounded responses.

---

## ✨ Features

| Feature | Description |
|----------|-------------|
| 🔐 JWT Authentication | Secure API endpoints |
| 📄 PDF Ingestion | Automatic chunking & preprocessing |
| 🔍 Semantic Search | Vector similarity search with ChromaDB |
| 🤖 RAG Pipeline | Context-aware response generation |
| 📊 MLflow | Experiment tracking |
| 🖥 Streamlit | Interactive chat UI |
| 🐳 Docker | One-command deployment |
| 📈 Monitoring | Prometheus & Grafana |
| ⚡ Redis Cache | Faster retrieval |
| 📝 Logging | Structured logs |



---

# 📂 Project Structure

```text
rag-banking-assistant/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── pipeline.py
│   │   └── generator.py
│   │
│   ├── models/
│   │
│   └── main.py
│
├── chromadb/
├── streamlit/
├── scripts/
├── monitoring/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Quick Start

## Clone Repository

```bash
git clone https://github.com/SobhanAlizadeh/rag-banking-assistant.git

cd rag-banking-assistant
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

```bash
cp .env.example .env
```

Edit the environment variables before running the application.

---

# 📥 Document Ingestion

Before using the assistant, your banking documents must be indexed into ChromaDB.

```bash
python scripts/ingest.py
```

The ingestion pipeline performs:

- 📄 PDF loading
- ✂️ Smart text chunking
- 🧠 Embedding generation
- 🗂 Vector indexing into ChromaDB
- 💾 Persistent storage

---

# ▶️ Running the Application

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

Application:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Start Streamlit

```bash
streamlit run streamlit/chat_app.py
```

Default URL

```
http://localhost:8501
```

---

# 🐳 Docker Deployment

Build all services

```bash
docker compose up --build
```

Run in background

```bash
docker compose up -d
```

Stop containers

```bash
docker compose down
```

Rebuild

```bash
docker compose up --build --force-recreate
```

---

# 🧠 MLflow Tracking

Start only MLflow

```bash
docker compose up -d mlflow
```

Open

```
http://localhost:5000
```

Track:

- Parameters
- Metrics
- Artifacts
- Experiments
- Models

Example

```python
import mlflow

with mlflow.start_run():

    mlflow.log_param("chunk_size",512)

    mlflow.log_metric("accuracy",0.94)
```

---

# ⚡ Redis Cache

Redis is used for:

- Session cache
- Prompt cache
- Response cache
- Query history
- Rate limiting

Run

```bash
docker compose up -d redis
```

Verify

```bash
docker ps
```

---

# 📈 Monitoring

Monitoring stack includes

- Prometheus
- Grafana

Start

```bash
docker compose up -d prometheus grafana
```

Access

Prometheus

```
http://localhost:9090
```

Grafana

```
http://localhost:3000
```

Default credentials

```
admin
admin
```

---

# 🔐 Authentication

Every protected endpoint requires a JWT token.

Example

```
Authorization:
Bearer YOUR_ACCESS_TOKEN
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /login | User authentication |
| POST | /register | Create user |
| POST | /ask | Ask questions |
| POST | /ingest | Upload new documents |
| GET | /health | Health check |
| GET | /metrics | Prometheus metrics |

---

# ⚙️ Environment Variables

Example

```env
APP_NAME=RAG Banking Assistant

DEBUG=True

SECRET_KEY=YOUR_SECRET_KEY

JWT_EXPIRE_MINUTES=60

OPENAI_API_KEY=YOUR_KEY

MODEL_NAME=gpt-4o-mini

CHROMA_DB=chromadb

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

REDIS_HOST=redis

REDIS_PORT=6379

MLFLOW_TRACKING_URI=http://mlflow:5000
```

---

# 🧪 Running Tests

Execute all tests

```bash
pytest
```

Verbose

```bash
pytest -v
```

Coverage

```bash
pytest --cov=app
```

Generate HTML report

```bash
pytest --cov=app --cov-report=html
```

---

# 📊 Example Request

```bash
curl -X POST http://localhost:8000/ask \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "question":"What is the minimum balance for a savings account?"
}'
```

---

# 📦 Docker Services

| Service | Port |
|----------|------|
| FastAPI | 8000 |
| Streamlit | 8501 |
| MLflow | 5000 |
| Redis | 6379 |
| Prometheus | 9090 |
| Grafana | 3000 |

---

# 🧰 Tech Stack

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/ChromaDB-7C3AED?style=for-the-badge"/>

<img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge"/>

<img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>

<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>

<img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white"/>

<img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white"/>

</p>

---

# ⚠️ Troubleshooting

### ChromaDB is empty

```bash
python scripts/ingest.py
```

---

### Redis connection failed

Check

```bash
docker ps
```

Verify Redis is running.

---

### MLflow unavailable

Run

```bash
docker compose up -d mlflow
```

---

### API returns 401

Your JWT token has expired.

Authenticate again.

---

### Docker build failed

Rebuild

```bash
docker compose build --no-cache
```

---

# 📊 GitHub Stats

<p align="center">

<img src="https://github-readme-stats.vercel.app/api?username=SobhanAlizadeh&show_icons=true&theme=tokyonight" height="160"/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=SobhanAlizadeh&theme=tokyonight" height="160"/>

</p>

<p align="center">

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=SobhanAlizadeh&layout=compact&theme=tokyonight"/>

</p>

---

# 🗺️ Roadmap

- [x] RAG pipeline with ChromaDB
- [x] FastAPI backend
- [x] Streamlit UI
- [x] JWT Authentication
- [x] Docker support
- [x] MLflow tracking
- [x] Redis caching
- [x] Kubernetes deployment
- [ ] Multi-LLM support (OpenAI, Claude, Local LLMs)
- [ ] Role-based access control (RBAC)
- [ ] Multi-language answers (FA / EN / AR)
- [ ] Advanced reranking model


---

# 🤝 Contributing

We welcome contributions!

### Steps

```bash
# 1. Fork the repo
# 2. Clone your fork
git clone https://github.com/SobhanAlizadeh/rag-banking-assistant.git

# 3. Create a branch
git checkout -b feature/new-feature

# 4. Commit changes
git commit -m "Add new feature"

# 5. Push
git push origin feature/new-feature
```

Then open a Pull Request 🚀

---

# 📜 License

This project is licensed under the MIT License.

```
MIT License © 2026 Sobhan Alizadeh
```

---

# 👨‍💻 Author

<p align="center">

<img src="https://github.com/SobhanAlizadeh.png" width="120" style="border-radius:50%"/>

</p>

<h2 align="center">Sobhan Alizadeh</h2>

<p align="center">
AI Engineer · Builder of Intelligent Systems · RAG & LLM Enthusiast
</p>

<p align="center">

<a href="https://github.com/SobhanAlizadeh">
<img src="https://img.shields.io/badge/GitHub-SobhanAlizadeh-181717?style=for-the-badge&logo=github"/>
</a>

<a href="https://linkedin.com/in/sobhan-alizadeh">
<img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin"/>
</a>

</p>

---

# 🚀 Future Improvements

- Vector DB migration to Weaviate / Pinecone
- GPU-accelerated embeddings
- Streaming responses (SSE / WebSocket)
- Fine-tuned banking LLM
- Document OCR support
- Audit logging system
- Enterprise RBAC + SSO

---

# 🙏 Acknowledgements

Special thanks to:

- OpenAI for LLM APIs
- FastAPI team
- ChromaDB team
- MLflow project
- Open-source community ❤️





<p align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer&text=Built%20with%20Passion%20🚀&fontSize=24&fontColor=ffffff"/>

