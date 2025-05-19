@echo off
REM Windows batch script to install the RAG database in the Docker container

echo ===== Creating RAG Database in Docker Container =====

REM Make sure Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Find the container ID
for /f "tokens=*" %%i in ('docker ps ^| findstr farmlore-web') do (
    set CONTAINER_LINE=%%i
    goto :found_container
)

echo ERROR: Farmlore web container is not running. Please start it first.
exit /b 1

:found_container
for /f "tokens=1" %%i in ("%CONTAINER_LINE%") do set CONTAINER_ID=%%i
echo Found container ID: %CONTAINER_ID%

REM Make sure the rag_database_creator.py exists
if not exist ".\rag_database_creator.py" (
    echo ERROR: rag_database_creator.py not found.
    exit /b 1
)

REM Copy the database creator script to the container
echo Copying rag_database_creator.py to container...
docker cp .\rag_database_creator.py %CONTAINER_ID%:/app/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy rag_database_creator.py to container.
    exit /b 1
)
echo Successfully copied rag_database_creator.py to container.

REM Make the script executable
echo Making script executable...
docker exec %CONTAINER_ID% chmod +x /app/rag_database_creator.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to make rag_database_creator.py executable.
    exit /b 1
)
echo Successfully made script executable.

REM Install required packages
echo Installing required packages...
docker exec %CONTAINER_ID% pip install langchain-text-splitters langchain-core
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required packages.
    exit /b 1
)
echo Successfully installed required packages.

REM Run the database creator script
echo Creating RAG database...
docker exec %CONTAINER_ID% bash -c "cd /app && python /app/rag_database_creator.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create RAG database.
    exit /b 1
)
echo Successfully created RAG database.

REM Restart the web service
echo Restarting web service...
for /f "tokens=*" %%i in ('docker exec %CONTAINER_ID% ps aux ^| findstr "python manage.py runserver" ^| findstr /v grep') do (
    for /f "tokens=2" %%j in ("%%i") do (
        docker exec %CONTAINER_ID% kill -9 %%j 2>nul
    )
)
docker exec -d %CONTAINER_ID% bash -c "cd /app && python manage.py runserver 0.0.0.0:8000"
echo Web service restarted.

echo ===== RAG Database Creation Complete! =====
echo You can now test the RAG integration with queries related to pest management.
echo Try a query like: 'How do I control aphids on tomatoes?' 