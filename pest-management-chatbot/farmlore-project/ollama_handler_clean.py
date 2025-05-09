import requests
import json
import logging
from typing import Dict, List, Optional, Any
import time
import re
import threading
from core.data_structures import ConcurrentCache

logger = logging.getLogger(__name__)

class OllamaHandler:
    """Handler for interacting with Ollama API."""
    
    def __init__(self, base_url="http://localhost:11434", timeout=60):
        """Initialize the Ollama handler."""
        self.base_url = base_url
        # Ensure the base_url doesn't end with a slash
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        # Set API endpoints
        self.api_generate = f"{self.base_url}/api/generate"
        self.api_chat = f"{self.base_url}/api/chat"
        self.api_tags = f"{self.base_url}/api/tags"
        
        self.timeout = timeout  # Increased timeout to 60 seconds
        
        # Create a session object for connection pooling
        self.session = requests.Session()
        
        # Initialize response cache for performance
        self.response_cache = ConcurrentCache(max_size=500)
        
        # Setup non-blocking initialization
        self._initialization_complete = threading.Event()
        self._initialization_success = False
        
        # Start non-blocking initialization
        self._initialize_in_background()
    
    def _initialize_in_background(self):
        """Initialize the Ollama API connection in a background thread."""
        logger.info(f"Starting non-blocking initialization of Ollama handler with endpoint: {self.base_url}")
        
        thread = threading.Thread(target=self._initialize)
        thread.daemon = True
        thread.start()
    
    def _initialize(self):
        """Perform the actual initialization work."""
        try:
            self.is_available = self._check_availability()
            self._initialization_success = self.is_available
        except Exception as e:
            logger.error(f"Error during Ollama initialization: {str(e)}")
            self.is_available = False
            self._initialization_success = False
        finally:
            self._initialization_complete.set()
    
    def wait_for_initialization(self, timeout=30):
        """
        Wait for initialization to complete with timeout.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        if self._initialization_complete.wait(timeout):
            return self._initialization_success
        logger.warning(f"Timed out waiting for Ollama initialization after {timeout} seconds")
        return False
    
    def _check_availability(self):
        """Check if Ollama is available and fully operational."""
        try:
            # First check basic connectivity
            response = self.session.get(self.api_tags, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Ollama returned non-200 status: {response.status_code}")
                return False
            
            # Try to get the list of models
            tags_data = response.json()
            logger.info(f"Ollama model tags: {tags_data}")
            
            # Check if we have any models available
            if 'models' not in tags_data or not tags_data['models']:
                logger.warning("No models available in Ollama")
                return False
            
            # List available models
            available_models = [model.get('name', 'unknown') for model in tags_data.get('models', [])]
            logger.info(f"Available Ollama models: {', '.join(available_models)}")
            
            # Find the preferred model to use based on what's available
            # Try tinyllama first, then gemma, then the first available model
            preferred_models = ['tinyllama', 'gemma', 'llama2']
            model_to_use = None
            
            for preferred in preferred_models:
                for available in available_models:
                    if preferred in available:
                        model_to_use = available
                        break
                if model_to_use:
                    break
            
            # If no preferred model, use the first available
            if not model_to_use and available_models:
                model_to_use = available_models[0]
                
            if not model_to_use:
                logger.warning("No suitable models found in Ollama")
                return False
            
            logger.info(f"Using model: {model_to_use}")
            
            # Test a minimal generation to verify the API is working
            test_payload = {
                "model": model_to_use,
                "prompt": "test",
                "stream": False
            }
            
            try:
                logger.info(f"Testing Ollama API with model {model_to_use}")
                logger.info(f"This may take up to 30 seconds for the first inference...")
                test_response = self.session.post(
                    self.api_generate,
                    json=test_payload, 
                    timeout=self.timeout
                )
                
                logger.info(f"Ollama API test response status: {test_response.status_code}")
                
                if test_response.status_code == 404:
                    # Log error details
                    logger.warning(f"API endpoint not found. Response: {test_response.text}")
                    return False
                
                if test_response.status_code != 200:
                    logger.warning(f"Ollama API test failed with status: {test_response.status_code}")
                    return False
                    
                # Try to parse the response as JSON
                test_result = test_response.json()
                logger.info(f"Ollama API test response: {json.dumps(test_result)[:100]}...")
                
                if "response" not in test_result:
                    logger.warning("Ollama API test returned unexpected response format")
                    return False
                    
                return True
                
            except Exception as e:
                logger.warning(f"Ollama API test failed: {str(e)}")
                return False
                
        except Exception as e:
            logger.warning(f"Ollama availability check failed: {str(e)}")
            return False
    
    def _validate_and_clean_response(self, response_text):
        """
        Clean and validate the response from Ollama API.
        
        Args:
            response_text (str): The raw response text from Ollama API
            
        Returns:
            str: Cleaned and validated response text
        """
        if not response_text or not isinstance(response_text, str):
            logger.warning(f"Invalid response type: {type(response_text)}")
            return ""
        
        # Remove any markdown code block indicators
        cleaned = re.sub(r'```[a-zA-Z]*\n|```', '', response_text)
        
        # Remove excessive newlines (more than 2 in a row)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Check if the response is too short or meaningless
        if len(cleaned) < 5 or cleaned.lower() in ["i don't know", "unknown", "error"]:
            logger.warning(f"Response too short or meaningless: '{cleaned}'")
            return ""
        
        return cleaned
    
    def _generate_fallback_response(self, prompt):
        """
        Generate a fallback response when Ollama is not available.
        
        Args:
            prompt (str): The original prompt
            
        Returns:
            str: A generic fallback response
        """
        logger.info("Generating fallback response")
        
        # Return a generic response based on the type of query
        if "?" in prompt:
            return "I'm unable to provide specific information at the moment. Please try again later or consult with a local agricultural expert."
        elif any(keyword in prompt.lower() for keyword in ["help", "advice", "suggest", "recommend"]):
            return ("For pest management, consider reviewing common organic practices such as companion planting, "
                   "physical barriers, crop rotation, and natural predators. These approaches have been traditionally "
                   "effective and are environmentally friendly.")
        else:
            return ("Thank you for your input. While I'm currently operating with limited capabilities, "
                   "I recommend consulting traditional farming knowledge and practices for sustainable pest management solutions.")
    
    def generate_response(self, prompt, model=None, temperature=0.7, max_tokens=500):
        """Generate a response using the Ollama API."""
        # Wait for initialization to complete if it hasn't already
        if not self._initialization_complete.is_set():
            logger.info("Waiting for Ollama initialization to complete...")
            self.wait_for_initialization(timeout=10)
        
        # Create a cache key based on the prompt and parameters
        cache_key = f"{prompt}_{model}_{temperature}_{max_tokens}"
        
        # Check if we have a cached response
        cached_response = self.response_cache.get(cache_key)
        if cached_response is not None:
            logger.info("Using cached LLM response")
            return cached_response
        
        # Always keep fallback ready in case of any issues
        fallback_response = self._generate_fallback_response(prompt)
        
        if not self.is_available:
            logger.info("Ollama not available, using fallback response")
            return fallback_response
        
        # If model is None, try to get available models
        if model is None:
            try:
                response = self.session.get(self.api_tags, timeout=5)
                if response.status_code == 200:
                    tags_data = response.json()
                    available_models = [m.get('name') for m in tags_data.get('models', [])]
                    
                    # Prefer tinyllama, gemma, or first available
                    for preferred in ['tinyllama', 'gemma', 'llama2']:
                        for available in available_models:
                            if preferred in available:
                                model = available
                                break
                        if model:
                            break
                    
                    if not model and available_models:
                        model = available_models[0]
                        
                if not model:
                    model = "tinyllama"  # Default fallback
            except Exception as e:
                logger.error(f"Error getting available models: {str(e)}")
                model = "tinyllama"  # Default fallback
        
        try:
            logger.info(f"Sending request to Ollama API with model {model}")
            
            # Use a simpler payload to avoid potential issues
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            # Log the request
            logger.debug(f"Request payload: {json.dumps(payload)}")
            
            # Set a timeout to avoid hanging
            start_time = time.time()
            response = self.session.post(self.api_generate, json=payload, timeout=self.timeout)
            response_time = time.time() - start_time
            
            logger.info(f"Ollama response received in {response_time:.2f} seconds")
            logger.debug(f"Response status: {response.status_code}")
            
            # Check status code before proceeding
            if response.status_code != 200:
                logger.error(f"Ollama returned non-200 status: {response.status_code}")
                return fallback_response
            
            try:
                # Try to parse as JSON
                result = response.json()
                logger.debug(f"Parsed JSON response with keys: {', '.join(result.keys())}")
                
                if "response" in result:
                    response_text = result["response"]
                    cleaned_response = self._validate_and_clean_response(response_text)
                    
                    if cleaned_response:
                        # Cache the successful response
                        self.response_cache.set(cache_key, cleaned_response)
                        return cleaned_response
                    else:
                        logger.warning("Empty or invalid response from Ollama")
                        return fallback_response
                else:
                    logger.warning(f"Unexpected response format: {json.dumps(result)[:100]}...")
                    return fallback_response
                    
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {response.text[:100]}...")
                return fallback_response
                
        except requests.exceptions.Timeout:
            logger.error(f"Request to Ollama API timed out after {self.timeout} seconds")
            return fallback_response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return fallback_response 