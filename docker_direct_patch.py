#!/usr/bin/env python
"""
Direct patch script to modify the HybridEngine inside the Docker container
to properly integrate RAG capabilities.
"""

import os
import sys
import logging
import importlib
import inspect
import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_direct_patch")

def apply_direct_patch():
    """
    Apply a direct patch to the HybridEngine to integrate RAG
    by monkey patching its methods in memory.
    """
    try:
        # Step 1: Import necessary modules
        logger.info("Importing HybridEngine...")
        sys.path.append('/app')
        
        # Import the actual HybridEngine class
        from api.inference_engine.hybrid_engine import HybridEngine
        
        # Import the RAG implementation
        from api.inference_engine.implement_rag import get_rag_system
        
        # Step 2: Access the HybridEngine instance
        logger.info("Accessing HybridEngine instance...")
        try:
            from api.inference_engine import hybrid_engine
            engine_instance = hybrid_engine
            logger.info("Successfully accessed existing HybridEngine instance")
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to access existing HybridEngine instance: {str(e)}")
            logger.info("Creating a temporary HybridEngine instance for patching...")
            engine_instance = HybridEngine()
        
        # Step 3: Create the RAG system
        logger.info("Creating RAG system...")
        rag_system = get_rag_system()
        if not rag_system:
            logger.error("Failed to create RAG system")
            return False
        
        # Attach RAG system to the engine instance
        engine_instance.rag_system = rag_system
        logger.info("RAG system attached to HybridEngine")
        
        # Step 4: Inspect the HybridEngine to find its methods
        logger.info("Inspecting HybridEngine methods...")
        
        # Get all methods of the instance
        methods = [m for m in dir(engine_instance) if callable(getattr(engine_instance, m))]
        logger.info(f"Available methods: {methods}")
        
        # Look for query-related methods
        query_methods = [m for m in methods if any(x in m.lower() for x in ['query', 'process', 'pest', 'management', 'control'])]
        logger.info(f"Potential query methods: {query_methods}")
        
        # Check if we found the methods we need
        if not query_methods:
            logger.error("Could not find any query-related methods in HybridEngine")
            return False
            
        # Step 5: Find the main entry point method(s)
        # We'll try to identify the main entry point based on the known method names
        main_method = None
        for method_name in ['query', '_process_general_query', '_process_query', '_process_query_by_type']:
            if method_name in methods:
                logger.info(f"Found main entry method: {method_name}")
                main_method = method_name
                break
        
        if not main_method:
            # If we couldn't find a known method, look for _process methods
            process_methods = [m for m in methods if m.startswith('_process_')]
            if process_methods:
                logger.info(f"Found process methods: {process_methods}")
                # The process_query_by_type method is a good candidate if available
                if '_process_query_by_type' in process_methods:
                    main_method = '_process_query_by_type'
                    logger.info(f"Using {main_method} as main entry point")
                else:
                    # Use the first process method as the main entry point
                    main_method = process_methods[0]
                    logger.info(f"Using {main_method} as main entry point")
        
        # Step 6: Patch identified methods with RAG
        if main_method:
            # Get the original method
            original_method = getattr(engine_instance, main_method)
            
            # Define the enhanced method
            def enhanced_method(self, *args, **kwargs):
                """Enhanced method with RAG capabilities"""
                logger.info(f"Enhanced {main_method} called with args: {args}, kwargs: {kwargs}")
                
                # Extract the user query from the arguments
                user_query = None
                params = None
                
                # Try to extract from args based on position
                if args and len(args) > 0:
                    # If args[0] is a dict, it might be the params
                    if isinstance(args[0], dict):
                        params = args[0]
                        user_query = params.get("message") or params.get("query")
                    # If there are 2+ args and the second is a dict, it could be params
                    elif len(args) > 1 and isinstance(args[1], dict):
                        params = args[1]
                        user_query = params.get("message") or params.get("query")
                
                # Try to extract from kwargs
                if not user_query and "params" in kwargs:
                    params = kwargs["params"]
                    user_query = params.get("message") or params.get("query")
                
                # Add RAG context if applicable
                if user_query and hasattr(self, 'rag_system') and self.rag_system:
                    try:
                        logger.info(f"Querying RAG system with: {user_query}")
                        rag_results = self.rag_system.query(user_query)
                        
                        if rag_results:
                            context = "\n\n".join(rag_results)
                            logger.info(f"RAG found relevant information ({len(context)} chars)")
                            
                            # Modify the arguments to include RAG context
                            if params:
                                params['rag_context'] = context
                            
                            # If we're using Ollama, try to include the context in the query
                            if hasattr(self, 'ollama_handler') and self.ollama_handler:
                                original_query = user_query
                                if params:
                                    params['original_query'] = original_query
                                    params['query'] = f"Based on this information:\n{context}\n\nUser's question: {original_query}"
                    except Exception as e:
                        logger.error(f"Error in RAG query: {str(e)}")
                
                # Call the original method
                result = original_method(*args, **kwargs)
                
                # Add RAG info to the result if it wasn't already used
                if user_query and hasattr(self, 'rag_system') and self.rag_system and isinstance(result, dict):
                    try:
                        if 'response' in result and result.get('source') != 'ollama':
                            rag_results = self.rag_system.query(user_query)
                            if rag_results:
                                context = "\n\n".join(rag_results)
                                result['response'] = result['response'] + "\n\nAdditional relevant information:\n" + context
                                result['source'] = f"{result.get('source', 'unknown')}_with_rag"
                    except Exception as e:
                        logger.error(f"Error adding RAG info to result: {str(e)}")
                
                return result
            
            # Bind the enhanced method to the engine instance
            setattr(engine_instance, main_method, types.MethodType(enhanced_method, engine_instance))
            logger.info(f"Successfully patched {main_method} with RAG capabilities")
            
            # If we patched _process_query_by_type, also patch the specific processing methods
            if main_method == '_process_query_by_type':
                # Look for specific process methods to patch
                specific_methods = [
                    '_process_general_query',
                    '_process_pest_identification',
                    '_process_control_methods',
                    '_process_indigenous_knowledge',
                    '_process_crop_pests'
                ]
                
                for method_name in specific_methods:
                    if hasattr(engine_instance, method_name):
                        logger.info(f"Patching specific method: {method_name}")
                        # Store original method
                        original_specific = getattr(engine_instance, method_name)
                        
                        # Define enhanced method
                        def enhance_specific_method(original_method, method_name):
                            def wrapper(self, params, attempt_ollama_call):
                                """Enhanced specific method with RAG"""
                                logger.info(f"Enhanced {method_name} called")
                                
                                # Extract RAG context if available
                                rag_context = params.pop('rag_context', None) if params else None
                                
                                # If we have RAG context and using Ollama would be good, ensure we do
                                if rag_context:
                                    attempt_ollama_call = True
                                
                                # Call the original method
                                result = original_method(params, attempt_ollama_call)
                                
                                # Add RAG context to the result if not already using Ollama
                                if rag_context and 'response' in result and result.get('source') != 'ollama':
                                    result['response'] = result['response'] + "\n\nAdditional relevant information:\n" + rag_context
                                    result['source'] = f"{result.get('source', 'unknown')}_with_rag"
                                    logger.info(f"Enhanced {method_name} response with RAG context")
                                
                                return result
                            return wrapper
                        
                        # Bind the enhanced method
                        enhanced_specific = enhance_specific_method(original_specific, method_name)
                        setattr(engine_instance, method_name, types.MethodType(enhanced_specific, engine_instance))
                        logger.info(f"Successfully patched {method_name}")
                
                logger.info("Successfully patched all specific processing methods")
        else:
            logger.error("Could not identify a main entry point method to patch")
            return False
        
        # Step 7: Test the patched engine
        logger.info("Testing the patched engine...")
        try:
            # Test the RAG system directly first
            test_query = "How to control aphids on roses"
            logger.info(f"Testing RAG with query: {test_query}")
            
            rag_results = engine_instance.rag_system.query(test_query)
            if rag_results:
                logger.info(f"RAG system found {len(rag_results)} results")
                logger.info(f"First result sample: {rag_results[0][:100]}...")
            else:
                logger.warning("RAG system returned no results")
            
            # Test calling a method on the engine
            if main_method == '_process_query_by_type':
                # This requires specific parameters
                logger.info("Testing _process_query_by_type with general_query...")
                test_params = {"query": test_query}
                try:
                    result = engine_instance._process_query_by_type("general_query", test_params, True)
                    logger.info(f"Test query result source: {result.get('source', 'unknown')}")
                    logger.info(f"Test query result sample: {result.get('response', '')[:100]}...")
                except Exception as e:
                    logger.error(f"Error testing _process_query_by_type: {str(e)}")
            
            logger.info("RAG patch testing completed")
            return True
        except Exception as e:
            logger.error(f"Error testing patched engine: {str(e)}")
            return False
        
    except Exception as e:
        logger.error(f"Error applying direct patch: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting direct patching of HybridEngine...")
    success = apply_direct_patch()
    if success:
        logger.info("HybridEngine successfully patched with RAG capabilities!")
    else:
        logger.error("Failed to patch HybridEngine") 