#!/usr/bin/env python
"""
API RAG Integration Test

Tests if the RAG integration is working through the API endpoint.
"""
import requests
import time
import sys

# Test parameters
API_URL = "http://localhost:80/api/chat/"
QUERIES = [
    "How do I control aphids on my tomato plants?",
    "What's the best way to manage spider mites in my garden?",
    "How can I get rid of tomato hornworms?"
]

# Wait for API to be fully initialized
print("Waiting for API to be fully initialized (5 seconds)...")
time.sleep(5)

# Test each query
for i, query in enumerate(QUERIES, 1):
    print(f"\n=== Testing Query {i}: '{query}' ===")
    
    try:
        # Send request to API
        print("Sending request to API...")
        response = requests.post(
            API_URL,
            json={"message": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Check response
        if response.status_code == 200:
            print(f"Response received successfully (Status: {response.status_code})")
            data = response.json()
            
            # Print response details
            print(f"Response source: {data.get('source', 'unknown')}")
            
            # Check if response contains agricultural database information (RAG enhancement)
            response_text = data.get('response', '')
            if "agricultural database" in response_text:
                print("\n✅ RAG ENHANCEMENT DETECTED!")
                print("\nResponse excerpt:")
                # Print the first 200 characters of the response
                print(f"{response_text[:200]}...")
            else:
                print("\n❌ No RAG enhancement detected in the response")
                print("\nResponse excerpt:")
                print(f"{response_text[:200]}...")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Error during API test: {str(e)}")

print("\nAPI RAG integration test completed.") 