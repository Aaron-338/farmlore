"""
Script to integrate the RAG (Retrieval-Augmented Generation) system into the standard query pipeline
of the HybridEngine.

This script patches the HybridEngine methods to use RAG capabilities for all supported query types.
"""

import os
import logging
import types
import importlib
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def integrate_rag_into_query_pipeline():
    """
    Integrate RAG capabilities into the HybridEngine's query pipeline for all relevant query types.
    """
    try:
        logger.info("Starting RAG integration into the query pipeline...")
        
        # Import required modules
        try:
            # Import HybridEngine class and the getter for the shared instance
            from api.views import get_prolog_engine # Changed import
            from api.inference_engine.hybrid_engine import HybridEngine # Keep for type hinting if needed
            from api.inference_engine.implement_rag import extend_hybrid_engine, get_rag_system
            from api.inference_engine.prompt_templates import PromptType, format_prompt
            
            # Store references to imported modules for use in the enhanced methods
            modules = {
                'PromptType': PromptType,
                'format_prompt': format_prompt
            }
        except ImportError as e:
            logger.error(f"Failed to import required modules: {e}. Make sure you're running this script from the correct directory.")
            return False
        
        # Get the shared HybridEngine instance from api.views
        try:
            engine_instance = get_prolog_engine() # Use the getter
            if engine_instance is None:
                logger.error("Failed to get HybridEngine instance from api.views.get_prolog_engine(). Returned None.")
                return False
            # Ensure it's the correct type, not a stub if views.py had an issue
            if not isinstance(engine_instance, HybridEngine):
                 logger.error(f"Retrieved engine is not an instance of HybridEngine, but {type(engine_instance)}. This might be a stub due to an earlier error.")
                 # Potentially, we could try to create a new one, but it's better to fix the root cause in views.py
                 return False # Exit if it's a stub or wrong type
            logger.info("Successfully retrieved shared HybridEngine instance.")
        except Exception as e:
            logger.error(f"Error getting HybridEngine instance via get_prolog_engine(): {e}")
            return False
        
        # Check if RAG system is already attached to the engine instance
        if not hasattr(engine_instance, 'rag_system'):
            # Extend the engine with RAG capabilities using existing function
            logger.info("Attaching RAG system to HybridEngine instance")
            extend_hybrid_engine(engine_instance) # Pass the instance
            
            if not hasattr(engine_instance, 'rag_system') or not engine_instance.rag_system:
                logger.error("Failed to attach RAG system to HybridEngine instance")
                return False
        else:
            logger.info("RAG system already attached to HybridEngine instance")

        # Store original processing methods on the instance
        logger.info("Storing original processing methods on the instance")
        if not hasattr(engine_instance, '_original_process_general_query'):
            if not hasattr(engine_instance, '_process_general_query'):
                logger.error("HybridEngine instance does not have attribute '_process_general_query'. Cannot proceed.")
                return False
            engine_instance._original_process_general_query = engine_instance._process_general_query
        
        if not hasattr(engine_instance, '_original_process_control_methods'): # Corrected attribute name
            if not hasattr(engine_instance, '_process_control_methods'):
                logger.warning("HybridEngine instance does not have attribute '_process_control_methods'. Skipping patch.")
            else:
                engine_instance._original_process_control_methods = engine_instance._process_control_methods
            
        if not hasattr(engine_instance, '_original_process_pest_identification'):
            if not hasattr(engine_instance, '_process_pest_identification'):
                logger.warning("HybridEngine instance does not have attribute '_process_pest_identification'. Skipping patch.")
            else:
                engine_instance._original_process_pest_identification = engine_instance._process_pest_identification
            
        if not hasattr(engine_instance, '_original_process_crop_pests'):
            if not hasattr(engine_instance, '_process_crop_pests'):
                logger.warning("HybridEngine instance does not have attribute '_process_crop_pests'. Skipping patch.")
            else:
                engine_instance._original_process_crop_pests = engine_instance._process_crop_pests
            
        if not hasattr(engine_instance, '_original_process_indigenous_knowledge'):
            if not hasattr(engine_instance, '_process_indigenous_knowledge'):
                logger.warning("HybridEngine instance does not have attribute '_process_indigenous_knowledge'. Skipping patch.")
            else:
                engine_instance._original_process_indigenous_knowledge = engine_instance._process_indigenous_knowledge
            
        if not hasattr(engine_instance, '_original_process_soil_analysis'):
            if not hasattr(engine_instance, '_process_soil_analysis'):
                logger.warning("HybridEngine instance does not have attribute '_process_soil_analysis'. Skipping patch.")
            else:
                engine_instance._original_process_soil_analysis = engine_instance._process_soil_analysis
        
        # Define enhanced methods that use RAG

        # Enhanced general query method
        def enhanced_general_query(self, params, attempt_ollama_call):
            """Enhanced version of _process_general_query that incorporates RAG"""
            logger.info("Using RAG-enhanced general query processor")
            
            # Get the user query
            user_query = params.get("query", "") or params.get("message", "")
            
            if not user_query:
                return {
                    "response": "I couldn't understand your query. Please provide a clearer question.",
                    "source": "error_no_query"
                }
            
            # Try RAG first
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
                            
                            # Get references to imported modules
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            # Create context combining RAG results and user query
                            ollama_context = f"Based on our knowledge base:\n\n{combined_result}\n\nUser query: {user_query}\n\nPlease provide a comprehensive answer to the user's query using the information above."
                            
                            # Format prompt for Ollama
                            prompt_content = format_prompt(
                                PromptType.GENERAL,
                                query=ollama_context
                            )
                            
                            # Generate response
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"],
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
        
        # Enhanced pest management method
        def enhanced_pest_management(self, params, attempt_ollama_call):
            """Enhanced version of _process_control_methods that incorporates RAG"""
            user_query = params.get("query", "") or params.get("message", "")
            pest_name = params.get("pest")
            
            # Build an optimized query for RAG
            rag_query = user_query
            if pest_name:
                rag_query = f"pest management control methods for {pest_name} " + rag_query
            
            logger.info(f"INTEGRATE_RAG: Using RAG-enhanced pest management processor with RAG query: '{rag_query}'")
            
            # Try RAG first
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"INTEGRATE_RAG: Querying RAG vector store for pest management with: '{rag_query}'")
                    rag_results = self.rag_system.query(rag_query, k=3) # Actual RAG query
                    logger.info(f"INTEGRATE_RAG: RAG vector store results for '{rag_query}': {rag_results}")
                    
                    if rag_results:
                        logger.info(f"INTEGRATE_RAG: RAG found {len(rag_results)} relevant results for pest management.")
                        rag_context = "\\n\\n".join(rag_results)
                        logger.info(f"INTEGRATE_RAG: RAG context for '{rag_query}' (first 200 chars): {rag_context[:200]}")
                        
                        # If Ollama is available, use it to refine the response
                        # The decision to call Ollama might also depend on HybridEngine's internal logic for 'attempt_ollama_call'
                        # Forcing it true here for RAG context for now if results found, or let it be governed by params.
                        # Let's assume attempt_ollama_call passed in is the primary determinant for now.
                        if attempt_ollama_call and self.ollama_handler:
                            logger.info(f"INTEGRATE_RAG: Ollama call is True. Will attempt to use RAG context with Ollama.")
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            prompt_content = format_prompt(
                                PromptType.PEST_MANAGEMENT_RAG, 
                                query=user_query, 
                                context=rag_context, 
                                pest=pest_name
                            )
                            logger.info(f"INTEGRATE_RAG: Constructed Ollama prompt with RAG context for '{user_query}':\\nUSER_PROMPT: {prompt_content.get('user_prompt')}")
                            
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"], 
                                query_type="pest_management" 
                            )
                            
                            if llm_response and llm_response.strip():
                                logger.info(f"INTEGRATE_RAG: Ollama successfully refined RAG results for '{user_query}'. Response: {llm_response[:200]}...")
                                return {"response": llm_response, "source": "ollama_via_rag_integrate"} 
                            else:
                                logger.warning(f"INTEGRATE_RAG: Ollama refinement failed for '{user_query}', but RAG context was available. Falling back.")
                        
                        # If Ollama refinement wasn't attempted or failed, but we have RAG results.
                        logger.info(f"INTEGRATE_RAG: Ollama not used/failed for RAG refinement of '{user_query}'. Returning formatted RAG direct results.")
                        return {"response": f"Based on our knowledge base for '{user_query}':\\n\\n{rag_context}", "source": "rag_direct_integrate"}

                    else:
                        logger.info(f"INTEGRATE_RAG: RAG found no relevant results for pest management query: '{rag_query}'")
                except Exception as e:
                    logger.error(f"INTEGRATE_RAG: Error querying RAG system in pest management for '{rag_query}': {str(e)}")
            
            # Fall back to original method if RAG didn't provide results or an error occurred
            logger.info(f"INTEGRATE_RAG: Pest management RAG processing failed or found no results for '{rag_query}', falling back to original method _original_process_control_methods.")
            return self._original_process_control_methods(params, attempt_ollama_call) # Original method for pest_management
        
        # Enhanced pest identification method (similar pattern to pest management)
        def enhanced_pest_identification(self, params, attempt_ollama_call):
            """Enhanced version of _process_pest_identification that incorporates RAG"""
            user_query = params.get("query", "") or params.get("message", "")
            pest_name = params.get("pest")
            
            # Build an optimized query for RAG
            rag_query = user_query
            if pest_name:
                rag_query = f"pest identification information about {pest_name} " + rag_query
            
            logger.info(f"Using RAG-enhanced pest identification processor with query: {rag_query}")
            
            # Try RAG first
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    rag_results = self.rag_system.query(rag_query, k=3)
                    
                    if rag_results:
                        rag_context = "\n\n".join(rag_results)
                        
                        if attempt_ollama_call and self.ollama_handler:
                            # Get references to imported modules
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            ollama_context = f"Based on our knowledge base about pest identification:\n\n{rag_context}\n\nUser query: {user_query}\n\nPlease provide comprehensive pest identification information."
                            
                            prompt_content = format_prompt(
                                PromptType.PEST_IDENTIFICATION,
                                query=ollama_context,
                                pest=pest_name
                            )
                            
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"],
                                query_type="pest_identification"
                            )
                            
                            if llm_response and llm_response.strip():
                                return {"response": llm_response, "source": "rag_ollama"}
                        
                        response = f"Based on our knowledge base about pest identification:\n\n{rag_context}"
                        return {"response": response, "source": "rag"}
                except Exception as e:
                    logger.error(f"Error in RAG for pest identification: {str(e)}")
            
            # Fall back to original method
            return self._original_process_pest_identification(params, attempt_ollama_call)

        # Enhanced crop pests method
        def enhanced_crop_pests(self, params, attempt_ollama_call):
            """Enhanced version of _process_crop_pests that incorporates RAG"""
            user_query = params.get("query", "") or params.get("message", "")
            
            logger.info(f"Using RAG-enhanced crop pests processor with query: {user_query}")
            
            # Try RAG first
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system for crop pests: {user_query}")
                    rag_results = self.rag_system.query(user_query, k=3)
                    
                    if rag_results:
                        logger.info(f"RAG found {len(rag_results)} relevant results for crop pests")
                        # Format RAG results
                        rag_context = "\n\n".join(rag_results)
                        
                        # If Ollama is available, use it to refine the response
                        if attempt_ollama_call and self.ollama_handler:
                            # Get references to imported modules
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            # Create enhanced context combining RAG results and user query
                            ollama_context = f"Based on our knowledge base about crop pests:\n\n{rag_context}\n\nUser query: {user_query}\n\nPlease provide comprehensive crop pests advice."
                            
                            # Format prompt
                            prompt_content = format_prompt(
                                PromptType.CROP_PESTS,
                                query=ollama_context
                            )
                            
                            # Generate response
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"],
                                query_type="crop_pests"
                            )
                            
                            if llm_response and llm_response.strip():
                                return {"response": llm_response, "source": "rag_ollama"}
                        
                        # If Ollama refinement wasn't attempted or failed, return RAG results directly
                        response = f"Based on our knowledge base about crop pests:\n\n{rag_context}"
                        return {"response": response, "source": "rag"}
                except Exception as e:
                    logger.error(f"Error in RAG for crop pests: {str(e)}")
            
            # Fall back to original method
            return self._original_process_crop_pests(params, attempt_ollama_call)
        
        # Enhanced indigenous knowledge method
        def enhanced_indigenous_knowledge(self, params, attempt_ollama_call):
            """Enhanced version of _process_indigenous_knowledge that incorporates RAG"""
            user_query = params.get("query", "") or params.get("message", "")
            
            logger.info(f"Using RAG-enhanced indigenous knowledge processor with query: {user_query}")
            
            # Try RAG first
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system for indigenous knowledge: {user_query}")
                    rag_results = self.rag_system.query(user_query, k=3)
                    
                    if rag_results:
                        rag_context = "\n\n".join(rag_results)
                        
                        if attempt_ollama_call and self.ollama_handler:
                            # Get references to imported modules
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            ollama_context = f"Based on our knowledge base about indigenous knowledge:\n\n{rag_context}\n\nUser query: {user_query}\n\nPlease provide comprehensive indigenous knowledge information."
                            
                            prompt_content = format_prompt(
                                PromptType.INDIGENOUS_KNOWLEDGE,
                                query=ollama_context
                            )
                            
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"],
                                query_type="indigenous_knowledge"
                            )
                            
                            if llm_response and llm_response.strip():
                                return {"response": llm_response, "source": "rag_ollama"}
                        
                        response = f"Based on our knowledge base about indigenous knowledge:\n\n{rag_context}"
                        return {"response": response, "source": "rag"}
                except Exception as e:
                    logger.error(f"Error in RAG for indigenous knowledge: {str(e)}")
            
            # Fall back to original method
            return self._original_process_indigenous_knowledge(params, attempt_ollama_call)
        
        # Enhanced soil analysis method
        def enhanced_soil_analysis(self, params, attempt_ollama_call):
            """Enhanced version of _process_soil_analysis that incorporates RAG"""
            user_query = params.get("query", "") or params.get("message", "")
            
            logger.info(f"Using RAG-enhanced soil analysis processor with query: {user_query}")
            
            # Try RAG first
            if hasattr(self, 'rag_system') and self.rag_system:
                try:
                    logger.info(f"Querying RAG system for soil analysis: {user_query}")
                    rag_results = self.rag_system.query(user_query, k=3)
                    
                    if rag_results:
                        rag_context = "\n\n".join(rag_results)
                        
                        if attempt_ollama_call and self.ollama_handler:
                            # Get references to imported modules
                            PromptType = modules['PromptType']
                            format_prompt = modules['format_prompt']
                            
                            ollama_context = f"Based on our knowledge base about soil analysis:\n\n{rag_context}\n\nUser query: {user_query}\n\nPlease provide comprehensive soil analysis information."
                            
                            prompt_content = format_prompt(
                                PromptType.SOIL_ANALYSIS,
                                query=ollama_context
                            )
                            
                            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                                prompt=prompt_content["user_prompt"],
                                query_type="soil_analysis"
                            )
                            
                            if llm_response and llm_response.strip():
                                return {"response": llm_response, "source": "rag_ollama"}
                        
                        response = f"Based on our knowledge base about soil analysis:\n\n{rag_context}"
                        return {"response": response, "source": "rag"}
                except Exception as e:
                    logger.error(f"Error in RAG for soil analysis: {str(e)}")
            
            # Fall back to original method
            return self._original_process_soil_analysis(params, attempt_ollama_call)

        # Patch the methods on the HybridEngine instance
        logger.info("Patching HybridEngine instance methods with RAG-enhanced versions")
        engine_instance._process_general_query = types.MethodType(enhanced_general_query, engine_instance)
        if hasattr(engine_instance, '_original_process_control_methods'): # Check before patching
            engine_instance._process_control_methods = types.MethodType(enhanced_pest_management, engine_instance)
        if hasattr(engine_instance, '_original_process_pest_identification'):
            engine_instance._process_pest_identification = types.MethodType(enhanced_pest_identification, engine_instance)
        if hasattr(engine_instance, '_original_process_crop_pests'):
            engine_instance._process_crop_pests = types.MethodType(enhanced_crop_pests, engine_instance)
        if hasattr(engine_instance, '_original_process_indigenous_knowledge'):
            engine_instance._process_indigenous_knowledge = types.MethodType(enhanced_indigenous_knowledge, engine_instance)
        if hasattr(engine_instance, '_original_process_soil_analysis'):
            engine_instance._process_soil_analysis = types.MethodType(enhanced_soil_analysis, engine_instance)
        
        logger.info("Successfully patched HybridEngine instance methods for RAG integration")
        return True
        
    except AttributeError as e:
        logger.error(f"AttributeError during RAG integration: {str(e)}. This might indicate a mismatch in expected HybridEngine structure.", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error during RAG integration: {str(e)}", exc_info=True)
        return False

# Main execution block (for testing or direct invocation if needed)
if __name__ == "__main__":
    # This part is primarily for testing the integration logic directly.
    # In the Django app, this function will be called from initialize_rag.py or similar.
    logger.info("Running RAG integration script directly...")
    
    # Ensure Django settings are configured if running standalone and accessing Django components indirectly
    # This is a simplified setup for standalone testing. A full Django app context might be needed for complex cases.
    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings') # Adjust to your project
        import django
        try:
            django.setup()
            logger.info("Django setup completed for standalone script execution.")
        except Exception as e:
            logger.error(f"Error setting up Django: {e}. Some functionalities might not work.")

    # Perform the integration
    integration_successful = integrate_rag_into_query_pipeline()
    
    if integration_successful:
        logger.info("RAG integration into query pipeline completed successfully (standalone test).")
        # Example: You could try to get the engine instance and check its methods
        # from api.views import get_prolog_engine
        # test_engine = get_prolog_engine()
        # if test_engine and hasattr(test_engine, '_process_general_query'):
        #     logger.info(f"_process_general_query method source: {test_engine._process_general_query.__code__.co_filename}")
    else:
        logger.error("RAG integration into query pipeline failed (standalone test).") 