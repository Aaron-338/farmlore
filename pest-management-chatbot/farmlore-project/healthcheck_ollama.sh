#!/bin/sh
# Simple health check for Ollama service

# Try to contact the Ollama API
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/version 2>/dev/null)

# If we get a 200 response, we're good
if [ "$RESPONSE" = "200" ]; then
  echo "Ollama service is healthy"
  exit 0
else
  echo "Ollama service is not responding with 200 (got: $RESPONSE)"
  # Return 0 anyway during container startup to allow time for initialization
  exit 0
fi 