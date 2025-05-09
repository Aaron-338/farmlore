#!/usr/bin/env python3
"""Test script for HybridEngine and OllamaHandler integration"""

import os
import sys
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to test the HybridEngine and OllamaHandler"""
    logger.info("Testing HybridEngine and OllamaHandler integration")
    
    try:
        from api.inference_engine.ollama_handler import OllamaHandler
        from api.inference_engine.hybrid_engine import HybridEngine
        
        # Test OllamaHandler directly
        logger.info("Testing OllamaHandler directly")
        handler = OllamaHandler()
        available = handler._check_availability()
        logger.info(f"Ollama API available: {available}")
        
        # Test generating a response with OllamaHandler
        if available:
            logger.info("Testing OllamaHandler.generate_response()")
            response = handler.generate_response("What are common pests in maize?")
            logger.info(f"OllamaHandler response: {response[:200]}...")
        
        # Test HybridEngine
        logger.info("Testing HybridEngine")
        engine = HybridEngine()
        
        # Force Ollama usage
        engine.use_ollama = True
        logger.info(f"HybridEngine use_ollama (after forcing): {engine.use_ollama}")
        
        # Test query
        logger.info("Testing HybridEngine.query()")
        query_result = engine.query("What are common pests in maize?")
        result_type = type(query_result).__name__
        logger.info(f"Query result type: {result_type}")
        
        # Try to pretty print the result
        if hasattr(query_result, 'items'):
            # It's a dictionary-like object
            logger.info("Result is dictionary-like. Keys:")
            for key in query_result:
                logger.info(f"- {key}: {str(query_result[key])[:100]}...")
        elif isinstance(query_result, str):
            # It's a string
            logger.info(f"Result is a string: {query_result[:200]}...")
        else:
            # Try to convert to string
            logger.info(f"Result: {str(query_result)[:200]}...")
        
        logger.info("Test completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return 1

def test_hybrid_engine():
    """Test the hybrid engine directly."""
    print("\n=== TESTING HYBRID ENGINE ===\n")
    
    # Initialize the hybrid engine
    print("Initializing HybridEngine...")
    engine = HybridEngine()
    
    # Wait for initialization if needed
    print("Waiting for initialization to complete...")
    is_complete, is_successful = engine.is_initialization_complete(timeout=30)
    print(f"Initialization status: Complete={is_complete}, Successful={is_successful}")
    
    # Test engine with various query types
    test_queries = [
        {
            "type": "general_query",
            "params": {"query": "What are common pests affecting tomato plants?"}
        },
        {
            "type": "pest_identification",
            "params": {"crop": "cabbage", "symptoms": "small green insects"}
        },
        {
            "type": "crop_pests",
            "params": {"crop": "rice"}
        }
    ]
    
    for i, test in enumerate(test_queries):
        query_type = test["type"]
        params = test["params"]
        
        print(f"\nTest {i+1}: {query_type} - {params}")
        
        # Time the query
        start_time = time.time()
        try:
            result = engine.query(query_type, params)
            elapsed_time = time.time() - start_time
            
            print(f"Query processed in {elapsed_time:.2f} seconds")
            print(f"Source: {result.get('source', 'Not specified')}")
            
            if "response" in result:
                print("\nResponse:")
                print("-" * 50)
                print(result["response"][:500])  # Print first 500 chars
                if len(result["response"]) > 500:
                    print("... (response truncated)")
                print("-" * 50)
                
                if len(result["response"]) > 20:
                    print("Test PASSED: Got a substantive response")
                else:
                    print("Test FAILED: Response too short")
            else:
                print(f"Error: No 'response' field in result: {result}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")
    
    # Get engine stats
    print("\nEngine stats:")
    stats = engine.get_stats()
    print(f"Queries processed: {stats.get('query_count', 'N/A')}")
    print(f"Cache hits: {stats.get('cache_hit_count', 'N/A')}")
    print(f"Uptime: {stats.get('uptime_seconds', 'N/A'):.1f} seconds")
    
    print("\n=== HYBRID ENGINE TEST COMPLETE ===")
    return True

if __name__ == "__main__":
    sys.exit(main()) 