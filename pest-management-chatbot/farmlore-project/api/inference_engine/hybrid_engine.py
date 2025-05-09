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

from .prolog_engine import PrologEngine
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
        
        # Initialize the Prolog engine
        self.prolog_engine = PrologEngine()
        
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
    
    @lru_cache(maxsize=100)
    def _cached_prolog_query(self, query_str: str) -> List[Dict]:
        """Cache Prolog queries for performance"""
        return self.prolog_engine.query(query_str)
    
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
        """
        Process pest identification requests using hybrid approach
        
        Args:
            params: Parameters including symptoms, crop, etc.
            
        Returns:
            Dict with identification results
        """
        # Extract parameters
        symptoms = params.get("symptoms", [])
        crop_name = params.get("crop", "")
        description = params.get("description", "")
        query = params.get("query", "")
        
        # Try Prolog first for structured knowledge
        prolog_results = []
        try:
            if symptoms:
                symptom_list = ", ".join([f"'{s}'" for s in symptoms])
                prolog_query = f"pest_identification([{symptom_list}], Pests)"
                prolog_results = self._cached_prolog_query(prolog_query)
        except Exception as e:
            logging.error(f"Prolog query failed: {str(e)}")
        
        # Use Ollama if available to enhance or provide identification
        if self.use_ollama and self.ollama_handler.is_available:
            # Format a prompt with all available information
            prompt_vars = {
                "pest_description": description,
                "affected_crops": crop_name,
                "location": params.get("location", "Lesotho"),
                "observation_time": params.get("time", "recently"),
                "symptoms": ", ".join(symptoms) if symptoms else "unknown"
            }
            
            # Use the pest identification prompt template
            response = self.ollama_handler.generate_response(
                query if query else f"Identify pests affecting {crop_name} with symptoms: {', '.join(symptoms)}",
                prompt_type=PromptType.PEST_IDENTIFICATION,
                **prompt_vars
            )
            
            # Combine Prolog and Ollama results if we have both
            if prolog_results and len(prolog_results) > 0 and "Pests" in prolog_results[0]:
                # If Prolog returned results, include them in the response
                prolog_pests = prolog_results[0]["Pests"]
                
                return {
                    "response": response,
                    "structured_data": {
                        "pests": prolog_pests
                    },
                    "source": "hybrid"
                }
            else:
                # If only Ollama results, return them
                return {
                    "response": response,
                    "source": "ollama"
                }
        
        # Fallback to mock data if neither is available
        if not prolog_results or len(prolog_results) == 0:
            return {
                "response": "Based on the symptoms, these could be aphids or spider mites. Aphids cause yellowing leaves and stunted growth, while spider mites create webbing and leaf spotting.",
                "structured_data": self._mock_pest_identification(params),
                "source": "mock"
            }
        
        # Return Prolog results if that's all we have
        return {
            "response": f"Based on the symptoms, I've identified these pests: {', '.join(prolog_results[0].get('Pests', []))}",
            "structured_data": {"pests": prolog_results[0].get("Pests", [])},
            "source": "prolog"
        }
    
    def _process_control_methods(self, params: Dict) -> Dict[str, Any]:
        """
        Process pest control method requests
        
        Args:
            params: Parameters including pest name, crop, etc.
            
        Returns:
            Dict with control method results
        """
        # Extract parameters
        pest_name = params.get("pest", "")
        crop_name = params.get("crop", "")
        query = params.get("query", "")
        
        # Try Prolog for structured knowledge
        prolog_results = []
        try:
            if pest_name:
                prolog_query = f"control_methods('{pest_name}', Methods)"
                prolog_results = self._cached_prolog_query(prolog_query)
        except Exception as e:
            logging.error(f"Prolog query failed: {str(e)}")
            
        # Use Ollama if available
        if self.use_ollama and self.ollama_handler.is_available:
            # Format prompt with all available information
            prompt_vars = {
                "pest_name": pest_name,
                "crop_type": crop_name,
                "location": params.get("location", "Lesotho"),
                "severity": params.get("severity", "moderate"),
                "conditions": params.get("conditions", "traditional small-scale farming")
            }
            
            # Use the pest management prompt template
            response = self.ollama_handler.generate_response(
                query if query else f"How to control {pest_name} on {crop_name}?",
                prompt_type=PromptType.PEST_MANAGEMENT,
                **prompt_vars
            )
            
            # Combine Prolog and Ollama results if we have both
            if prolog_results and len(prolog_results) > 0 and "Methods" in prolog_results[0]:
                return {
                    "response": response,
                    "structured_data": {
                        "methods": prolog_results[0]["Methods"]
                    },
                    "source": "hybrid"
                }
            else:
                return {
                    "response": response,
                    "source": "ollama"
                }
        
        # Fallback to mock data
        if not prolog_results or len(prolog_results) == 0:
            return {
                "response": "For controlling these pests, you can use natural methods like neem oil spray or insecticidal soap. Apply directly to affected areas, focusing on the undersides of leaves.",
                "structured_data": self._mock_control_methods(params),
                "source": "mock"
            }
            
        # Return Prolog results if that's all we have
        return {
            "response": f"Here are some methods to control {pest_name}: {', '.join(prolog_results[0].get('Methods', []))}",
            "structured_data": {"methods": prolog_results[0].get("Methods", [])},
            "source": "prolog"
        }
    
    def _process_crop_pests(self, params: Dict) -> Dict[str, Any]:
        """Process crop pest information requests"""
        crop_name = params.get("crop", "")
        query = params.get("query", "")
        
        # Try Prolog first
        prolog_results = []
        try:
            if crop_name:
                prolog_query = f"crop_pests('{crop_name}', Pests)"
                prolog_results = self._cached_prolog_query(prolog_query)
        except Exception as e:
            logging.error(f"Prolog query failed: {str(e)}")
            
        # Use Ollama if available
        if self.use_ollama and self.ollama_handler.is_available:
            # Use general template but customize with crop information
            response = self.ollama_handler.generate_response(
                query if query else f"What pests affect {crop_name} crops and how to identify them?",
                prompt_type=PromptType.GENERAL
            )
            
            # Combine results if we have both
            if prolog_results and len(prolog_results) > 0 and "Pests" in prolog_results[0]:
                return {
                    "response": response,
                    "structured_data": {
                        "crop": crop_name,
                        "pests": prolog_results[0]["Pests"]
                    },
                    "source": "hybrid"
                }
            else:
                return {
                    "response": response,
                    "source": "ollama"
                }
        
        # Fallback to mock data
        return {
            "response": f"Common pests affecting {crop_name} include tomato hornworm and aphids. Hornworms cause severe damage in summer, while aphids are present spring through fall causing moderate damage.",
            "structured_data": self._mock_crop_pests(params),
            "source": "mock"
        }
    
    def _process_indigenous_knowledge(self, params: Dict) -> Dict[str, Any]:
        """Process indigenous knowledge requests"""
        practice = params.get("practice", "")
        query = params.get("query", "")
        
        # Try Prolog first for structured knowledge
        prolog_results = []
        try:
            if practice:
                prolog_query = f"indigenous_knowledge('{practice}', Methods)"
                prolog_results = self._cached_prolog_query(prolog_query)
        except Exception as e:
            logging.error(f"Prolog query failed: {str(e)}")
            
        # Use Ollama if available
        if self.use_ollama and self.ollama_handler.is_available:
            # Format with indigenous knowledge template
            prompt_vars = {
                "practice_name": practice,
                "purpose": params.get("purpose", "pest management")
            }
            
            response = self.ollama_handler.generate_response(
                query if query else f"Tell me about the traditional practice of {practice} in Lesotho farming",
                prompt_type=PromptType.INDIGENOUS_KNOWLEDGE,
                **prompt_vars
            )
            
            return {
                "response": response,
                "source": "ollama"
            }
        
        # Fallback to mock data
        return {
            "response": f"Traditional methods like ash sprinkle and chili pepper spray are used in Lesotho for pest control. These methods have been passed down through generations of farmers.",
            "structured_data": self._mock_indigenous_knowledge(params),
            "source": "mock"
        }
    
    def _process_general_query(self, params: Dict) -> Dict[str, Any]:
        """Process general queries that don't fit specific categories"""
        query = params.get("query", "")
        
        if not query:
            return {
                "response": "I need a question to answer. Please provide more details.",
                "source": "system"
            }
            
        # Use Ollama if available
        if self.use_ollama and self.ollama_handler.is_available:
            response = self.ollama_handler.generate_response(
                query,
                prompt_type=PromptType.GENERAL
            )
            
            return {
                "response": response,
                "source": "ollama"
            }
            
        # Fallback to a generic response
        return {
            "response": "I don't have enough information to answer that question. Please try asking about pest identification, control methods, or indigenous knowledge.",
            "source": "system"
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
