#!/usr/bin/env python
import requests
import json

def print_separator():
    print("\n" + "="*60 + "\n")

# Function to make RAG enhance requests with full output
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
                
                # Extract the title of the enhancement (assuming format "Additional information...")
                lines = enhancement.split("\n")
                content_start = False
                content_text = []
                
                for i, line in enumerate(lines):
                    if i == 0:  # This is the header
                        continue
                    if line.strip() and not content_start:
                        content_start = True
                    if content_start and line.strip():
                        content_text.append(line.strip())
                        if len(content_text) >= 3:  # Get first few content lines
                            break
                
                print("\n--- ENHANCEMENT SUMMARY ---")
                print(f"Title: {content_text[0] if content_text else 'N/A'}")
                print(f"Content sample: {' '.join(content_text[:3]) if len(content_text) >= 3 else 'N/A'}")
                
                # Check for tomato or cucumber mentions in the content
                tomato_mention = "tomato" in enhancement.lower()
                cucumber_mention = "cucumber" in enhancement.lower()
                
                print(f"\nContent mentions tomatoes: {'YES' if tomato_mention else 'NO'}")
                print(f"Content mentions cucumbers: {'YES' if cucumber_mention else 'NO'}")
                
                # Identify what plant type the content is about
                if tomato_mention and not cucumber_mention:
                    print("\nEnhancement is correctly about TOMATOES")
                elif cucumber_mention and not tomato_mention:
                    print("\nEnhancement is incorrectly about CUCUMBERS")
                elif tomato_mention and cucumber_mention:
                    print("\nEnhancement mentions both TOMATOES and CUCUMBERS")
                else:
                    print("\nEnhancement does not specifically mention either plant type")
                
                
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