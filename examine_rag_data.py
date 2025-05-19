#!/usr/bin/env python
import requests
import json

def print_separator():
    print("\n" + "="*60 + "\n")

# Function to make RAG enhance requests
def test_rag_enhancement(query, response):
    print(f"Query: {query}")
    print(f"Original response: {response}")
    
    try:
        response_obj = requests.post(
            "http://localhost/rag-api/rag-enhance",
            json={"query": query, "response": response},
            timeout=10
        )
        
        if response_obj.status_code == 200:
            data = response_obj.json()
            
            print(f"\nWas enhanced: {data.get('was_enhanced', False)}")
            if data.get('was_enhanced', False):
                # Find where the enhancement starts
                original = data.get('original', '')
                enhanced = data.get('enhanced', '')
                
                # Simple way to find where enhancement begins
                enhancement = enhanced.replace(original, "").strip()
                
                print("\n--- ENHANCEMENT ONLY ---")
                print(enhancement)
            else:
                print("\nNo enhancement was applied.")
        else:
            print(f"\nError: Received status code {response_obj.status_code}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

# Test 1: Aphids on tomatoes
print_separator()
print("TEST 1: APHIDS ON TOMATOES")
test_rag_enhancement(
    "How do I control aphids on my tomato plants?",
    "You should use insecticides."
)

# Test 2: Specific test for tomato plants
print_separator()
print("TEST 2: SPECIFIC TEST FOR TOMATO PLANTS")
test_rag_enhancement(
    "What pests affect tomato plants?",
    "Tomato plants can be affected by various pests."
)

# Test 3: Test with aphids in a different context
print_separator()
print("TEST 3: APHIDS ON A DIFFERENT PLANT")
test_rag_enhancement(
    "How do I treat aphids on roses?",
    "Aphids on roses can be treated with insecticides or natural predators."
) 