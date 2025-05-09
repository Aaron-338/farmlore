#!/bin/bash
# Enhanced script to initialize Ollama models and validate their availability

echo "Initializing Ollama models..."

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be available..."
MAX_RETRIES=60
RETRY_COUNT=0

while ! curl -s http://localhost:11434/api/version > /dev/null; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Ollama service not available after $MAX_RETRIES attempts. Exiting."
        exit 1
    fi
    echo "Ollama service not ready yet. Retrying in 5 seconds..."
    sleep 5
done

echo "Ollama service is available."

# Pull the TinyLlama model
echo "Pulling TinyLlama model..."
ollama pull tinyllama:latest

# Verify the model was successfully pulled
echo "Verifying model availability..."
MAX_CHECK_RETRIES=10
CHECK_RETRY_COUNT=0

while true; do
    MODEL_CHECK=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"tinyllama"' || echo "")
    
    if [ -n "$MODEL_CHECK" ]; then
        echo "TinyLlama model successfully pulled and available."
        break
    fi
    
    CHECK_RETRY_COUNT=$((CHECK_RETRY_COUNT+1))
    if [ $CHECK_RETRY_COUNT -ge $MAX_CHECK_RETRIES ]; then
        echo "Warning: TinyLlama model not verified after $MAX_CHECK_RETRIES attempts."
        echo "The model may not be available for inference yet."
        break
    fi
    
    echo "Model not yet available. Checking again in 10 seconds..."
    sleep 10
done

# Test the model with a simple inference
echo "Testing model with simple inference..."
TEST_RESPONSE=$(curl -s -X POST http://localhost:11434/api/generate -d '{
    "model": "tinyllama",
    "prompt": "Hello, how are you?",
    "stream": false
}')

if echo "$TEST_RESPONSE" | grep -q "response"; then
    echo "Model tested successfully!"
    echo "Ollama model initialization complete."
else
    echo "Warning: Model test failed. Response: $TEST_RESPONSE"
    echo "Ollama service is running but model inference may not work correctly."
fi
