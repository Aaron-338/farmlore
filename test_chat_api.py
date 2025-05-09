import requests
import json
import time

def test_chat_api():
    """Test the chat API endpoint, verifying Prolog and Ollama integration."""
    print("\n=== TESTING CHAT API (Hybrid Engine) ===\n")
    
    # The chat endpoint URL
    url = "http://localhost:8000/api/chat"
    
    # --- Test Cases ---
    # Tuple format: (query, expected_source_hint)
    # expected_source_hint: 'prolog' if we expect direct KB hit, 'ollama' or 'fallback' otherwise.
    # Note: Even if Prolog data is found, source might be 'ollama' if it was used for generation.
    # This is just a hint for manual review of the output.
    test_cases = [
        # Existing General Queries (likely Ollama)
        ("What are common pests affecting tomato plants?", "ollama/prolog"), 
        ("How can I control aphids on my cabbage plants?", "ollama/prolog"),
        ("What are natural ways to improve soil fertility?", "ollama"),
        # Specific Pest Query (Expect Prolog Hit)
        ("Tell me about tuta absoluta", "prolog"),
        # Specific Pest Control Query (Expect Prolog Hit)
        ("How to control wireworm?", "prolog"),
        # Specific Crop Pests Query (Expect Prolog Hit)
        ("What pests affect tomato?", "prolog"),
        # Specific Practice Query (Expect Prolog Hit)
        ("Tell me about contour plowing", "prolog"),
        # Vague query (likely Ollama)
        ("My plants look sick, what should I do?", "ollama"),
        # Query not in KB (likely Ollama/Fallback)
        ("What's the weather like for farming today?", "ollama/fallback"),
    ]
    
    all_passed = True
    
    for i, (query, expected_source_hint) in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Query: '{query}'")
        print(f"(Expected source likely contains: '{expected_source_hint}')")
        
        test_passed = False
        payload = {"message": query}
        
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, timeout=180) # Increased timeout
            elapsed_time = time.time() - start_time
            
            print(f"Response received in {elapsed_time:.2f} seconds")
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Check for primary response key first (adjust if API structure changes)
                response_key = 'response' # Assuming the main text is here
                if 'message' in result and isinstance(result['message'], dict) and 'content' in result['message']:
                    response_text = result['message']['content']
                    source = result.get('source', result.get('metadata', {}).get('source', 'Not Specified'))
                elif response_key in result: # Fallback to checking top-level 'response'
                    response_text = result[response_key]
                    source = result.get('source', 'Not Specified') # Assuming source is top-level here
                else:
                    print(f"Error: Cannot find response content in result: {json.dumps(result)[:200]}")
                    response_text = None
                    source = 'Error'
                
                if response_text:
                    print("\nAPI Response Content:")
                    print("-" * 50)
                    print(response_text[:500]) 
                    if len(response_text) > 500:
                        print("... (response truncated)")
                    print("-" * 50)
                    print(f"Source: {source}")
                    
                    # Basic success criteria: non-empty response
                    if len(response_text.strip()) > 10:
                        print("-> Test PASSED: Got a substantive response.")
                        test_passed = True
                    else:
                        print("-> Test FAILED: Response was too short or empty.")
                else:
                     print("-> Test FAILED: Response content key not found or empty.")

            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response Text: {response.text[:200]}")
                print("-> Test FAILED: Non-200 status code.")
                
        except requests.exceptions.Timeout:
             print(f"Error: Request timed out after 180 seconds.")
             print("-> Test FAILED: Timeout.")
        except Exception as e:
            print(f"Error calling API: {str(e)}")
            print("-> Test FAILED: Exception during request.")
            
        if not test_passed:
            all_passed = False
        print("---") # End Test Case

    print("\n=== CHAT API TEST COMPLETE ===")
    if all_passed:
        print("Overall Result: All basic tests passed (received substantive responses). Manual review of content and source needed.")
        return True
    else:
        print("Overall Result: Some tests FAILED.")
        return False

if __name__ == "__main__":
    test_chat_api() 