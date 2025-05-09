import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ollama_simple():
    """Test a simple request to Ollama API."""
    print("Testing simple Ollama API request...")
    
    base_url = "http://localhost:11434"
    api_generate = f"{base_url}/api/generate"
    
    payload = {
        "model": "tinyllama",
        "prompt": "What are common garden pests?",
        "stream": False
    }
    
    try:
        print("Sending request to Ollama API...")
        response = requests.post(api_generate, json=payload)
        response.raise_for_status()
        
        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers.get('Content-Type')}")
        print(f"Raw response text:\n{response.text[:500]}...")
        
        # Try to parse the response
        try:
            result = json.loads(response.text)
            print(f"\nParsed JSON response:\n{json.dumps(result, indent=2)[:500]}...")
            
            if "response" in result:
                print(f"\nExtracted response:\n{result['response'][:500]}...")
            else:
                print("\nNo 'response' field found in the JSON response.")
        except json.JSONDecodeError as e:
            print(f"\nError parsing JSON: {str(e)}")
            
            # If there are multiple lines, try parsing the last line
            if '\n' in response.text:
                print("\nTrying to parse the last line...")
                last_line = response.text.strip().split('\n')[-1]
                try:
                    result = json.loads(last_line)
                    print(f"Parsed JSON from last line:\n{json.dumps(result, indent=2)[:500]}...")
                    
                    if "response" in result:
                        print(f"\nExtracted response from last line:\n{result['response'][:500]}...")
                    else:
                        print("\nNo 'response' field found in the JSON from last line.")
                except json.JSONDecodeError as e2:
                    print(f"Error parsing JSON from last line: {str(e2)}")
        
    except Exception as e:
        print(f"Error making request to Ollama API: {str(e)}")

if __name__ == "__main__":
    test_ollama_simple()
