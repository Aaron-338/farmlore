#!/usr/bin/env python
"""
Docker Aphid RAG Test

This script tests the direct RAG functionality for aphid control queries in the Docker container.
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, "/app")

# Import the direct_rag_integration module
print("Importing direct_rag_integration module...")
from api.inference_engine.direct_rag_integration import enhance_response, enhance_hybrid_engine_response

# Test with a directly relevant aphid control query
query = "What's the best way to control aphids on tomatoes?"
print(f"\nQuery: '{query}'")

# Simple original response
original_response = "You can control aphids using various methods."
print(f"Original response: '{original_response}'")

# Enhance the response
print("\nCalling enhance_response...")
enhanced_response, search_results = enhance_response(query, original_response)

# Print search results
print(f"\nFound {len(search_results)} relevant documents:")
for i, result in enumerate(search_results, 1):
    print(f"{i}. {result['title']} (Score: {result['score']:.2f})")

# Print the enhanced response
print("\n=== Enhanced Response ===")
print(enhanced_response)
print("========================")

# Create a sample hybrid engine response format
hybrid_response = {
    "result": "Aphids can be managed using natural methods.",
    "source": "test",
    "success": True
}

# Enhance the hybrid engine response
params = {"query": query}
print("\nEnhancing hybrid engine response...")
enhanced_hybrid_response = enhance_hybrid_engine_response(None, params, hybrid_response)

# Print the enhanced hybrid response
print("\n=== Enhanced Hybrid Response ===")
print(enhanced_hybrid_response["result"])
print("================================")

# Print metadata if available
if "metadata" in enhanced_hybrid_response and "rag_sources" in enhanced_hybrid_response["metadata"]:
    print("\nRAG sources in metadata:")
    for i, source in enumerate(enhanced_hybrid_response["metadata"]["rag_sources"], 1):
        print(f"{i}. {source['title']} (relevance: {source['relevance']:.2f})")

print("\n✅ Aphid control RAG test in Docker completed successfully!") 