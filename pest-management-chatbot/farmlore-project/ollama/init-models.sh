#!/bin/bash
# Script to initialize specialized models for FarmLore

echo "Starting Ollama server on 0.0.0.0:11434..."
# Start Ollama server in the background, binding to all interfaces
export OLLAMA_HOST=0.0.0.0
ollama serve &

echo "Initializing specialized models for FarmLore..."

# Wait for Ollama to be ready
max_retries=30
retry_count=0
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "Waiting for Ollama service to be ready..."
    sleep 10
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
        echo "Ollama service not available after maximum retries. Exiting."
        exit 1
    fi
done

echo "Ollama service is ready. Creating specialized models..."

# Create specialized models from Modelfiles
ollama create farmlore-pest-id -f /modelfiles/pest_identification.modelfile
ollama create farmlore-pest-mgmt -f /modelfiles/pest_management.modelfile
ollama create farmlore-indigenous -f /modelfiles/indigenous_knowledge.modelfile
ollama create farmlore-crop-pests -f /modelfiles/crop_pests.modelfile
ollama create farmlore-general -f /modelfiles/general_query.modelfile

echo "All specialized models created successfully!"

# Keep the container running
tail -f /dev/null
