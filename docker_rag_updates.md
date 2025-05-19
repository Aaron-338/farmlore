# Docker Setup Updates for RAG Integration

## 1. Update docker-compose.yml

Add a volume for the Chroma vector database:

```yaml
volumes:
  postgres_data:
  static_volume:
  media_volume:
  ollama_data:
  chroma_data:  # New volume for vector database storage
```

Update the web service to mount the vector database volume and set RAG environment variables:

```yaml
web:
  # ... existing config ...
  volumes:
    - ./pest-management-chatbot/farmlore-project:/app
    - static_volume:/app/staticfiles
    - media_volume:/app/media
    - chroma_data:/app/data/chromadb  # Mount for vector database
  environment:
    # ... existing env vars ...
    - USE_RAG=true  # Enable RAG system
    - RAG_PERSIST_DIR=/app/data/chromadb
```

## 2. Create a requirements_rag.txt file in the Docker context

This file should be added to the Docker build context (pest-management-chatbot/farmlore-project/):

```
langchain==0.1.8
langchain-community==0.0.19
chromadb==0.4.24
sentence-transformers==2.5.1
huggingface-hub==0.20.3
pysbd==0.3.4
regex==2023.12.25
```

## 3. Update the Dockerfile

Add installation of RAG requirements:

```Dockerfile
# Copy requirements first for better cache usage
COPY pest-management-chatbot/farmlore-project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install RAG requirements
COPY pest-management-chatbot/farmlore-project/requirements_rag.txt .
RUN pip install --no-cache-dir -r requirements_rag.txt
```

## 4. Copy RAG Implementation Files to Docker Context

Copy these files to the `pest-management-chatbot/farmlore-project/api/inference_engine/` directory:

- `implement_rag.py`
- `hybrid_engine_patch.py`

## 5. Update start_web.sh Script

Add the following to the `start_web.sh` script to initialize the RAG system during startup:

```bash
# Initialize RAG if enabled
if [ "$USE_RAG" = "true" ]; then
    echo "Initializing RAG system..."
    python -c "
import logging
logging.basicConfig(level=logging.INFO)
try:
    from api.inference_engine.implement_rag import PrologToRAGConverter
    converter = PrologToRAGConverter(persist_directory='${RAG_PERSIST_DIR}')
    vector_store = converter.process_all_knowledge_bases()
    if vector_store:
        logging.info('RAG vector store successfully created/loaded')
    else:
        logging.error('Failed to initialize RAG vector store')
except Exception as e:
    logging.error(f'Error initializing RAG: {str(e)}')
"
fi
```

## 6. Integrate RAG with HybridEngine

Add code to initialize the HybridEngine with RAG in `api/inference_engine/__init__.py`:

```python
# Initialize the HybridEngine with RAG if enabled
import os
from api.inference_engine.hybrid_engine import HybridEngine

# Create singleton instance
hybrid_engine = HybridEngine()

# Apply RAG patches if enabled
if os.environ.get('USE_RAG', 'false').lower() == 'true':
    try:
        from api.inference_engine.hybrid_engine_patch import HybridEnginePatch
        HybridEnginePatch.apply_patches(hybrid_engine)
    except Exception as e:
        import logging
        logging.error(f"Failed to apply RAG patches: {str(e)}")
```

## 7. File Path Updates

Update the file paths in `implement_rag.py` to use absolute paths based on the Docker container:

```python
# List of prolog files to process
prolog_files = [
    '/app/knowledgebase_docker.pl',
    '/app/pea_updates_docker.pl',
    '/app/advanced_queries_docker.pl'
]
```

## 8. Testing the RAG System in Docker

After deploying, test the RAG system with:

```bash
# Run a query
docker exec farmlore_web_1 python -c "
from api.inference_engine.implement_rag import PrologToRAGConverter, RAGQuery
converter = PrologToRAGConverter()
vector_store = converter.process_all_knowledge_bases()
rag = RAGQuery(vector_store)
results = rag.query('How do I control aphids on peas?')
for r in results:
    print(r)
"
``` 