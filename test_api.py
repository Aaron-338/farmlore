#!/usr/bin/env python
"""
Test script for the embeddings classifier API
"""

import requests
import json
import sys
import time

API_URL = "http://localhost:5001"

def test_health():
    """Test the API health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"Health check: {data['status']}")
        print(f"Service: {data['service']}")
        return True
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return False

def test_classification(query):
    """Test the classification endpoint with a query"""
    try:
        payload = {"query": query}
        response = requests.post(
            f"{API_URL}/classify",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        
        data = response.json()
        if data['success']:
            print(f"Query: '{data['query']}'")
            print(f"Classification: {data['classification']}")
            return True
        else:
            print(f"Classification failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"API request failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("Testing embeddings classifier API...")
    
    # Wait for API to be ready
    max_retries = 5
    retry_count = 0
    health_ok = False
    
    while retry_count < max_retries and not health_ok:
        health_ok = test_health()
        if not health_ok:
            retry_count += 1
            print(f"Waiting for API to be ready (attempt {retry_count}/{max_retries})...")
            time.sleep(3)
    
    if not health_ok:
        print("API is not responding. Exiting.")
        return 1
    
    print("\nTesting classification endpoint with sample queries...\n")
    
    test_queries = [
        # A mix of different query types
        "How to control aphids on tomatoes?",
        "My tomato leaves have yellow spots",
        "What's the best soil pH for carrots?",
        "Traditional farming methods for pest control",
        "When should I plant tomatoes?",
        "My crops are turning purple"
    ]
    
    for query in test_queries:
        print("-" * 50)
        test_classification(query)
        print()
    
    print("Tests completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 