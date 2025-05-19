#!/bin/bash
# Install RAG using the direct query wrapper approach
# This script copies the necessary files to the docker container
# and sets up the environment for RAG integration

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Installing RAG with Direct Query Wrapper =====${NC}"

# Make sure the Docker container is running
CONTAINER_ID=$(docker ps | grep farmlore-web | awk '{print $1}')
if [ -z "$CONTAINER_ID" ]; then
    echo -e "${RED}Error: Farmlore web container is not running. Please start it first.${NC}"
    exit 1
fi

echo -e "${BLUE}Found container ID: ${CONTAINER_ID}${NC}"

# Make sure the docker_query_wrapper.py exists
if [ ! -f "./docker_query_wrapper.py" ]; then
    echo -e "${RED}Error: docker_query_wrapper.py not found.${NC}"
    exit 1
fi

# Copy the RAG query wrapper to the container
echo "Copying docker_query_wrapper.py to container..."
docker cp ./docker_query_wrapper.py $CONTAINER_ID:/app/api/inference_engine/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy docker_query_wrapper.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied docker_query_wrapper.py to container.${NC}"

# Create or update start_web_rag.sh script
echo "Creating updated start_web_rag.sh script..."
cat > start_web_rag.sh << 'EOF'
#!/bin/bash
# Modified startup script that loads the RAG system

# Set environment variables for RAG
export USE_RAG=true
export RAG_PERSIST_DIR=/app/data/chromadb

# Create RAG data directory if it doesn't exist
mkdir -p /app/data/chromadb

# First, apply the RAG wrapper to enhance the HybridEngine
echo "Applying RAG wrapper to HybridEngine..."
python3 /app/api/inference_engine/docker_query_wrapper.py

# Then start the web server as usual
echo "Starting Django server..."
cd /app
python manage.py runserver 0.0.0.0:8000
EOF

# Copy the new startup script to the container
echo "Copying start_web_rag.sh to container..."
docker cp ./start_web_rag.sh $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy start_web_rag.sh to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied start_web_rag.sh to container.${NC}"

# Make the script executable
echo "Making start_web_rag.sh executable..."
docker exec $CONTAINER_ID chmod +x /app/start_web_rag.sh
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make start_web_rag.sh executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made start_web_rag.sh executable.${NC}"

# Install required packages in the container
echo "Installing required packages for RAG in container..."
docker exec $CONTAINER_ID pip install langchain-community huggingface_hub sentence-transformers chromadb
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install required packages.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully installed required packages.${NC}"

# Test RAG wrapper
echo "Testing RAG wrapper..."
docker exec $CONTAINER_ID python3 /app/api/inference_engine/docker_query_wrapper.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to run docker_query_wrapper.py.${NC}"
    exit 1
fi
echo -e "${GREEN}RAG wrapper test completed successfully.${NC}"

# Restart the web service using the new script
echo "Restarting web service with RAG integration..."
docker exec -d $CONTAINER_ID pkill -f "python manage.py runserver"
docker exec -d $CONTAINER_ID /app/start_web_rag.sh
echo -e "${GREEN}Web service restarted with RAG integration.${NC}"

echo -e "${GREEN}===== RAG installation with direct query wrapper complete! =====${NC}"
echo -e "${BLUE}The system will now use RAG to enhance query responses.${NC}"
echo -e "${BLUE}Please test the system by asking a question related to your knowledge base.${NC}" 