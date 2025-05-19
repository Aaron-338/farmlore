#!/bin/bash

set -e

echo "Deploying RAG Connector for FarmLore"
echo "==================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Copy the RAG chat template to the Django templates directory
echo "Copying RAG chat template to Django templates directory..."
mkdir -p pest-management-chatbot/farmlore-project/chatbot/templates/chatbot/
cp rag_chat.html pest-management-chatbot/farmlore-project/chatbot/templates/chatbot/

# Make sure files are available
if [ ! -f "standalone_rag.py" ] || [ ! -f "rag_web_connector.py" ]; then
    echo "Required files missing. Please make sure standalone_rag.py and rag_web_connector.py exist."
    exit 1
fi

# Build and start the services
echo "Building and starting services..."
docker-compose build
docker-compose up -d

echo ""
echo "RAG Connector Deployment Complete!"
echo "=================================="
echo ""
echo "Access the RAG-enhanced chat at: http://localhost/chatbot/rag-chat/"
echo ""
echo "To verify the RAG connector is working:"
echo "  - Try asking questions about agricultural pests like:"
echo "    - How do I control aphids on my tomato plants?"
echo "    - What pests affect cucumber plants?"
echo "    - How to deal with spider mites in my garden?"
echo ""
echo "To check logs:"
echo "  - docker-compose logs -f rag_connector"
echo "" 