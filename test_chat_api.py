import sys
import json
import os
import requests

# Function to test the chat API via direct HTTP request
def test_chat_api():
    try:
        # Make a direct HTTP request to the API
        print("1. Sending request to chat API...")
        
        # Try both direct web container and through nginx
        urls = [
            "http://localhost:8000/api/chat/",  # Direct to web container
            "http://localhost:80/api/chat/"     # Through nginx
        ]
        
        payload = {"message": "hello"}
        headers = {"Content-Type": "application/json"}
        
        for url in urls:
            print(f"\nTesting URL: {url}")
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                print(f"2. Response status code: {response.status_code}")
                print(f"3. Response headers: {response.headers}")
                print("4. Response content:")
                
                try:
                    content = response.json()
                    print(json.dumps(content, indent=2))
                except:
                    print(response.text)
                    
            except Exception as e:
                print(f"Error with {url}: {str(e)}")
                
        return {"message": "Test completed"}
        
    except Exception as e:
        print(f"Error testing chat_api: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    print("\n===== DIRECT CHAT_API TEST =====\n")
    result = test_chat_api()
    print("\n===== TEST COMPLETE =====\n") 