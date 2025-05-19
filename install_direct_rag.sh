#!/bin/bash
# Script to install the direct RAG integration in the Docker container

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Installing Direct RAG Integration =====${NC}"

# Make sure the Docker container is running
CONTAINER_ID=$(docker ps | grep farmlore-web | awk '{print $1}')
if [ -z "$CONTAINER_ID" ]; then
    echo -e "${RED}Error: Farmlore web container is not running. Please start it first.${NC}"
    exit 1
fi

echo -e "${BLUE}Found container ID: ${CONTAINER_ID}${NC}"

# Make sure the direct_rag_integration.py exists
if [ ! -f "./direct_rag_integration.py" ]; then
    echo -e "${RED}Error: direct_rag_integration.py not found.${NC}"
    exit 1
fi

# Copy the integration file to the container
echo "Copying direct_rag_integration.py to container..."
docker cp ./direct_rag_integration.py $CONTAINER_ID:/app/api/inference_engine/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy direct_rag_integration.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied direct_rag_integration.py to container.${NC}"

# Create the integration script
echo "Creating HybridEngine patch script..."
cat > hybrid_engine_integrator.py << 'EOF'
#!/usr/bin/env python
"""
HybridEngine RAG Integrator

This script patches the HybridEngine class to use the Direct RAG integration.
"""
import os
import sys
import logging
import importlib
from types import MethodType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("hybrid_engine_integrator")

def patch_hybrid_engine():
    """Patch the HybridEngine class with RAG capabilities"""
    try:
        # Import the HybridEngine module
        logger.info("Importing HybridEngine module...")
        hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")
        HybridEngine = hybrid_engine_module.HybridEngine
        logger.info("Successfully imported HybridEngine")
        
        # Import the direct RAG integration
        logger.info("Importing Direct RAG integration...")
        direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")
        enhance_hybrid_engine_response = direct_rag.enhance_hybrid_engine_response
        logger.info("Successfully imported Direct RAG integration")
        
        # Create a proxy for the query method
        def patched_query(self, query_type, **params):
            """Patched query method that enhances responses with RAG"""
            logger.info(f"Patched HybridEngine.query called with type: {query_type}")
            
            # Call the original query method
            original_response = self._original_query(query_type, **params)
            
            # Enhance the response with RAG
            enhanced_response = enhance_hybrid_engine_response(self, params, original_response)
            
            logger.info("Processed query with RAG enhancement")
            return enhanced_response
        
        # Get a reference to the original query method
        original_query = HybridEngine.query
        
        # Patch the HybridEngine class
        logger.info("Patching HybridEngine.query method...")
        HybridEngine._original_query = original_query
        HybridEngine.query = patched_query
        
        # Test the patch with a simple instance
        logger.info("Creating test HybridEngine instance...")
        engine = HybridEngine()
        engine.rag_integration_active = True
        
        logger.info("Successfully patched HybridEngine with RAG capabilities")
        return True
    
    except Exception as e:
        logger.error(f"Error patching HybridEngine: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = patch_hybrid_engine()
    
    if success:
        print("✅ Successfully patched HybridEngine with Direct RAG integration")
        sys.exit(0)
    else:
        print("❌ Failed to patch HybridEngine")
        sys.exit(1)
EOF

echo "Copying HybridEngine patch script to container..."
docker cp ./hybrid_engine_integrator.py $CONTAINER_ID:/app/api/inference_engine/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy hybrid_engine_integrator.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied hybrid_engine_integrator.py to container.${NC}"

# Make the scripts executable
echo "Making scripts executable..."
docker exec $CONTAINER_ID chmod +x /app/api/inference_engine/direct_rag_integration.py /app/api/inference_engine/hybrid_engine_integrator.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make scripts executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made scripts executable.${NC}"

# Create startup script that applies the patch
echo "Creating startup script..."
cat > start_with_rag.py << 'EOF'
#!/usr/bin/env python
"""
Start server with RAG integration

This script applies the RAG patch to the HybridEngine and then starts the server.
"""
import os
import sys
import logging
import importlib
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("start_with_rag")

def run_server():
    """Apply the RAG patch and run the server"""
    try:
        # Apply the RAG patch
        logger.info("Applying RAG patch to HybridEngine...")
        integrator = importlib.import_module("api.inference_engine.hybrid_engine_integrator")
        success = integrator.patch_hybrid_engine()
        
        if not success:
            logger.error("Failed to apply RAG patch")
            return False
        
        logger.info("Successfully applied RAG patch")
        
        # Run the server
        logger.info("Starting server...")
        os.chdir("/app")
        server_process = subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"], 
                                         check=True)
        
        return server_process.returncode == 0
    
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = run_server()
    
    if not success:
        logger.error("Server exited with an error")
        sys.exit(1)
EOF

echo "Copying startup script to container..."
docker cp ./start_with_rag.py $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy start_with_rag.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied start_with_rag.py to container.${NC}"

# Make the startup script executable
echo "Making startup script executable..."
docker exec $CONTAINER_ID chmod +x /app/start_with_rag.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make startup script executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made startup script executable.${NC}"

# Create test script
echo "Creating test script..."
cat > test_direct_rag.py << 'EOF'
#!/usr/bin/env python
"""
Test Direct RAG Integration

Run simple tests on the Direct RAG integration.
"""
import os
import sys
import logging
import importlib
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_direct_rag")

def test_direct_rag_integration():
    """Test the Direct RAG integration"""
    try:
        # Import the direct RAG integration
        logger.info("Importing Direct RAG integration...")
        direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")
        logger.info("Successfully imported Direct RAG integration")
        
        # Test the search function
        test_query = "How do I control aphids on tomatoes?"
        logger.info(f"Testing search with query: '{test_query}'")
        
        results = direct_rag.search_pest_data(test_query)
        if not results:
            logger.error("Search returned no results")
            return False
        
        logger.info(f"Found {len(results)} results")
        for i, result in enumerate(results, 1):
            logger.info(f"Result {i}: {result['title']} (Score: {result['score']:.2f})")
        
        # Test the enhancement function
        logger.info("Testing response enhancement...")
        
        original_response = "Aphids can be controlled using various methods."
        enhanced_response, results = direct_rag.enhance_response(test_query, original_response)
        
        logger.info(f"Original response: {original_response}")
        logger.info(f"Enhanced response length: {len(enhanced_response)} characters")
        logger.info(f"Enhancement added {len(enhanced_response) - len(original_response)} characters")
        
        # Try to import the patched HybridEngine (if it exists)
        try:
            logger.info("Checking if HybridEngine is patched...")
            hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")
            engine = hybrid_engine_module.HybridEngine()
            
            if hasattr(engine, "_original_query") and hasattr(engine, "rag_integration_active"):
                logger.info("HybridEngine is successfully patched with RAG integration")
            else:
                logger.info("HybridEngine is not yet patched")
        except Exception as e:
            logger.warning(f"Could not check HybridEngine patch status: {str(e)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing Direct RAG integration: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== Testing Direct RAG Integration ===")
    
    success = test_direct_rag_integration()
    
    if success:
        print("✅ Direct RAG integration is working correctly")
        sys.exit(0)
    else:
        print("❌ Direct RAG integration test failed")
        sys.exit(1)
EOF

echo "Copying test script to container..."
docker cp ./test_direct_rag.py $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy test_direct_rag.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied test_direct_rag.py to container.${NC}"

# Make the test script executable
echo "Making test script executable..."
docker exec $CONTAINER_ID chmod +x /app/test_direct_rag.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make test script executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made test script executable.${NC}"

# Run the test script
echo "Running Direct RAG integration test..."
docker exec $CONTAINER_ID python /app/test_direct_rag.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Direct RAG integration test failed.${NC}"
    exit 1
fi
echo -e "${GREEN}Direct RAG integration test passed.${NC}"

echo -e "${GREEN}===== Direct RAG Integration Installation Complete! =====${NC}"
echo -e "${BLUE}You can now restart the server with RAG integration enabled:${NC}"
echo -e "${BLUE}docker exec -it $CONTAINER_ID python /app/start_with_rag.py${NC}" 