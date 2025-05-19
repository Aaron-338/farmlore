# FarmLore RAG Integration - Simplified Approach

This guide explains how to integrate RAG (Retrieval-Augmented Generation) capabilities into the FarmLore system. The implementation directly enhances the HybridEngine without requiring extensive patching or restructuring.

## Overview

The RAG system enables natural language queries against the Prolog knowledge base by:

1. Converting Prolog frames to text chunks
2. Creating vector embeddings of those chunks
3. Storing them in a ChromaDB vector database
4. Retrieving relevant chunks for user queries

## Files

This implementation adds 3 files to the system:

1. `implement_rag.py` - Core RAG implementation
2. `add_rag_to_hybrid_engine.py` - Simple script to integrate RAG with HybridEngine
3. `initialize_rag.py` - Startup script for Docker container

## Setup Instructions

### 1. Add the RAG Implementation Files

Place the following files in your project directory:
- `implement_rag.py`
- `add_rag_to_hybrid_engine.py` 
- `initialize_rag.py`

### 2. Update Docker Configuration

Run the `add_rag_to_hybrid_engine.py` script to automatically:
- Update `docker-compose.yml` to add the ChromaDB volume
- Add RAG environment variables to the web service
- Update requirements.txt to include RAG dependencies

```bash
python add_rag_to_hybrid_engine.py
```

### 3. Update Docker Startup

Add the RAG initialization to your container startup process by modifying the start_web.sh script to include:

```bash
# Initialize RAG if enabled
if [ "$USE_RAG" = "true" ]; then
    echo "Initializing RAG system..."
    python initialize_rag.py
fi
```

### 4. Rebuild and Deploy

```bash
docker-compose build web
docker-compose up -d
```

## How It Works

1. **During Container Startup**: The `initialize_rag.py` script creates vector embeddings from the Prolog knowledge base.

2. **At Runtime**: When a user issues a natural language query:
   - The query is processed by HybridEngine's `_process_general_query` method
   - The enhanced method first checks if the RAG system has a relevant answer
   - If RAG finds an answer, it returns it directly
   - If not, it falls back to the original Prolog or Ollama methods

3. **Integration**: The RAG system is integrated directly into HybridEngine by modifying its `_process_general_query` method at runtime.

## Testing

You can test if the RAG system is working by running:

```bash
docker exec farmlore_web_1 python -c "
from implement_rag import get_rag_system
rag = get_rag_system()
results = rag.query('How do I control aphids on peas?')
for r in results:
    print(r)
"
```

## Features

- **Smart Path Detection**: Works in both Docker and local environments without code changes
- **Direct HybridEngine Integration**: No multi-file patching required
- **Cache-friendly**: Loads existing vector stores if available
- **Environment Variable Controls**: Enable/disable via environment variables

## Troubleshooting

Check the logs for RAG initialization messages:

```bash
docker-compose logs -f web | grep rag_initializer
``` 