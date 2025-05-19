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
