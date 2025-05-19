"""
Enhanced Hybrid Engine that combines rule-based reasoning and LLM capabilities.
This system leverages both Prolog's logical inference and Ollama's language understanding.
"""
import os
import logging
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import time
from functools import lru_cache
from django.conf import settings

# Revert to direct import as relative import failed in container
from prolog_integration.service import PrologService
# from ..prolog_integration.service import PrologService
from .ollama_handler import OllamaHandler
from .prompt_templates import PromptType, format_prompt
from core.data_structures import SimilarQueryDetector
from api.monitoring import record_query_performance

# Define keywords for clarification logic (expand these lists as needed)
VAGUE_SYMPTOM_WORDS = ["spots", "yellow leaves", "sick", "dying", "problem", "disease", "issue", "blight", "wilt", "rust", "mold", "rot", "lesions", "stunted"]
VAGUE_PEST_WORDS = ["pests", "bugs", "insects", "infestation"]
KNOWN_CROP_NAMES = [
    "maize", "corn", "cabbage", "potato", "tomato", "tomatoes", "rice", "beans", 
    "carrot", "carrots", "apple", "apples", "lettuce", "spinach", "pepper", "peppers", 
    "cucumber", "cucumbers", "strawberry", "strawberries", "grape", "grapes",
    "onion", "onions", "garlic", "broccoli", "cauliflower", "squash", "pumpkin",
    "wheat", "barley", "oats", "soybean", "soybeans", "sunflower", "cotton"
]
# TODO: Consider loading KNOWN_CROP_NAMES dynamically from Prolog KB if possible

# Set up logging for this module
logger = logging.getLogger(__name__)

class HybridEngine:
    """
    An enhanced hybrid inference engine that combines rule-based and LLM-based approaches.
    
    This engine provides:
    1. Integration between Prolog and Ollama
    2. Fallback mechanisms
    3. Caching for performance
    4. Query routing based on content
    5. Structured and unstructured response handling
    """
    def __init__(self):
        """Initialize the hybrid engine with both Prolog and Ollama capabilities"""
        logging.info("Initializing HybridEngine")
        
        # Initialize the Prolog service (formerly Prolog engine)
        # self.prolog_engine = PrologEngine()
        self.prolog_service = PrologService()
        
        # Initialize Ollama handler directly if available
        self.use_ollama = os.environ.get('USE_OLLAMA', 'false').lower() == 'true'
        self.ollama_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = os.environ.get('OLLAMA_MODEL', 'gemma:2b')
        
        # Set Prolog as primary if specified in environment variables or by default for resource-constrained systems
        self.use_prolog_as_primary = os.environ.get('USE_PROLOG_PRIMARY', 'false').lower() == 'true'
        self.ollama_for_complex_only = self.use_prolog_as_primary
        
        if self.use_ollama:
            logger.info(f"Initializing with Ollama integration at {self.ollama_url} using model {self.ollama_model} as default.")
            # Use the OllamaHandler's non-blocking initialization
            self.ollama_handler = OllamaHandler(base_url=self.ollama_url, default_model_name=self.ollama_model)
            # Non-blocking initialization happens automatically in the OllamaHandler constructor
            logger.info("Ollama integration initialized in non-blocking mode. The web server will start while Ollama initializes in the background.")
            if self.use_prolog_as_primary:
                logging.info("Using Prolog as primary engine. Ollama will only be used for complex queries.")
        else:
            logging.info("Using mock Prolog implementation (Ollama integration disabled)")
            self.ollama_handler = None
            
        # Initialize similar query detector for caching semantically similar queries
        self.similar_query_detector = SimilarQueryDetector(threshold=0.85)
        
        # Track metrics
        self.query_count = 0
        self.cache_hit_count = 0
        self.start_time = time.time()
        
        logging.info("HybridEngine initialized successfully")
    
    def is_initialization_complete(self, wait_timeout: Optional[float] = None):
        """
        Check if the Ollama handler has completed initialization.
        If wait_timeout is provided, it will wait for the OllamaHandler.
        
        Args:
            wait_timeout: Maximum time to wait in seconds for OllamaHandler initialization.
                          If None, checks current status without waiting.
            
        Returns:
            tuple: (is_ready: bool, status_message: str)
        """
        if not self.use_ollama or self.ollama_handler is None:
            return True, "Ollama not in use."
            
        # If a wait_timeout is provided, call OllamaHandler's wait_for_initialization
        if wait_timeout is not None:
            logger.info(f"HybridEngine: Waiting up to {wait_timeout}s for Ollama handler initialization...")
            initialization_was_successful_after_wait = self.ollama_handler.wait_for_initialization(timeout=wait_timeout)
            is_complete_after_wait = self.ollama_handler._initialization_complete.is_set()
            logger.info(f"HybridEngine: After wait, Ollama handler complete={is_complete_after_wait}, success={initialization_was_successful_after_wait}")
            if not is_complete_after_wait:
                return False, "Ollama handler initialization timed out."
            if not initialization_was_successful_after_wait:
                 return True, "Ollama handler initialization completed but reported failure. Check Ollama service."
            return True, "Ollama handler initialized successfully after wait."

        # If no wait_timeout, just check current status
        is_complete_now = self.ollama_handler._initialization_complete.is_set()
        initialization_was_successful_now = self.ollama_handler._initialization_success

        if is_complete_now:
            if initialization_was_successful_now:
                return True, "Ollama handler initialized successfully."
            else:
                return True, "Ollama handler initialization failed. Check Ollama service."
        else:
            return False, "Ollama handler is still initializing. Please try again shortly."
    
    @record_query_performance
    def query(self, query_type: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a query using the appropriate engine or combination of engines
        
        Args:
            query_type: Type of query to process (pest_identification, control_methods, etc.)
            params: Parameters for the query
            
        Returns:
            dict: Results of the query
        """
        user_query = params.get("message") or params.get("query") if params else None
        logger.info(f"HybridEngine query: {query_type} with params: {params}")

        # Step 1: Wait for the engine to be fully initialized (up to 45 seconds)
        # Increased timeout as Ollama first model load can be slow.
        is_ready, status_message = self.is_initialization_complete(wait_timeout=45.0)
        if not is_ready:
            logger.warning(f"HybridEngine not ready after wait: {status_message}. Returning initialization status.")
            return {"response": status_message, "source": "hybrid_engine_initializing_timeout", "success": False}
        elif "failure" in status_message or "failed" in status_message: # Check if init completed but failed
            logger.warning(f"HybridEngine initialization completed but failed: {status_message}. Returning status.")
            return {"response": status_message, "source": "hybrid_engine_initialization_failed", "success": False}

        self.query_count += 1
        params = params or {}
        
        logging.info(f"Processing query of type: {query_type} with params: {params}")
        
        # Check if we've seen a similar query before
        if user_query:
            similar_result = self.similar_query_detector.find_similar_query(user_query)
            if similar_result:
                self.cache_hit_count += 1
                # Check if similar_result has the expected structure (query, response, score)
                if isinstance(similar_result, tuple) and len(similar_result) == 3:
                    logging.info(f"Found similar query in cache. Similarity: {similar_result[2]:.2f}")
                    # Cache hit: Use the cached response directly
                    return {"response": similar_result[1], "source": "cache", "success": True}
                else:
                    # Log an error if the structure is unexpected, then proceed without using this cache entry
                    logging.warning(f"HybridEngine: Similar query detector returned an unexpected result format: {similar_result}. Proceeding without cache for this query.")
        
        # When using Prolog as primary, determine if this query should use Ollama
        if self.use_prolog_as_primary and self.use_ollama and self.ollama_for_complex_only:
            # Determine if this is a complex query that needs Ollama
            should_use_ollama_for_this_specific_query = self._should_use_ollama_for_query(query_type, params)
            
            logging.info(f"[QUERY_METHOD] Decision for query_type '{query_type}': attempt_ollama_call = {should_use_ollama_for_this_specific_query}")

            try:
                # Process the query, passing the decision explicitly
                result = self._process_query_by_type(query_type, params, attempt_ollama_call=should_use_ollama_for_this_specific_query)
                
                # Cache this query-response pair if successful
                if user_query and "response" in result and len(result["response"]) > 10 and result.get("source") != "cache" and result.get("source") != "hybrid_engine_initializing":
                    self.similar_query_detector.add_query(user_query, result["response"])
                    
                return result
            except Exception as e:
                logging.error(f"HybridEngine query error: {str(e)}", exc_info=True)
                return {
                    "error": f"HybridEngine Error (A1): {str(e)}",
                    "response": f"DEBUG ERROR - I encountered a specific error (A1): {str(e)}. Please try again or rephrase your question.",
                    "source": "hybrid_engine_error_A1"
                }
        else:
            # Handle based on query type (original behavior - assumes Ollama should be tried if available and enabled globally)
            # Determine if Ollama should be attempted based on global settings
            should_attempt_ollama = self.use_ollama # Use the global setting
            logging.info(f"[QUERY_METHOD] Not in Prolog-primary mode. Query_type '{query_type}'. attempt_ollama_call = {should_attempt_ollama}")
            try:
                # Call _process_query_by_type, passing the decision
                result = self._process_query_by_type(query_type, params, attempt_ollama_call=should_attempt_ollama)
                
                # Cache this query-response pair if successful
                if user_query and "response" in result and len(result["response"]) > 10 and result.get("source") != "cache" and result.get("source") != "hybrid_engine_initializing":
                    self.similar_query_detector.add_query(user_query, result["response"])
                    
                return result
            except Exception as e:
                logging.error(f"HybridEngine query error (non-Prolog-primary path): {str(e)}", exc_info=True)
                return {
                    "error": f"HybridEngine Error (B1): {str(e)}",
                    "response": f"DEBUG ERROR - I encountered a specific error (B1): {str(e)}. Please try again or rephrase your question.",
                    "source": "hybrid_engine_error_B1"
                }
    
    def _should_use_ollama_for_query(self, query_type: str, params: Dict) -> bool:
        """
        Determine if Ollama should be used for this query type based on complexity and keywords.
        For resource-constrained systems, we want to be very selective about when to use Ollama.
        
        Args:
            query_type: The type of query being processed
            params: The parameters for the query, including the message
            
        Returns:
            bool: True if Ollama should be used, False if Prolog should be used
        """
        # Define query types that are particularly well-suited for Prolog
        prolog_suitable_queries = [
            "pest_identification", 
            "disease_identification",
            "pest_management",
            "fertilizer_recommendation",
            "crop_rotation",
            "watering_schedule",
            "planting_guide"
        ]
        
        # Define query types that are high-value for LLM processing
        high_value_llm_queries = [
            "complex_farming_strategy",
            "detailed_explanation",
            "multi_factor_analysis"
        ]
        
        # Keywords that might indicate a complex query better suited for LLM
        llm_keywords = [
            "explain", "why", "how", "compare", "difference", 
            "versus", "vs", "complex", "detailed", "comprehensive"
        ]
        
        # Get the query message
        message = params.get("message", "").lower()
        
        # Check for complexity indicators
        is_complex_query = len(message.split()) > 20
        has_llm_keywords = any(keyword in message.lower() for keyword in llm_keywords)
        
        # Check if Ollama is actually available and initialized
        ollama_available = False
        if self.ollama_handler:
            try:
                # Simplified check: just see if handler thinks it's available.
                # The decision to USE it is separate.
                ollama_available = self.ollama_handler.is_available
            except:
                ollama_available = False
        
        # If Ollama is not technically available, don't attempt to use it
        if not ollama_available:
            return False # Cannot use Ollama if it's not working
            
        # Logic based on query type (assuming Ollama IS available)
        if query_type == "general_query": 
            return True # Always TRY Ollama for general query if it's available
        elif query_type in high_value_llm_queries:
            return True
        elif query_type in prolog_suitable_queries:
            # Only use LLM for specific prolog types if complex AND has keywords
            return is_complex_query and has_llm_keywords
        else:
            # For unknown query types, default to Prolog unless complex
            return is_complex_query and has_llm_keywords and len(message) > 50
    
    def _process_query_by_type(self, query_type: str, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process a query based on its type, honouring attempt_ollama_call flag."""
        if query_type == "pest_identification":
            return self._process_pest_identification(params, attempt_ollama_call=attempt_ollama_call)
        elif query_type == "control_methods" or query_type == "pest_management":
            # Handle both 'control_methods' and 'pest_management' query types with the same method
            return self._process_control_methods(params, attempt_ollama_call=attempt_ollama_call)
        elif query_type == "crop_pests":
            return self._process_crop_pests(params, attempt_ollama_call=attempt_ollama_call)
        elif query_type == "indigenous_knowledge":
            return self._process_indigenous_knowledge(params, attempt_ollama_call=attempt_ollama_call)
        elif query_type == "general_query":
            return self._process_general_query(params, attempt_ollama_call=attempt_ollama_call)
        elif query_type == "soil_analysis":
            # Handle soil_analysis with the pest_management processor when it contains pest-related terms
            user_query = params.get("query", "").lower()
            if any(term in user_query for term in ["aphid", "pest", "insect", "predator", "bug"]):
                logging.info("Soil analysis query contains pest terms, redirecting to pest management.")
                return self._process_control_methods(params, attempt_ollama_call=attempt_ollama_call)
            return self._process_soil_analysis(params, attempt_ollama_call=attempt_ollama_call)
        else:
            return {"error": "Unknown query type"}
    
    def _process_pest_identification(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process pest identification queries using Prolog and/or Ollama."""
        user_query = params.get("query", "")
        pest_name = params.get("pest") # Extracted by view
        crop_name = params.get("crop") # Extracted by view
        
        prolog_info_parts = []
        prolog_data_found = False

        if pest_name:
            logging.info(f"Attempting to get pest info for '{pest_name}' from PrologService.")
            pest_info = self.prolog_service.get_pest_info(pest_name)
            if pest_info:
                prolog_data_found = True
                prolog_info_parts.append(f"Information for {pest_info.get('name', pest_name)} (Type: {pest_info.get('type', 'N/A')}, Scientific Name: {pest_info.get('scientific_name', 'N/A')}):")
                if pest_info.get('symptoms'):
                    prolog_info_parts.append(f"  Symptoms: {', '.join(pest_info['symptoms'])}")
                if pest_info.get('monitoring'):
                    prolog_info_parts.append(f"  Monitoring: {', '.join(pest_info['monitoring'])}")
                
                # Get solutions for this pest
                solutions = self.prolog_service.get_pest_solutions(pest_name)
                if solutions:
                    solution_strings = []
                    for sol in solutions:
                        s_str = f"{sol.get('name')} ({sol.get('type', 'N/A')})"
                        if sol.get('description'):
                            s_str += f": {sol['description']}"
                        solution_strings.append(s_str)
                    if solution_strings:
                        prolog_info_parts.append(f"  Potential Solutions: {'; '.join(solution_strings)}")
                else:
                    prolog_info_parts.append("  No specific solutions found in knowledge base for this pest.")
        else:
            # If no specific pest name, we might try a broader search or rely more on LLM
            # For now, this path will likely lead to LLM or generic fallback
            logging.info("No specific pest name provided for Prolog lookup in pest identification.")

        # Decision logic simplified: If Prolog data insufficient OR ollama is requested, try Ollama.
        prolog_sufficient = prolog_data_found # Simple check for now

        if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:
             # The original check `if self.use_ollama and self.ollama_handler:` is replaced by checking the passed flag
            logging.info(f"[PEST_ID] Using Ollama for pest identification (prolog_sufficient={prolog_sufficient}, attempt_ollama_call={attempt_ollama_call}).")
            # Prepare context for Ollama, potentially including Prolog findings
            ollama_context = ""
            if prolog_data_found:
                ollama_context = "Based on our knowledge base:\n" + "\n".join(prolog_info_parts) + "\n\nUser is asking: " + user_query
            else:
                ollama_context = user_query

            prompt_content = format_prompt(
                PromptType.PEST_IDENTIFICATION,
                query=ollama_context, # Pass the potentially augmented query
                pest=pest_name,
                crop=crop_name
            )
            
            # Use specialized model for pest identification
            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                prompt=prompt_content["user_prompt"],
                query_type="pest_identification"
            )
            
            if llm_response and llm_response.strip():
                final_response = llm_response
                if prolog_data_found and not llm_response.startswith("Based on our knowledge base"):
                    # Prepend prolog context if LLM didn't seem to use it and we want to ensure it's there
                    # This is a simple way, could be more sophisticated
                    # final_response = "From our knowledge base:\n" + "\n".join(prolog_info_parts) + "\n\nAdditionally, the AI model suggests:\n" + llm_response
                    pass # Decided to let LLM response stand, as prompt already included it.

                return {"response": final_response, "source": "ollama"}
            else:
                logging.warning("[PEST_ID] Ollama returned empty response.")
        
        # Fallback logic
        if prolog_data_found:
             logging.info("[PEST_ID] Ollama not used or failed; returning specific Prolog data.")
             return {"response": "\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("[PEST_ID] Using mock response as other methods failed.")
        return self._mock_pest_identification(params)
    
    def _process_control_methods(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process queries for pest control methods."""
        user_query = params.get("query", "")
        pest_name = params.get("pest")
        crop_name = params.get("crop") # May be used for context or region in future
        region = params.get("region", "global") # Default to global, can be refined

        prolog_info_parts = []
        prolog_data_found = False

        if pest_name:
            logging.info(f"Attempting to get control methods for '{pest_name}' from PrologService.")
            solutions = self.prolog_service.get_pest_solutions(pest_name, region)
            recommended_solution = self.prolog_service.recommend_solution(pest_name)

            if solutions:
                prolog_data_found = True
                prolog_info_parts.append(f"Control methods for {pest_name}:")
                for sol in solutions:
                    s_str = f"- {sol.get('name')} ({sol.get('type', 'N/A')})"
                    if sol.get('description'):
                        s_str += f": {sol['description']}"
                    if sol.get('cost') and sol.get('difficulty'):
                        s_str += f" (Cost: {sol['cost']}, Difficulty: {sol['difficulty']})"
                    prolog_info_parts.append(s_str)
                
                if recommended_solution and recommended_solution.get('name'):
                    # Check if recommendation is already detailed in the solutions list
                    # For simplicity, we just add a note here. Could be integrated better.
                    prolog_info_parts.append(f"Recommended: {recommended_solution.get('name')} - {recommended_solution.get('description', 'See details above.')}")
            elif recommended_solution and recommended_solution.get('name'): # Only recommendation found
                prolog_data_found = True
                prolog_info_parts.append(f"Recommended control method for {pest_name}:")
                rs = recommended_solution
                s_str = f"- {rs.get('name')} ({rs.get('type', 'N/A')})"
                if rs.get('description'):
                    s_str += f": {rs['description']}"
                if rs.get('cost') and rs.get('difficulty'):
                    s_str += f" (Cost: {rs['cost']}, Difficulty: {rs['difficulty']})"
                prolog_info_parts.append(s_str)
            else:
                logging.info(f"No specific control methods found in Prolog for '{pest_name}'.")
        else:
            logging.info("No specific pest name provided for Prolog lookup in control methods.")

        prolog_sufficient = prolog_data_found # Simple check

        if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:
            logging.info(f"[CONTROL_METHODS] Using Ollama (prolog_sufficient={prolog_sufficient}, attempt_ollama_call={attempt_ollama_call}).")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = "Based on our knowledge base for " + pest_name + ":\n" + "\n".join(prolog_info_parts) + "\n\nUser is asking for control methods: " + user_query
            
            prompt_content = format_prompt(
                PromptType.PEST_MANAGEMENT,
                query=ollama_context,
                pest=pest_name,
                crop=crop_name
            )
            
            # Use specialized model for pest management
            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                prompt=prompt_content["user_prompt"],
                query_type="pest_management"
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("[CONTROL_METHODS] Ollama returned empty response.")
        
        if prolog_data_found:
            logging.info("[CONTROL_METHODS] Ollama not used or failed; returning specific Prolog data.")
            return {"response": "\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("[CONTROL_METHODS] Using mock response as other methods failed.")
        return self._mock_control_methods(params)
    
    def _process_crop_pests(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process queries for pests affecting specific crops."""
        user_query = params.get("query", "")
        crop_name = params.get("crop")

        prolog_info_parts = []
        prolog_data_found = False
        pest_list_for_ollama = []

        if crop_name:
            logging.info(f"Attempting to get crop info for '{crop_name}' from PrologService.")
            # Use the new PrologService method
            crop_details = self.prolog_service.get_crop_details(crop_name)
            
            # Check if details were found and if there's a pests list
            if crop_details and not crop_details.get('error') and isinstance(crop_details.get('pests'), list):
                pest_list_for_ollama = crop_details['pests']
                if pest_list_for_ollama:
                    prolog_data_found = True
                    prolog_info_parts.append(f"Pests known to affect {crop_name}:")
                    prolog_info_parts.extend([f"- {p}" for p in pest_list_for_ollama])
            
            if not prolog_data_found:
                 # Log if details were found but no pests, or if details weren't found
                 if crop_details and not crop_details.get('error'):
                      logging.info(f"Prolog found details for crop '{crop_name}' but no 'pests' list.")
                 else:
                      logging.info(f"No specific pest list found in Prolog for crop '{crop_name}'. get_crop_details failed.")

        else:
            logging.info("No specific crop name provided for Prolog lookup in crop pests.")

        prolog_sufficient = prolog_data_found
        
        if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:
            logging.info(f"[CROP_PESTS] Using Ollama (prolog_sufficient={prolog_sufficient}, attempt_ollama_call={attempt_ollama_call}).")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = f"According to our knowledge base, {crop_name} can be affected by: {', '.join(pest_list_for_ollama)}.\n\nUser is asking: {user_query}"
            
            prompt_content = format_prompt(
                PromptType.GENERAL, 
                query=ollama_context,
                crop=crop_name,
            )
            
            # Use specialized model for pest management
            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                prompt=prompt_content["user_prompt"],
                query_type="pest_management"
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("[CROP_PESTS] Ollama returned empty response.")
        
        if prolog_data_found:
            logging.info("[CROP_PESTS] Ollama not used or failed; returning specific Prolog data.")
            return {"response": "\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("[CROP_PESTS] Using mock response as other methods failed.")
        return self._mock_crop_pests(params)
    
    def _process_indigenous_knowledge(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process queries about indigenous knowledge."""
        user_query = params.get("query", "")
        practice_name = params.get("practice")

        prolog_info_parts = []
        prolog_data_found = False

        if practice_name:
            logging.info(f"Attempting to get indigenous practice details for '{practice_name}' from PrologService.")
            # Use the new PrologService method
            practice_details = self.prolog_service.get_practice_details(practice_name)
            
            if practice_details and not practice_details.get('error'):
                prolog_data_found = True
                prolog_info_parts.append(f"Details for indigenous practice '{practice_name}':")
                # Use the returned dictionary directly
                if practice_details.get('description'):
                    prolog_info_parts.append(f"  Description: {practice_details['description']}")
                if practice_details.get('type'):
                    prolog_info_parts.append(f"  Type: {practice_details['type']}")
                # Access parsed lists directly if parser handled them
                if isinstance(practice_details.get('controls'), list):
                    prolog_info_parts.append(f"  Controls: {', '.join(practice_details['controls'])}") 
                if isinstance(practice_details.get('resolves'), list):
                    prolog_info_parts.append(f"  Resolves: {', '.join(practice_details['resolves'])}")
                if isinstance(practice_details.get('cultural_context'), list):
                    prolog_info_parts.append(f"  Cultural Context: {', '.join(practice_details['cultural_context'])}")
                # Add other relevant attributes as needed
            else:
                logging.info(f"No specific details found in Prolog for practice '{practice_name}'.")
        else:
            # If no specific practice name, try the general search_prolog_kb
            logging.info("No specific practice name, trying prolog_service.search_prolog_kb for indigenous knowledge.")
            prolog_search_result = self.prolog_service.search_prolog_kb(user_query)
            if prolog_search_result and not prolog_search_result.get('generic_response'):
                prolog_data_found = True
                if prolog_search_result.get('practice_found'):
                    p_info = prolog_search_result['practice_info'] # practice_info is already a dict
                    prolog_info_parts.append(f"Found information related to indigenous practice '{p_info.get('name')}':")
                    if p_info.get('description'): prolog_info_parts.append(f"  Description: {p_info['description']}")
                    if p_info.get('type'): prolog_info_parts.append(f"  Type: {p_info['type']}")
                    if isinstance(p_info.get('controls'), list): prolog_info_parts.append(f"  Controls: {', '.join(p_info['controls'])}") 
                elif prolog_search_result.get('pest_found'):
                     prolog_info_parts.append("Found pest-related information that might involve indigenous practices. Please ask specifically about a practice.")

        prolog_sufficient = prolog_data_found

        if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:
            logging.info(f"[INDIGENOUS] Using Ollama (prolog_sufficient={prolog_sufficient}, attempt_ollama_call={attempt_ollama_call}).")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = "Our knowledge base contains the following on this topic:\n" + "\n".join(prolog_info_parts) + "\n\nUser is asking: " + user_query
            
            prompt_content = format_prompt(
                PromptType.INDIGENOUS_KNOWLEDGE,
                query=ollama_context,
                practice_name=params.get('practice_name', practice_name), 
                purpose=params.get('purpose', '')
            )
            
            # Use specialized model for pest management
            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                prompt=prompt_content["user_prompt"],
                query_type="pest_management"
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("[INDIGENOUS] Ollama returned empty response.")
        
        if prolog_data_found:
            logging.info("[INDIGENOUS] Ollama not used or failed; returning specific Prolog data.")
            return {"response": "\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("[INDIGENOUS] Using mock response as other methods failed.")
        return self._mock_indigenous_knowledge(params)
    
    def _process_general_query(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process general queries, trying Prolog KB search first, then Ollama, with clarification logic."""
        user_query = params.get("message", "").lower() # Work with lowercase
        prolog_info_parts = []
        prolog_data_found = False

        # --- START: Clarification Logic --- 
        needs_clarification = False
        required_info = None
        clarification_question = ""

        has_vague_symptom = any(word in user_query for word in VAGUE_SYMPTOM_WORDS)
        has_vague_pest = any(word in user_query for word in VAGUE_PEST_WORDS)
        has_known_crop = any(crop in user_query for crop in KNOWN_CROP_NAMES)

        if (has_vague_symptom or has_vague_pest) and not has_known_crop:
            needs_clarification = True
            required_info = "crop_name"
            clarification_question = "Okay, I understand there's an issue. To help further, could you please specify which crop you are asking about?"
            # TODO: Consider more specific questions based on the trigger words.

        if needs_clarification:
            logging.info(f"[CLARIFICATION] Query '{user_query}' is vague, requires {required_info}. Asking: {clarification_question}")
            # TODO: Implement state management here (e.g., save original query and required_info in session/cache)
            # For now, just return the clarification request directly
            return {
                "response": clarification_question,
                "source": "clarification_request", 
                "success": True,
                "action_needed": "ask_user_for_clarification", # Hint for frontend/caller
                "required_info": required_info
            }
        # --- END: Clarification Logic --- 

        # If no clarification needed, proceed with original logic...
        logging.info(f"[GENERAL_QUERY] Attempting general KB search with PrologService for: {user_query}")
        prolog_search_result = self.prolog_service.search_prolog_kb(user_query)

        if prolog_search_result and not prolog_search_result.get('generic_response'):
            prolog_data_found = True
            # Format a response based on what search_prolog_kb found (pest or practice)
            if prolog_search_result.get('pest_found'):
                pest_info = prolog_search_result.get('pest_info', {})
                solutions = prolog_search_result.get('solutions', [])
                recommendation = prolog_search_result.get('recommendation', {})
                
                prolog_info_parts.append(f"Found information about pest '{prolog_search_result['pest_found']}':")
                if pest_info.get('scientific_name'): prolog_info_parts.append(f"  Scientific Name: {pest_info['scientific_name']}")
                if pest_info.get('symptoms'): prolog_info_parts.append(f"  Symptoms: {', '.join(pest_info['symptoms'])}")
                if solutions:
                    prolog_info_parts.append("  Solutions:")
                    for sol in solutions:
                        prolog_info_parts.append(f"    - {sol.get('name')} ({sol.get('type', 'N/A')}): {sol.get('description', '')}")
                if recommendation.get('name'):
                    prolog_info_parts.append(f"  Recommended: {recommendation.get('name')}")

            elif prolog_search_result.get('practice_found'):
                p_info = prolog_search_result.get('practice_info', {})
                prolog_info_parts.append(f"Found information about practice '{p_info.get('name')}':")
                if p_info.get('description'): prolog_info_parts.append(f"  Description: {p_info['description']}")
                if p_info.get('type'): prolog_info_parts.append(f"  Type: {p_info['type']}")
                if p_info.get('controls'): prolog_info_parts.append(f"  Controls: {', '.join(p_info['controls'])}")
            else:
                prolog_data_found = False
                logging.info("[GENERAL_QUERY] Prolog search_prolog_kb returned non-generic but unhandled result.")
        else:
            logging.info("[GENERAL_QUERY] No specific information found by prolog_service.search_prolog_kb.")

        # Log the state right before the decision
        logging.info(f"[GENERAL_QUERY_CHECK] Checking Ollama condition: attempt_ollama_call = {attempt_ollama_call}, self.ollama_handler is None = {self.ollama_handler is None}")
        
        # Use the passed flag to decide whether to try Ollama.
        if attempt_ollama_call and self.ollama_handler:
            logging.info("[GENERAL_QUERY] Using Ollama for general query.") # THIS LOG IS KEY
            ollama_context = user_query
            if prolog_data_found: # Prepend any specific findings from KB search
                ollama_context = "Based on our knowledge base:\n" + "\n".join(prolog_info_parts) + "\n\nUser is asking: " + user_query
            
            prompt_content = format_prompt(
                PromptType.GENERAL,
                query=ollama_context
            )
            
            # Use specialized model for pest management
            llm_response = self.ollama_handler.generate_response_with_specialized_model(
                prompt=prompt_content["user_prompt"],
                query_type="pest_management"
            )

            if llm_response and llm_response.strip():
                logging.info(f"[GENERAL_QUERY] Ollama returned a response: {llm_response[:100]}...")
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("[GENERAL_QUERY] Ollama returned empty or whitespace response.")
        
        # Fallback if Ollama was not used, or failed, or returned empty.
        # If Prolog found something specific earlier, return that.
        if prolog_data_found:
            logging.info("[GENERAL_QUERY] Ollama not used or failed; returning specific Prolog data.")
            return {"response": "\n".join(prolog_info_parts), "source": "prolog_partial"}
        
        logging.info("[GENERAL_QUERY] Using default/fallback response as other methods failed.")
        return {
            "response": "I'm sorry, I couldn't find specific information for your query. Could you try rephrasing or asking about a specific pest, crop, or farming practice?",
            "source": "fallback"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics and engine status"""
        uptime = time.time() - self.start_time
        cache_hit_rate = self.cache_hit_count / self.query_count if self.query_count > 0 else 0
        
        ollama_handler_available = False
        ollama_handler_initialized_successfully = False
        ollama_handler_initialization_pending = True # Assume pending until proven otherwise
        ollama_handler_circuit_state = "N/A"
        
        if self.ollama_handler:
            ollama_handler_available = self.ollama_handler.is_available
            # Check if initialization thread has finished and if it was successful
            if self.ollama_handler._initialization_complete.is_set():
                ollama_handler_initialization_pending = False
                ollama_handler_initialized_successfully = self.ollama_handler._initialization_success
            else:
                ollama_handler_initialization_pending = True # Still running
                ollama_handler_initialized_successfully = False # Not yet successful
            
            # Get circuit breaker states if possible (assuming they have a get_state method)
            if hasattr(self.ollama_handler, 'availability_circuit') and hasattr(self.ollama_handler.availability_circuit, 'get_state'):
                ollama_handler_circuit_state = self.ollama_handler.availability_circuit.get_state()
            # Could add other circuit states like generate_circuit, chat_circuit etc.

        prolog_service_available = False
        if self.prolog_service and hasattr(self.prolog_service, 'is_kb_loaded'): # Assuming a way to check prolog status
            prolog_service_available = self.prolog_service.is_kb_loaded() # Example check
        
        return {
            "uptime_seconds": uptime,
            "query_count": self.query_count,
            "cache_hits": self.cache_hit_count,
            "cache_hit_rate": cache_hit_rate,
            "ollama_handler_stats": {
                "configured": self.use_ollama,
                "available": ollama_handler_available,
                "initialization_successful": ollama_handler_initialized_successfully,
                "initialization_pending": ollama_handler_initialization_pending,
                "circuit_breaker_state": ollama_handler_circuit_state
            },
            "prolog_service_stats": {
                "available": prolog_service_available
            },
            "similar_queries_cached": len(self.similar_query_detector.queries) if hasattr(self.similar_query_detector, 'queries') else 0
        }
    
    # Mock implementations for fallback
    def _mock_pest_identification(self, params):
        """Mock pest identification"""
        return {
            "pests": [
                {
                    "name": "Aphid",
                    "probability": 0.85,
                    "symptoms": ["Yellowing leaves", "Stunted growth", "Sticky residue"],
                    "description": "Small sap-sucking insects that can cause significant damage to crops"
                },
                {
                    "name": "Spider Mite",
                    "probability": 0.65,
                    "symptoms": ["Webbing", "Leaf spotting", "Yellowing"],
                    "description": "Tiny arachnids that feed on plant cells"
                }
            ]
        }
    
    def _mock_control_methods(self, params):
        """Mock control methods"""
        return {
            "methods": [
                {
                    "name": "Neem Oil Spray",
                    "effectiveness": "High",
                    "organic": True,
                    "application": "Spray directly on affected areas"
                },
                {
                    "name": "Insecticidal Soap",
                    "effectiveness": "Medium",
                    "organic": True,
                    "application": "Apply to infected plants, focusing on undersides of leaves"
                }
            ]
        }
    
    def _mock_crop_pests(self, params):
        """Mock crop pests information"""
        crop = params.get("crop", "Tomato")
        return {
            "crop": crop,
            "pests": [
                {
                    "name": "Tomato Hornworm",
                    "prevalence": "High",
                    "damage_level": "Severe",
                    "season": "Summer"
                },
                {
                    "name": "Aphid",
                    "prevalence": "Medium",
                    "damage_level": "Moderate",
                    "season": "Spring-Fall"
                }
            ]
        }
    
    def _mock_indigenous_knowledge(self, params):
        """Mock indigenous knowledge"""
        return {
            "methods": [
                {
                    "name": "Ash Sprinkle Method",
                    "description": "Traditional method of using wood ash to control pests on crops",
                    "materials": "Wood ash from cooking fires, container for collecting ash",
                    "season": "During the growing season, especially after rainfall"
                },
                {
                    "name": "Chili Pepper Spray",
                    "description": "Traditional method using hot chili peppers to create a natural insect repellent",
                    "materials": "Hot chili peppers, water, container for mixing, spray bottle",
                    "season": "Throughout growing season as needed"
                }
            ]
        }

    def _process_soil_analysis(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:
        """Process soil analysis queries using Ollama."""
        user_query = params.get("query", "")
        soil_type = params.get("soil_type")
        crop_name = params.get("crop")
        
        logging.info(f"Processing soil analysis query: '{user_query}'")
        
        if attempt_ollama_call and self.ollama_handler:
            logging.info("[SOIL_ANALYSIS] Using Ollama for response generation.")
            
            # Use the general prompt template for soil queries
            prompt_content = format_prompt(
                PromptType.SOIL_ANALYSIS, 
                soil_description=soil_type or "not specified",
                location="Lesotho",
                current_crops=crop_name or "not specified",
                problems=user_query
            )
            
            # Use the general model for soil analysis
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"],
                system_prompt=prompt_content["system_prompt"]
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("[SOIL_ANALYSIS] Ollama returned empty response.")
                
        # Fallback to general query if Ollama is not available or failed
        logging.info("[SOIL_ANALYSIS] Using general query processor as fallback.")
        return self._process_general_query(params, attempt_ollama_call=attempt_ollama_call)
