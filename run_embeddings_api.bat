@echo off
echo Building and running embeddings classifier API in Docker...

REM Check if Docker is running
docker info > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker is not running! Please start Docker Desktop and try again.
    exit /b 1
)

REM Build and run with Docker Compose
docker-compose -f docker-compose.embeddings.yml build embeddings-api
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to build Docker images.
    exit /b 1
)

echo.
echo Running embeddings classifier API on port 5001...
echo API will be available at: http://localhost:5001/health
echo.
docker-compose -f docker-compose.embeddings.yml up embeddings-api 