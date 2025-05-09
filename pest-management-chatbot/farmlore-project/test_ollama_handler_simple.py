import requests
import json
import time

def test_ollama_direct():
    """Test Ollama API directly without using the handler."""
    print("\n=== TESTING OLLAMA API DIRECTLY ===\n")
    
    base_url = "http://ollama:11434"
    api_generate = f"{base_url}/api/generate"
    api_tags = f"{base_url}/api/tags"
    
    # Create a session for connection pooling
    session = requests.Session()
    
    # Check model availability
    print("Checking model availability...")
    try:
        response = session.get(api_tags, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            tags_data = response.json()
            
            if 'models' in tags_data and tags_data['models']:
                models = [model.get('name', 'unknown') for model in tags_data.get('models', [])]
                print(f"Available models: {', '.join(models)}")
                model_to_use = models[0]
            else:
                print("No models available.")
                return False
        else:
            print(f"Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error checking models: {str(e)}")
        return False
    
    # Test generation
    print(f"\nTesting generation with model: {model_to_use}")
    
    prompts = [
        "What are common pests affecting tomato plants?",
        "How can I control aphids on my cabbage plants?",
        "What are natural ways to improve soil fertility?"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\nTest {i+1}: '{prompt}'")
        
        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Time the response generation
            start_time = time.time()
            response = session.post(api_generate, json=payload, timeout=60)
            elapsed_time = time.time() - start_time
            
            print(f"Response generated in {elapsed_time:.2f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                
                if "response" in result:
                    print("\nResponse:")
                    print("-" * 50)
                    print(result["response"][:500])  # Print first 500 chars
                    if len(result["response"]) > 500:
                        print("... (response truncated)")
                    print("-" * 50)
                    
                    if len(result["response"]) > 20:
                        print("Test PASSED: Got a substantive response")
                    else:
                        print("Test FAILED: Response too short")
                else:
                    print(f"Error: No 'response' field in result: {json.dumps(result)[:100]}")
            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response: {response.text[:100]}")
        except Exception as e:
            print(f"Error generating response: {str(e)}")
    
    print("\n=== OLLAMA API TEST COMPLETE ===")
    return True

if __name__ == "__main__":
    test_ollama_direct() 