#!/usr/bin/env python3
"""Test script for HybridEngine and OllamaHandler integration"""

import os
import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
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
        query_text = "What are common pests in maize?"
        query_result = engine.query(query_type="general_query", params={"query": query_text})
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

if __name__ == "__main__":
    sys.exit(main()) 