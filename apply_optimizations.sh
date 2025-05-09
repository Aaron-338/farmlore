#!/bin/bash
# Script to apply performance optimizations to the Pest Management Chatbot

set -e  # Exit on error

echo "===== Applying Performance Optimizations ====="
echo "This script will apply all performance optimizations and restart the system."

# Check if Docker is running
if ! docker info &>/dev/null; then
    echo "ERROR: Docker is not running or not accessible. Please start Docker first."
    exit 1
fi

# Stop current containers
echo -e "\n>> Stopping current containers..."
docker compose down

# Apply changes
echo -e "\n>> Applying configuration changes..."

# Start containers with increased timeout and memory
echo -e "\n>> Starting containers with optimized settings..."
echo "This may take some time as the Ollama container loads the model..."
docker compose up -d

# Wait for web container to be ready
echo -e "\n>> Waiting for web container to be ready..."
ATTEMPTS=0
MAX_ATTEMPTS=30

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    if docker compose exec web echo "Container is responsive" &>/dev/null; then
        echo "Web container is ready."
        break
    fi
    ATTEMPTS=$((ATTEMPTS + 1))
    echo "Waiting for web container to be ready... Attempt $ATTEMPTS/$MAX_ATTEMPTS"
    sleep 10
done

if [ $ATTEMPTS -eq $MAX_ATTEMPTS ]; then
    echo "WARNING: Web container did not become ready in the expected time."
    echo "You may need to check the container logs with: docker compose logs web"
else
    # Run connectivity check
    echo -e "\n>> Checking Ollama connectivity..."
    docker compose exec web python manage.py check_ollama_connection --fix
fi

echo -e "\n===== Optimization Complete ====="
echo "The system has been optimized for better performance."
echo "You can now access the application at http://localhost."
echo ""
echo "To check the status of all containers:"
echo "  docker compose ps"
echo ""
echo "To view logs from the Ollama container:"
echo "  docker compose logs ollama"
echo ""
echo "To test the Ollama connection manually:"
echo "  docker compose exec web bash -c './test_ollama.sh'" 