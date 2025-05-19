@echo off
REM Windows batch script to install the simple RAG database in the Docker container

echo ===== Creating Simple RAG Database in Docker Container =====

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

REM Make sure the simple_rag_db_creator.py exists
if not exist ".\simple_rag_db_creator.py" (
    echo ERROR: simple_rag_db_creator.py not found.
    exit /b 1
)

REM Copy the database creator script to the container
echo Copying simple_rag_db_creator.py to container...
docker cp .\simple_rag_db_creator.py %CONTAINER_ID%:/app/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy simple_rag_db_creator.py to container.
    exit /b 1
)
echo Successfully copied simple_rag_db_creator.py to container.

REM Make the script executable
echo Making script executable...
docker exec %CONTAINER_ID% chmod +x /app/simple_rag_db_creator.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to make simple_rag_db_creator.py executable.
    exit /b 1
)
echo Successfully made script executable.

REM Install required packages
echo Installing required packages...
docker exec %CONTAINER_ID% pip install chromadb sentence-transformers
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install required packages.
    exit /b 1
)
echo Successfully installed required packages.

REM Run the database creator script
echo Creating RAG database...
docker exec %CONTAINER_ID% bash -c "cd /app && python /app/simple_rag_db_creator.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create RAG database.
    exit /b 1
)
echo Successfully created RAG database.

REM Create direct query script
echo Creating direct query script...
echo #!/usr/bin/env python > direct_rag_query.py
echo """>> direct_rag_query.py
echo Direct RAG Query Script>> direct_rag_query.py
echo. >> direct_rag_query.py
echo Query the RAG database directly and test its functionality.>> direct_rag_query.py
echo """>> direct_rag_query.py
echo import os>> direct_rag_query.py
echo import json>> direct_rag_query.py
echo import logging>> direct_rag_query.py
echo from typing import List, Dict, Any>> direct_rag_query.py
echo. >> direct_rag_query.py
echo # Configure logging>> direct_rag_query.py
echo logging.basicConfig(>> direct_rag_query.py
echo     level=logging.INFO,>> direct_rag_query.py
echo     format='%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s'>> direct_rag_query.py
echo )>> direct_rag_query.py
echo logger = logging.getLogger("direct_rag_query")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo def query_rag_database(query_text: str, persist_dir: str = "./data/chromadb", n_results: int = 3) -^> List[Dict[str, Any]]:>> direct_rag_query.py
echo     """Query the RAG database directly""">> direct_rag_query.py
echo     try:>> direct_rag_query.py
echo         # Import necessary libraries>> direct_rag_query.py
echo         import chromadb>> direct_rag_query.py
echo         from sentence_transformers import SentenceTransformer>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Check if directory exists>> direct_rag_query.py
echo         if not os.path.exists(persist_dir):>> direct_rag_query.py
echo             logger.error(f"Database directory {persist_dir} does not exist")>> direct_rag_query.py
echo             return []>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Initialize sentence transformer model>> direct_rag_query.py
echo         model = SentenceTransformer("all-MiniLM-L6-v2")>> direct_rag_query.py
echo         logger.info("Initialized sentence transformer model")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Initialize ChromaDB client>> direct_rag_query.py
echo         client = chromadb.PersistentClient(path=persist_dir)>> direct_rag_query.py
echo         logger.info(f"Connected to ChromaDB at {persist_dir}")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Get collection>> direct_rag_query.py
echo         collection = client.get_collection(name="pest_management")>> direct_rag_query.py
echo         logger.info("Connected to pest_management collection")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Generate embedding for query>> direct_rag_query.py
echo         query_embedding = model.encode(query_text).tolist()>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Query the collection>> direct_rag_query.py
echo         results = collection.query(>> direct_rag_query.py
echo             query_embeddings=[query_embedding],>> direct_rag_query.py
echo             n_results=n_results>> direct_rag_query.py
echo         )>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         # Format results>> direct_rag_query.py
echo         formatted_results = []>> direct_rag_query.py
echo         if results and results['documents'] and len(results['documents'][0]) ^> 0:>> direct_rag_query.py
echo             for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):>> direct_rag_query.py
echo                 formatted_results.append({>> direct_rag_query.py
echo                     "text": doc,>> direct_rag_query.py
echo                     "title": metadata.get("title", "Unknown"),>> direct_rag_query.py
echo                     "similarity": results['distances'][0][i] if 'distances' in results else None>> direct_rag_query.py
echo                 })>> direct_rag_query.py
echo. >> direct_rag_query.py
echo         return formatted_results>> direct_rag_query.py
echo. >> direct_rag_query.py
echo     except Exception as e:>> direct_rag_query.py
echo         logger.error(f"Error querying RAG database: {str(e)}")>> direct_rag_query.py
echo         import traceback>> direct_rag_query.py
echo         logger.error(traceback.format_exc())>> direct_rag_query.py
echo         return []>> direct_rag_query.py
echo. >> direct_rag_query.py
echo if __name__ == "__main__":>> direct_rag_query.py
echo     print("=== Direct RAG Query Test ===")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo     # Get persistence directory from environment or use default>> direct_rag_query.py
echo     persist_dir = os.environ.get("RAG_PERSIST_DIR", "./data/chromadb")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo     # Sample query>> direct_rag_query.py
echo     query = "How do I control aphids on tomatoes?">> direct_rag_query.py
echo     print(f"Querying: '{query}'")>> direct_rag_query.py
echo. >> direct_rag_query.py
echo     # Get results>> direct_rag_query.py
echo     results = query_rag_database(query, persist_dir)>> direct_rag_query.py
echo. >> direct_rag_query.py
echo     if results:>> direct_rag_query.py
echo         print(f"✅ Found {len(results)} relevant results:")>> direct_rag_query.py
echo         for i, result in enumerate(results, 1):>> direct_rag_query.py
echo             print(f"\nResult {i} - {result['title']}:")>> direct_rag_query.py
echo             print(f"Snippet: {result['text'][:200]}...")>> direct_rag_query.py
echo     else:>> direct_rag_query.py
echo         print("❌ No results found.")>> direct_rag_query.py

echo Copying direct query script to container...
docker cp .\direct_rag_query.py %CONTAINER_ID%:/app/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy direct_rag_query.py to container.
    exit /b 1
)
echo Successfully copied direct_rag_query.py to container.

REM Make the query script executable
echo Making query script executable...
docker exec %CONTAINER_ID% chmod +x /app/direct_rag_query.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to make direct_rag_query.py executable.
    exit /b 1
)
echo Successfully made query script executable.

REM Test querying the RAG database
echo Testing RAG database queries...
docker exec %CONTAINER_ID% bash -c "cd /app && python /app/direct_rag_query.py"

echo ===== Simple RAG Database Creation Complete! =====
echo You can now integrate the RAG database with your application.
echo Use direct_rag_query.py as a reference for making queries to the RAG database. 