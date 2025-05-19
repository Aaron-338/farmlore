#!/usr/bin/env python
"""
Docker Query Wrapper V2 for HybridEngine RAG Integration

This script provides a more reliable approach to integrate RAG capabilities
with the HybridEngine by directly modifying the module-level HybridEngine class.
"""
import os
import sys
import logging
import importlib
import inspect
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("docker_query_wrapper_v2")

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

def apply_rag_direct():
    """Apply the RAG enhancement directly to HybridEngine class"""
    
    # Add app directory to path if needed
    if os.path.exists('/app') and '/app' not in sys.path:
        sys.path.append('/app')
    
    try:
        # Import the module that contains HybridEngine
        import api.inference_engine.hybrid_engine as engine_module
        
        # Get the original HybridEngine class
        HybridEngine = engine_module.HybridEngine
        
        # Check if the integration has already been applied
        if hasattr(HybridEngine, '_rag_enhanced'):
            logger.info("RAG enhancement already applied to HybridEngine")
            return True
            
        # Create RAG integration singleton
        rag_integration = RAGQueryIntegration()
        
        # Store the original query method
        original_query = HybridEngine.query
        
        # Define the enhanced query method
        def enhanced_query(self, query_type, params=None):
            logger.info(f"RAG-enhanced query called: {query_type} with params: {params}")
            
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
            
            # Call the original query method
            result = original_query(self, query_type, params)
            
            # Enhance the response with RAG if we have context and Ollama is available
            if rag_context and hasattr(self, 'ollama_handler') and self.ollama_handler:
                logger.info("Using RAG context with Ollama...")
                
                # Only proceed if Ollama handler is initialized
                is_ready, _ = self.is_initialization_complete()
                if is_ready:
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

        # Add RAG system and tag as properties to the HybridEngine class
        HybridEngine.rag_system = property(lambda self: rag_integration)
        HybridEngine._rag_enhanced = True
        
        # Replace the query method with our enhanced version
        HybridEngine.query = enhanced_query
        
        logger.info("Successfully applied RAG enhancement to HybridEngine")
        return True
            
    except ImportError as e:
        logger.error(f"Failed to import HybridEngine module: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error enhancing HybridEngine: {str(e)}")
        return False

def apply_direct_monkey_patch():
    """Apply direct monkey patching to the running HybridEngine instance"""
    
    # Add app directory to path if needed
    if os.path.exists('/app') and '/app' not in sys.path:
        sys.path.append('/app')
    
    try:
        # Import the module that contains HybridEngine
        from api.inference_engine import hybrid_engine
        
        # Create RAG integration singleton
        rag_integration = RAGQueryIntegration()
        
        # Check if we have a HybridEngine instance in the module
        engine_instances = []
        for name, obj in inspect.getmembers(hybrid_engine):
            if isinstance(obj, hybrid_engine.HybridEngine):
                engine_instances.append((name, obj))
        
        if not engine_instances:
            logger.warning("No existing HybridEngine instance found")
            # We'll still apply the class-level enhancement
        else:
            logger.info(f"Found {len(engine_instances)} HybridEngine instances")
            for name, engine in engine_instances:
                logger.info(f"Enhancing instance: {name}")
                
                # Attach RAG system directly to the instance
                engine.rag_system = rag_integration
                
                # Store the original query method for this instance
                original_query = engine.query
                
                # Define an enhanced query method as a closure over this instance's original method
                def make_enhanced_query(orig_query):
                    def enhanced_query(query_type, params=None):
                        logger.info(f"Instance RAG-enhanced query called: {query_type}")
                        
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
                        
                        # Call the original query method
                        result = orig_query(query_type, params)
                        
                        # Enhance the response with RAG if we have context and Ollama is available
                        if rag_context and hasattr(engine, 'ollama_handler') and engine.ollama_handler:
                            logger.info("Using RAG context with Ollama...")
                            
                            # Only proceed if Ollama handler is initialized
                            is_ready, _ = engine.is_initialization_complete()
                            if is_ready:
                                # Create an enhanced prompt with RAG context
                                enhanced_prompt = f"""Based on the following information from our knowledge base, 
                                answer the user's question: {user_query}

                                KNOWLEDGE BASE INFORMATION:
                                {rag_context}

                                Answer with detailed, accurate information from the knowledge base."""
                                
                                # Get an enhanced response from Ollama
                                enhanced_response = engine.ollama_handler.generate_response(enhanced_prompt)
                                
                                if enhanced_response:
                                    # Replace the response with the enhanced version
                                    result["response"] = enhanced_response
                                    result["source"] = "rag_enhanced"
                                    logger.info("Response enhanced with RAG context")
                        
                        return result
                    return enhanced_query
                
                # Apply the enhanced method to this instance
                engine.query = make_enhanced_query(original_query)
                logger.info(f"Enhanced query method applied to instance {name}")
        
        # Now apply the class-level enhancement
        return apply_rag_direct()
            
    except ImportError as e:
        logger.error(f"Failed to import HybridEngine module for instance patching: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error enhancing HybridEngine instances: {str(e)}")
        return False

if __name__ == "__main__":
    print("===== Docker Query Wrapper V2 for RAG =====")
    
    # Apply both instance-level and class-level enhancements
    instance_result = apply_direct_monkey_patch()
    class_result = apply_rag_direct()
    
    if instance_result and class_result:
        print("✅ RAG integration successful! Both instance and class enhanced.")
    elif class_result:
        print("⚠️ Partial success: Class enhanced, but no instances found to enhance.")
    else:
        print("❌ Failed to apply RAG enhancements.")
    
    print("The system will now use RAG to enhance query responses.") 