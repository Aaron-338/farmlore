#!/bin/bash
# Script to install the RAG database in the Docker container

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Creating RAG Database in Docker Container =====${NC}"

# Make sure the Docker container is running
CONTAINER_ID=$(docker ps | grep farmlore-web | awk '{print $1}')
if [ -z "$CONTAINER_ID" ]; then
    echo -e "${RED}Error: Farmlore web container is not running. Please start it first.${NC}"
    exit 1
fi

echo -e "${BLUE}Found container ID: ${CONTAINER_ID}${NC}"

# Make sure the rag_database_creator.py exists
if [ ! -f "./rag_database_creator.py" ]; then
    echo -e "${RED}Error: rag_database_creator.py not found.${NC}"
    exit 1
fi

# Copy the database creator script to the container
echo "Copying rag_database_creator.py to container..."
docker cp ./rag_database_creator.py $CONTAINER_ID:/app/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy rag_database_creator.py to container.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully copied rag_database_creator.py to container.${NC}"

# Make the script executable
echo "Making script executable..."
docker exec $CONTAINER_ID chmod +x /app/rag_database_creator.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make rag_database_creator.py executable.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully made script executable.${NC}"

# Install required packages
echo "Installing required packages..."
docker exec $CONTAINER_ID pip install langchain-text-splitters langchain-core
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install required packages.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully installed required packages.${NC}"

# Run the database creator script
echo "Creating RAG database..."
docker exec $CONTAINER_ID bash -c "cd /app && python /app/rag_database_creator.py"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create RAG database.${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully created RAG database.${NC}"

# Restart the web service to make sure it uses the new database
echo "Restarting web service..."
docker exec $CONTAINER_ID ps aux | grep "python manage.py runserver" | grep -v grep | awk '{print $2}' | xargs -r docker exec $CONTAINER_ID kill -9 || true
docker exec -d $CONTAINER_ID bash -c "cd /app && python manage.py runserver 0.0.0.0:8000"
echo -e "${GREEN}Web service restarted.${NC}"

echo -e "${GREEN}===== RAG Database Creation Complete! =====${NC}"
echo -e "${BLUE}You can now test the RAG integration with queries related to pest management.${NC}"
echo -e "${BLUE}Try a query like: 'How do I control aphids on tomatoes?'${NC}" 