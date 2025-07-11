import requests
import json

print("\n===== TESTING FARMLORE API =====\n")

# Test direct access to the web container
try:
    print("Testing direct access to web container...")
    response = requests.post("http://localhost:8000/api/chat/", 
                           json={"message": "Hello"}, 
                           timeout=5)
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error with direct access: {str(e)}")

print("\n------------------------------\n")

# Test access through nginx
try:
    print("Testing access through nginx...")
    response = requests.post("http://localhost:80/api/chat/", 
                           json={"message": "Hello"}, 
                           timeout=5)
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error with nginx access: {str(e)}")

print("\n===== TEST COMPLETE =====\n")
