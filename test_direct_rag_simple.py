#!/usr/bin/env python
"""
Simple Direct RAG Test

This is a minimal test script that demonstrates the direct RAG functionality.
"""
import sys
import os

# Simply import the direct_rag_integration module
print("Importing direct_rag_integration module...")
import direct_rag_integration

# Test the basic enhancement function
print("\nTesting direct RAG enhancement...")

# Define a test query
query = "How do I get rid of aphids on my tomato plants?"
print(f"Query: '{query}'")

# Define a simple original response
original_response = "Aphids can be controlled using insecticidal soaps or by introducing natural predators."
print(f"Original response: '{original_response}'")

# Enhance the response
print("\nCalling enhance_response...")
enhanced_response, search_results = direct_rag_integration.enhance_response(query, original_response)

# Print search results
print(f"\nFound {len(search_results)} relevant documents:")
for i, result in enumerate(search_results, 1):
    print(f"{i}. {result['title']} (Score: {result['score']:.2f})")

# Print the enhanced response
print("\n=== Enhanced Response ===")
print(enhanced_response)
print("========================")

# Test the hybrid engine integration function
print("\nTesting hybrid engine response enhancement...")

# Create a sample hybrid engine response
hybrid_response = {
    "result": "Aphids are common garden pests that can be managed using various techniques.",
    "source": "test",
    "success": True
}
print(f"Original hybrid response: {hybrid_response['result']}")

# Enhance the hybrid engine response
params = {"query": query}
enhanced_hybrid_response = direct_rag_integration.enhance_hybrid_engine_response(None, params, hybrid_response)

# Print the enhanced hybrid response
print("\n=== Enhanced Hybrid Response ===")
print(enhanced_hybrid_response["result"])
print("================================")

# Print metadata if available
if "metadata" in enhanced_hybrid_response and "rag_sources" in enhanced_hybrid_response["metadata"]:
    print("\nRAG sources in metadata:")
    for i, source in enumerate(enhanced_hybrid_response["metadata"]["rag_sources"], 1):
        print(f"{i}. {source['title']} (relevance: {source['relevance']:.2f})")

print("\n✅ Direct RAG test completed successfully!") 