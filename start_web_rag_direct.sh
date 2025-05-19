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
