#!/bin/bash

set -e # exit immediately if any command fails

echo "[1/5] Creating Docker network (if not exists)..."
docker network inspect app-net >/dev/null 2>&1 || docker network create app-net

echo "[2/5] Starting Redis container..."
docker ps -a --format '{{.Names}}' | grep -q '^redis$' && {
  echo "   Redis container already exists. Restarting..."
  docker start redis
} || {
  docker run -d --name redis --network app-net redis:7
}

echo "[3/5] Building FastAPI Docker image..."
docker build -t fastapi-app .

echo "[4/5] Cleaning up old FastAPI container (if exists)..."
docker rm -f fastapi-app 2>/dev/null || true

echo "[5/5] Running FastAPI app on port 8000..."
docker run -d --name fastapi-app \
  --network app-net \
  -p 8000:8000 \
  -v $(pwd)/app.db:/app/app.db \
  fastapi-app

echo "App is running at http://localhost:8000"
