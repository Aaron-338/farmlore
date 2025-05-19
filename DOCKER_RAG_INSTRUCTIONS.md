# RAG Integration for Docker Environment

This guide explains how to integrate RAG (Retrieval-Augmented Generation) capabilities into the pest management chatbot when running in Docker.

## Option 1: Update docker-compose.yml

The simplest way to enable RAG is to update your docker-compose.yml file to include the necessary environment variables:

1. Open your `docker-compose.yml` file
2. Find the `web` service
3. Add the following environment variables:

```yaml
web:
  # ... existing configuration ...
  environment:
    - USE_RAG=true
    - RAG_PERSIST_DIR=/app/data/chromadb
  volumes:
    # ... existing volumes ...
    - ./data:/app/data  # Make sure this volume exists to persist the RAG database
```

4. Restart your containers:

```bash
docker-compose down
docker-compose up -d
```

## Option 2: Use the docker_enable_rag.py script

We've created a script that automatically updates your docker-compose.yml and restarts the containers:

```bash
python docker_enable_rag.py
```

## Option 3: Enable RAG in a running container

If you want to enable RAG in an already running container without restarting:

1. Copy the `docker_rag_integration.py` script into the container:

```bash
docker cp docker_rag_integration.py farmlore_web_1:/app/
```

2. Run the script inside the container:

```bash
docker exec -it farmlore_web_1 python /app/docker_rag_integration.py
```

## Verifying RAG Integration

You can verify that RAG is working by:

1. Checking the container logs:

```bash
docker-compose logs web | grep "RAG"
```

2. Look for messages like "Successfully extended HybridEngine with RAG capabilities" or "Using RAG-enhanced general query processor"

3. Try a query that would be answered by RAG, such as "What are natural predators for aphids?" 
   - If responses include the phrase "Based on our knowledge base:", RAG is working.

## Troubleshooting

### Missing Dependencies

If RAG integration fails due to missing dependencies, you can install them in the container:

```bash
docker exec -it farmlore_web_1 pip install langchain langchain-community sentence-transformers chromadb unstructured
```

### Persistence Issues

If RAG data isn't persisting between container restarts:

1. Make sure you've mapped the `/app/data` directory to a volume
2. Check permissions on the host directory
3. Verify the `RAG_PERSIST_DIR` environment variable is set correctly

### Integration Failed

If RAG integration fails, check the logs for specific error messages:

```bash
docker-compose logs web
```

Common issues include:
- Missing Python dependencies
- File permission problems
- Incorrect paths in the container
- Memory limitations

## Additional Notes

- The RAG system enhances responses by retrieving relevant information from your knowledge base
- It works alongside Ollama to provide more accurate and comprehensive responses
- RAG requires more memory than the base system, so ensure your Docker environment has sufficient resources
- The ChromaDB database will grow over time as more data is added to the vector store 