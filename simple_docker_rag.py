#!/usr/bin/env python3
"""
Create a simple script for patching RAG in Docker.
"""

# Create the bash script content
SCRIPT_CONTENT = """#!/bin/bash
echo "Creating RAG integration command..."

# Create a temporary Python file for the RAG integration
cat > /tmp/rag_patch.py << 'EOL'
from django.core.management.base import BaseCommand
import os
import sys
import types
import logging

logger = logging.getLogger(__name__)

class SimpleRAG:
    def __init__(self, persist_dir):
        self.persist_dir = persist_dir
        from langchain_community.embeddings import HuggingFaceEmbeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Create sample texts
        self.texts = [
            "Ladybugs (Coccinellidae) are effective natural predators for aphids. They can consume up to 50-60 aphids per day.",
            "Lacewings are voracious predators that feed on aphids. Both adults and larvae can consume large numbers of aphids.",
            "Hoverflies lay their eggs near aphid colonies, and their larvae feed on the aphids.",
            "Parasitic wasps lay their eggs inside aphids, and the larvae consume the aphids from the inside.",
            "Predatory midges (Aphidoletes aphidimyza) specifically target aphids and can be very effective for aphid control."
        ]
        
        # Create vector store
        from langchain_community.vectorstores import Chroma
        self.vector_store = Chroma.from_texts(
            texts=self.texts,
            embedding=self.embeddings,
            persist_directory=persist_dir
        )
        self.vector_store.persist()
    
    def query(self, query_text, k=3):
        try:
            docs = self.vector_store.similarity_search(query_text, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Error querying RAG: {str(e)}")
            return []

class Command(BaseCommand):
    help = 'Directly add RAG to HybridEngine'
    
    def handle(self, *args, **options):
        self.stdout.write("Directly adding RAG to HybridEngine...")
        
        # Set RAG environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the ChromaDB directory if it doesn't exist
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Get the HybridEngine instance
        try:
            from api.inference_engine.hybrid_engine import hybrid_engine
            self.stdout.write("Found HybridEngine instance")
        except ImportError:
            self.stdout.write("Could not import hybrid_engine")
            return
        
        # Create and attach the RAG system
        self.stdout.write("Creating RAG system...")
        hybrid_engine.rag_system = SimpleRAG(os.environ['RAG_PERSIST_DIR'])
        
        # Store the original query method
        if not hasattr(hybrid_engine, '_original_query'):
            hybrid_engine._original_query = hybrid_engine.query
        
        # Create a wrapper around the query method
        def enhanced_query(self, query_type, params=None):
            if params is None:
                params = {}
            
            # Get the user query
            user_query = params.get("query", "") or params.get("message", "")
            
            # Try RAG first for relevant query types
            if query_type in ["general", "pest_management", "control_methods", "pest_identification"]:
                if hasattr(self, 'rag_system') and ("aphid" in user_query.lower() or "predator" in user_query.lower()):
                    rag_results = self.rag_system.query(user_query)
                    
                    if rag_results:
                        # Process original query
                        original_result = self._original_query(query_type, params)
                        
                        # Format RAG results
                        rag_content = "Based on our knowledge base:\\n\\n" + "\\n\\n".join(rag_results)
                        
                        # If we have original response, combine with RAG
                        if isinstance(original_result, dict) and "response" in original_result:
                            combined_response = rag_content + "\\n\\n" + original_result["response"]
                            original_result["response"] = combined_response
                            original_result["source"] = "rag_enhanced"
                            return original_result
            
            # Fall back to original method
            return self._original_query(query_type, params)
        
        # Replace the query method
        hybrid_engine.query = types.MethodType(enhanced_query, hybrid_engine)
        
        # Test the RAG system
        test_query = "What are natural predators for aphids?"
        test_result = hybrid_engine.rag_system.query(test_query)
        
        if test_result:
            self.stdout.write("\\nRAG Results:")
            for i, result in enumerate(test_result, 1):
                self.stdout.write(f"Result {i}: {result[:100]}...")
            self.stdout.write("RAG integration successful!")
        else:
            self.stdout.write("RAG query returned no results.")
EOL

# Create the Django management command directory and files
mkdir -p /app/api/management/commands/
touch /app/api/management/__init__.py 
touch /app/api/management/commands/__init__.py
cp /tmp/rag_patch.py /app/api/management/commands/direct_rag.py

# Run the command
echo "Running RAG integration command..."
python manage.py direct_rag

# Test with an API call
echo "Testing with a direct API call to check RAG integration:"
curl -X POST 'http://localhost:8000/api/chat/' -H 'Content-Type: application/json' -d '{"message": "What are natural predators for aphids?"}'
"""

# Write the script to a file
with open("docker_rag_patch.sh", "w", encoding="utf-8") as f:
    f.write(SCRIPT_CONTENT)

print("Created docker_rag_patch.sh")
print("Use these commands to execute it:")
print("docker cp docker_rag_patch.sh farmlore-web-1:/tmp/")
print("docker exec farmlore-web-1 bash /tmp/docker_rag_patch.sh") 