"""
Simplified test script to directly test the Ollama integration
"""
import os
import sys
import logging
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set environment variables to enable Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://ollama:11434'
os.environ['OLLAMA_MODEL'] = 'tinyllama'

# Test direct import of ollama_handler
try:
    # First try to include the app directory in path
    sys.path.insert(0, '/app')
    logging.info(f"Python path: {sys.path}")
    
    # Import the ollama_handler
    from api.inference_engine.ollama_handler import OllamaHandler
    
    logging.info("Successfully imported OllamaHandler module")
    
    # Initialize OllamaHandler
    handler = OllamaHandler(base_url="http://ollama:11434", timeout=30)
    
    logging.info(f"OllamaHandler initialized with base_url: {handler.base_url}")
    logging.info(f"API tags endpoint: {handler.api_tags}")
    logging.info(f"API generate endpoint: {handler.api_generate}")
    
    # Check Ollama availability manually
    try:
        logging.info("Checking Ollama availability...")
        response = requests.get(handler.api_tags, timeout=10)
        is_available = response.status_code == 200
        logging.info(f"Ollama tags response status: {response.status_code}")
        if is_available:
            logging.info(f"Available models: {response.json()}")
    except Exception as e:
        is_available = False
        logging.error(f"Error checking Ollama availability: {str(e)}")
    
    logging.info(f"Ollama is_available: {is_available}")
    
    if is_available:
        # Test generating text
        logging.info("Testing text generation with Ollama...")
        
        prompt = "What are common pests that affect tomato plants?"
        logging.info(f"Testing generation with prompt: '{prompt}'")
        
        # Look for generate method
        if hasattr(handler, 'generate'):
            start_time = time.time()
            response = handler.generate(prompt)
            duration = time.time() - start_time
            
            logging.info(f"Generation completed in {duration:.2f}s")
            logging.info(f"Response: {response}")
        else:
            logging.error("OllamaHandler does not have a generate method")
            
            # Try direct generation via API
            logging.info("Trying direct generation via API...")
            payload = {
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
            
            start_time = time.time()
            response = requests.post(handler.api_generate, json=payload, timeout=60)
            duration = time.time() - start_time
            
            logging.info(f"Direct API generation completed in {duration:.2f}s with status: {response.status_code}")
            if response.status_code == 200:
                logging.info(f"Generated text: {response.json().get('response', 'No response')}")
            else:
                logging.error(f"Failed to generate text: {response.text}")
        
except ImportError as e:
    logging.error(f"Import error: {str(e)}")
except Exception as e:
    logging.error(f"Error testing Ollama handler: {str(e)}")

print("\n===== OLLAMA DIRECT INTEGRATION TEST COMPLETE =====\n") 