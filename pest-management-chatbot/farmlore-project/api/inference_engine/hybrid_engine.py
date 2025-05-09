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

from prolog_integration.service import PrologService
from .ollama_handler import OllamaHandler
from .prompt_templates import PromptType, format_prompt
from core.data_structures import SimilarQueryDetector
from api.monitoring import record_query_performance

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
            logging.info(f"Initializing with Ollama integration at {self.ollama_url} using model {self.ollama_model}")
            # Use the OllamaHandler's non-blocking initialization
            self.ollama_handler = OllamaHandler(base_url=self.ollama_url)
            # Non-blocking initialization happens automatically in the OllamaHandler constructor
            logging.info("Ollama integration initialized in non-blocking mode. The web server will start while Ollama initializes in the background.")
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
    
    def is_initialization_complete(self, timeout=None):
        """
        Check if the Ollama handler has completed initialization.
        
        Args:
            timeout: Maximum time to wait in seconds, or None to just check current status
            
        Returns:
            tuple: (is_complete, is_successful) indicating if initialization is complete and if it was successful
        """
        if not self.use_ollama or self.ollama_handler is None:
            # If Ollama is not enabled, initialization is "complete and successful"
            return True, True
            
        if timeout is not None:
            # Wait for initialization with timeout
            success = self.ollama_handler.wait_for_initialization(timeout=timeout)
            return self.ollama_handler._initialization_complete.is_set(), success
        else:
            # Just check current status without waiting
            return self.ollama_handler._initialization_complete.is_set(), self.ollama_handler._initialization_success
    
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
        self.query_count += 1
        params = params or {}
        
        logging.info(f"Processing query of type: {query_type} with params: {params}")
        
        # Check if we've seen a similar query before
        user_query = params.get("query", "")
        if user_query:
            similar_result = self.similar_query_detector.find_similar_query(user_query)
            if similar_result:
                self.cache_hit_count += 1
                logging.info(f"Found similar query in cache. Similarity: {similar_result[2]:.2f}")
                return {"response": similar_result[1], "source": "cache"}
        
        # When using Prolog as primary, determine if this query should use Ollama
        if self.use_prolog_as_primary and self.use_ollama and self.ollama_for_complex_only:
            # Determine if this is a complex query that needs Ollama
            should_use_ollama = self._should_use_ollama_for_query(query_type, params)
            
            # Override use_ollama flag temporarily for this query
            original_use_ollama = self.use_ollama
            self.use_ollama = should_use_ollama
            
            try:
                # Process the query with the appropriate engine
                result = self._process_query_by_type(query_type, params)
                
                # Add source information to indicate which engine was used
                if "source" not in result:
                    result["source"] = "ollama" if should_use_ollama else "prolog"
                
                # Restore original setting
                self.use_ollama = original_use_ollama
                
                # Cache this query-response pair if successful
                if user_query and "response" in result and len(result["response"]) > 10:
                    self.similar_query_detector.add_query(user_query, result["response"])
                    
                return result
            except Exception as e:
                # Restore original setting in case of error
                self.use_ollama = original_use_ollama
                logging.error(f"Error processing query: {str(e)}")
                return {
                    "error": f"Error processing query: {str(e)}",
                    "response": "I encountered an error while processing your query. Please try again or rephrase your question."
                }
        else:
            # Handle based on query type (original behavior)
            try:
                result = None
                
                if query_type == "pest_identification":
                    result = self._process_pest_identification(params)
                elif query_type == "control_methods":
                    result = self._process_control_methods(params)
                elif query_type == "crop_pests":
                    result = self._process_crop_pests(params)
                elif query_type == "indigenous_knowledge":
                    result = self._process_indigenous_knowledge(params)
                elif query_type == "general_query":
                    result = self._process_general_query(params)
                else:
                    result = {"error": "Unknown query type"}
                
                # Cache this query-response pair if successful
                if user_query and "response" in result and len(result["response"]) > 10:
                    self.similar_query_detector.add_query(user_query, result["response"])
                    
                return result
                
            except Exception as e:
                logging.error(f"Error processing query: {str(e)}")
                return {
                    "error": f"Error processing query: {str(e)}",
                    "response": "I encountered an error while processing your query. Please try again or rephrase your question."
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
                # Only check if Ollama is available if we're considering using it
                # This avoids unnecessary API calls for simple queries
                if high_value_llm_queries or (is_complex_query and has_llm_keywords):
                    ollama_available = self.ollama_handler.is_available()
            except:
                ollama_available = False
        
        # If Ollama is not available, always use Prolog
        if not ollama_available:
            return False
            
        # For resource-constrained systems, be very selective about using Ollama
        # Only use it for specifically designated high-value LLM queries
        if query_type in high_value_llm_queries:
            return True
        elif query_type in prolog_suitable_queries:
            # Even for Prolog-suitable queries, only use LLM if it's both complex AND has LLM keywords
            # This is more restrictive than the previous implementation
            return is_complex_query and has_llm_keywords
        else:
            # For unknown query types, default to Prolog unless it's clearly a complex query
            return is_complex_query and has_llm_keywords and len(message) > 50
    
    def _process_query_by_type(self, query_type: str, params: Dict) -> Dict[str, Any]:
        """Process a query based on its type"""
        if query_type == "pest_identification":
            return self._process_pest_identification(params)
        elif query_type == "control_methods":
            return self._process_control_methods(params)
        elif query_type == "crop_pests":
            return self._process_crop_pests(params)
        elif query_type == "indigenous_knowledge":
            return self._process_indigenous_knowledge(params)
        elif query_type == "general_query":
            return self._process_general_query(params)
        else:
            return {"error": "Unknown query type"}
    
    def _process_pest_identification(self, params: Dict) -> Dict[str, Any]:
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

        # Decide if we need to use Ollama
        # (self.use_ollama is the original flag, not the per-query one for prolog-primary mode)
        # If prolog found substantial data AND we are not in a mode that forces ollama for this query type
        # (e.g. complex query as per _should_use_ollama_for_query) we might return prolog data directly.
        # This logic needs refinement based on ollama_for_complex_only and _should_use_ollama_for_query.
        
        # For now, let's assume if we have prolog_data_found, we use it. 
        # If not, or if ollama is generally enabled, we proceed to ollama.
        
        if prolog_data_found and not (self.use_ollama and self._should_use_ollama_for_query("pest_identification", params)):
            # If Prolog found data and Ollama is not strictly needed for this query type
            logging.info("Sufficient data found in Prolog for pest identification. Formatting response.")
            response_text = "\\n".join(prolog_info_parts)
            return {"response": response_text, "source": "prolog"}

        # If Prolog data is not enough, or Ollama is indicated, or it's the primary engine
        if self.use_ollama and self.ollama_handler:
            logging.info("Using Ollama for pest identification.")
            # Prepare context for Ollama, potentially including Prolog findings
            ollama_context = ""
            if prolog_data_found:
                ollama_context = "Based on our knowledge base:\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking: " + user_query
            else:
                ollama_context = user_query

            prompt_content = format_prompt(
                PromptType.PEST_IDENTIFICATION,
                query=ollama_context, # Pass the potentially augmented query
                pest=pest_name,
                crop=crop_name
            )
            
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"], # Assuming system prompt is handled by handler or template
                model=self.ollama_model
            )
            
            if llm_response and llm_response.strip():
                final_response = llm_response
                if prolog_data_found and not llm_response.startswith("Based on our knowledge base"):
                    # Prepend prolog context if LLM didn't seem to use it and we want to ensure it's there
                    # This is a simple way, could be more sophisticated
                    # final_response = "From our knowledge base:\\n" + "\\n".join(prolog_info_parts) + "\\n\\nAdditionally, the AI model suggests:\\n" + llm_response
                    pass # Decided to let LLM response stand, as prompt already included it.

                return {"response": final_response, "source": "ollama"}
            else:
                logging.warning("Ollama returned empty response for pest identification.")
        
        # Fallback if Prolog didn't yield enough and Ollama failed or is disabled
        if prolog_data_found: # At least return what prolog found
             return {"response": "\\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("Using mock response for pest identification as other methods failed.")
        return self._mock_pest_identification(params) # Fallback to mock
    
    def _process_control_methods(self, params: Dict) -> Dict[str, Any]:
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

        # Decision logic similar to _process_pest_identification
        if prolog_data_found and not (self.use_ollama and self._should_use_ollama_for_query("pest_management", params)):
            logging.info("Sufficient data found in Prolog for control methods. Formatting response.")
            response_text = "\\n".join(prolog_info_parts)
            return {"response": response_text, "source": "prolog"}

        if self.use_ollama and self.ollama_handler:
            logging.info("Using Ollama for control methods.")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = "Based on our knowledge base for " + pest_name + ":\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking for control methods: " + user_query
            
            prompt_content = format_prompt(
                PromptType.PEST_MANAGEMENT,
                query=ollama_context,
                pest=pest_name,
                crop=crop_name
            )
            
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"],
                model=self.ollama_model
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("Ollama returned empty response for control methods.")
        
        if prolog_data_found:
            return {"response": "\\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("Using mock response for control methods as other methods failed.")
        return self._mock_control_methods(params)
    
    def _process_crop_pests(self, params: Dict) -> Dict[str, Any]:
        """Process queries for pests affecting specific crops."""
        user_query = params.get("query", "")
        crop_name = params.get("crop")

        prolog_info_parts = []
        prolog_data_found = False
        pest_list_for_ollama = []

        if crop_name:
            logging.info(f"Attempting to get crop info for '{crop_name}' from PrologService.")
            # Use the connector directly for frame-based queries if service doesn't have specific method
            # The PrologConnector.query returns a list of dicts, or empty list on failure.
            # Each dict represents a solution. If query is `crop(name:crop_name, X)`, X should be the attributes.
            crop_details_results = self.prolog_service.connector.query(f"crop(name:{crop_name.lower()}, X)")
            
            if crop_details_results and isinstance(crop_details_results[0].get('X'), list):
                crop_attributes = crop_details_results[0]['X']
                # The attributes are expected to be like ['pests:[pest1, pest2]', 'diseases:[d1]', ...]
                # We need to parse this to find the 'pests' list.
                for attr in crop_attributes:
                    if isinstance(attr, str) and attr.startswith("pests:["):
                        # Basic parsing, assuming format pests:[pestA,pestB]
                        pests_str = attr[len("pests:["):-1] # Remove prefix and suffix ]
                        if pests_str:
                            pest_list_for_ollama = [p.strip() for p in pests_str.split(',')]
                            if pest_list_for_ollama:
                                prolog_data_found = True
                                prolog_info_parts.append(f"Pests known to affect {crop_name}:")
                                prolog_info_parts.extend([f"- {p}" for p in pest_list_for_ollama])
                        break
            if not prolog_data_found:
                 logging.info(f"No specific pest list found in Prolog for crop '{crop_name}'. Query was: crop(name:{crop_name.lower()}, X)")

        else:
            logging.info("No specific crop name provided for Prolog lookup in crop pests.")

        if prolog_data_found and not (self.use_ollama and self._should_use_ollama_for_query("crop_pests", params)):
            logging.info("Sufficient data found in Prolog for crop pests. Formatting response.")
            response_text = "\\n".join(prolog_info_parts)
            return {"response": response_text, "source": "prolog"}

        if self.use_ollama and self.ollama_handler:
            logging.info("Using Ollama for crop pests.")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = f"According to our knowledge base, {crop_name} can be affected by: {', '.join(pest_list_for_ollama)}.\\n\\nUser is asking: {user_query}"
            
            # PromptType.CROP_PESTS doesn't exist, so we use a general or pest_management prompt.
            # Let's assume a general approach or adapt a prompt type if available.
            # For now, we use GENERAL and pass the context directly.
            prompt_content = format_prompt(
                PromptType.GENERAL, # Or a more specific one like PEST_IDENTIFICATION if appropriate
                query=ollama_context,
                crop=crop_name,
                # pests_list=pest_list_for_ollama # Pass to template if it supports it
            )
            
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"],
                model=self.ollama_model
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("Ollama returned empty response for crop pests.")
        
        if prolog_data_found:
            return {"response": "\\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("Using mock response for crop pests as other methods failed.")
        return self._mock_crop_pests(params)
    
    def _process_indigenous_knowledge(self, params: Dict) -> Dict[str, Any]:
        """Process queries about indigenous knowledge."""
        user_query = params.get("query", "")
        # Try to find a specific practice name if provided by entity extraction, or use the whole query
        practice_name = params.get("practice") # Assuming 'practice' could be an extracted entity

        prolog_info_parts = []
        prolog_data_found = False

        if practice_name:
            logging.info(f"Attempting to get indigenous practice details for '{practice_name}' from PrologService.")
            # The PrologService.search_prolog_kb also has a way to get practice_info by name match
            # Or we can query directly via connector if a more specific service method is not available
            # For frame `practice(name:PName, X)`, X has all attributes.
            practice_details_results = self.prolog_service.connector.query(f"practice(name:{practice_name.lower()}, X)")
            if practice_details_results and isinstance(practice_details_results[0].get('X'), list):
                attributes = practice_details_results[0]['X']
                prolog_data_found = True
                prolog_info_parts.append(f"Details for indigenous practice '{practice_name}':")
                # Convert attribute list (e.g., ['type:organic_pesticide', 'description:Details here']) to a dict
                attrs_dict = {}
                for attr_str in attributes:
                    if isinstance(attr_str, str) and ':' in attr_str:
                        key, val = attr_str.split(':', 1)
                        attrs_dict[key.strip()] = val.strip()
                
                if attrs_dict.get('description'):
                    prolog_info_parts.append(f"  Description: {attrs_dict['description']}")
                if attrs_dict.get('type'):
                    prolog_info_parts.append(f"  Type: {attrs_dict['type']}")
                if attrs_dict.get('controls'): # This would be a string like '[aphids,whiteflies]'
                    prolog_info_parts.append(f"  Controls: {attrs_dict['controls'].strip('[]')}") # Basic display
                if attrs_dict.get('resolves'):
                    prolog_info_parts.append(f"  Resolves: {attrs_dict['resolves'].strip('[]')}")
                if attrs_dict.get('cultural_context'):
                    prolog_info_parts.append(f"  Cultural Context: {attrs_dict['cultural_context'].strip('[]')}")
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
                    p_info = prolog_search_result['practice_info']
                    prolog_info_parts.append(f"Found information related to indigenous practice '{p_info.get('name')}':")
                    if p_info.get('description'): prolog_info_parts.append(f"  Description: {p_info['description']}")
                    if p_info.get('type'): prolog_info_parts.append(f"  Type: {p_info['type']}")
                    # ... (add more details from p_info as needed)
                elif prolog_search_result.get('pest_found'): # Less likely for IK query but possible
                     prolog_info_parts.append("Found pest-related information that might involve indigenous practices. Please ask specifically about a practice.")

        if prolog_data_found and not (self.use_ollama and self._should_use_ollama_for_query("indigenous_knowledge", params)):
            logging.info("Sufficient data found in Prolog for indigenous knowledge. Formatting response.")
            response_text = "\\n".join(prolog_info_parts)
            return {"response": response_text, "source": "prolog"}

        if self.use_ollama and self.ollama_handler:
            logging.info("Using Ollama for indigenous knowledge.")
            ollama_context = user_query
            if prolog_data_found:
                ollama_context = "Our knowledge base contains the following on this topic:\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking: " + user_query
            
            prompt_content = format_prompt(
                PromptType.INDIGENOUS_KNOWLEDGE,
                query=ollama_context,
                practice_name=params.get('practice_name', practice_name), # Pass to template
                purpose=params.get('purpose', '') # Pass to template
            )
            
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"],
                model=self.ollama_model
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("Ollama returned empty response for indigenous knowledge.")
        
        if prolog_data_found:
            return {"response": "\\n".join(prolog_info_parts), "source": "prolog_partial"}

        logging.info("Using mock response for indigenous knowledge as other methods failed.")
        return self._mock_indigenous_knowledge(params)
    
    def _process_general_query(self, params: Dict) -> Dict[str, Any]:
        """Process general queries, trying Prolog KB search first, then Ollama."""
        user_query = params.get("query", "")
        prolog_info_parts = []
        prolog_data_found = False

        logging.info(f"Attempting general KB search with PrologService for: {user_query}")
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
                # search_prolog_kb returned something but not pest or practice, which is unusual for its current design
                prolog_data_found = False # Treat as not found for specific formatting
                logging.info("Prolog search_prolog_kb returned non-generic but unhandled result.")
        else:
            logging.info("No specific information found by prolog_service.search_prolog_kb.")

        # Decision logic
        if prolog_data_found and not (self.use_ollama and self._should_use_ollama_for_query("general_query", params)):
            logging.info("Sufficient specific data found in Prolog via general search. Formatting response.")
            response_text = "\\n".join(prolog_info_parts)
            return {"response": response_text, "source": "prolog"}

        # If Prolog data is not enough, or Ollama is indicated, or it's the primary engine for general queries
        if self.use_ollama and self.ollama_handler:
            logging.info("Using Ollama for general query.")
            ollama_context = user_query
            if prolog_data_found: # Prepend any specific findings from KB search
                ollama_context = "Based on our knowledge base:\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking: " + user_query
            
            prompt_content = format_prompt(
                PromptType.GENERAL,
                query=ollama_context
            )
            
            llm_response = self.ollama_handler.generate_response(
                prompt=prompt_content["user_prompt"],
                model=self.ollama_model
            )

            if llm_response and llm_response.strip():
                return {"response": llm_response, "source": "ollama"}
            else:
                logging.warning("Ollama returned empty response for general query.")
        
        # Fallback if Prolog didn't yield specific info and Ollama failed or is disabled
        if prolog_data_found: # Return what little prolog might have found (e.g. partial search result)
             return {"response": "\\n".join(prolog_info_parts), "source": "prolog_partial"}
        
        logging.info("Using default/mock response for general query as other methods failed.")
        # The original mock for general query was in HybridEngine._mock_general_query, which is not defined.
        # We should return a generic message or use a generic mock if available.
        return {
            "response": "I'm sorry, I couldn't find specific information for your query. Could you try rephrasing or asking about a specific pest, crop, or farming practice?",
            "source": "fallback"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        uptime = time.time() - self.start_time
        cache_hit_rate = self.cache_hit_count / self.query_count if self.query_count > 0 else 0
        
        return {
            "uptime_seconds": uptime,
            "query_count": self.query_count,
            "cache_hits": self.cache_hit_count,
            "cache_hit_rate": cache_hit_rate,
            "ollama_available": self.use_ollama and (self.ollama_handler.is_available if self.ollama_handler else False),
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
