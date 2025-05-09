import requests
import json
import sys

def test_ollama_generation(prompt="What are common pests affecting tomato plants?"):
    print(f"Testing Ollama generation with prompt: '{prompt}'")
    
    # Use the Ollama API endpoint
    url = "http://ollama:11434/api/generate"
    
    # Prepare the request payload
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Send the request
        response = requests.post(url, json=payload, timeout=60)
        
        # Check if the request was successful
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            
            # Extract and print the response
            if "response" in result:
                print("\nModel Response:")
                print("-" * 50)
                print(result["response"])
                print("-" * 50)
                print("\nGeneration successful!")
                return True
            else:
                print("Error: Response doesn't contain 'response' field")
                print(f"Response content: {json.dumps(result, indent=2)}")
                return False
        else:
            print(f"Error: HTTP status {response.status_code}")
            print(f"Response content: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Use command line argument if provided, otherwise use default prompt
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What are common pests affecting tomato plants?"
    test_ollama_generation(prompt) 