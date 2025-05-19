#!/usr/bin/env python
"""
Test script for RAG integration with the docker query wrapper approach
"""
import os
import sys
import json
import requests
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_rag_wrapper")

def test_rag_direct():
    """Test RAG integration directly by importing the wrapper"""
    try:
        # Add app directory to path if needed
        if os.path.exists('/app') and '/app' not in sys.path:
            sys.path.append('/app')
        
        # Import our wrapper
        logger.info("Testing RAG wrapper direct import...")
        from api.inference_engine.docker_query_wrapper import rag_integration
        
        # Test a simple query
        results = rag_integration.query("How do I control aphids on roses?")
        if results:
            logger.info(f"RAG direct query successful, found {len(results)} results")
            for i, result in enumerate(results, 1):
                logger.info(f"Result {i}:\n{result[:200]}...")
            return True
        else:
            logger.warning("RAG direct query returned no results")
            return False
            
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error in direct test: {str(e)}")
        return False

def test_rag_api():
    """Test RAG integration via the API"""
    try:
        # API endpoint
        api_url = 'http://localhost:8000/api/chat'
        
        # Wait a moment for API to be ready
        time.sleep(2)
        
        # Test data
        test_queries = [
            "How do I control aphids on roses?",
            "What are natural predators for aphids?",
            "How do I treat powdery mildew on plants?"
        ]
        
        successful_tests = 0
        
        for query in test_queries:
            logger.info(f"Testing API with query: {query}")
            
            # Send request
            response = requests.post(
                api_url,
                json={"message": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"API response: {data.get('message', '')[:200]}...")
                logger.info(f"Source: {data.get('source', 'unknown')}")
                
                # Check if response has RAG-enhanced flag
                if data.get('source') == 'rag_enhanced' or 'rag' in str(data).lower():
                    logger.info("RAG enhancement detected in response")
                    successful_tests += 1
                    
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
        
        success_rate = successful_tests / len(test_queries)
        logger.info(f"API test success rate: {success_rate * 100:.1f}%")
        
        return success_rate > 0
            
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error in API test: {str(e)}")
        return False

def print_results(direct_test, api_test):
    """Print test results in a nice format"""
    print("\n===== RAG Integration Test Results =====")
    print(f"Direct RAG test: {'PASSED' if direct_test else 'FAILED'}")
    print(f"API RAG test: {'PASSED' if api_test else 'FAILED'}")
    
    if direct_test and api_test:
        print("\n✅ SUCCESS: RAG integration is working correctly!")
        print("The system is now using RAG to enhance query responses.")
    elif direct_test:
        print("\n⚠️ PARTIAL SUCCESS: RAG system works but may not be fully integrated with the API.")
        print("Check the API configuration and restart the service if needed.")
    else:
        print("\n❌ FAILURE: RAG integration is not working correctly.")
        print("Please check the logs and make sure all dependencies are installed.")

if __name__ == "__main__":
    print("===== Testing RAG Integration =====")
    
    # Check if running in container
    in_container = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)
    if not in_container:
        print("Warning: This script is meant to be run inside the Docker container.")
        print("Some tests may fail if run outside the container.")
    
    # Run tests
    print("Running direct RAG test...")
    direct_test_result = test_rag_direct()
    
    print("Running API RAG test...")
    api_test_result = test_rag_api()
    
    # Print results
    print_results(direct_test_result, api_test_result) 