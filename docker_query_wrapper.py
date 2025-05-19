#!/usr/bin/env python
"""
Docker Query Wrapper for HybridEngine RAG Integration

This script provides a more reliable approach to integrate RAG capabilities
with the HybridEngine by directly importing and extending the HybridEngine class,
rather than trying to patch methods at runtime.
"""
import os
import sys
import logging
import importlib
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("docker_query_wrapper")

class RAGQueryIntegration:
    """Helper class to query the RAG system"""
    
    def __init__(self, persist_directory=None):
        """Initialize the RAG system"""
        self.vector_store = None
        self.persist_directory = persist_directory or os.environ.get('RAG_PERSIST_DIR', './data/chromadb')
        self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize the RAG system"""
        try:
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
            # Create the persist directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Load vector store if it exists
            if os.path.exists(self.persist_directory):
                logger.info(f"Loading existing vector store from {self.persist_directory}")
                self.vector_store = Chroma(
                    embedding_function=embeddings,
                    persist_directory=self.persist_directory
                )
                logger.info("Successfully loaded RAG vector store")
            else:
                logger.warning(f"No vector store found at {self.persist_directory}")
                logger.info("Please run rag_database_creator.py to create the vector store")
        except Exception as e:
            logger.error(f"Error initializing RAG: {str(e)}")
            self.vector_store = None
    
    def query(self, query_text: str, k: int = 3) -> List[str]:
        """
        Query the RAG system
        
        Args:
            query_text: Natural language query
            k: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        if not self.vector_store:
            logger.warning("RAG system not initialized")
            return []
            
        try:
            # Get similar documents
            docs = self.vector_store.similarity_search(query_text, k=k)
            
            # Extract content from documents
            results = [doc.page_content for doc in docs]
            
            logger.info(f"RAG query returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            return []

# Create a singleton instance of RAG integration
rag_integration = RAGQueryIntegration()

# Import and extend HybridEngine
try:
    logger.info("Importing HybridEngine...")
    
    # Add app directory to path if needed
    if os.path.exists('/app') and '/app' not in sys.path:
        sys.path.append('/app')
    
    # Import the original HybridEngine
    from api.inference_engine.hybrid_engine import HybridEngine as OriginalHybridEngine

    class EnhancedHybridEngine(OriginalHybridEngine):
        """Enhanced HybridEngine with RAG capabilities"""
        
        def __init__(self, *args, **kwargs):
            """Initialize the enhanced engine"""
            super().__init__(*args, **kwargs)
            logger.info("Initialized EnhancedHybridEngine with RAG capabilities")
            
        def query(self, query_type: str, params: Optional[Dict] = None) -> Dict[str, Any]:
            """
            Enhanced query method that incorporates RAG results
            
            Args:
                query_type: Type of query to process
                params: Parameters for the query
                
            Returns:
                dict: Results of the query with RAG enhancement
            """
            logger.info(f"RAG-enhanced query: {query_type} with params: {params}")
            
            # Get the user's query text
            user_query = params.get("message") or params.get("query") if params else None
            
            # First check if we can get relevant information from RAG
            rag_context = None
            if user_query:
                logger.info(f"Querying RAG system with: {user_query}")
                rag_results = rag_integration.query(user_query)
                
                if rag_results:
                    rag_context = "\n\n".join(rag_results)
                    logger.info(f"RAG context found, {len(rag_context)} characters")
                else:
                    logger.info("No RAG context found")
            
            # Call the original query method from the parent class
            result = super().query(query_type, params)
            
            # Enhance the response with RAG if we have context and Ollama is available
            if rag_context and hasattr(self, 'ollama_handler') and self.ollama_handler:
                logger.info("Using RAG context with Ollama...")
                
                # Only proceed if Ollama handler is initialized
                if self.ollama_handler._initialization_complete.is_set():
                    # Create an enhanced prompt with RAG context
                    enhanced_prompt = f"""Based on the following information from our knowledge base, 
                    answer the user's question: {user_query}

                    KNOWLEDGE BASE INFORMATION:
                    {rag_context}

                    Answer with detailed, accurate information from the knowledge base."""
                    
                    # Get an enhanced response from Ollama
                    enhanced_response = self.ollama_handler.generate_response(enhanced_prompt)
                    
                    if enhanced_response:
                        # Replace the response with the enhanced version
                        result["response"] = enhanced_response
                        result["source"] = "rag_enhanced"
                        logger.info("Response enhanced with RAG context")
            
            return result

    # Replace the original HybridEngine with our enhanced version
    logger.info("Replacing original HybridEngine with EnhancedHybridEngine...")
    import api.inference_engine.hybrid_engine
    api.inference_engine.hybrid_engine.HybridEngine = EnhancedHybridEngine
    
    # Also make EnhancedHybridEngine available for import
    sys.modules['api.inference_engine.hybrid_engine'].HybridEngine = EnhancedHybridEngine
    
    logger.info("Successfully replaced HybridEngine with RAG-enhanced version")

except ImportError as e:
    logger.error(f"Failed to import HybridEngine: {str(e)}")
except Exception as e:
    logger.error(f"Error setting up EnhancedHybridEngine: {str(e)}")

# Entry point for direct execution
if __name__ == "__main__":
    print("===== Docker Query Wrapper for RAG =====")
    print("RAG integration complete. HybridEngine has been enhanced with RAG capabilities.")
    print("The system will now use RAG to enhance query responses.") 