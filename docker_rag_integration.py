#!/usr/bin/env python3
"""
Docker-specific RAG integration script.
This script can be copied and run inside a Docker container to enable RAG.
"""
import os
import sys
import logging
import types
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def integrate_rag_in_docker():
    """
    Directly integrate RAG into the HybridEngine when running in Docker.
    This doesn't require modifying files on disk.
    """
    try:
        # Enable RAG
        os.environ['USE_RAG'] = 'true'
        
        # Set the ChromaDB persistence directory
        if 'RAG_PERSIST_DIR' not in os.environ:
            os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the directory if it doesn't exist
        os.makedirs(os.environ['RAG_PERSIST_DIR'], exist_ok=True)
        
        # Import required modules
        try:
            # Add the parent directory to sys.path to allow importing from api package
            sys.path.append('/app')
            
            from api.inference_engine.hybrid_engine import HybridEngine
            try:
                from api.inference_engine.implement_rag import extend_hybrid_engine, get_rag_system
                rag_module_found = True
            except ImportError:
                logger.warning("Could not import implement_rag. RAG module may not be fully installed.")
                rag_module_found = False
                
            try:
                from api.inference_engine.prompt_templates import PromptType, format_prompt
                prompt_module_found = True
            except ImportError:
                logger.warning("Could not import prompt_templates. Will use fallback approach.")
                prompt_module_found = False
            
        except ImportError as e:
            logger.error(f"Failed to import required modules: {str(e)}")
            return False
        
        # Get HybridEngine instance
        try:
            from api.inference_engine import hybrid_engine
            engine = hybrid_engine
            logger.info("Found existing HybridEngine instance")
        except (ImportError, AttributeError):
            logger.info("Creating new HybridEngine instance")
            engine = HybridEngine()
        
        if rag_module_found:
            # Extend with RAG using the existing method
            try:
                # Only extend if not already extended
                if not hasattr(engine, 'rag_system'):
                    logger.info("Extending HybridEngine with RAG using existing method")
                    extend_hybrid_engine(engine)
                else:
                    logger.info("HybridEngine already has RAG system attached")
            except Exception as e:
                logger.error(f"Error extending HybridEngine with RAG: {str(e)}")
                # Continue with our custom integration
        
        # Create our custom integration
        logger.info("Setting up custom RAG integration")
        
        # Store original methods if not already stored
        if not hasattr(engine, '_original_process_general_query'):
            engine._original_process_general_query = engine._process_general_query
        
        # Define enhanced query method using RAG
        def enhanced_general_query(self, params, attempt_ollama_call):
            """Enhanced version of _process_general_query that incorporates RAG"""
            logger.info("Using RAG-enhanced general query processor (Docker version)")
            
            # Get the user query
            user_query = params.get("query", "") or params.get("message", "")
            
            if not user_query:
                return {
                    "response": "I couldn't understand your query. Please provide a clearer question.",
                    "source": "error_no_query"
                }
            
            # Try RAG first if available
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system for general query: {user_query}")
                    rag_results = self.rag_system.query(user_query, k=3)
                    
                    if rag_results:
                        logger.info(f"RAG found {len(rag_results)} relevant results")
                        # Format RAG results
                        combined_result = "Based on our knowledge base:\n\n" + "\n\n".join(rag_results)
                        
                        # If Ollama is available, use it to refine the response
                        if attempt_ollama_call and self.ollama_handler:
                            logger.info("Using Ollama to refine RAG results")
                            
                            # Create context combining RAG results and user query
                            ollama_context = f"Based on our knowledge base:\n\n{combined_result}\n\nUser query: {user_query}\n\nPlease provide a comprehensive answer to the user's query using the information above."
                            
                            # Use existing format_prompt if available
                            if prompt_module_found:
                                prompt_content = format_prompt(
                                    PromptType.GENERAL,
                                    query=ollama_context
                                )
                                prompt = prompt_content["user_prompt"]
                            else:
                                # Simple fallback prompt
                                prompt = f"Answer this question based on the following information:\n\n{combined_result}\n\nQuestion: {user_query}"
                            
                            # Generate response
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt,
                                query_type="pest_management"
                            )
                            
                            if llm_response and llm_response.strip():
                                logger.info("Successfully refined RAG results with Ollama")
                                return {"response": llm_response, "source": "rag_ollama"}
                        
                        # If Ollama refinement wasn't attempted or failed, return RAG results directly
                        return {"response": combined_result, "source": "rag"}
                    else:
                        logger.info("RAG found no relevant results")
                except Exception as e:
                    logger.error(f"Error querying RAG system: {str(e)}")
            
            # Fall back to original method if RAG didn't provide results
            logger.info("RAG processing failed or found no results, falling back to original method")
            return self._original_process_general_query(params, attempt_ollama_call)
        
        # Replace the original method with the enhanced version
        logger.info("Replacing _process_general_query method with RAG-enhanced version")
        engine._process_general_query = types.MethodType(enhanced_general_query, engine)
        
        logger.info("Successfully integrated RAG into HybridEngine in Docker environment")
        return True
        
    except Exception as e:
        logger.error(f"Error integrating RAG in Docker: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Integrating RAG in Docker environment...")
    success = integrate_rag_in_docker()
    if success:
        print("✓ RAG successfully integrated in Docker!")
        print("\nTo verify it's working, check if your queries are answered with 'Based on our knowledge base:'")
    else:
        print("⚠ Failed to integrate RAG in Docker. See logs for details.") 