FROM python:3.12-alpine

# For some packages that need compiling (safe for PyMySQL / psycopg[binary])
RUN apk add --no-cache build-base

WORKDIR /workspaces/BACKEND

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source comes from the bind mount; keep image lean
