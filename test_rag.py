#!/usr/bin/env python
"""
Test script for demonstrating RAG integration with the FarmLore system.
"""
import os
import sys
import json
import logging
import requests
from pprint import pprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("rag_test")

try:
    # Try importing directly if running inside container
    from api.inference_engine.implement_rag import get_rag_system, RAGQuery
    from api.inference_engine.hybrid_engine import HybridEngine
    IN_CONTAINER = True
except ImportError:
    logger.warning("Not running inside container, will use API calls instead")
    IN_CONTAINER = False

def test_rag_directly():
    """Test RAG functionality directly if running in container"""
    logger.info("Testing RAG functionality directly...")
    
    # Get RAG system
    rag_system = get_rag_system()
    if not rag_system:
        logger.error("Failed to initialize RAG system")
        return False
    
    # Test queries
    test_queries = [
        "What are indigenous methods for controlling pests on maize?",
        "How do I control aphids on roses using natural methods?",
        "What traditional knowledge exists for managing pests in Africa?",
        "How can I identify common crop diseases?"
    ]
    
    for query in test_queries:
        logger.info(f"\nTesting RAG query: {query}")
        
        # Get RAG results
        results = rag_system.query(query, k=3)
        
        logger.info(f"RAG returned {len(results)} results")
        for i, result in enumerate(results):
            logger.info(f"  Result {i+1}:\n{result[:300]}...")
    
    return True

def test_rag_via_api():
    """Test RAG functionality via API calls"""
    logger.info("Testing RAG functionality via API...")
    
    # Test queries
    test_queries = [
        "What are indigenous methods for controlling pests on maize?",
        "How do I control aphids on roses using natural methods?",
        "What traditional knowledge exists for managing pests in Africa?",
        "How can I identify common crop diseases?"
    ]
    
    api_url = "http://localhost:8000/api/chat/"
    
    for query in test_queries:
        logger.info(f"\nTesting API with query: {query}")
        
        try:
            # Send request to API
            payload = {"message": query}
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"API response:\n{result['response'][:300]}...")
                logger.info(f"Source: {result.get('source', 'unknown')}")
            else:
                logger.error(f"API request failed with status code {response.status_code}")
                logger.error(f"Response: {response.text}")
        
        except Exception as e:
            logger.error(f"Error making API request: {str(e)}")
    
    return True

if __name__ == "__main__":
    logger.info("Starting RAG integration test")
    
    if IN_CONTAINER:
        success = test_rag_directly()
    else:
        success = test_rag_via_api()
    
    if success:
        logger.info("RAG integration test completed successfully")
    else:
        logger.error("RAG integration test failed") 