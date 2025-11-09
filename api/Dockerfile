FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential default-libmysqlclient-dev pkg-config curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy (empty for now, but directory must exist)
COPY app ./app

# Non-root (optional)
RUN useradd -m appuser
USER appuser

EXPOSE 8000
