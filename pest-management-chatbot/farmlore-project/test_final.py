"""
Final test script for the PrologEngine with longer timeout
"""
import os
import sys
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set environment variables to enable Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://ollama:11434'
os.environ['OLLAMA_MODEL'] = 'tinyllama'

# Add the app directory to the path
sys.path.append('/app')

# First patch the OllamaHandler class to increase the timeout
def patch_ollama_handler():
    """Patch the OllamaHandler timeout"""
    from api.inference_engine.ollama_handler import OllamaHandler
    
    # Store the original constructor
    original_init = OllamaHandler.__init__
    
    # Create a patched constructor with longer timeout
    def patched_init(self, base_url="http://localhost:11434", timeout=60):
        logging.info(f"Initializing OllamaHandler with patched timeout: {timeout}s")
        original_init(self, base_url, timeout)
    
    # Replace the constructor
    OllamaHandler.__init__ = patched_init
    
    logging.info("OllamaHandler patched successfully")

# Now test the PrologEngine
def test_prolog_engine():
    """Test the PrologEngine with Ollama integration"""
    from api.inference_engine.prolog_engine import PrologEngine
    
    logging.info("Initializing PrologEngine with Ollama integration...")
    
    # Initialize the PrologEngine
    engine = PrologEngine()
    
    # Check if Ollama integration is enabled
    logging.info(f"Ollama integration enabled: {engine.use_ollama}")
    logging.info(f"Ollama is available: {engine.ollama_handler.is_available if engine.use_ollama else 'N/A'}")
    
    # If Ollama is not available, try to manually check availability
    if engine.use_ollama and not engine.ollama_handler.is_available:
        logging.info("Ollama not available. Trying to manually check with longer timeout...")
        
        # Try to access the Ollama API directly
        import requests
        try:
            # First try the tags endpoint
            response = requests.get(engine.ollama_handler.api_tags, timeout=5)
            if response.status_code == 200:
                logging.info(f"Tags API successful: {response.json()}")
                
                # Then try a simple generation
                test_payload = {
                    "model": "tinyllama",
                    "prompt": "test",
                    "stream": False
                }
                
                logging.info("Testing generate endpoint with long timeout...")
                try:
                    start_time = time.time()
                    test_response = requests.post(
                        engine.ollama_handler.api_generate,
                        json=test_payload,
                        timeout=60  # Long timeout
                    )
                    duration = time.time() - start_time
                    
                    logging.info(f"Generation response received in {duration:.2f}s with status: {test_response.status_code}")
                    
                    if test_response.status_code == 200:
                        # Manually set the handler to available
                        engine.ollama_handler.is_available = True
                        engine.use_ollama = True
                        logging.info("Manually enabled Ollama integration")
                except Exception as e:
                    logging.error(f"Error testing generate endpoint: {str(e)}")
        except Exception as e:
            logging.error(f"Error testing Ollama API: {str(e)}")
    
    # Test a query
    if engine.use_ollama and engine.ollama_handler.is_available:
        logging.info("Testing query with Ollama integration...")
        query = "What are some effective organic methods to control aphids on tomato plants?"
        
        start_time = time.time()
        results = engine.query(query)
        duration = time.time() - start_time
        
        logging.info(f"Query completed in {duration:.2f}s")
        
        # Display results
        logging.info(f"Query results: {results}")
        
        if results and isinstance(results, list) and len(results) > 0:
            if 'response' in results[0]:
                logging.info(f"Response content: {results[0]['response']}")
            else:
                logging.info(f"Unexpected response format: {results[0]}")
        else:
            logging.info("No results returned")
    else:
        logging.info("Ollama integration not available, using mock PrologEngine")
        query = "What are some effective organic methods to control aphids on tomato plants?"
        results = engine.query(query)
        logging.info(f"Mock query results: {results}")

if __name__ == "__main__":
    # First patch the OllamaHandler
    patch_ollama_handler()
    
    # Then test the PrologEngine
    test_prolog_engine() 