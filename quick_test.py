import requests
import json

print("\n===== QUICK TEST OF API =====\n")

# Try direct access to the web container with shorter timeout
try:
    print("Testing direct access to web container (port 8000)...")
    response = requests.post(
        "http://localhost:8000/api/chat/", 
        json={"message": "How do I control aphids on peas?"}, 
        timeout=10  # Shorter timeout
    )
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {str(e)}")

print("\n===== TEST COMPLETE =====\n") 