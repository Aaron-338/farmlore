import os 
import sys 
import logging 
 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger("rag_setup") 
 
def setup_rag_in_container(): 
    """Set up RAG inside the container""" 
    sys.path.append('/app') 
 
    try: 
        # Set environment variables 
        os.environ['USE_RAG'] = 'true' 
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb' 
 
        # Create necessary directories 
        os.makedirs('/app/data/chromadb', exist_ok=True) 
        logger.info("Created data directory: /app/data/chromadb") 
 
        # Initialize RAG 
        logger.info("Initializing RAG...") 
        from initialize_rag import initialize_rag 
        success = initialize_rag() 
        logger.info(f"RAG initialization: {'SUCCESS' if success else 'FAILED'}") 
 
        # Add RAG to HybridEngine 
        logger.info("Extending HybridEngine with RAG...") 
        from add_rag_to_hybrid_engine import add_rag_to_hybrid_engine 
        rag_success = add_rag_to_hybrid_engine() 
        logger.info(f"RAG integration: {'SUCCESS' if rag_success else 'FAILED'}") 
 
        return success and rag_success 
    except Exception as e: 
        logger.error(f"Error setting up RAG: {str(e)}") 
        return False 
 
if __name__ == "__main__": 
    print("=== RAG Setup Inside Container ===") 
    success = setup_rag_in_container() 
    print(f"RAG setup: {'SUCCESSFUL' if success else 'FAILED'}") 
    sys.exit(0 if success else 1) 
