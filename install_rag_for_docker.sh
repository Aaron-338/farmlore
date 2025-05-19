#!/bin/bash
# Master script to install RAG in the Docker environment

# Ensure we stop on errors
set -e

echo "===== FarmLore RAG Docker Installation ====="

# 1. Check if Docker is running
echo "Checking Docker status..."
if ! docker ps > /dev/null 2>&1; then
    echo "Error: Docker does not appear to be running. Please start Docker and try again."
    exit 1
fi

# 2. Identify container name
echo "Identifying container name..."
CONTAINER_NAME=$(docker-compose ps | grep web | awk '{print $1}')

if [ -z "$CONTAINER_NAME" ]; then
    echo "Could not find web container. Trying default name 'farmlore_web_1'..."
    CONTAINER_NAME="farmlore_web_1"
fi

echo "Using container name: $CONTAINER_NAME"

# Check if the container exists
if ! docker ps -a | grep -q "$CONTAINER_NAME"; then
    echo "Error: Container $CONTAINER_NAME not found. Make sure the FarmLore container is running."
    echo "You can start it with: docker-compose up -d"
    exit 1
fi

# 3. Set permissions on scripts
echo "Setting execute permissions on scripts..."
chmod +x docker_update_rag.sh test_docker_rag.sh

# 4. Create a Python script to handle container-specific operations
cat > run_in_container.py << 'EOL'
#!/usr/bin/env python
"""
Script to be run inside the Docker container to set up RAG.
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_setup")

def setup_rag_in_container():
    """Set up RAG inside the container"""
    # Add current directory to path
    sys.path.append('/app')
    
    try:
        # 1. Set environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # 2. Create necessary directories
        os.makedirs('/app/data/chromadb', exist_ok=True)
        logger.info("Created data directory: /app/data/chromadb")
        
        # 3. Initialize RAG
        logger.info("Initializing RAG...")
        from initialize_rag import initialize_rag
        success = initialize_rag()
        logger.info(f"RAG initialization: {'SUCCESS' if success else 'FAILED'}")
        
        # 4. Add RAG to HybridEngine
        logger.info("Extending HybridEngine with RAG...")
        from add_rag_to_hybrid_engine import add_rag_to_hybrid_engine
        rag_success = add_rag_to_hybrid_engine()
        logger.info(f"RAG integration: {'SUCCESS' if rag_success else 'FAILED'}")
        
        # 5. Test RAG query
        if success and rag_success:
            logger.info("Testing RAG query...")
            from api.inference_engine.implement_rag import get_rag_system
            rag = get_rag_system()
            if rag:
                results = rag.query("How do I control aphids on peas?", k=2)
                if results:
                    logger.info(f"Found {len(results)} results")
                    for i, result in enumerate(results, 1):
                        logger.info(f"Result {i}: {result[:100]}...")
                else:
                    logger.warning("No results found")
            else:
                logger.warning("RAG system not available")
        
        return success and rag_success
    except Exception as e:
        logger.error(f"Error setting up RAG: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== RAG Setup Inside Container ===")
    success = setup_rag_in_container()
    print(f"RAG setup: {'SUCCESSFUL' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
EOL

# 5. Update the docker-compose.yml file
echo "Checking docker-compose.yml for RAG configuration..."
if ! grep -q "RAG_PERSIST_DIR" docker-compose.yml; then
    echo "Adding RAG configuration to docker-compose.yml..."
    cp docker-compose.yml docker-compose.yml.bak
    
    # Add environment variables and volume
    # Note: This is a simple approach and might need adjustment based on your docker-compose.yml structure
    sed -i 's/services:/services:\n  volumes:\n    chroma_data:\n/' docker-compose.yml
    sed -i '/web:/,/volumes:/ s/volumes:/volumes:\n      - chroma_data:\/app\/data\/chromadb/' docker-compose.yml
    sed -i '/web:/,/environment:/ s/environment:/environment:\n      - USE_RAG=true\n      - RAG_PERSIST_DIR=\/app\/data\/chromadb/' docker-compose.yml
fi

# 6. Run the update script
echo "Running update script to copy files to container..."
./docker_update_rag.sh

# 7. Run setup inside the container
echo "Running setup inside the container..."
docker cp run_in_container.py $CONTAINER_NAME:/app/
docker exec $CONTAINER_NAME python /app/run_in_container.py

# 8. Done
echo "===== RAG Installation Complete ====="
echo "To test RAG integration, run: ./test_docker_rag.sh"
echo "To restart the container with RAG enabled, run: docker-compose restart web"
echo "Then check logs with: docker-compose logs -f web" 