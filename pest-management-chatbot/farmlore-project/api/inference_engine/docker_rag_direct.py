#!/usr/bin/env python
"""
Docker RAG Direct - A straightforward script that directly uses RAG
without trying to modify the HybridEngine.

This script provides a direct route to using RAG capabilities in the Docker container.
"""
import os
import sys
import logging
from typing import List, Dict, Any, Optional
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("docker_rag_direct")

class RAGDirectSystem:
    """A direct RAG system that doesn't rely on modifying HybridEngine"""
    
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

# Create a singleton instance
rag_system = RAGDirectSystem()

def inject_rag_into_api():
    """
    Inject RAG directly into the API views without modifying HybridEngine
    """
    try:
        # Add app directory to path if needed
        if os.path.exists('/app') and '/app' not in sys.path:
            sys.path.append('/app')
            
        # Import the views module where the chat endpoint is defined
        import api.views
        
        # Store the original handle_chat function
        original_handle_chat = api.views.handle_chat
        
        # Define the enhanced handle_chat function
        @wraps(original_handle_chat)
        def enhanced_handle_chat(request):
            """Enhanced version of handle_chat with RAG capabilities"""
            try:
                # Get the message from the request
                import json
                data = json.loads(request.body.decode('utf-8'))
                message = data.get('message', '')
                
                if message:
                    logger.info(f"Processing chat request with message: {message}")
                    
                    # Query RAG for relevant information
                    rag_results = rag_system.query(message)
                    
                    if rag_results:
                        # We have RAG results, enhance the message with context
                        context = "\n\n".join(rag_results)
                        logger.info(f"Found RAG context ({len(context)} chars) for message: {message}")
                        
                        # Get the hybrid engine to use for Ollama
                        from api.inference_engine.hybrid_engine import HybridEngine
                        engine = HybridEngine()
                        
                        # Wait for Ollama to be ready
                        is_ready, _ = engine.is_initialization_complete(wait_timeout=30.0)
                        
                        if is_ready and engine.ollama_handler:
                            # Create an enhanced prompt with RAG context
                            enhanced_prompt = f"""Based on the following information from our knowledge base, 
                            answer the user's question: {message}

                            KNOWLEDGE BASE INFORMATION:
                            {context}

                            Answer with detailed, accurate information from the knowledge base."""
                            
                            # Use Ollama directly
                            rag_response = engine.ollama_handler.generate_response(enhanced_prompt)
                            
                            if rag_response:
                                # Return the RAG-enhanced response directly
                                logger.info("Returning RAG-enhanced response")
                                from django.http import JsonResponse
                                return JsonResponse({
                                    "response": rag_response,
                                    "source": "rag_direct",
                                    "success": True
                                })
            except Exception as e:
                logger.error(f"Error in RAG enhancement: {str(e)}")
            
            # Call the original function
            return original_handle_chat(request)
        
        # Replace the original function with our enhanced version
        api.views.handle_chat = enhanced_handle_chat
        logger.info("Successfully injected RAG into API views")
        return True
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error injecting RAG into API: {str(e)}")
        return False

def test_rag():
    """Test if the RAG system is working"""
    query = "How do I control aphids on tomatoes?"
    logger.info(f"Testing RAG with query: {query}")
    
    results = rag_system.query(query)
    if results:
        logger.info(f"RAG test successful! Found {len(results)} results")
        for i, result in enumerate(results, 1):
            logger.info(f"Result {i}: {result[:200]}...")
        return True
    else:
        logger.warning("RAG test did not return any results")
        return False

if __name__ == "__main__":
    print("===== Docker RAG Direct =====")
    
    # Test RAG
    rag_test_result = test_rag()
    print(f"RAG test: {'SUCCESS' if rag_test_result else 'FAILED'}")
    
    # Inject RAG into API
    api_inject_result = inject_rag_into_api()
    print(f"API injection: {'SUCCESS' if api_inject_result else 'FAILED'}")
    
    if rag_test_result and api_inject_result:
        print("\n✅ RAG Direct installation successful!")
        print("The system will now use RAG to enhance query responses without modifying HybridEngine.")
    else:
        print("\n⚠️ RAG Direct installation partially successful.")
        print("Check the logs for more information.") 