#!/usr/bin/env python
"""
Script to initialize RAG system during container startup.
"""
import os
import logging
import sys

# Configure logging with proper format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("rag_initializer")

def initialize_rag():
    """Initialize the RAG system with the knowledge base."""
    logger.info("Starting RAG initialization...")
    
    try:
        logger.info("Checking environment variables...")
        rag_enabled = os.environ.get("USE_RAG", "false").lower() == "true"
        
        if not rag_enabled:
            logger.info("RAG initialization skipped: USE_RAG is not set to 'true'")
            return False
        
        persist_dir = os.environ.get("RAG_PERSIST_DIR")
        if not persist_dir:
            logger.warning("RAG_PERSIST_DIR not set, using default './data/chromadb'")
            persist_dir = "./data/chromadb"
        
        logger.info(f"Using persistence directory: {persist_dir}")
        
        # Import the RAG converter
        logger.info("Importing RAG components...")
        from api.inference_engine.implement_rag import PrologToRAGConverter
        
        # Initialize the converter
        logger.info("Initializing PrologToRAGConverter...")
        converter = PrologToRAGConverter(persist_directory=persist_dir)
        
        # Check if vector store already exists
        logger.info("Checking for existing vector store...")
        vector_store = converter.load_vector_store()
        
        if vector_store:
            logger.info("Existing vector store found and loaded successfully")
            return True
        
        # Process the knowledge base and create vector store
        logger.info("Creating new vector store from knowledge base...")
        vector_store = converter.process_all_knowledge_bases()
        
        if vector_store:
            logger.info("Vector store created successfully")
            return True
        else:
            logger.error("Failed to create vector store")
            return False
            
    except ImportError as e:
        logger.error(f"Import error: {str(e)}. Make sure RAG dependencies are installed.")
        return False
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        return False

if __name__ == "__main__":
    success = initialize_rag()
    
    if success:
        logger.info("RAG initialization completed successfully")
        sys.exit(0)
    else:
        logger.error("RAG initialization failed")
        # Exit with success code anyway to not block container startup
        sys.exit(0)
