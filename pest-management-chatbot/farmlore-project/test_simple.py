"""
Simple test script for Ollama connection
"""
import requests
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_ollama():
    """Test the connection to Ollama API"""
    try:
        # Check if the tags endpoint works
        tags_url = "http://ollama:11434/api/tags"
        logging.info(f"Testing tags endpoint: {tags_url}")
        response = requests.get(tags_url, timeout=5)
        
        if response.status_code == 200:
            logging.info(f"Tags endpoint successful. Status: {response.status_code}")
            models = response.json()
            logging.info(f"Available models: {models}")
            
            # Check if tinyllama is available
            model_names = [model.get('name') for model in models.get('models', [])]
            if 'tinyllama:latest' in model_names:
                logging.info("Found tinyllama model!")
                
                # Test generate endpoint with a simple query
                try:
                    generate_url = "http://ollama:11434/api/generate"
                    payload = {
                        "model": "tinyllama",
                        "prompt": "How do I control aphids on tomato plants?",
                        "stream": False
                    }
                    
                    logging.info(f"Testing generate endpoint: {generate_url}")
                    logging.info(f"This may take up to 30 seconds...")
                    
                    start_time = time.time()
                    gen_response = requests.post(generate_url, json=payload, timeout=60)
                    duration = time.time() - start_time
                    
                    logging.info(f"Generate response received in {duration:.2f} seconds with status: {gen_response.status_code}")
                    
                    if gen_response.status_code == 200:
                        result = gen_response.json()
                        logging.info(f"Generate response: {result.get('response', '')[:200]}...")
                    else:
                        logging.error(f"Generate failed with status: {gen_response.status_code}")
                        if gen_response.text:
                            logging.error(f"Error: {gen_response.text}")
                except Exception as e:
                    logging.error(f"Error testing generate: {str(e)}")
            else:
                logging.warning(f"tinyllama model not found. Available: {model_names}")
        else:
            logging.error(f"Tags endpoint failed with status: {response.status_code}")
            if response.text:
                logging.error(f"Error: {response.text}")
    except Exception as e:
        logging.error(f"Error testing Ollama: {str(e)}")

if __name__ == "__main__":
    test_ollama() 