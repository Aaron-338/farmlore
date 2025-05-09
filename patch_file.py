"""
Script to directly modify the OllamaHandler.py file in the container
"""
import os

def create_patched_file():
    # Find where the file is located
    find_cmd = "docker compose exec web bash -c 'find /app -name ollama_handler.py'"
    print(f"Finding file with: {find_cmd}")
    
    # Create a patched version
    patch = """
import requests
import json
import logging
from typing import Dict, List, Optional, Any
import time
import re
from core.data_structures import ConcurrentCache

logger = logging.getLogger(__name__)

class OllamaHandler:
    \"\"\"Handler for interacting with Ollama API.\"\"\"
    
    def __init__(self, base_url="http://localhost:11434", timeout=30):
        \"\"\"Initialize the Ollama handler.\"\"\"
        self.base_url = base_url
        # Ensure the base_url doesn't end with a slash
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        # Set API endpoints
        self.api_generate = f"{self.base_url}/api/generate"
        self.api_chat = f"{self.base_url}/api/chat"
        self.api_tags = f"{self.base_url}/api/tags"
        
        self.timeout = timeout  # Increased timeout to 30 seconds
        
        # Create a session object for connection pooling
        self.session = requests.Session()
        
        self.is_available = self._check_availability()
        
        # Initialize response cache for performance
        self.response_cache = ConcurrentCache(max_size=500)
        
        if not self.is_available:
            logger.warning("Ollama is not available. Using Prolog-based fallback.")
        else:
            logger.info("Ollama is available and will be used for response generation.")
    
    def _check_availability(self):
        \"\"\"Check if Ollama is available and fully operational.\"\"\"
        try:
            # First check basic connectivity
            response = self.session.get(self.api_tags, timeout=5)
            if response.status_code != 200:
                logger.warning(f"Ollama returned non-200 status: {response.status_code}")
                return False
            
            # Try to get the list of models
            tags_data = response.json()
            logger.info(f"Ollama model tags: {tags_data}")
            
            # Test a minimal generation to verify the API is working
            test_payload = {
                "model": "tinyllama",
                "prompt": "test",
                "stream": False
            }
            
            try:
                logger.info(f"Testing Ollama API with endpoint: {self.api_generate}")
                logger.info(f"This may take up to 30 seconds for the first inference...")
                test_response = self.session.post(
                    self.api_generate,
                    json=test_payload, 
                    timeout=30  # Increased timeout for first inference
                )
                
                logger.info(f"Ollama API test response status: {test_response.status_code}")
                
                if test_response.status_code == 404:
                    # Log error details
                    logger.warning(f"API endpoint not found. Response: {test_response.text}")
                    # Try the alternative endpoint format
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
        
    def generate_response(self, prompt, model="tinyllama", temperature=0.7, max_tokens=500):
        \"\"\"Generate a response using the Ollama API.\"\"\"
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
                    raw_response = result["response"]
                    # Validate and clean the response
                    cleaned_response = self._validate_and_clean_response(raw_response)
                    
                    # Only cache if we got a valid response
                    if cleaned_response and len(cleaned_response) > 10:
                        self.response_cache.put(cache_key, cleaned_response)
                        return cleaned_response
                    else:
                        logger.warning("Ollama returned empty or invalid response")
                        return fallback_response
                else:
                    logger.warning("No 'response' field in Ollama API response")
                    return fallback_response
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing Ollama response as JSON: {str(e)}")
                return fallback_response
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while waiting for Ollama response (timeout={self.timeout}s)")
            return fallback_response
            
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            return fallback_response
    """
    
    return patch

if __name__ == "__main__":
    patch_content = create_patched_file()
    
    # Write the patch to a file
    with open("ollama_handler_patched.py", "w") as f:
        f.write(patch_content)
    
    print("Created patched file: ollama_handler_patched.py")
    print("Now copy it to the container with:")
    print("docker compose exec web bash -c 'find /app -name ollama_handler.py'")
    print("docker compose cp ollama_handler_patched.py web:/app/api/inference_engine/ollama_handler.py") 