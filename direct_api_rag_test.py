#!/usr/bin/env python
"""
Direct API RAG Test

This script directly connects to the API and enhances the responses with RAG.
"""
import os
import sys
import json
import time
import requests
from urllib.parse import urljoin

# Add the standalone RAG module directly to the script
import re
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple

# Sample pest management data
PEST_DATA = [
    {
        "title": "Aphid Control on Tomatoes",
        "content": """
Aphids are common pests on tomato plants. They are small, soft-bodied insects that can be green, yellow, brown, red, or black. They feed on plant sap and can cause stunted growth, yellowed leaves, and reduced yields.

Effective control methods for aphids on tomatoes include:

1. Biological control: Introduce natural predators like ladybugs, lacewings, and parasitic wasps that feed on aphids.
2. Neem oil: Apply neem oil spray, which disrupts the aphid life cycle and acts as a repellent.
3. Insecticidal soap: Use insecticidal soap sprays that are specifically designed for soft-bodied insects like aphids.
4. Water spray: Use a strong stream of water to physically remove aphids from plants.
5. Companion planting: Plant aphid-repelling plants like marigolds, nasturtiums, and garlic near tomatoes.
"""
    },
    {
        "title": "Spider Mite Management in Gardens",
        "content": """
Spider mites are tiny arachnids that can cause significant damage to garden plants. They appear as tiny moving dots, often red, brown, or yellow. Signs of infestation include fine webbing on plants and stippled, discolored leaves.

Effective management strategies include:

1. Water spray: Regular, forceful spraying with water can dislodge mites and reduce populations.
2. Increase humidity: Spider mites thrive in dry conditions, so increasing humidity can discourage them.
3. Neem oil: Apply neem oil as a natural miticide that disrupts the spider mite life cycle.
4. Insecticidal soap: Use specifically formulated soaps that are effective against mites but gentle on plants.
5. Predatory mites: Introduce beneficial predatory mites that feed on spider mites.
"""
    },
    {
        "title": "Controlling Tomato Hornworms",
        "content": """
Tomato hornworms are large, green caterpillars with white stripes and a horn-like projection on their rear end. They can quickly defoliate tomato plants and damage developing fruit.

Effective control methods include:

1. Hand-picking: Regularly inspect plants and manually remove hornworms. Drop them in soapy water or relocate them far from your garden.
2. Bacillus thuringiensis (Bt): Apply this natural bacterial insecticide that specifically targets caterpillars without harming beneficial insects.
3. Parasitic wasps: Encourage or introduce parasitic wasps like Braconid wasps that lay eggs on hornworms.
4. Companion planting: Plant dill, basil, marigold, or borage near tomatoes to repel hornworms or attract beneficial insects.
5. Crop rotation: Change where you plant tomatoes each year to disrupt the life cycle of overwintering pupae.
"""
    }
]

# RAG utility functions
def clean_text(text: str) -> str:
    """Clean and normalize text for better matching"""
    text = text.lower()
    text = re.sub(r'[\n\r\t]+', ' ', text)  # Replace newlines, tabs with spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def get_keywords(text: str) -> List[str]:
    """Extract important keywords from text"""
    text = clean_text(text)
    # Remove common stop words
    stop_words = {"the", "a", "an", "in", "on", "at", "is", "are", "and", "or", "to", "of", "for", "with", "how", "do", "i", "can", "what", "when", "why"}
    words = [word for word in text.split() if word not in stop_words]
    return words

def simple_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using SequenceMatcher"""
    return SequenceMatcher(None, clean_text(text1), clean_text(text2)).ratio()

def search_pest_data(query: str, top_n: int = 2) -> List[Dict[str, Any]]:
    """Search the pest data directly using keyword matching and text similarity"""
    query_keywords = set(get_keywords(query))
    results = []
    
    for item in PEST_DATA:
        title = item["title"]
        content = item["content"]
        
        # Calculate keyword matching score
        content_keywords = set(get_keywords(content))
        title_keywords = set(get_keywords(title))
        
        # Count matching keywords
        content_match_count = len(query_keywords.intersection(content_keywords))
        title_match_count = len(query_keywords.intersection(title_keywords))
        
        # Calculate similarity scores
        title_sim = simple_similarity(query, title)
        content_sim = simple_similarity(query, content)
        
        # Combined score (weight title matches more heavily)
        score = (
            (content_match_count * 0.5) + 
            (title_match_count * 2.0) + 
            (title_sim * 3.0) + 
            (content_sim * 1.0)
        )
        
        results.append({
            "title": title,
            "content": content,
            "score": score
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top_n results
    return results[:top_n]

def enhance_response(query: str, original_response: str) -> str:
    """Enhance a response using the RAG approach with direct text search"""
    try:
        # Search for relevant information
        search_results = search_pest_data(query)
        
        if not search_results:
            print("No relevant information found to enhance response")
            return original_response
        
        top_result = search_results[0]
        
        print(f"Found relevant information: {top_result['title']} (Score: {top_result['score']:.2f})")
        
        # Check if result is highly relevant
        if top_result["score"] < 1.0:
            print(f"Top result score ({top_result['score']}) below threshold, not enhancing")
            return original_response
        
        # Extract useful information from the top result
        top_content = top_result["content"].strip()
        
        # Combine the original response with RAG content
        enhanced_response = f"{original_response}\n\nAdditional information from our agricultural database:\n\n{top_content}"
        
        print("Successfully enhanced response with RAG information")
        return enhanced_response
    except Exception as e:
        print(f"Error enhancing response: {str(e)}")
        return original_response

# Direct API testing functions
def call_api(query, timeout=60):
    """Call the API directly and return the response"""
    try:
        # Get base URL from environment or use default
        base_url = os.environ.get('API_URL', 'http://localhost:8000')
        endpoint = '/api/chat/'
        
        # Build full URL
        url = urljoin(base_url, endpoint)
        
        print(f"Sending query to API: '{query}'")
        print(f"URL: {url}")
        
        # Prepare the request payload
        payload = {
            "message": query
        }
        
        # Send the request
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        
        # Check response status
        if response.status_code == 200:
            print(f"Received response (Status: {response.status_code})")
            return response.json()
        else:
            print(f"Error: API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error calling API: {str(e)}")
        return None

def test_api_with_rag(queries=None):
    """Test the API with RAG enhancement"""
    if queries is None:
        queries = [
            "How do I control aphids on my tomato plants?",
            "What's the best way to deal with spider mites in my garden?",
            "How can I get rid of tomato hornworms?"
        ]
    
    results = []
    
    for query in queries:
        print(f"\n--- Testing query: '{query}' ---")
        
        # Call the API
        api_response = call_api(query)
        
        if not api_response:
            print("Skipping RAG enhancement due to API error")
            continue
        
        # Extract original response
        if 'response' in api_response:
            original_text = api_response['response']
        else:
            print("Response format unexpected, cannot extract text to enhance")
            continue
            
        print(f"Original response ({len(original_text)} chars): '{original_text[:100]}...'")
        
        # Enhance with RAG
        enhanced_text = enhance_response(query, original_text)
        
        # Check if enhancement was applied
        if enhanced_text != original_text:
            print("✅ Response was enhanced with RAG")
            results.append({
                "query": query,
                "original": original_text,
                "enhanced": enhanced_text,
                "was_enhanced": True
            })
        else:
            print("❌ Response was not enhanced (no relevant information found)")
            results.append({
                "query": query,
                "original": original_text,
                "enhanced": enhanced_text,
                "was_enhanced": False
            })
    
    return results

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        queries = sys.argv[1:]
    else:
        queries = None
    
    # Set API URL based on Docker setup
    os.environ['API_URL'] = 'http://localhost:80'
    
    # Run the test
    print("Starting API RAG test...")
    results = test_api_with_rag(queries)
    
    # Print summary
    print("\n=== Test Summary ===")
    for i, result in enumerate(results, 1):
        print(f"{i}. Query: '{result['query']}'")
        print(f"   Enhanced: {'Yes' if result['was_enhanced'] else 'No'}")
        
    # Calculate statistics
    enhanced_count = sum(1 for r in results if r.get('was_enhanced', False))
    total_count = len(results)
    
    print(f"\nEnhanced {enhanced_count} out of {total_count} responses ({enhanced_count / total_count * 100:.1f}% enhancement rate)")
    print("\nTest completed") 