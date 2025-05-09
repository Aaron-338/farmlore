#!/bin/sh
# Basic health check for Ollama service

# Try to contact the Ollama API
if curl -s -f http://localhost:11434/api/version > /dev/null; then
  echo "Ollama service is healthy"
  exit 0
else
  echo "Ollama service is not responding"
  exit 1
fi 