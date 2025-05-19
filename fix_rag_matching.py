#!/usr/bin/env python
import requests

# Get pest data and analyze the titles
def analyze_rag_issue():
    print("Analyzing RAG data matching issue...")
    
    # Create a container with our test script
    payload = """
from standalone_rag import *

# Print all available pest data titles
print("\\n=== ALL PEST DATA ENTRIES ===")
for i, item in enumerate(PEST_DATA):
    print(f"{i+1}. {item['title']}")

# Test query
query = "How do I control aphids on my tomato plants?"
print(f"\\n=== TESTING QUERY: {query} ===")

# Print the search results
results = search_pest_data(query, top_n=3)
print("\\n=== TOP 3 MATCHES ===")
for i, r in enumerate(results):
    print(f"MATCH {i+1}: {r['title']} (Score: {r['score']:.2f})")

# Find the aphid tomato entry
print("\\n=== APHID TOMATO ENTRY ===")
found = False
for i, item in enumerate(PEST_DATA):
    if "Aphid" in item["title"] and "Tomato" in item["title"]:
        print(f"Found at index {i}: {item['title']}")
        
        # Calculate direct similarity score
        sim_score = simple_similarity(query, item['title'])
        print(f"Direct similarity score: {sim_score:.4f}")
        
        # Calculate component scores like in the search function
        content_keywords = set(get_keywords(item['content']))
        title_keywords = set(get_keywords(item['title']))
        query_keywords = set(get_keywords(query))
        
        content_match_count = len(query_keywords.intersection(content_keywords))
        title_match_count = len(query_keywords.intersection(title_keywords))
        title_sim = simple_similarity(query, item['title'])
        content_sim = simple_similarity(query, item['content'])
        
        # Calculate the score as done in search_pest_data function
        score = (
            (content_match_count * 0.5) +
            (title_match_count * 2.0) +
            (title_sim * 3.0) +
            (content_sim * 1.0)
        )
        
        print(f"Keyword match statistics:")
        print(f"  Content keyword matches: {content_match_count} ({query_keywords.intersection(content_keywords)})")
        print(f"  Title keyword matches: {title_match_count} ({query_keywords.intersection(title_keywords)})")
        print(f"  Title similarity: {title_sim:.4f}")
        print(f"  Content similarity: {content_sim:.4f}")
        print(f"  Calculated score: {score:.4f}")
        
        found = True
        break

if not found:
    print("No entry found with 'Aphid' and 'Tomato' in the title")

# Print the actual top match
print("\\n=== TOP MATCH ANALYSIS ===")
if results:
    top_match = results[0]
    print(f"Title: {top_match['title']}")
    
    # Calculate component scores
    content_keywords = set(get_keywords(top_match['content']))
    title_keywords = set(get_keywords(top_match['title']))
    query_keywords = set(get_keywords(query))
    
    content_match_count = len(query_keywords.intersection(content_keywords))
    title_match_count = len(query_keywords.intersection(title_keywords))
    title_sim = simple_similarity(query, top_match['title'])
    content_sim = simple_similarity(query, top_match['content'])
    
    print(f"Keyword match statistics:")
    print(f"  Content keyword matches: {content_match_count} ({query_keywords.intersection(content_keywords)})")
    print(f"  Title keyword matches: {title_match_count} ({query_keywords.intersection(title_keywords)})")
    print(f"  Title similarity: {title_sim:.4f}")
    print(f"  Content similarity: {content_sim:.4f}")
    
    # Print query keywords
    print(f"\\nQuery keywords: {query_keywords}")
"""

    # Use Docker to execute this script in the container
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get('farmlore-rag_connector-1')
        result = container.exec_run(["python", "-c", payload])
        print(result.output.decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_rag_issue() 