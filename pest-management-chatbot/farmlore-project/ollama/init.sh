#!/bin/bash

echo "Starting Ollama server..."
export OLLAMA_HOST=0.0.0.0
ollama serve &

echo "Ollama server started in background. Waiting for it to be ready..."
# Wait for a few seconds for the server to initialize
sleep 10 # Adjust as needed, 10 seconds should be ample

echo "Creating specialized models if they don't exist..."
ollama create farmlore-crop-pests -f /app/modelfiles/crop_pests.modelfile
ollama create farmlore-general -f /app/modelfiles/general_query.modelfile
ollama create farmlore-indigenous -f /app/modelfiles/indigenous_knowledge.modelfile
ollama create farmlore-pest-id -f /app/modelfiles/pest_identification.modelfile
ollama create farmlore-pest-mgmt -f /app/modelfiles/pest_management.modelfile
echo "Specialized model creation process finished."

# Keep container running
echo "Ollama setup complete. Keeping container alive."
tail -f /dev/null 