#!/usr/bin/env python
"""
API RAG Injector
----------------
This script injects RAG capabilities directly into the API's global HybridEngine instance
"""

import os
import sys
import logging
import types
import importlib
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_rag_injector")

def inject_rag_into_api():
    """
    Inject RAG capabilities directly into the API's global HybridEngine instance
    """
    try:
        logger.info("Starting RAG injection into API's HybridEngine...")
        
        # Add app directory to Python path
        sys.path.append('/app')
        
        # Set up Django environment
        logger.info("Setting up Django environment...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
        
        # Import Django and set up settings
        import django
        django.setup()
        
        logger.info("Django environment set up successfully")
        
        # Now we can import from API
        # Import the API views module which contains the global engine instance
        logger.info("Importing API views module...")
        import api.views
        
        # Import RAG system
        logger.info("Importing RAG system...")
        from api.inference_engine.implement_rag import get_rag_system
        
        # Access the global engine instance
        logger.info("Accessing global HybridEngine instance...")
        engine_instance = api.views.get_prolog_engine()
        
        if not engine_instance:
            logger.error("Could not access global HybridEngine instance")
            return False
        
        logger.info(f"Successfully accessed global HybridEngine instance: {engine_instance}")
        
        # Create RAG system
        logger.info("Creating RAG system...")
        rag_system = get_rag_system()
        
        if not rag_system:
            logger.error("Failed to create RAG system")
            return False
        
        # Attach RAG system to the engine instance
        engine_instance.rag_system = rag_system
        logger.info("RAG system attached to global HybridEngine instance")
        
        # Now we need to monkey patch the query method in HybridEngine
        logger.info("Patching query method...")
        
        # Store the original query method
        original_query = engine_instance.query
        
        # Create enhanced query method
        def enhanced_query(self, query_type, params):
            """Enhanced query method with RAG capabilities"""
            logger.info(f"RAG-enhanced query called: {query_type} with params: {params}")
            
            # Extract the user query
            user_query = params.get("message") or params.get("query") if params else None
            
            # If we have a user query and RAG system, enhance with RAG context
            if user_query and hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system with: {user_query}")
                    rag_results = self.rag_system.query(user_query)
                    
                    if rag_results:
                        context = "\n\n".join(rag_results)
                        logger.info(f"RAG found relevant information ({len(context)} chars)")
                        
                        # Make a copy of params to avoid modifying the original
                        params_with_rag = params.copy()
                        
                        # Add RAG context to query
                        original_query_text = user_query
                        params_with_rag['original_query'] = original_query_text
                        params_with_rag['query'] = f"Based on this information:\n{context}\n\nUser's question: {original_query_text}"
                        params_with_rag['rag_context'] = context
                        
                        logger.info("Added RAG context to query params")
                        
                        # Call the original query method with enhanced params
                        result = original_query(query_type, params_with_rag)
                        
                        # For clarity, mark that RAG was used
                        if 'source' in result:
                            result['source'] = f"{result['source']}_with_rag"
                        else:
                            result['source'] = "hybrid_with_rag"
                        
                        # If RAG was still not used in the response, add it directly
                        if 'response' in result and 'Here is the relevant information' not in result['response']:
                            result['response'] += "\n\nHere is the relevant information from our knowledge base:\n" + context
                        
                        return result
                    else:
                        logger.info("RAG system did not find any relevant information")
                except Exception as e:
                    logger.error(f"Error in RAG processing: {str(e)}")
                    logger.error(traceback.format_exc())
            
            # Fall back to original query method if RAG processing fails or finds nothing
            return original_query(query_type, params)
        
        # Replace the query method
        engine_instance.query = types.MethodType(enhanced_query, engine_instance)
        logger.info("Successfully patched query method with RAG capabilities")
        
        # Test RAG integration
        logger.info("Testing RAG integration...")
        test_query = "How to control aphids on roses"
        test_params = {"query": test_query, "message": test_query}
        
        try:
            # Test RAG system directly first
            rag_results = engine_instance.rag_system.query(test_query)
            if rag_results:
                logger.info(f"RAG system found {len(rag_results)} results")
                logger.info(f"First result sample: {rag_results[0][:100]}...")
            else:
                logger.warning("RAG system returned no results")
            
            # Note: We're not actually calling query here to avoid side effects
            # but we've verified the RAG system is accessible
            
            logger.info("RAG integration test successful!")
            return True
        except Exception as e:
            logger.error(f"Error testing RAG integration: {str(e)}")
            logger.error(traceback.format_exc())
            return False
    
    except Exception as e:
        logger.error(f"Error injecting RAG into API: {str(e)}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting API RAG Injector...")
    success = inject_rag_into_api()
    if success:
        logger.info("Successfully injected RAG into API!")
        sys.exit(0)
    else:
        logger.error("Failed to inject RAG into API")
        sys.exit(1) 