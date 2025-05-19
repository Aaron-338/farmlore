import logging
from typing import Dict, Any, Optional
from implement_rag import PrologToRAGConverter, RAGQuery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridEnginePatch:
    """
    This class provides patches to integrate RAG capabilities into the existing HybridEngine.
    Instead of modifying the HybridEngine directly, this approach allows for easier testing
    and rollback if needed.
    """
    
    @staticmethod
    def initialize_rag_system(hybrid_engine):
        """
        Initialize the RAG system and attach it to the HybridEngine
        
        Args:
            hybrid_engine: Instance of HybridEngine to patch
        """
        logger.info("Initializing RAG system for HybridEngine")
        
        try:
            # Create the RAG converter
            converter = PrologToRAGConverter()
            
            # Process all knowledge bases and create vector store
            vector_store = converter.process_all_knowledge_bases()
            
            if not vector_store:
                logger.error("Failed to create vector store for RAG system")
                return
            
            # Create RAG query system
            rag_system = RAGQuery(vector_store)
            
            # Attach RAG system to HybridEngine
            hybrid_engine.rag_system = rag_system
            
            logger.info("RAG system successfully attached to HybridEngine")
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {str(e)}")
    
    @staticmethod
    def patch_process_general_query(hybrid_engine):
        """
        Patch the _process_general_query method to use RAG for queries
        
        Args:
            hybrid_engine: Instance of HybridEngine to patch
        """
        # Store the original method
        original_process_general_query = hybrid_engine._process_general_query
        
        # Define the patched method
        def patched_process_general_query(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
            """
            Patched version of _process_general_query that incorporates RAG
            """
            logger.info("Using patched _process_general_query with RAG capabilities")
            
            # Try to extract Prolog information first (first part of original method)
            prolog_data_found = False
            prolog_info_parts = []
            
            # Get the query
            user_query = params.get("query", "") or params.get("message", "")
            
            if not user_query:
                return {
                    "response": "I couldn't understand your query. Please provide a clearer question.",
                    "source": "error_no_query"
                }
            
            # Try RAG before falling back to Ollama
            if hasattr(self, 'rag_system'):
                try:
                    logger.info(f"Querying RAG system with: {user_query}")
                    rag_results = self.rag_system.query(user_query)
                    
                    if rag_results:
                        # Format RAG results
                        combined_result = "Based on our knowledge base:\n\n" + "\n\n".join(rag_results)
                        return {"response": combined_result, "source": "rag"}
                    else:
                        logger.info("RAG system returned no results")
                except Exception as e:
                    logger.error(f"Error querying RAG system: {str(e)}")
            
            # If RAG didn't produce results, fall back to original method
            return original_process_general_query(self, params, attempt_ollama_call)
        
        # Replace the original method with the patched one
        hybrid_engine._process_general_query = patched_process_general_query.__get__(hybrid_engine)
        
        logger.info("Successfully patched _process_general_query method")
    
    @staticmethod
    def apply_patches(hybrid_engine):
        """
        Apply all patches to the HybridEngine
        
        Args:
            hybrid_engine: Instance of HybridEngine to patch
        """
        logger.info("Applying RAG patches to HybridEngine")
        
        # Initialize the RAG system
        HybridEnginePatch.initialize_rag_system(hybrid_engine)
        
        # Patch methods
        HybridEnginePatch.patch_process_general_query(hybrid_engine)
        
        logger.info("All RAG patches applied to HybridEngine")

if __name__ == "__main__":
    # This would be used in the main application code
    """
    from api.inference_engine.hybrid_engine import HybridEngine
    from hybrid_engine_patch import HybridEnginePatch
    
    # Initialize the hybrid engine as usual
    engine = HybridEngine()
    
    # Apply RAG patches
    HybridEnginePatch.apply_patches(engine)
    
    # Continue with normal initialization
    """
    pass 