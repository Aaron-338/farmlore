@echo off
REM Windows batch script to run the install_rag_docker_wrapper.sh for RAG integration

echo ===== Installing RAG with Direct Query Wrapper =====

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if the Docker container is running
for /f "tokens=*" %%i in ('docker ps ^| findstr farmlore-web') do (
    set CONTAINER_FOUND=true
)

if not defined CONTAINER_FOUND (
    echo ERROR: Farmlore web container is not running. Please start it first.
    exit /b 1
)

REM Make sure the docker_query_wrapper.py exists
if not exist ".\docker_query_wrapper.py" (
    echo ERROR: docker_query_wrapper.py not found.
    exit /b 1
)

REM Run the shell script using Git Bash if available
where bash >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Running installation using Bash...
    bash ./install_rag_docker_wrapper.sh
    goto end
)

REM If Git Bash is not available, try running in WSL
where wsl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Running installation using WSL...
    wsl ./install_rag_docker_wrapper.sh
    goto end
)

REM If neither is available, run the Docker commands directly
echo Running installation directly with Docker commands...

REM Get the container ID
for /f "tokens=1" %%i in ('docker ps ^| findstr farmlore-web') do (
    set CONTAINER_ID=%%i
)

echo Found container ID: %CONTAINER_ID%

REM Copy files to the container
echo Copying docker_query_wrapper.py to container...
docker cp .\docker_query_wrapper.py %CONTAINER_ID%:/app/api/inference_engine/

REM Create the start_web_rag.sh script
echo Creating start_web_rag.sh script...
(
    echo #!/bin/bash
    echo # Modified startup script that loads the RAG system
    echo.
    echo # Set environment variables for RAG
    echo export USE_RAG=true
    echo export RAG_PERSIST_DIR=/app/data/chromadb
    echo.
    echo # Create RAG data directory if it doesn't exist
    echo mkdir -p /app/data/chromadb
    echo.
    echo # First, apply the RAG wrapper to enhance the HybridEngine
    echo echo "Applying RAG wrapper to HybridEngine..."
    echo python3 /app/api/inference_engine/docker_query_wrapper.py
    echo.
    echo # Then start the web server as usual
    echo echo "Starting Django server..."
    echo cd /app
    echo python manage.py runserver 0.0.0.0:8000
) > start_web_rag.sh

REM Copy the startup script to the container
echo Copying start_web_rag.sh to container...
docker cp .\start_web_rag.sh %CONTAINER_ID%:/app/

REM Make the script executable
echo Making start_web_rag.sh executable...
docker exec %CONTAINER_ID% chmod +x /app/start_web_rag.sh

REM Install required packages in the container
echo Installing required packages for RAG in container...
docker exec %CONTAINER_ID% pip install langchain-community huggingface_hub sentence-transformers chromadb

REM Test the RAG wrapper
echo Testing RAG wrapper...
docker exec %CONTAINER_ID% python3 /app/api/inference_engine/docker_query_wrapper.py

REM Restart the web service
echo Restarting web service with RAG integration...
docker exec -d %CONTAINER_ID% pkill -f "python manage.py runserver"
docker exec -d %CONTAINER_ID% /app/start_web_rag.sh

echo.
echo ===== RAG installation with direct query wrapper complete! =====
echo The system will now use RAG to enhance query responses.
echo Please test the system by asking a question related to your knowledge base.

:end 