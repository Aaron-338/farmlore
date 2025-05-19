#!/usr/bin/env python3
"""
Direct RAG integration script for Docker.
This script uses the RAG system directly without method patching.
"""
import os
import sys
import logging
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def direct_rag_query():
    """
    Directly query the RAG system in the Docker container.
    """
    try:
        # Add the app directory to the path
        sys.path.append('/app')
        
        # Set RAG environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the ChromaDB directory if it doesn't exist
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Import the required modules
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
        except ImportError:
            logger.error("Failed to import LangChain modules. Make sure they're installed.")
            return False
        
        # Test query about aphids
        test_query = "What are natural predators for aphids?"
        logger.info(f"Test query: '{test_query}'")
        
        # Load the RAG system directly
        try:
            logger.info("Loading embeddings model...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            logger.info(f"Checking for existing vector store in {os.environ['RAG_PERSIST_DIR']}")
            if os.path.exists(os.environ['RAG_PERSIST_DIR']):
                logger.info("Loading existing vector store...")
                vector_store = Chroma(
                    embedding_function=embeddings,
                    persist_directory=os.environ['RAG_PERSIST_DIR']
                )
                
                # Query the vector store
                logger.info("Querying vector store...")
                docs = vector_store.similarity_search(test_query, k=3)
                
                # Extract content from documents
                results = [doc.page_content for doc in docs]
                
                # Print the results
                if results:
                    print("\nRAG Results:")
                    print("===========")
                    for i, result in enumerate(results, 1):
                        print(f"Result {i}:")
                        print(result)
                        print("-" * 40)
                    
                    print("\n✓ RAG is working correctly!")
                    return True
                else:
                    logger.warning("Vector store didn't return any results.")
                    print("\n⚠ The vector store is working but returned no results for this query.")
                    return True
            else:
                logger.warning(f"No vector store found at {os.environ['RAG_PERSIST_DIR']}")
                print("\n⚠ No vector store found. You need to create one first.")
                
                # Let's create one with sample data
                logger.info("Creating a sample vector store...")
                
                # Sample knowledge about aphids and their predators
                texts = [
                    "Ladybugs (Coccinellidae) are effective natural predators for aphids. They can consume up to 50-60 aphids per day.",
                    "Lacewings are voracious predators that feed on aphids. Both adults and larvae can consume large numbers of aphids.",
                    "Hoverflies lay their eggs near aphid colonies, and their larvae feed on the aphids.",
                    "Parasitic wasps lay their eggs inside aphids, and the larvae consume the aphids from the inside.",
                    "Predatory midges (Aphidoletes aphidimyza) specifically target aphids and can be very effective for aphid control."
                ]
                
                # Create the vector store
                vector_store = Chroma.from_texts(
                    texts=texts,
                    embedding=embeddings,
                    persist_directory=os.environ['RAG_PERSIST_DIR']
                )
                vector_store.persist()
                
                logger.info("Sample vector store created.")
                print("\n✓ Created a sample vector store with information about aphid predators.")
                
                # Now query it
                logger.info("Querying new vector store...")
                docs = vector_store.similarity_search(test_query, k=3)
                results = [doc.page_content for doc in docs]
                
                if results:
                    print("\nRAG Results:")
                    print("===========")
                    for i, result in enumerate(results, 1):
                        print(f"Result {i}:")
                        print(result)
                        print("-" * 40)
                    
                    print("\n✓ RAG is now working correctly!")
                    return True
                else:
                    logger.warning("New vector store didn't return any results.")
                    print("\n⚠ Created a vector store, but it returned no results.")
                    return False
        
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        
    except Exception as e:
        logger.error(f"Error in direct RAG query: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Testing direct RAG query in Docker...")
    success = direct_rag_query()
    if success:
        print("\n✓ RAG system is available in Docker.")
    else:
        print("\n⚠ RAG system could not be tested successfully.")
        
        # Check if dependencies are installed
        try:
            import pkg_resources
            required_packages = ['langchain', 'langchain-community', 'sentence-transformers', 'chromadb']
            
            missing_packages = []
            for package in required_packages:
                try:
                    pkg_resources.get_distribution(package)
                except pkg_resources.DistributionNotFound:
                    missing_packages.append(package)
            
            if missing_packages:
                print("\nMissing dependencies:")
                print(", ".join(missing_packages))
                print("\nInstall them with:")
                print(f"pip install {' '.join(missing_packages)}")
        except:
            print("\nCould not check for missing dependencies.") 