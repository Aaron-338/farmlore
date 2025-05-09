import sys
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import the handler directly since we don't need Django
sys.path.append('/app')  # Ensure we can import from the app root

# Import only what we need
from ollama_handler_clean import OllamaHandler

def test_ollama_handler():
    """Test the OllamaHandler directly with the clean implementation."""
    print("\n=== TESTING OLLAMA HANDLER DIRECTLY ===\n")
    
    # Initialize the handler with a longer timeout
    print("Initializing OllamaHandler with longer timeout...")
    handler = OllamaHandler(base_url="http://ollama:11434", timeout=300)
    
    # Wait for initialization to complete with a longer timeout
    print("Waiting for initialization to complete (this may take 2-3 minutes)...")
    if not hasattr(handler, '_initialization_complete'):
        # If we're using the original implementation, simulate waiting
        time.sleep(5)
        print("Using original handler implementation, no initialization event to wait for.")
        if hasattr(handler, 'is_available'):
            print(f"Handler availability: {handler.is_available}")
    else:
        # Wait for newer implementation
        success = handler.wait_for_initialization(timeout=180)  # 3 minutes
        print(f"Initialization complete. Success: {success}")
    
    # Test the handler response generation
    test_prompts = [
        "What are common pests affecting tomato plants?",
        "How can I control aphids on my cabbage plants?",
        "What are natural ways to improve soil fertility?"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\nTest {i+1}: '{prompt}'")
        
        # Time the response generation with a longer timeout
        start_time = time.time()
        response = handler.generate_response(prompt)
        elapsed_time = time.time() - start_time
        
        print(f"Response generated in {elapsed_time:.2f} seconds")
        
        if response:
            print("\nResponse:")
            print("-" * 50)
            print(response[:500])  # Print first 500 chars
            if len(response) > 500:
                print("... (response truncated)")
            print("-" * 50)
            
            if len(response) > 20:
                print("Test PASSED: Got a substantive response")
            else:
                print("Test FAILED: Response too short")
        else:
            print("Test FAILED: No response received")
    
    print("\n=== OLLAMA HANDLER TEST COMPLETE ===")
    return True

if __name__ == "__main__":
    test_ollama_handler() 