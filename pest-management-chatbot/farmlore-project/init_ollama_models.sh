#!/bin/bash
# Enhanced script to initialize Ollama models and validate their availability

echo "[INIT_SCRIPT] Initializing Ollama models..."

# Wait for Ollama service to be ready
echo "[INIT_SCRIPT] Waiting for Ollama service to be available at http://ollama:11434..."
MAX_RETRIES=60 # Approx 5 minutes
RETRY_COUNT=0
RETRY_DELAY=5

until curl -s --fail http://ollama:11434/api/version > /dev/null; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "[INIT_SCRIPT] CRITICAL: Ollama service not available after $MAX_RETRIES attempts. Exiting."
        exit 1
    fi
    echo "[INIT_SCRIPT] Ollama service not ready yet (attempt $RETRY_COUNT/$MAX_RETRIES). Retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
done

echo "[INIT_SCRIPT] Ollama service is available."

# Pull the TinyLlama model
MODEL_NAME="tinyllama:latest"
echo "[INIT_SCRIPT] Pulling $MODEL_NAME model... This might take a while."
# Added --fail to error out on server errors, removed -d for GET-like behavior for pull status
# The actual pull command should be POST, the previous one was fine, this is a check
# Correcting the pull command to be a POST and ensuring output for debugging
echo "[INIT_SCRIPT] curl -s -X POST --fail http://ollama:11434/api/pull -d '''{"name": "'''$MODEL_NAME'''"}'''"
PULL_OUTPUT=$(curl -s -X POST --fail http://ollama:11434/api/pull -d '''{"name": "'''$MODEL_NAME'''"}''' 2>&1)

if [ $? -ne 0 ]; then
    echo "[INIT_SCRIPT] CRITICAL: Failed to initiate pull for $MODEL_NAME."
    echo "[INIT_SCRIPT] Ollama PULL output: $PULL_OUTPUT"
    exit 1
fi

# Monitor pull status - Ollama's pull API streams status, then a final message.
# We need to wait for the "success" status or similar indicator.
echo "[INIT_SCRIPT] Model pull initiated. Monitoring status..."
echo "[INIT_SCRIPT] Ollama PULL raw output: $PULL_OUTPUT"

# Simplified check: give it time and then check /api/tags
# A more robust check would parse the streaming output of the pull command.
# For now, we assume the pull command itself will take time and then we verify.
# The previous script waited on the command, let's ensure it has enough time.
# The actual `ollama pull` command in terminal blocks until download is complete.
# `curl` POST to /api/pull returns immediately after starting the download.
# So we must poll /api/tags.

echo "[INIT_SCRIPT] Waiting for model to become available after pull initiation (up to 5 minutes)..."
MAX_CHECK_RETRIES=60 # 60 * 5s = 300s = 5 minutes
CHECK_RETRY_COUNT=0
MODEL_AVAILABLE=false

while [ $CHECK_RETRY_COUNT -lt $MAX_CHECK_RETRIES ]; do
    # Check if the model tag exists, allow for variations like "tinyllama:latest"
    TAG_CHECK_OUTPUT=$(curl -s --fail http://ollama:11434/api/tags 2>&1)
    if echo "$TAG_CHECK_OUTPUT" | grep -q "\"name\":\"$MODEL_NAME\""; then
        echo "[INIT_SCRIPT] SUCCESS: $MODEL_NAME model is listed in /api/tags."
        MODEL_AVAILABLE=true
        break
    fi
    
    CHECK_RETRY_COUNT=$((CHECK_RETRY_COUNT+1))
    echo "[INIT_SCRIPT] $MODEL_NAME not yet listed in /api/tags (attempt $CHECK_RETRY_COUNT/$MAX_CHECK_RETRIES). Retrying in $RETRY_DELAY seconds..."
    echo "[INIT_SCRIPT] Current /api/tags output: $TAG_CHECK_OUTPUT"
    sleep $RETRY_DELAY
done

if [ "$MODEL_AVAILABLE" != "true" ]; then
    echo "[INIT_SCRIPT] CRITICAL: $MODEL_NAME model not available after pull attempt and retries."
    exit 1
fi

# Test the model with a simple inference
echo "[INIT_SCRIPT] Testing $MODEL_NAME model with simple inference..."
TEST_PROMPT='{"model": "'''$MODEL_NAME'''", "prompt": "Hello, how are you?", "stream": false}'
TEST_RESPONSE=$(curl -s -X POST --fail http://ollama:11434/api/generate -d "$TEST_PROMPT" 2>&1)

if echo "$TEST_RESPONSE" | grep -q "\"response\""; then
    echo "[INIT_SCRIPT] SUCCESS: Model tested successfully!"
    echo "[INIT_SCRIPT] Ollama model initialization complete."
    exit 0
else
    echo "[INIT_SCRIPT] CRITICAL: Model test failed for $MODEL_NAME."
    echo "[INIT_SCRIPT] Test prompt: $TEST_PROMPT"
    echo "[INIT_SCRIPT] Test response: $TEST_RESPONSE"
    exit 1
fi
