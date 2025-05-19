#!/bin/bash
# Install RAG using the direct query wrapper v2 approach
# This script copies the necessary files to the docker container
# and applies the RAG enhancement directly to the class and instances

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Installing RAG with Direct Query Wrapper V2 =====${NC}"

# Make sure the Docker container is running
CONTAINER_ID=$(docker ps | grep farmlore-web | awk '{print $1}')
if [ -z "$CONTAINER_ID" ]; then
    echo -e "${RED}Error: Farmlore web container is not running. Please start it first.${NC}"
    exit 1
fi

echo -e "${BLUE}Found container ID: ${CONTAINER_ID}${NC}"

# Make sure the docker_query_wrapper_v2.py exists
if [ ! -f "./docker_query_wrapper_v2.py" ]; then
    echo -e "${RED}Error: docker_query_wrapper_v2.py not found.${NC}"
    exit 1
fi

# Copy the RAG query wrapper to the container
echo "Copying docker_query_wrapper_v2.py to container..."
docker cp ./docker_query_wrapper_v2.py $CONTAINER_ID:/app/api/inference_engine/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy docker_query_wrapper_v2.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied docker_query_wrapper_v2.py to container.${NC}"

# Create or update start_web_rag_v2.sh script
echo "Creating updated start_web_rag_v2.sh script..."
cat > start_web_rag_v2.sh << 'EOF'
#!/bin/bash
# Modified startup script that loads the RAG system with direct patching

# Set environment variables for RAG
export USE_RAG=true
export RAG_PERSIST_DIR=/app/data/chromadb

# Create RAG data directory if it doesn't exist
mkdir -p /app/data/chromadb

# First, apply the RAG wrapper to enhance the HybridEngine
echo "Applying RAG wrapper V2 to HybridEngine..."
cd /app
python3 /app/api/inference_engine/docker_query_wrapper_v2.py

# Then start the web server as usual
echo "Starting Django server..."
cd /app
python manage.py runserver 0.0.0.0:8000
EOF

# Copy the new startup script to the container
echo "Copying start_web_rag_v2.sh to container..."
docker cp ./start_web_rag_v2.sh $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy start_web_rag_v2.sh to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied start_web_rag_v2.sh to container.${NC}"

# Make the script executable
echo "Making start_web_rag_v2.sh executable..."
docker exec $CONTAINER_ID chmod +x /app/start_web_rag_v2.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make start_web_rag_v2.sh executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made start_web_rag_v2.sh executable.${NC}"

# Create a test script to verify RAG integration
echo "Creating test script..."
cat > test_rag_v2.py << 'EOF'
#!/usr/bin/env python
"""
Test script for RAG integration with the direct query wrapper v2
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_rag_v2")

def test_rag_integration():
    """Test if RAG integration is working correctly"""
    # Add app directory to path if needed
    if os.path.exists('/app') and '/app' not in sys.path:
        sys.path.append('/app')
    
    try:
        # Import HybridEngine
        from api.inference_engine.hybrid_engine import HybridEngine
        
        # Create an instance
        engine = HybridEngine()
        
        # Check if it has RAG capability
        has_rag = hasattr(engine, 'rag_system') or hasattr(HybridEngine, 'rag_system') or hasattr(engine, '_rag_enhanced') or hasattr(HybridEngine, '_rag_enhanced')
        
        if has_rag:
            print("✅ RAG integration successful! HybridEngine has RAG capabilities.")
            
            # Try to use RAG
            query_text = "How do I control aphids on tomatoes?"
            
            if hasattr(engine, 'rag_system') and callable(getattr(engine.rag_system, 'query', None)):
                print(f"Testing RAG query with: '{query_text}'")
                results = engine.rag_system.query(query_text)
                
                if results:
                    print(f"RAG query returned {len(results)} results:")
                    for i, result in enumerate(results, 1):
                        print(f"Result {i}: {result[:200]}...")
                else:
                    print("RAG query returned no results.")
            
            return True
        else:
            print("❌ RAG integration failed! HybridEngine does not have RAG capabilities.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing RAG integration: {e}")
        return False

if __name__ == "__main__":
    print("===== Testing RAG Integration V2 =====")
    test_rag_integration()
EOF

# Copy the test script to the container
echo "Copying test_rag_v2.py to container..."
docker cp ./test_rag_v2.py $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy test_rag_v2.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied test_rag_v2.py to container.${NC}"

# Make the test script executable
echo "Making test_rag_v2.py executable..."
docker exec $CONTAINER_ID chmod +x /app/test_rag_v2.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make test_rag_v2.py executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made test_rag_v2.py executable.${NC}"

# Install required packages in the container
echo "Installing required packages for RAG in container..."
docker exec $CONTAINER_ID pip install langchain-community huggingface_hub sentence-transformers chromadb
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install required packages.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully installed required packages.${NC}"

# Apply RAG wrapper inside the container
echo "Applying RAG wrapper..."
docker exec $CONTAINER_ID python3 /app/api/inference_engine/docker_query_wrapper_v2.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to apply RAG wrapper.${NC}"
    exit 1
fi
echo -e "${GREEN}RAG wrapper applied successfully.${NC}"

# Test RAG integration
echo "Testing RAG integration..."
docker exec $CONTAINER_ID python3 /app/test_rag_v2.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: RAG integration test failed.${NC}"
fi

# Stop the current web service
echo "Stopping current web service..."
docker exec $CONTAINER_ID ps aux | grep "python manage.py runserver" | grep -v grep | awk '{print $2}' | xargs docker exec $CONTAINER_ID kill -9 || true

# Restart the web service using our new script
echo "Restarting web service with RAG integration..."
docker exec -d $CONTAINER_ID /app/start_web_rag_v2.sh
echo -e "${GREEN}Web service restarted with RAG integration.${NC}"

echo -e "${GREEN}===== RAG installation with direct query wrapper V2 complete! =====${NC}"
echo -e "${BLUE}The system will now use RAG to enhance query responses.${NC}"
echo -e "${BLUE}Please test the system by asking a question related to your knowledge base.${NC}" 