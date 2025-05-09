import requests
import json
import time

print("=== TESTING DIRECT CONNECTION TO OLLAMA WITH LONGER TIMEOUT ===")

# Use the working endpoint
endpoint = "http://pest-management-chatbot-ollama-1:11434"
print(f"Connecting to: {endpoint}")

# Use a very simple prompt for faster processing
payload = {
    "model": "tinyllama:latest",
    "prompt": "Hello",  # Very simple prompt to minimize processing time
    "stream": False
}

print(f"Using payload: {json.dumps(payload)}")
print("Setting request timeout to 60 seconds...")

try:
    start_time = time.time()
    gen_response = requests.post(
        f"{endpoint}/api/generate", 
        json=payload, 
        timeout=60  # Set a long timeout
    )
    duration = time.time() - start_time
    
    print(f"Response received in {duration:.2f} seconds")
    print(f"Status code: {gen_response.status_code}")
    
    if gen_response.status_code == 200:
        result = gen_response.json()
        if "response" in result:
            print(f"Response: {result['response']}")
            print("\nSUCCESS: The Ollama knowledge base is working!")
    else:
        print(f"Request failed: {gen_response.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")

print("\n=== TEST COMPLETED ===")
print("If this test succeeded, it means the knowledge base is accessible but takes time to respond.") 