import requests
import json
import time

print("=== TESTING DIRECT CONNECTION TO OLLAMA ===")

# Try different endpoints to find the Ollama service
endpoints = [
    "http://ollama:11434",
    "http://localhost:11434",
    "http://pest-management-chatbot-ollama-1:11434"
]

for endpoint in endpoints:
    print(f"\nTrying to connect to: {endpoint}")
    try:
        # First test the /api/tags endpoint (lightweight)
        tags_url = f"{endpoint}/api/tags"
        print(f"Testing tags endpoint: {tags_url}")
        
        start_time = time.time()
        tags_response = requests.get(tags_url, timeout=5)
        duration = time.time() - start_time
        
        print(f"Status code: {tags_response.status_code}")
        print(f"Response time: {duration:.2f} seconds")
        
        if tags_response.status_code == 200:
            models = tags_response.json().get('models', [])
            print(f"Available models: {[m.get('name') for m in models]}")
            
            # Now test a simple generation
            if models:
                model_name = models[0].get('name', 'tinyllama')
                generate_url = f"{endpoint}/api/generate"
                payload = {
                    "model": model_name,
                    "prompt": "What is a tomato hornworm?",
                    "stream": False
                }
                
                print(f"\nTrying generation with model {model_name}")
                
                try:
                    start_time = time.time()
                    gen_response = requests.post(generate_url, json=payload, timeout=10)
                    duration = time.time() - start_time
                    
                    print(f"Generation status code: {gen_response.status_code}")
                    print(f"Generation time: {duration:.2f} seconds")
                    
                    if gen_response.status_code == 200:
                        result = gen_response.json()
                        if "response" in result:
                            print(f"Response snippet: {result['response'][:100]}...")
                            print(f"\nSUCCESS: Direct connection to Ollama is working at {endpoint}")
                    else:
                        print(f"Generation failed: {gen_response.text[:100]}...")
                        
                except Exception as e:
                    print(f"Generation error: {str(e)}")
        else:
            print(f"Tags endpoint failed: {tags_response.text[:100]}...")
            
    except requests.exceptions.ConnectTimeout:
        print("Connection timeout - endpoint might be unreachable")
    except requests.exceptions.ReadTimeout:
        print("Read timeout - endpoint might be slow to respond")
    except Exception as e:
        print(f"Error: {str(e)}")

print("\n=== TEST COMPLETED ===")
print("If all endpoints failed, check Docker networking and Ollama container status.") 