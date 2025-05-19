import requests
import json
import time

def test_query():
    """Test a specific query about aphids on peas"""
    print("\n===== TESTING SPECIFIC QUERY =====\n")
    
    query = "How do I control aphids on peas?"
    print(f"Query: \"{query}\"\n")
    
    # First try the nginx endpoint
    try:
        print("Sending request to API via nginx (port 80)...")
        response = requests.post(
            "http://localhost:80/api/chat/",
            json={"message": query},
            timeout=30
        )
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("\nResponse:")
                print(json.dumps(result, indent=2))
                
                # Check for keywords related to our pea_updates.pl
                response_text = result.get('response', '').lower()
                if 'aphid' in response_text and 'pea' in response_text:
                    print("\nVerification: ✓ Response contains relevant keywords (aphid, pea)")
                else:
                    print("\nVerification: ✗ Response doesn't contain expected keywords")
                    
            except json.JSONDecodeError:
                print("Error: Could not parse JSON response")
                print(response.text)
        else:
            print(f"Error: Got status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    
    # Wait a moment and then try direct access
    time.sleep(1)
    
    # Then try direct access to the web container
    try:
        print("\nSending request to API via direct web access (port 8000)...")
        response = requests.post(
            "http://localhost:8000/api/chat/",
            json={"message": query},
            timeout=30
        )
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("\nResponse:")
                print(json.dumps(result, indent=2))
                
                # Check for keywords related to our pea_updates.pl
                response_text = result.get('response', '').lower()
                if 'aphid' in response_text and 'pea' in response_text:
                    print("\nVerification: ✓ Response contains relevant keywords (aphid, pea)")
                else:
                    print("\nVerification: ✗ Response doesn't contain expected keywords")
                    
            except json.JSONDecodeError:
                print("Error: Could not parse JSON response")
                print(response.text)
        else:
            print(f"Error: Got status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
    
    print("\n===== TEST COMPLETED =====\n")

if __name__ == "__main__":
    test_query() 