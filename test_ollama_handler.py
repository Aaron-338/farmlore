import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import our handler from the correct module path
sys.path.append('/app')  # Ensure we can import from the app root
from api.inference_engine.ollama_handler import OllamaHandler

def test_ollama_handler():
    print("\n=== TESTING OLLAMA HANDLER ===\n")
    
    # Initialize the handler with the correct endpoint
    handler = OllamaHandler(base_url="http://ollama:11434", timeout=60)
    
    # Wait for initialization to complete
    print("Waiting for handler initialization...")
    success = handler.wait_for_initialization(timeout=30)
    print(f"Initialization complete. Success: {success}")
    
    if not success:
        print("Handler initialization failed. The Ollama service might not be available.")
        return False
    
    # Get the list of available models
    try:
        print("\nTesting model availability...")
        response = handler.session.get(handler.api_tags)
        if response.status_code == 200:
            tags_data = response.json()
            if 'models' in tags_data and tags_data['models']:
                print(f"Available models: {[m.get('name', 'unknown') for m in tags_data['models']]}")
            else:
                print("No models available in Ollama")
        else:
            print(f"Failed to get models. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error checking model availability: {str(e)}")
    
    # Test with a simple prompt
    print("\nTesting response generation...")
    prompts = [
        "What are common pests affecting tomato plants?",
        "How can I control aphids on my cabbage plants?",
        "What are natural ways to improve soil fertility?"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\nTest {i+1}: '{prompt}'")
        
        try:
            # Time the response generation
            start_time = time.time()
            response = handler.generate_response(prompt, model="tinyllama")
            elapsed_time = time.time() - start_time
            
            print(f"Response generated in {elapsed_time:.2f} seconds")
            print("\nResponse:")
            print("-" * 50)
            print(response)
            print("-" * 50)
            
            if response and len(response) > 20:
                print("Test PASSED: Got a substantive response")
            else:
                print("Test FAILED: Response too short or empty")
                
        except Exception as e:
            print(f"Error generating response: {str(e)}")
    
    print("\n=== OLLAMA HANDLER TEST COMPLETE ===")
    return True

if __name__ == "__main__":
    test_ollama_handler() 