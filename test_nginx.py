import requests
import json

# Function to test the deployed chat API through the nginx proxy
def test_nginx_api():
    print("\n===== TESTING NGINX API =====\n")
    
    # Local test directly to the web container
    print("1. Testing direct web container endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/",
            json={"message": "hello direct test"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error with direct test: {str(e)}")
    
    # Test through nginx
    print("\n2. Testing through nginx proxy...")
    try:
        response = requests.post(
            "http://localhost:8080/api/chat/",
            json={"message": "hello nginx test"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error with nginx test: {str(e)}")
    
    print("\n===== TEST COMPLETE =====\n")

if __name__ == "__main__":
    test_nginx_api() 