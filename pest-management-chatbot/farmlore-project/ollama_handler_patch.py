"""
A script to patch the OllamaHandler class in the container to increase timeouts
"""
import os
import sys
import logging
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the app directory to the path
sys.path.append('/app')

# Import the OllamaHandler class
from api.inference_engine.ollama_handler import OllamaHandler

def patch_ollama_handler():
    """Patch the OllamaHandler class to increase timeouts and retry logic"""
    logging.info("Patching OllamaHandler class...")
    
    # Create a simple test function to call Ollama directly
    def test_ollama_directly():
        try:
            logging.info("Testing Ollama API directly...")
            # First test with a simple GET to check if the service is up
            response = requests.get("http://ollama:11434/api/tags", timeout=5)
            logging.info(f"Tags API response: {response.status_code}")
            
            if response.status_code == 200:
                logging.info(f"Available models: {response.json()}")
                
                # Then try a simple generation
                payload = {
                    "model": "tinyllama",
                    "prompt": "Hello, world!",
                    "stream": False
                }
                
                logging.info("Sending test prompt to Ollama API...")
                gen_response = requests.post(
                    "http://ollama:11434/api/generate",
                    json=payload,
                    timeout=60  # Long timeout
                )
                
                if gen_response.status_code == 200:
                    result = gen_response.json()
                    logging.info(f"Generation successful. Response: {result.get('response', '')[:100]}...")
                    return True
                else:
                    logging.error(f"Generation failed with status: {gen_response.status_code}")
                    logging.error(f"Response: {gen_response.text}")
            else:
                logging.error(f"Tags API failed with status: {response.status_code}")
                
            return False
        except Exception as e:
            logging.error(f"Error testing Ollama API: {str(e)}")
            return False
    
    # Test direct API access
    if test_ollama_directly():
        logging.info("Direct Ollama API access works!")
    else:
        logging.warning("Direct Ollama API access failed.")
    
    # Create a custom instance with increased timeout
    ollama = OllamaHandler(base_url="http://ollama:11434", timeout=60)
    
    # Patch the _check_availability method for longer timeouts
    original_check = ollama._check_availability
    
    def patched_check():
        try:
            # Simple connectivity check first
            response = requests.get(ollama.api_tags, timeout=5)
            logging.info(f"Tags API response in patched method: {response.status_code}")
            
            if response.status_code != 200:
                return False
            
            # Try a super simple generation with large timeout
            for attempt in range(3):  # Try up to 3 times
                try:
                    logging.info(f"Testing Ollama generation (attempt {attempt+1}/3)")
                    test_payload = {"model": "tinyllama", "prompt": "test", "stream": False}
                    
                    start_time = time.time()
                    test_response = requests.post(
                        ollama.api_generate,
                        json=test_payload,
                        timeout=30  # 30 second timeout
                    )
                    duration = time.time() - start_time
                    
                    logging.info(f"Ollama response received in {duration:.2f} seconds")
                    
                    if test_response.status_code == 200:
                        result = test_response.json()
                        logging.info(f"Test response: {result.get('response', '')[:50]}...")
                        return True
                    else:
                        logging.warning(f"Test failed with status: {test_response.status_code}")
                        time.sleep(2)  # Wait before retry
                except Exception as e:
                    logging.warning(f"Test attempt {attempt+1} failed: {str(e)}")
                    time.sleep(2)  # Wait before retry
            
            return False
        except Exception as e:
            logging.error(f"Availability check failed: {str(e)}")
            return False
    
    # Replace the method
    ollama._check_availability = patched_check
    
    # Re-check availability with the patched method
    ollama.is_available = ollama._check_availability()
    
    logging.info(f"Patched OllamaHandler available: {ollama.is_available}")
    
    if ollama.is_available:
        logging.info("Testing patched OllamaHandler...")
        response = ollama.generate_response(
            "What are common pests for tomato plants?",
            model="tinyllama",
            temperature=0.7
        )
        logging.info(f"Patched response: {response[:200]}...")
    else:
        logging.error("Patched OllamaHandler still not available")

if __name__ == "__main__":
    patch_ollama_handler() 