#!/bin/bash

echo "Building and running embeddings classifier API in Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running! Please start Docker and try again."
    exit 1
fi

# Build and run with Docker Compose
docker-compose -f docker-compose.embeddings.yml build embeddings-api
if [ $? -ne 0 ]; then
    echo "Error: Failed to build Docker images."
    exit 1
fi

echo
echo "Running embeddings classifier API on port 5001..."
echo "API will be available at: http://localhost:5001/health"
echo
docker-compose -f docker-compose.embeddings.yml up embeddings-api 