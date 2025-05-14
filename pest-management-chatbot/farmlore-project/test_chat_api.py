import sys
import json
import os

# Function to simulate a request to chat_api
def test_chat_api():
    try:
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
        import django
        django.setup()
        
        # Import the chat_api function
        from api.views import chat_api
        
        # Create a mock request
        from django.http import HttpRequest
        
        print("1. Creating mock request...")
        http_request = HttpRequest()
        http_request.method = 'POST'
        http_request._body = json.dumps({"message": "hello"}).encode('utf-8')
        http_request.META['CONTENT_TYPE'] = 'application/json'
        
        print("2. Calling chat_api function...")
        response = chat_api(http_request)
        
        print("3. Response status code:", response.status_code)
        print("4. Response content:")
        print(json.dumps(response.data, indent=2))
        
        return response.data
    except Exception as e:
        print(f"Error testing chat_api: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    print("\n===== DIRECT CHAT_API TEST =====\n")
    result = test_chat_api()
    print("\n===== TEST COMPLETE =====\n") 