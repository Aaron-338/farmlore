import requests
import json

def test_internal_chat_api():
    print("Testing chat API internally...")
    
    try:
        url = 'http://localhost:8000/api/chat/'
        payload = {'message': 'hello'}
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response JSON: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_internal_chat_api() 