# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bookworm

# نصب وابستگی‌های سیستم برای psycopg2 و ابزارهای مفید
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        redis-tools \
        curl \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# نصب MinIO Client (mc)
RUN curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
    && chmod +x mc \
    && mv mc /usr/local/bin/mc

# نصب پکیج‌های پایتون
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

# ایجاد باکت MinIO به‌صورت خودکار هنگام اولین اجرا
RUN echo '#!/bin/bash\n\
mc alias set myminio http://minio:9000 minioadmin minioadmin --api S3v4\n\
mc mb myminio/mybucket --ignore-existing || true\n\
mc anonymous set download myminio/mybucket || true\n\
' > /usr/local/bin/create-minio-bucket.sh && chmod +x /usr/local/bin/create-minio-bucket.sh

WORKDIR /workspace