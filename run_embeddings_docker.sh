#!/bin/bash

echo "Building and running embeddings classifier in Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running! Please start Docker and try again."
    exit 1
fi

# Build and run with Docker Compose
docker-compose -f docker-compose.embeddings.yml build
if [ $? -ne 0 ]; then
    echo "Error: Failed to build Docker images."
    exit 1
fi

echo
echo "Running embeddings classifier..."
echo
docker-compose -f docker-compose.embeddings.yml up embeddings-classifier

echo
echo "To run classifier comparison test, use:"
echo "docker-compose -f docker-compose.embeddings.yml up compare-classifiers"
echo 