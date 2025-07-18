# run.ps1

$ErrorActionPreference = "Stop"  # Exit on error

Write-Host "`n[1/5] Creating Docker network (if not exists)..."
if (-not (docker network ls --format "{{.Name}}" | Select-String -Pattern "^app-net$")) {
    docker network create app-net
}

Write-Host "`n[2/5] Starting Redis container..."
if (docker ps -a --format "{{.Names}}" | Select-String -Pattern "^redis$") {
    Write-Host "   Redis container already exists. Restarting..."
    docker start redis
} else {
    docker run -d --name redis --network app-net redis:7
}

Write-Host "`n[3/5] Building FastAPI Docker image..."
docker build -t fastapi-app .

Write-Host "`n[4/5] Cleaning up old FastAPI container (if exists)..."
try {
    docker rm -f fastapi-app -ErrorAction SilentlyContinue
} catch {}

Write-Host "`n[5/5] Running FastAPI app on port 8000..."
$pwdPath = (Get-Location).Path
docker run -d --name fastapi-app `
  --network app-net `
  -p 8000:8000 `
  -v "${pwdPath}\app.db:/app/app.db" `
  fastapi-app

Write-Host "`nApp is running at http://localhost:8000`n"

