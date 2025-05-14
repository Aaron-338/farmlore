import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:80"  # Assuming Nginx is on port 80
API_ENDPOINT = "/api/chat/"
TIMEOUT_SECONDS = 60  # Increased timeout for potentially long first Ollama responses

# Prompts to test
PROMPTS = [
    "What are common pests for tomato plants?",
    "Suggest an organic way to deal with aphids.",
    "What is companion planting for carrots?",
    "How to improve soil fertility for growing corn?",
    "Tell me about a common disease affecting apple trees and how to treat it organically.",
    "What are beneficial insects for a vegetable garden?",
    "How can I make my own compost at home?",
    "Explain the importance of crop rotation."
]

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def test_chat_api(prompt):
    """Sends a single prompt to the chat API and prints the response."""
    print(f"--- Testing prompt: '{prompt}' ---")
    payload = {"message": prompt}
    full_url = BASE_URL + API_ENDPOINT
    
    try:
        start_time = time.time()
        response = requests.post(full_url, headers=HEADERS, json=payload, timeout=TIMEOUT_SECONDS)
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} seconds")
        
        try:
            response_data = response.json()
            print("Response JSON:")
            print(json.dumps(response_data, indent=2))

            if response.status_code == 200:
                if response_data.get("success") is True:
                    # Check if 'response' key exists and is a string before slicing
                    if "response" in response_data and isinstance(response_data["response"], str):
                        print(f"LLM Response: {response_data['response'][:200]}...") # Print first 200 chars
                    elif "response" in response_data: # It exists but isn't a string, or is empty
                        print(f"LLM Response (non-string or empty): {response_data['response']}")
                    else:
                        print("Warning: 'response' key missing from successful JSON.")
                    
                    if "source" not in response_data:
                        print("Warning: 'source' key missing from JSON.")
                    print(f"Success: {response_data.get('success')}")
                else:
                    print(f"API returned success=false or missing. Full data: {response_data}")
            else:
                print(f"Error: API request failed with status {response.status_code}.")
                print(f"Response Text:\n{response.text}")

        except json.JSONDecodeError:
            print("Error: Could not decode JSON response.")
            print(f"Response Text:\n{response.text}")
            
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {TIMEOUT_SECONDS} seconds.")
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed. {e}")
    print("\n")

if __name__ == "__main__":
    print("===== STARTING DJANGO CHAT API TEST =====")
    print("\n")
    for p in PROMPTS:
        test_chat_api(p)
        time.sleep(1) # Small delay between requests to observe logs if needed
    print("===== DJANGO CHAT API TEST COMPLETE =====")