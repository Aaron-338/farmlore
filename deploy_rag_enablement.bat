@echo off
REM Deploy RAG enablement to Docker container

REM Set variables
set CONTAINER_NAME=farmlore-web-1
set SCRIPT_FILE=enable_rag.py
set CONTAINER_PATH=/app/

echo Deploying RAG enablement to Docker container...

REM Check if the container is running
docker ps | findstr %CONTAINER_NAME% >nul 2>&1
if errorlevel 1 (
  echo Error: Container %CONTAINER_NAME% is not running.
  echo Please make sure the container is running before deploying the fix.
  exit /b 1
)

REM Copy the script to the container
echo Copying RAG enablement script to container...
docker cp %SCRIPT_FILE% %CONTAINER_NAME%:%CONTAINER_PATH%

REM Execute the script in the container
echo Executing the RAG enablement script in the container...
docker exec %CONTAINER_NAME% python /app/enable_rag.py

REM Check if the script executed successfully
if errorlevel 1 (
  echo Error: The RAG enablement script failed to execute successfully.
  exit /b 1
)

REM Restart the container to ensure changes take effect
echo Restarting the container to ensure changes take effect...
docker restart %CONTAINER_NAME%

echo Waiting for container to restart (15 seconds)...
timeout /t 15 /nobreak

echo.
echo =========================================================
echo RAG enablement deployment complete! Container has been restarted.
echo.
echo To test the RAG functionality, try sending pest management queries:
echo   - "How do I control aphids on roses?"
echo   - "What are natural predators for aphids?"
echo.
echo You should now see "source": "rag_ollama" in responses
echo and logs showing "Querying RAG system for pest management knowledge..."
echo ========================================================= 