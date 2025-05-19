#!/bin/bash
# Install RAG using the direct approach
# This script copies the necessary files to the docker container
# and applies the RAG directly without modifying HybridEngine

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Installing RAG with Direct Approach =====${NC}"

# Make sure the Docker container is running
CONTAINER_ID=$(docker ps | grep farmlore-web | awk '{print $1}')
if [ -z "$CONTAINER_ID" ]; then
    echo -e "${RED}Error: Farmlore web container is not running. Please start it first.${NC}"
    exit 1
fi

echo -e "${BLUE}Found container ID: ${CONTAINER_ID}${NC}"

# Make sure the docker_rag_direct.py exists
if [ ! -f "./docker_rag_direct.py" ]; then
    echo -e "${RED}Error: docker_rag_direct.py not found.${NC}"
    exit 1
fi

# Copy the RAG direct script to the container
echo "Copying docker_rag_direct.py to container..."
docker cp ./docker_rag_direct.py $CONTAINER_ID:/app/api/inference_engine/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy docker_rag_direct.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied docker_rag_direct.py to container.${NC}"

# Create start_web_rag_direct.sh script
echo "Creating start_web_rag_direct.sh script..."
cat > start_web_rag_direct.sh << 'EOF'
#!/bin/bash
# Start script that loads the RAG system with direct approach

# Set environment variables for RAG
export USE_RAG=true
export RAG_PERSIST_DIR=/app/data/chromadb

# Create RAG data directory if it doesn't exist
mkdir -p /app/data/chromadb

# Apply the RAG direct approach
echo "Applying RAG direct approach..."
cd /app
python3 /app/api/inference_engine/docker_rag_direct.py

# Then start the web server as usual
echo "Starting Django server..."
cd /app
python manage.py runserver 0.0.0.0:8000
EOF

# Copy the start script to the container
echo "Copying start_web_rag_direct.sh to container..."
docker cp ./start_web_rag_direct.sh $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy start_web_rag_direct.sh to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied start_web_rag_direct.sh to container.${NC}"

# Make the script executable
echo "Making start_web_rag_direct.sh executable..."
docker exec $CONTAINER_ID chmod +x /app/start_web_rag_direct.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make start_web_rag_direct.sh executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made start_web_rag_direct.sh executable.${NC}"

# Install required packages in the container
echo "Installing required packages for RAG in container..."
docker exec $CONTAINER_ID pip install langchain-community huggingface_hub sentence-transformers chromadb
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install required packages.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully installed required packages.${NC}"

# Test RAG system inside the container
echo "Testing RAG system..."
docker exec $CONTAINER_ID python3 /app/api/inference_engine/docker_rag_direct.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: RAG system test failed.${NC}"
    exit 1
fi

# Stop the current web service
echo "Stopping current web service..."
docker exec $CONTAINER_ID ps aux | grep "python manage.py runserver" | grep -v grep | awk '{print $2}' | xargs -r docker exec $CONTAINER_ID kill -9 || true

# Restart the web service using our new script
echo "Restarting web service with direct RAG integration..."
docker exec -d $CONTAINER_ID /app/start_web_rag_direct.sh
echo -e "${GREEN}Web service restarted with direct RAG integration.${NC}"

echo -e "${GREEN}===== RAG installation with direct approach complete! =====${NC}"
echo -e "${BLUE}The system will now use RAG to enhance query responses.${NC}"
echo -e "${BLUE}Please test the system by asking a question related to your knowledge base.${NC}" 