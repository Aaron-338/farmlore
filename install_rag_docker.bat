@echo off
REM Windows batch file for installing RAG in Docker environment

echo ===== FarmLore RAG Docker Installation =====

REM Check if Docker is running
echo Checking Docker status...
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker does not appear to be running. Please start Docker and try again.
    exit /b 1
)

REM Identify container name
echo Identifying container name...
for /f "tokens=1" %%i in ('docker-compose ps ^| findstr web') do set CONTAINER_NAME=%%i

if "%CONTAINER_NAME%"=="" (
    echo Could not find web container. Trying default name 'farmlore_web_1'...
    set CONTAINER_NAME=farmlore_web_1
)

echo Using container name: %CONTAINER_NAME%

REM Check if the container exists
docker ps -a | findstr %CONTAINER_NAME% >nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Container %CONTAINER_NAME% not found. Make sure the FarmLore container is running.
    echo You can start it with: docker-compose up -d
    exit /b 1
)

REM Create RAG requirements file
echo Creating RAG requirements file...
echo # RAG dependencies > requirements_rag_docker.txt
echo langchain==0.1.8 >> requirements_rag_docker.txt
echo langchain-community>=0.0.21 >> requirements_rag_docker.txt
echo langchain-text-splitters>=0.0.1 >> requirements_rag_docker.txt
echo chromadb==0.4.24 >> requirements_rag_docker.txt
echo sentence-transformers==2.5.1 >> requirements_rag_docker.txt
echo huggingface-hub==0.20.3 >> requirements_rag_docker.txt
echo pysbd==0.3.4 >> requirements_rag_docker.txt
echo regex==2023.12.25 >> requirements_rag_docker.txt

REM Copy files to container
echo Copying RAG implementation files to container...
docker cp implement_rag.py %CONTAINER_NAME%:/app/api/inference_engine/
docker cp add_rag_to_hybrid_engine.py %CONTAINER_NAME%:/app/
docker cp initialize_rag.py %CONTAINER_NAME%:/app/
docker cp start_web_rag.sh %CONTAINER_NAME%:/app/
docker cp requirements_rag_docker.txt %CONTAINER_NAME%:/app/requirements_rag.txt

REM Install dependencies in container
echo Installing RAG dependencies in container...
docker exec %CONTAINER_NAME% pip install -r /app/requirements_rag.txt

REM Create helper script for container
echo Creating setup script for container...
echo import os > run_in_container.py
echo import sys >> run_in_container.py
echo import logging >> run_in_container.py
echo. >> run_in_container.py
echo logging.basicConfig(level=logging.INFO) >> run_in_container.py
echo logger = logging.getLogger("rag_setup") >> run_in_container.py
echo. >> run_in_container.py
echo def setup_rag_in_container(): >> run_in_container.py
echo     """Set up RAG inside the container""" >> run_in_container.py
echo     sys.path.append('/app') >> run_in_container.py
echo. >> run_in_container.py
echo     try: >> run_in_container.py
echo         # Set environment variables >> run_in_container.py
echo         os.environ['USE_RAG'] = 'true' >> run_in_container.py
echo         os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb' >> run_in_container.py
echo. >> run_in_container.py
echo         # Create necessary directories >> run_in_container.py
echo         os.makedirs('/app/data/chromadb', exist_ok=True) >> run_in_container.py
echo         logger.info("Created data directory: /app/data/chromadb") >> run_in_container.py
echo. >> run_in_container.py
echo         # Initialize RAG >> run_in_container.py
echo         logger.info("Initializing RAG...") >> run_in_container.py
echo         from initialize_rag import initialize_rag >> run_in_container.py
echo         success = initialize_rag() >> run_in_container.py
echo         logger.info(f"RAG initialization: {'SUCCESS' if success else 'FAILED'}") >> run_in_container.py
echo. >> run_in_container.py
echo         # Add RAG to HybridEngine >> run_in_container.py
echo         logger.info("Extending HybridEngine with RAG...") >> run_in_container.py
echo         from add_rag_to_hybrid_engine import add_rag_to_hybrid_engine >> run_in_container.py
echo         rag_success = add_rag_to_hybrid_engine() >> run_in_container.py
echo         logger.info(f"RAG integration: {'SUCCESS' if rag_success else 'FAILED'}") >> run_in_container.py
echo. >> run_in_container.py
echo         return success and rag_success >> run_in_container.py
echo     except Exception as e: >> run_in_container.py
echo         logger.error(f"Error setting up RAG: {str(e)}") >> run_in_container.py
echo         return False >> run_in_container.py
echo. >> run_in_container.py
echo if __name__ == "__main__": >> run_in_container.py
echo     print("=== RAG Setup Inside Container ===") >> run_in_container.py
echo     success = setup_rag_in_container() >> run_in_container.py
echo     print(f"RAG setup: {'SUCCESSFUL' if success else 'FAILED'}") >> run_in_container.py
echo     sys.exit(0 if success else 1) >> run_in_container.py

REM Run setup inside the container
echo Running setup inside the container...
docker cp run_in_container.py %CONTAINER_NAME%:/app/
docker exec %CONTAINER_NAME% python /app/run_in_container.py

REM Done
echo ===== RAG Installation Complete =====
echo To restart the container with RAG enabled, run: docker-compose restart web
echo Then check logs with: docker-compose logs -f web 