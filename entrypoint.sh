#!/bin/bash
set -e

# مسیر دیتابیس (همان مسیری که در کد استفاده شده)
DB_PATH="/app/chromadb"

# اگر دیتابیس وجود ندارد یا خالی است، ingest را اجرا کن
if [ ! -d "$DB_PATH" ] || [ -z "$(ls -A $DB_PATH)" ]; then
    echo "📦 ChromaDB database is empty or missing. Running ingest script..."
    python scripts/ingest.py
else
    echo "✅ ChromaDB database already exists. Skipping ingest."
fi

# سپس اجرای uvicorn
echo "🚀 Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000