@echo off
REM Windows batch script to install the direct RAG integration in the Docker container

echo ===== Installing Direct RAG Integration =====

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

REM Make sure the direct_rag_integration.py exists
if not exist ".\direct_rag_integration.py" (
    echo ERROR: direct_rag_integration.py not found.
    exit /b 1
)

REM Copy the integration file to the container
echo Copying direct_rag_integration.py to container...
docker cp .\direct_rag_integration.py %CONTAINER_ID%:/app/api/inference_engine/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy direct_rag_integration.py to container.
    exit /b 1
)
echo Successfully copied direct_rag_integration.py to container.

REM Create the integration script
echo Creating HybridEngine patch script...
echo #!/usr/bin/env python > hybrid_engine_integrator.py
echo """>> hybrid_engine_integrator.py
echo HybridEngine RAG Integrator>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo This script patches the HybridEngine class to use the Direct RAG integration.>> hybrid_engine_integrator.py
echo """>> hybrid_engine_integrator.py
echo import os>> hybrid_engine_integrator.py
echo import sys>> hybrid_engine_integrator.py
echo import logging>> hybrid_engine_integrator.py
echo import importlib>> hybrid_engine_integrator.py
echo from types import MethodType>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo # Configure logging>> hybrid_engine_integrator.py
echo logging.basicConfig(>> hybrid_engine_integrator.py
echo     level=logging.INFO,>> hybrid_engine_integrator.py
echo     format='%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s'>> hybrid_engine_integrator.py
echo )>> hybrid_engine_integrator.py
echo logger = logging.getLogger("hybrid_engine_integrator")>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo def patch_hybrid_engine():>> hybrid_engine_integrator.py
echo     """Patch the HybridEngine class with RAG capabilities""">> hybrid_engine_integrator.py
echo     try:>> hybrid_engine_integrator.py
echo         # Import the HybridEngine module>> hybrid_engine_integrator.py
echo         logger.info("Importing HybridEngine module...")>> hybrid_engine_integrator.py
echo         hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")>> hybrid_engine_integrator.py
echo         HybridEngine = hybrid_engine_module.HybridEngine>> hybrid_engine_integrator.py
echo         logger.info("Successfully imported HybridEngine")>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         # Import the direct RAG integration>> hybrid_engine_integrator.py
echo         logger.info("Importing Direct RAG integration...")>> hybrid_engine_integrator.py
echo         direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")>> hybrid_engine_integrator.py
echo         enhance_hybrid_engine_response = direct_rag.enhance_hybrid_engine_response>> hybrid_engine_integrator.py
echo         logger.info("Successfully imported Direct RAG integration")>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         # Create a proxy for the query method>> hybrid_engine_integrator.py
echo         def patched_query(self, query_type, **params):>> hybrid_engine_integrator.py
echo             """Patched query method that enhances responses with RAG""">> hybrid_engine_integrator.py
echo             logger.info(f"Patched HybridEngine.query called with type: {query_type}")>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo             # Call the original query method>> hybrid_engine_integrator.py
echo             original_response = self._original_query(query_type, **params)>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo             # Enhance the response with RAG>> hybrid_engine_integrator.py
echo             enhanced_response = enhance_hybrid_engine_response(self, params, original_response)>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo             logger.info("Processed query with RAG enhancement")>> hybrid_engine_integrator.py
echo             return enhanced_response>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         # Get a reference to the original query method>> hybrid_engine_integrator.py
echo         original_query = HybridEngine.query>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         # Patch the HybridEngine class>> hybrid_engine_integrator.py
echo         logger.info("Patching HybridEngine.query method...")>> hybrid_engine_integrator.py
echo         HybridEngine._original_query = original_query>> hybrid_engine_integrator.py
echo         HybridEngine.query = patched_query>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         # Test the patch with a simple instance>> hybrid_engine_integrator.py
echo         logger.info("Creating test HybridEngine instance...")>> hybrid_engine_integrator.py
echo         engine = HybridEngine()>> hybrid_engine_integrator.py
echo         engine.rag_integration_active = True>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo         logger.info("Successfully patched HybridEngine with RAG capabilities")>> hybrid_engine_integrator.py
echo         return True>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo     except Exception as e:>> hybrid_engine_integrator.py
echo         logger.error(f"Error patching HybridEngine: {str(e)}")>> hybrid_engine_integrator.py
echo         import traceback>> hybrid_engine_integrator.py
echo         logger.error(traceback.format_exc())>> hybrid_engine_integrator.py
echo         return False>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo if __name__ == "__main__":>> hybrid_engine_integrator.py
echo     success = patch_hybrid_engine()>> hybrid_engine_integrator.py
echo. >> hybrid_engine_integrator.py
echo     if success:>> hybrid_engine_integrator.py
echo         print("✅ Successfully patched HybridEngine with Direct RAG integration")>> hybrid_engine_integrator.py
echo         sys.exit(0)>> hybrid_engine_integrator.py
echo     else:>> hybrid_engine_integrator.py
echo         print("❌ Failed to patch HybridEngine")>> hybrid_engine_integrator.py
echo         sys.exit(1)>> hybrid_engine_integrator.py

echo Copying HybridEngine patch script to container...
docker cp .\hybrid_engine_integrator.py %CONTAINER_ID%:/app/api/inference_engine/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy hybrid_engine_integrator.py to container.
    exit /b 1
)
echo Successfully copied hybrid_engine_integrator.py to container.

REM Make the scripts executable
echo Making scripts executable...
docker exec %CONTAINER_ID% chmod +x /app/api/inference_engine/direct_rag_integration.py /app/api/inference_engine/hybrid_engine_integrator.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to make scripts executable.
    exit /b 1
)
echo Successfully made scripts executable.

REM Create test script
echo Creating test script...
echo #!/usr/bin/env python > test_direct_rag.py
echo """>> test_direct_rag.py
echo Test Direct RAG Integration>> test_direct_rag.py
echo. >> test_direct_rag.py
echo Run simple tests on the Direct RAG integration.>> test_direct_rag.py
echo """>> test_direct_rag.py
echo import os>> test_direct_rag.py
echo import sys>> test_direct_rag.py
echo import logging>> test_direct_rag.py
echo import importlib>> test_direct_rag.py
echo import json>> test_direct_rag.py
echo. >> test_direct_rag.py
echo # Configure logging>> test_direct_rag.py
echo logging.basicConfig(>> test_direct_rag.py
echo     level=logging.INFO,>> test_direct_rag.py
echo     format='%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s'>> test_direct_rag.py
echo )>> test_direct_rag.py
echo logger = logging.getLogger("test_direct_rag")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo def test_direct_rag_integration():>> test_direct_rag.py
echo     """Test the Direct RAG integration""">> test_direct_rag.py
echo     try:>> test_direct_rag.py
echo         # Import the direct RAG integration>> test_direct_rag.py
echo         logger.info("Importing Direct RAG integration...")>> test_direct_rag.py
echo         direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")>> test_direct_rag.py
echo         logger.info("Successfully imported Direct RAG integration")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         # Test the search function>> test_direct_rag.py
echo         test_query = "How do I control aphids on tomatoes?">> test_direct_rag.py
echo         logger.info(f"Testing search with query: '{test_query}'")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         results = direct_rag.search_pest_data(test_query)>> test_direct_rag.py
echo         if not results:>> test_direct_rag.py
echo             logger.error("Search returned no results")>> test_direct_rag.py
echo             return False>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         logger.info(f"Found {len(results)} results")>> test_direct_rag.py
echo         for i, result in enumerate(results, 1):>> test_direct_rag.py
echo             logger.info(f"Result {i}: {result['title']} (Score: {result['score']:.2f})")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         # Test the enhancement function>> test_direct_rag.py
echo         logger.info("Testing response enhancement...")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         original_response = "Aphids can be controlled using various methods.">> test_direct_rag.py
echo         enhanced_response, results = direct_rag.enhance_response(test_query, original_response)>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         logger.info(f"Original response: {original_response}")>> test_direct_rag.py
echo         logger.info(f"Enhanced response length: {len(enhanced_response)} characters")>> test_direct_rag.py
echo         logger.info(f"Enhancement added {len(enhanced_response) - len(original_response)} characters")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         # Try to import the patched HybridEngine (if it exists)>> test_direct_rag.py
echo         try:>> test_direct_rag.py
echo             logger.info("Checking if HybridEngine is patched...")>> test_direct_rag.py
echo             hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")>> test_direct_rag.py
echo             engine = hybrid_engine_module.HybridEngine()>> test_direct_rag.py
echo. >> test_direct_rag.py
echo             if hasattr(engine, "_original_query") and hasattr(engine, "rag_integration_active"):>> test_direct_rag.py
echo                 logger.info("HybridEngine is successfully patched with RAG integration")>> test_direct_rag.py
echo             else:>> test_direct_rag.py
echo                 logger.info("HybridEngine is not yet patched")>> test_direct_rag.py
echo         except Exception as e:>> test_direct_rag.py
echo             logger.warning(f"Could not check HybridEngine patch status: {str(e)}")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo         return True>> test_direct_rag.py
echo. >> test_direct_rag.py
echo     except Exception as e:>> test_direct_rag.py
echo         logger.error(f"Error testing Direct RAG integration: {str(e)}")>> test_direct_rag.py
echo         import traceback>> test_direct_rag.py
echo         logger.error(traceback.format_exc())>> test_direct_rag.py
echo         return False>> test_direct_rag.py
echo. >> test_direct_rag.py
echo if __name__ == "__main__":>> test_direct_rag.py
echo     print("=== Testing Direct RAG Integration ===")>> test_direct_rag.py
echo. >> test_direct_rag.py
echo     success = test_direct_rag_integration()>> test_direct_rag.py
echo. >> test_direct_rag.py
echo     if success:>> test_direct_rag.py
echo         print("✅ Direct RAG integration is working correctly")>> test_direct_rag.py
echo         sys.exit(0)>> test_direct_rag.py
echo     else:>> test_direct_rag.py
echo         print("❌ Direct RAG integration test failed")>> test_direct_rag.py
echo         sys.exit(1)>> test_direct_rag.py

echo Copying test script to container...
docker cp .\test_direct_rag.py %CONTAINER_ID%:/app/
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy test_direct_rag.py to container.
    exit /b 1
)
echo Successfully copied test_direct_rag.py to container.

REM Make the test script executable
echo Making test script executable...
docker exec %CONTAINER_ID% chmod +x /app/test_direct_rag.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to make test script executable.
    exit /b 1
)
echo Successfully made test script executable.

REM Run the test script
echo Running Direct RAG integration test...
docker exec %CONTAINER_ID% python /app/test_direct_rag.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Direct RAG integration test failed.
    exit /b 1
)
echo Direct RAG integration test passed.

echo ===== Direct RAG Integration Installation Complete! =====
echo You can now apply the patch and restart the server with:
echo docker exec -it %CONTAINER_ID% python /app/api/inference_engine/hybrid_engine_integrator.py
echo. 