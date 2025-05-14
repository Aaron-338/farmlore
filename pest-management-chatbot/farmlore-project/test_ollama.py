"""
Test script for Ollama integration with the FarmLore application
"""
import os
import sys
import logging
import time
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set environment variables to enable Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://ollama:11434'
os.environ['OLLAMA_MODEL'] = 'tinyllama'

# Add the app directory to the path
sys.path.append('/app')

# Test direct connection to Ollama service
def test_ollama_connection():
    """Test direct connection to Ollama service"""
    logging.info("Testing direct connection to Ollama service...")
    
    ollama_base_url = "http://ollama:11434"
    api_tags = f"{ollama_base_url}/api/tags"
    
    try:
        logging.info(f"Sending request to Ollama tags API: {api_tags}")
        response = requests.get(api_tags, timeout=10)
        logging.info(f"Ollama tags response status: {response.status_code}")
        
        if response.status_code == 200:
            logging.info(f"Available models: {response.json()}")
            return True
        else:
            logging.error(f"Failed to get tags from Ollama: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error connecting to Ollama: {str(e)}")
        return False

# Test generating text with Ollama
def test_ollama_generate():
    """Test generating text with Ollama"""
    logging.info("Testing text generation with Ollama...")
    
    ollama_base_url = "http://ollama:11434"
    api_generate = f"{ollama_base_url}/api/generate"
    
    test_payload = {
        "model": "tinyllama",
        "prompt": "What are common pests that affect tomato plants?",
        "stream": False
    }
    
    try:
        logging.info(f"Sending request to Ollama generate API: {api_generate}")
        logging.info(f"Payload: {test_payload}")
        
        start_time = time.time()
        response = requests.post(api_generate, json=test_payload, timeout=60)
        duration = time.time() - start_time
        
        logging.info(f"Ollama generate response received in {duration:.2f}s with status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            logging.info(f"Generated text: {response_data.get('response', 'No response')}")
            return True
        else:
            logging.error(f"Failed to generate text with Ollama: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error generating text with Ollama: {str(e)}")
        return False

# Test the PrologEngine integration with Ollama
def test_prolog_engine():
    """Test the PrologEngine with Ollama integration"""
    try:
        from api.inference_engine.prolog_engine import PrologEngine
        
        logging.info("Initializing PrologEngine with Ollama integration...")
        
        # Initialize the PrologEngine
        engine = PrologEngine()
        
        # Check if Ollama integration is enabled
        logging.info(f"Ollama integration enabled: {engine.use_ollama}")
        
        if hasattr(engine, 'ollama_handler'):
            logging.info(f"Ollama handler available: {True}")
            logging.info(f"Ollama is available: {engine.ollama_handler.is_available if engine.use_ollama else 'N/A'}")
            
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
                return True
            else:
                logging.info("Ollama integration not available")
                return False
        else:
            logging.error("PrologEngine does not have ollama_handler attribute")
            return False
    except Exception as e:
        logging.error(f"Error testing PrologEngine with Ollama: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n===== TESTING FARMLORE OLLAMA INTEGRATION =====\n")
    
    # Test direct connection to Ollama
    print("\n--- Testing Direct Connection to Ollama ---\n")
    ollama_available = test_ollama_connection()
    
    if ollama_available:
        # Test generating text with Ollama
        print("\n--- Testing Text Generation with Ollama ---\n")
        test_ollama_generate()
        
        # Test PrologEngine integration with Ollama
        print("\n--- Testing PrologEngine Integration with Ollama ---\n")
        test_prolog_engine()
    
    print("\n===== OLLAMA INTEGRATION TEST COMPLETE =====\n") 