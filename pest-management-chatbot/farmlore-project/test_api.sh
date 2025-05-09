#!/bin/bash
# Test the chat API
curl -X POST "http://localhost:8000/api/chat/" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I control aphids on tomato plants?"}' 