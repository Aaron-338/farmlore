"""
Test script for the PrologEngine with Ollama integration
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set environment variables to enable Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://ollama:11434'
os.environ['OLLAMA_MODEL'] = 'tinyllama'

# Import the PrologEngine class
sys.path.append('/app')
from api.inference_engine.prolog_engine import PrologEngine
from api.inference_engine.ollama_handler import OllamaHandler

def test_prolog_engine():
    """Test the PrologEngine with Ollama integration"""
    logging.info("Initializing OllamaHandler with increased timeout...")
    
    # Test direct OllamaHandler with increased timeout
    direct_handler = OllamaHandler(base_url='http://ollama:11434', timeout=60)
    
    # Monkey patch the _check_availability method to use a longer timeout
    original_check = direct_handler._check_availability
    def patched_check():
        try:
            # First check basic connectivity
            response = direct_handler.session.get(direct_handler.api_tags, timeout=5)
            if response.status_code != 200:
                logging.warning(f"Ollama returned non-200 status: {response.status_code}")
                return False
            
            # Test a minimal generation to verify the API is working
            test_payload = {
                "model": "tinyllama",
                "prompt": "test",
                "stream": False
            }
            
            try:
                logging.info(f"Testing Ollama API with endpoint: {direct_handler.api_generate}")
                logging.info(f"This may take up to 30 seconds for the first inference...")
                test_response = direct_handler.session.post(
                    direct_handler.api_generate,
                    json=test_payload, 
                    timeout=30  # Increased timeout for first inference
                )
                
                logging.info(f"Ollama API test response status: {test_response.status_code}")
                
                if test_response.status_code != 200:
                    logging.warning(f"Ollama API test failed with status: {test_response.status_code}")
                    return False
                    
                # Try to parse the response as JSON
                test_result = test_response.json()
                logging.info(f"Ollama API test response: {test_result.get('response', '')[:50]}...")
                
                return True
                
            except Exception as e:
                logging.warning(f"Ollama API test failed: {str(e)}")
                return False
                
        except Exception as e:
            logging.warning(f"Ollama availability check failed: {str(e)}")
            return False
    
    # Replace the method
    direct_handler._check_availability = patched_check
    
    # Re-check availability with the patched method
    direct_handler.is_available = direct_handler._check_availability()
    
    logging.info(f"Direct OllamaHandler available: {direct_handler.is_available}")
    
    if direct_handler.is_available:
        logging.info("Testing direct OllamaHandler generate...")
        response = direct_handler.generate_response(
            "What are common pests for tomato plants?", 
            model="tinyllama",
            temperature=0.7
        )
        logging.info(f"Direct response: {response[:200]}...")
    
    logging.info("Initializing PrologEngine with Ollama integration...")
    # Initialize the PrologEngine
    engine = PrologEngine()
    
    # Check if Ollama integration is enabled
    logging.info(f"Ollama integration enabled: {engine.use_ollama}")
    logging.info(f"Ollama is available: {engine.ollama_handler.is_available if engine.use_ollama else 'N/A'}")
    
    # Test a query
    logging.info("Testing query...")
    query = "What are some effective organic methods to control aphids on tomato plants?"
    results = engine.query(query)
    
    # Display results
    logging.info(f"Query results: {results}")
    
    if results and isinstance(results, list) and len(results) > 0:
        if 'response' in results[0]:
            logging.info(f"Response content: {results[0]['response']}")
        else:
            logging.info(f"Unexpected response format: {results[0]}")
    else:
        logging.info("No results returned")

if __name__ == "__main__":
    test_prolog_engine() 