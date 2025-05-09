import requests
import json
import time

def test_chat_api():
    """Test the chat API endpoint that should use the Ollama model."""
    print("\n=== TESTING CHAT API ===\n")
    
    # The chat endpoint URL
    url = "http://localhost:8000/api/chat"
    
    # List of test queries
    test_queries = [
        "What are common pests affecting tomato plants?",
        "How can I control aphids on my cabbage plants?",
        "What are natural ways to improve soil fertility?"
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\nTest {i+1}: '{query}'")
        
        # Prepare the payload
        payload = {
            "message": query
        }
        
        try:
            # Time the request
            start_time = time.time()
            response = requests.post(url, json=payload, timeout=120)
            elapsed_time = time.time() - start_time
            
            print(f"Response received in {elapsed_time:.2f} seconds")
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if "response" in result:
                    print("\nAPI Response:")
                    print("-" * 50)
                    print(result["response"][:500])  # Print first 500 chars
                    if len(result["response"]) > 500:
                        print("... (response truncated)")
                    print("-" * 50)
                    
                    print(f"Source: {result.get('source', 'Not specified')}")
                    
                    if len(result["response"]) > 20:
                        print("Test PASSED: Got a substantive response")
                    else:
                        print("Test FAILED: Response too short")
                else:
                    print(f"Error: No 'response' field in result: {json.dumps(result)[:200]}")
            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"Error calling API: {str(e)}")
    
    print("\n=== CHAT API TEST COMPLETE ===")
    return True

if __name__ == "__main__":
    test_chat_api() 