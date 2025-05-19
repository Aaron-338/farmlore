#!/usr/bin/env python3
"""
Create a script to directly populate the ChromaDB directory with aphid predator data.
"""

SCRIPT_CONTENT = """#!/usr/bin/env python3
import os
import sys
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_rag_database():
    """Create and populate a new RAG database with aphid predator info."""
    try:
        # Set RAG environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Clear the existing ChromaDB directory and recreate it
        print(f"Clearing the existing ChromaDB directory at {os.environ['RAG_PERSIST_DIR']}")
        if os.path.exists(os.environ['RAG_PERSIST_DIR']):
            shutil.rmtree(os.environ['RAG_PERSIST_DIR'])
        
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Import the required modules
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
        except ImportError:
            print("Failed to import LangChain modules. Installing...")
            import subprocess
            subprocess.run(["pip", "install", "langchain", "langchain-community", "sentence-transformers", "chromadb"])
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
        
        # Create sample texts about aphid predators
        print("Creating sample texts about aphid predators")
        texts = [
            "Ladybugs (Coccinellidae) are effective natural predators for aphids. They can consume up to 50-60 aphids per day.",
            "Lacewings are voracious predators that feed on aphids. Both adults and larvae can consume large numbers of aphids.",
            "Hoverflies lay their eggs near aphid colonies, and their larvae feed on the aphids.",
            "Parasitic wasps lay their eggs inside aphids, and the larvae consume the aphids from the inside.",
            "Predatory midges (Aphidoletes aphidimyza) specifically target aphids and can be very effective for aphid control."
        ]
        
        # Create a new vector store
        print("Creating vector store with aphid predator information")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=os.environ['RAG_PERSIST_DIR']
        )
        vector_store.persist()
        
        # Test the vector store
        print("Testing the vector store with a query about aphid predators")
        test_query = "What are natural predators for aphids?"
        docs = vector_store.similarity_search(test_query, k=3)
        results = [doc.page_content for doc in docs]
        
        if results:
            print("RAG Results:")
            for i, result in enumerate(results, 1):
                print(f"Result {i}:")
                print(result)
                print("-" * 40)
            
            print("RAG database created and tested successfully!")
            return True
        else:
            print("Vector store created but returned no results for a test query.")
            return False
    
    except Exception as e:
        print(f"Error creating RAG database: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Creating and populating RAG database with aphid predator information...")
    success = create_rag_database()
    if success:
        print("RAG database successfully created and populated!")
        print("To test it, run:")
        print('curl -X POST "http://localhost:8000/api/chat/" -H "Content-Type: application/json" -d \'{"message": "What are natural predators for aphids?"}\'')
    else:
        print("Failed to create RAG database.")
"""

# Write the script to a file
with open("rag_database_creator.py", "w", encoding="utf-8") as f:
    f.write(SCRIPT_CONTENT)

print("Created rag_database_creator.py")
print("Copy and run this file in the Docker container with:")
print("docker cp rag_database_creator.py farmlore-web-1:/app/")
print("docker exec farmlore-web-1 python /app/rag_database_creator.py") 