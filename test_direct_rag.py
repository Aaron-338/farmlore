#!/usr/bin/env python 
Test Direct RAG Integration
 
Run simple tests on the Direct RAG integration.
import os
import sys
import logging
import importlib
import json
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_direct_rag")
 
def test_direct_rag_integration():
    """Test the Direct RAG integration"""
    try:
        # Import the direct RAG integration
        logger.info("Importing Direct RAG integration...")
        direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")
        logger.info("Successfully imported Direct RAG integration")
 
        # Test the search function
        test_query = "How do I control aphids on tomatoes?"
        logger.info(f"Testing search with query: '{test_query}'")
 
        results = direct_rag.search_pest_data(test_query)
        if not results:
            logger.error("Search returned no results")
            return False
 
        logger.info(f"Found {len(results)} results")
        for i, result in enumerate(results, 1):
            logger.info(f"Result {i}: {result['title']} (Score: {result['score']:.2f})")
 
        # Test the enhancement function
        logger.info("Testing response enhancement...")
 
        original_response = "Aphids can be controlled using various methods."
        enhanced_response, results = direct_rag.enhance_response(test_query, original_response)
 
        logger.info(f"Original response: {original_response}")
        logger.info(f"Enhanced response length: {len(enhanced_response)} characters")
        logger.info(f"Enhancement added {len(enhanced_response) - len(original_response)} characters")
 
        # Try to import the patched HybridEngine (if it exists)
        try:
            logger.info("Checking if HybridEngine is patched...")
            hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")
            engine = hybrid_engine_module.HybridEngine()
 
            if hasattr(engine, "_original_query") and hasattr(engine, "rag_integration_active"):
                logger.info("HybridEngine is successfully patched with RAG integration")
            else:
                logger.info("HybridEngine is not yet patched")
        except Exception as e:
            logger.warning(f"Could not check HybridEngine patch status: {str(e)}")
 
        return True
 
    except Exception as e:
        logger.error(f"Error testing Direct RAG integration: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
 
if __name__ == "__main__":
    print("=== Testing Direct RAG Integration ===")
 
    success = test_direct_rag_integration()
 
    if success:
        print("✅ Direct RAG integration is working correctly")
        sys.exit(0)
    else:
        print("❌ Direct RAG integration test failed")
        sys.exit(1)
