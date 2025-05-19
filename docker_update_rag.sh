#!/bin/bash
# Script to update RAG implementation in the Docker container

# Stop if any command fails
set -e

echo "===== Updating RAG Implementation in Docker Container ====="

# 1. Update requirements in the Dockerfile
echo "Updating requirements for RAG in Dockerfile..."
if grep -q "langchain-text-splitters" Dockerfile; then
    echo "Requirements already updated."
else
    echo "Adding RAG dependencies to Dockerfile..."
    # Create a temporary file
    cat > requirements_rag_docker.txt << EOL
# RAG dependencies
langchain==0.1.8
langchain-community>=0.0.21
langchain-text-splitters>=0.0.1
chromadb==0.4.24
sentence-transformers==2.5.1
huggingface-hub==0.20.3
pysbd==0.3.4
regex==2023.12.25
EOL
fi

# 2. Copy RAG implementation files to container
echo "Copying RAG implementation files to container..."
docker cp implement_rag.py farmlore_web_1:/app/api/inference_engine/
docker cp add_rag_to_hybrid_engine.py farmlore_web_1:/app/
docker cp initialize_rag.py farmlore_web_1:/app/
docker cp start_web_rag.sh farmlore_web_1:/app/
docker cp requirements_rag_docker.txt farmlore_web_1:/app/requirements_rag.txt

# 3. Run pip install inside container to install RAG requirements
echo "Installing RAG dependencies in container..."
docker exec farmlore_web_1 pip install -r /app/requirements_rag.txt

# 4. Execute integration script inside container
echo "Integrating RAG with HybridEngine in container..."
docker exec -it farmlore_web_1 bash -c "cd /app && python -c \"
import sys
import logging
logging.basicConfig(level=logging.INFO)
sys.path.append('/app')
from add_rag_to_hybrid_engine import add_rag_to_hybrid_engine
success = add_rag_to_hybrid_engine()
print('RAG integration with HybridEngine: ' + ('SUCCESS' if success else 'FAILED'))
\""

# 5. Create a simple test to verify integration
cat > test_docker_rag.sh << EOL
#!/bin/bash
# Test RAG integration in Docker container

echo "Testing RAG integration in Docker container..."
docker exec -it farmlore_web_1 bash -c "cd /app && python -c \"
import sys
import logging
logging.basicConfig(level=logging.INFO)
sys.path.append('/app')
try:
    from api.inference_engine.hybrid_engine import HybridEngine
    print('HybridEngine imported successfully')
    
    from api.inference_engine.implement_rag import get_rag_system
    print('RAG system imported successfully')
    
    # Test RAG system
    rag = get_rag_system()
    if rag:
        print('RAG system initialized successfully')
        results = rag.query('How do I control aphids on peas?', k=2)
        if results:
            print(f'Found {len(results)} results for query')
            for i, r in enumerate(results):
                print(f'Result {i+1}: {r[:100]}...')
        else:
            print('No results found')
    else:
        print('Failed to initialize RAG system')
except Exception as e:
    print(f'Error: {str(e)}')
\""
EOL

chmod +x test_docker_rag.sh

echo "===== Update Complete ====="
echo "Execute ./test_docker_rag.sh to test RAG integration"
echo "You can restart the container with: docker-compose restart web" 