<div align="center">

<!-- BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=200&section=header&text=RAG%20Banking%20Assistant&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Retrieval-Augmented%20Generation%20%E2%80%A2%20FastAPI%20%E2%80%A2%20ChromaDB%20%E2%80%A2%20MLflow&descAlignY=62&descSize=16&descColor=a78bfa" />

<br/>

<!-- BADGES -->
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-7C3AED?style=for-the-badge&logo=databricks&logoColor=white)](https://trychroma.com)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> **🏦 An intelligent, production-ready RAG pipeline tailored for banking Q&A —**
> **semantic search over your documents, served through a secure API, tracked with MLflow.**

</div>

---

## 🧠 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      USER / CLIENT                          │
│              Streamlit UI  ·  REST API                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
             ┌─────────────▼─────────────┐
             │        FastAPI Backend     │
             │   Auth  ·  Routes  ·  RAG  │
             └──────┬───────────┬─────────┘
                    │           │
         ┌──────────▼──┐  ┌────▼──────────┐
         │  ChromaDB   │  │  LLM / Model  │
         │ Vector Store│  │   Service     │
         └─────────────┘  └───────────────┘
                    │
         ┌──────────▼──────────┐
         │  MLflow Experiment  │
         │      Tracking       │
         └─────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 **Secure Auth** | JWT-based authentication on all API endpoints |
| 📄 **Smart PDF Ingestion** | Intelligent chunking and preprocessing of banking documents |
| 🔍 **Semantic Search** | ChromaDB-powered vector similarity search over your knowledge base |
| 🤖 **RAG Pipeline** | Context-aware answer generation grounded in retrieved documents |
| 📊 **MLflow Tracking** | Full experiment and run tracking for model evaluation |
| 🖥️ **Streamlit UI** | Lightweight chat interface for local demos and testing |
| 🐳 **Docker Ready** | One-command deployment with Docker Compose |

---

## 📁 Project Structure

```
rag-banking-assistant/
│
├── 📂 app/                    # Core application logic
│   ├── 📂 api/
│   │   ├── routes.py          # API endpoints
│   │   └── auth.py            # Authentication
│   ├── 📂 core/               # Logging & configuration
│   ├── 📂 rag/                # RAG engine: search, index, load
│   ├── 📂 model/              # Model files & weights
│   └── main.py                # FastAPI entrypoint
│
├── 📂 streamlit/
│   └── chat_app.py            # Local chat UI
│
├── 📂 chromadb/               # Persistent vector database
├── 📂 scripts/
│   └── ingest.py              # Document ingestion script
├── 📂 tests/                  # Unit & API tests
├── 📂 monitoring/             # Prometheus / Grafana configs
├── docker-compose.yml
├── requirements.txt
└── .envv.example
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Docker & Docker Compose** *(for containerized runs)*

---

### 1 · Clone & Set Up Environment

```bash
git clone https://github.com/SobhanAlizadeh/rag-banking-assistant.git
cd rag-banking-assistant

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2 · Configure Environment Variables

```bash
cp .envv.example .envv
# Edit .envv and fill in your API keys, model paths, and service addresses
```

### 3 · Ingest Documents

```bash
# Make sure chromadb/ directory is writable
python scripts/ingest.py
```

### 4 · Run the Services

<table>
<tr>
<td><b>API only (local)</b></td>
<td>

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

</td>
</tr>
<tr>
<td><b>Streamlit UI</b></td>
<td>

```bash
streamlit run streamlit/chat_app.py
```

</td>
</tr>
<tr>
<td><b>Full stack (Docker)</b></td>
<td>

```bash
docker compose up --build
```

</td>
</tr>
</table>

---

## 📊 MLflow Experiment Tracking

```bash
# Start MLflow as a container
docker compose up -d mlflow
```

Open the MLflow UI at **`http://localhost:5000`** to view runs, metrics, and artifacts.

---

## 🧪 Testing & Troubleshooting

```bash
pytest tests/
```

<details>
<summary><b>⚠️ Common Issues</b></summary>

<br/>

**ChromaDB is empty**
> Run `python scripts/ingest.py` before starting the server. Ensure the `chromadb/` folder is accessible and writable.

**Redis connection error**
> Check your Redis service is running and that the host/port in `.envv` matches.

**Model files missing or too large**
> Confirm files exist under `app/model/` and that you have sufficient disk space. Verify all paths in `.envv` are correct.

</details>

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/-ChromaDB-7C3AED?style=flat-square&logo=databricks&logoColor=white)
![MLflow](https://img.shields.io/badge/-MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Prometheus](https://img.shields.io/badge/-Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/-Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)

</div>

---

## 🤝 Contributing

PRs are welcome! Please follow these steps:

1. **Open an issue** describing the feature or bug
2. **Branch off** `main` with a descriptive name
3. **Add tests** and update documentation
4. **Submit a PR** — we'll review it promptly

---

## 👨‍💻 Author

<div align="center">

<img src="https://github.com/SobhanAlizadeh.png" width="96" style="border-radius:50%" alt="Sobhan Alizadeh"/>

**Sobhan Alizadeh**
*AI Engineer · Builder of intelligent systems*

[![GitHub](https://img.shields.io/badge/GitHub-SobhanAlizadeh-181717?style=for-the-badge&logo=github)](https://github.com/SobhanAlizadeh)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sobhan--alizadeh-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sobhan-alizadeh/)

</div>

---

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=100&section=footer" />

*Built with ❤️ for the AI Engineering community*

</div>