# this docker file is for dockerizing for whole project
FROM python:3.10-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

# Set working directory
WORKDIR /app

# System dependencies (e.g., LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy code and install dependencies
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Run training pipeline (now it will find src/)
RUN python pipeline/training_pipeline.py

EXPOSE 5000