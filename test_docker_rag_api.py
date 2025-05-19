#!/usr/bin/env python3
"""
Test script to query the chatbot API with aphid predator questions
"""
import requests
import json
import time

def test_api_with_rag_query():
    """
    Test the chatbot API with a query about aphid predators
    """
    print("Testing the API with a query about aphid predators...")
    
    # The API endpoint
    api_url = "http://localhost:8000/api/chat/"
    
    # Example query about aphid predators
    payload = {"message": "What are natural predators for aphids?"}
    
    # Make the request
    try:
        print(f"Sending request to {api_url} with payload: {payload}")
        response = requests.post(api_url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            print("\nAPI Response:")
            print("=============")
            
            # Parse the JSON response
            try:
                result = response.json()
                print(json.dumps(result, indent=2))
                
                # Check if the response contains RAG information
                if "response" in result:
                    response_text = result["response"]
                    if "based on our knowledge base" in response_text.lower():
                        print("\n✓ RAG is working correctly! The response includes knowledge base information.")
                    else:
                        print("\n⚠ The response doesn't mention the knowledge base. RAG might not be working.")
                else:
                    print("\n⚠ The response doesn't have the expected format.")
            except json.JSONDecodeError:
                print("\n⚠ Could not parse JSON response:")
                print(response.text)
        else:
            print(f"\n⚠ Request failed with status code: {response.status_code}")
            print("Response text:")
            print(response.text)
    except Exception as e:
        print(f"\n⚠ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_api_with_rag_query() 