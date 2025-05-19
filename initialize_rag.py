#!/usr/bin/env python3
"""
RAG Initialization Script
This script is run at container startup to initialize the RAG system with aphid predator information.
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_rag():
    """Initialize the RAG system with aphid predator information."""
    try:
        # Check if RAG is enabled
        if os.environ.get('USE_RAG', '').lower() != 'true':
            logger.info("RAG is not enabled. Skipping initialization.")
            return True
            
        # Get the persistence directory
        persist_dir = os.environ.get('RAG_PERSIST_DIR', '/app/data/chromadb')
        logger.info(f"Using persistence directory: {persist_dir}")
        
        # Make sure the directory exists
        os.makedirs(persist_dir, exist_ok=True)
        
        # Check if we already have a populated database
        if os.path.exists(persist_dir) and os.path.isdir(persist_dir) and any(os.listdir(persist_dir)):
            logger.info(f"Vector store already exists at {persist_dir}")
            return True
        
        # If the database doesn't exist, create it
        logger.info("No existing vector store found. Creating one...")
        
        # Import required modules
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
            from langchain_community.document_loaders import TextLoader
        except ImportError:
            logger.error("Failed to import required modules. Installing dependencies...")
            import subprocess
            subprocess.run(["pip", "install", "langchain", "langchain-community", "sentence-transformers", "chromadb"])
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma
            from langchain_community.document_loaders import TextLoader
        
        # Look for the aphid predators text file
        predators_file = Path('/app/aphid_predators.txt')
        
        if predators_file.exists():
            # Load the document
            logger.info(f"Loading aphid predator information from {predators_file}")
            loader = TextLoader(str(predators_file))
            documents = loader.load()
            
            # Initialize the embeddings model
            logger.info("Initializing embeddings model...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Create the vector store
            logger.info("Creating vector store...")
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=persist_dir
            )
            vector_store.persist()
            
            logger.info("Vector store created and persisted successfully!")
            
            # Test the vector store
            logger.info("Testing the vector store with a sample query...")
            test_query = "What are natural predators for aphids?"
            docs = vector_store.similarity_search(test_query, k=3)
            
            if docs:
                logger.info(f"Found {len(docs)} relevant documents:")
                for i, doc in enumerate(docs, 1):
                    logger.info(f"Document {i}: {doc.page_content[:100]}...")
                return True
            else:
                logger.warning("No documents found for test query.")
                return False
        else:
            # If we don't have a text file, use inline text
            logger.info("No aphid predators text file found. Using inline text...")
            
            texts = [
                "Ladybugs (Coccinellidae) are effective natural predators for aphids. They can consume up to 50-60 aphids per day.",
                "Lacewings are voracious predators that feed on aphids. Both adults and larvae can consume large numbers of aphids.",
                "Hoverflies lay their eggs near aphid colonies, and their larvae feed on the aphids.",
                "Parasitic wasps lay their eggs inside aphids, and the larvae consume the aphids from the inside.",
                "Predatory midges (Aphidoletes aphidimyza) specifically target aphids and can be very effective for aphid control."
            ]
            
            # Initialize the embeddings model
            logger.info("Initializing embeddings model...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Create the vector store
            logger.info("Creating vector store from inline text...")
            vector_store = Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                persist_directory=persist_dir
            )
            vector_store.persist()
            
            logger.info("Vector store created and persisted successfully!")
            return True
            
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Initializing RAG system on startup...")
    success = initialize_rag()
    if success:
        logger.info("RAG system initialized successfully!")
        sys.exit(0)
    else:
        logger.error("Failed to initialize RAG system.")
        sys.exit(1) 