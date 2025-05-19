#!/usr/bin/env python
"""
Test script for demonstrating RAG integration with the HybridEngine.
"""
import os
import sys
import json
import logging
from pprint import pprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("rag_hybrid_test")

# Import the necessary components
try:
    from api.inference_engine.implement_rag import get_rag_system, extend_hybrid_engine
    from api.inference_engine.hybrid_engine import HybridEngine
except ImportError as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

def test_hybrid_engine_with_rag():
    """Test the HybridEngine with RAG integration"""
    logger.info("Testing HybridEngine with RAG integration...")
    
    # Create a HybridEngine instance
    engine = HybridEngine()
    
    # Extend the engine with RAG capabilities
    extend_hybrid_engine(engine)
    
    # Check if the engine has been extended
    if not hasattr(engine, 'rag_system') or not engine.rag_system:
        logger.error("Failed to extend HybridEngine with RAG capabilities")
        return False
    
    # Test queries
    test_queries = [
        "What are indigenous methods for controlling pests on maize?",
        "How do I control aphids on roses using natural methods?",
        "What traditional knowledge exists for managing pests in Africa?",
        "How can I identify common crop diseases?"
    ]
    
    for query in test_queries:
        logger.info(f"\nTesting query: {query}")
        
        # Create parameters for the query
        params = {
            "query": query,
            "message": query
        }
        
        # Process the query with the enhanced _process_general_query method
        # First attempt without Ollama
        logger.info("Processing query without Ollama...")
        result = engine._process_general_query(params, attempt_ollama_call=False)
        
        # Log the result
        logger.info(f"Result source: {result.get('source', 'unknown')}")
        logger.info(f"Result (without Ollama):\n{result.get('response', '')[:300]}...")
        
        # Then attempt with Ollama
        logger.info("\nProcessing query with Ollama...")
        result_with_ollama = engine._process_general_query(params, attempt_ollama_call=True)
        
        # Log the result
        logger.info(f"Result source: {result_with_ollama.get('source', 'unknown')}")
        logger.info(f"Result (with Ollama):\n{result_with_ollama.get('response', '')[:300]}...")
    
    return True

if __name__ == "__main__":
    logger.info("Starting HybridEngine RAG integration test")
    
    success = test_hybrid_engine_with_rag()
    
    if success:
        logger.info("HybridEngine RAG integration test completed successfully")
    else:
        logger.error("HybridEngine RAG integration test failed") 