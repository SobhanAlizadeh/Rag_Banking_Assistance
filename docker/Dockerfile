# docker/Dockerfile.api
FROM python:3.11-slim

WORKDIR /app

# نصب وابستگی‌های سیستمی (در صورت نیاز)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های مورد نیاز
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# اجرای ingest در زمان build (اختیاری)
# RUN python scripts/ingest.py

EXPOSE 8000

CMD ["/entrypoint.sh"]