#!/usr/bin/env python
import requests
import json

# Define the test query and response
test_query = "How do I control aphids on my tomato plants?"
test_response = "You should use insecticides."

# Send a request to the RAG enhance endpoint
print("Testing RAG enhancement...")
print(f"Query: {test_query}")
print(f"Original response: {test_response}")
print("\nSending request to RAG enhance endpoint...")

try:
    # Send the request
    response = requests.post(
        "http://localhost/rag-api/rag-enhance",
        json={"query": test_query, "response": test_response},
        timeout=10
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("\nRAG enhancement successful!")
        print(f"\nWas enhanced: {data.get('was_enhanced', False)}")
        print("\n=== ORIGINAL RESPONSE ===")
        print(data.get('original', 'N/A'))
        print("\n=== ENHANCED RESPONSE ===")
        print(data.get('enhanced', 'N/A'))
    else:
        print(f"\nError: Received status code {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\nError: {str(e)}") 