"""
Custom performance test script for the FarmLore pest management chatbot.

This script tests various performance aspects:
1. Response time for different query types
2. Cache effectiveness
3. Fallback behavior when Ollama is unavailable
4. Throughput under load
"""

import time
import logging
import statistics
import requests
import json
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the hybrid engine directly for in-process testing
try:
    from api.inference_engine.hybrid_engine import HybridEngine
    from api.inference_engine.ollama_handler import OllamaHandler
    IN_PROCESS_TESTING = True
    logger.info("In-process testing enabled")
except ImportError:
    IN_PROCESS_TESTING = False
    logger.info("In-process testing disabled, will use API")

# Test configuration
API_URL = "http://localhost:8000/api/chat/"
DIRECT_API_URL = "http://localhost:8000/api/hybrid/"
TEST_QUERIES = [
    # General queries
    "What are common pests in maize?",
    "How do I control aphids on tomatoes?",
    "What are natural methods for soil fertilization?",
    "What are the signs of nutrient deficiency in plants?",
    
    # Pest identification
    "I see small green insects on my cabbage leaves, what could they be?",
    "My tomato plants have yellow leaves with black spots, what's wrong?",
    "There are small white flies around my pepper plants, what are they?",
    
    # Pest management
    "What's an organic solution for spider mites?",
    "How do I prevent fungal diseases in maize?",
    "What's the best way to deal with armyworms in my field?",
    
    # Indigenous knowledge
    "What traditional methods do farmers use to predict rainfall?",
    "Are there traditional crop rotation practices that help with pests?",
    "What indigenous knowledge helps with soil fertility?"
]

def test_response_time_api():
    """Test response time using the API"""
    logger.info("=== Testing API Response Time ===")
    
    times = []
    responses = []
    
    for query in TEST_QUERIES[:5]:  # Use a subset for faster testing
        payload = {
            "message": query
        }
        
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        elapsed = time.time() - start_time
        
        times.append(elapsed)
        responses.append(response.status_code)
        
        logger.info(f"Query: {query[:30]}... - Time: {elapsed:.2f}s - Status: {response.status_code}")
        
        # Brief pause to avoid overwhelming the API
        time.sleep(0.5)
    
    # Calculate statistics
    avg_time = sum(times) / len(times)
    median_time = statistics.median(times)
    max_time = max(times)
    min_time = min(times)
    
    logger.info(f"Average response time: {avg_time:.2f}s")
    logger.info(f"Median response time: {median_time:.2f}s")
    logger.info(f"Min/Max response time: {min_time:.2f}s / {max_time:.2f}s")
    success_rate = responses.count(200) / len(responses) * 100
    logger.info(f"Success rate: {success_rate:.2f}%")
    
    return avg_time, median_time, success_rate

def test_cache_effectiveness():
    """Test the effectiveness of caching by repeating the same queries"""
    logger.info("=== Testing Cache Effectiveness ===")
    
    if not IN_PROCESS_TESTING:
        logger.info("Cache testing requires in-process testing, skipping")
        return None
    
    # Create a direct instance of the HybridEngine
    engine = HybridEngine()
    
    # Test queries with timing
    first_run_times = []
    second_run_times = []
    
    for query in TEST_QUERIES[:5]:  # Use a subset for faster testing
        # First run
        start_time = time.time()
        engine.query("general_query", {"query": query})
        first_time = time.time() - start_time
        first_run_times.append(first_time)
        
        # Second run (should use cache)
        start_time = time.time()
        engine.query("general_query", {"query": query})
        second_time = time.time() - start_time
        second_run_times.append(second_time)
        
        improvement = (first_time - second_time) / first_time * 100 if first_time > 0 else 0
        logger.info(f"Query: {query[:30]}... - First: {first_time:.4f}s - Second: {second_time:.4f}s - Improvement: {improvement:.2f}%")
    
    # Calculate statistics
    avg_first = sum(first_run_times) / len(first_run_times)
    avg_second = sum(second_run_times) / len(second_run_times)
    improvement = (avg_first - avg_second) / avg_first * 100 if avg_first > 0 else 0
    
    logger.info(f"Average first run time: {avg_first:.4f}s")
    logger.info(f"Average second run time: {avg_second:.4f}s")
    logger.info(f"Average cache improvement: {improvement:.2f}%")
    
    return avg_first, avg_second, improvement

def test_throughput():
    """Test system throughput under concurrent load"""
    logger.info("=== Testing Throughput Under Load ===")
    
    concurrent_requests = 5
    results = {
        "success": 0,
        "failure": 0,
        "times": []
    }
    
    def make_request(query):
        try:
            start_time = time.time()
            response = requests.post(API_URL, json={"message": query})
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                results["success"] += 1
            else:
                results["failure"] += 1
                
            results["times"].append(elapsed)
            logger.info(f"Concurrent query completed in {elapsed:.2f}s with status {response.status_code}")
        except Exception as e:
            results["failure"] += 1
            logger.error(f"Error in concurrent request: {str(e)}")
    
    # Send concurrent requests
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        # Submit each query twice to see caching effects across threads
        for query in TEST_QUERIES[:3]:
            for _ in range(2):
                executor.submit(make_request, query)
    
    # Calculate statistics
    total_requests = results["success"] + results["failure"]
    success_rate = results["success"] / total_requests * 100
    avg_time = sum(results["times"]) / len(results["times"]) if results["times"] else 0
    
    logger.info(f"Throughput test completed with {total_requests} requests")
    logger.info(f"Success rate: {success_rate:.2f}%")
    logger.info(f"Average response time: {avg_time:.2f}s")
    
    return total_requests, success_rate, avg_time

def test_fallback_behavior():
    """Test fallback behavior when Ollama is unavailable"""
    logger.info("=== Testing Fallback Behavior ===")
    
    if not IN_PROCESS_TESTING:
        logger.info("Fallback testing requires in-process testing, skipping")
        return None
    
    # Create a direct instance of OllamaHandler
    handler = OllamaHandler(base_url="http://nonexistent:11434")  # Use invalid URL to force fallbacks
    
    # Test generation with fallback
    start_time = time.time()
    response = handler.generate_response("How do I control aphids on tomatoes?")
    elapsed = time.time() - start_time
    
    logger.info(f"Fallback response time: {elapsed:.2f}s")
    logger.info(f"Circuit state: {handler.generate_circuit.get_state()}")
    logger.info(f"Response received: {'Yes' if response else 'No'}")
    
    # Check circuit breaker state
    circuit_open = handler.generate_circuit.get_state() == "OPEN"
    
    logger.info(f"Circuit breaker open: {circuit_open}")
    
    return elapsed, circuit_open, bool(response)

def run_all_tests():
    """Run all performance tests and return results"""
    results = {}
    
    try:
        results["api_response_time"] = test_response_time_api()
    except Exception as e:
        logger.error(f"Error in API response time test: {str(e)}")
        results["api_response_time"] = None
    
    try:
        if IN_PROCESS_TESTING:
            results["cache_effectiveness"] = test_cache_effectiveness()
        else:
            results["cache_effectiveness"] = None
    except Exception as e:
        logger.error(f"Error in cache effectiveness test: {str(e)}")
        results["cache_effectiveness"] = None
    
    try:
        results["throughput"] = test_throughput()
    except Exception as e:
        logger.error(f"Error in throughput test: {str(e)}")
        results["throughput"] = None
    
    try:
        if IN_PROCESS_TESTING:
            results["fallback_behavior"] = test_fallback_behavior()
        else:
            results["fallback_behavior"] = None
    except Exception as e:
        logger.error(f"Error in fallback behavior test: {str(e)}")
        results["fallback_behavior"] = None
    
    return results

if __name__ == "__main__":
    logger.info("Starting comprehensive performance testing...")
    
    # Run all tests
    results = run_all_tests()
    
    # Print summary
    logger.info("\n\n=== PERFORMANCE TEST SUMMARY ===")
    
    if results["api_response_time"]:
        avg_time, median_time, success_rate = results["api_response_time"]
        logger.info(f"API Response Time: Avg={avg_time:.2f}s, Median={median_time:.2f}s, Success={success_rate:.2f}%")
    else:
        logger.info("API Response Time: Test failed")
    
    if results["cache_effectiveness"]:
        avg_first, avg_second, improvement = results["cache_effectiveness"]
        logger.info(f"Cache Effectiveness: First={avg_first:.4f}s, Second={avg_second:.4f}s, Improvement={improvement:.2f}%")
    else:
        logger.info("Cache Effectiveness: Test failed or skipped")
    
    if results["throughput"]:
        total_requests, success_rate, avg_time = results["throughput"]
        logger.info(f"Throughput: Requests={total_requests}, Success={success_rate:.2f}%, Avg Time={avg_time:.2f}s")
    else:
        logger.info("Throughput: Test failed")
    
    if results["fallback_behavior"]:
        elapsed, circuit_open, response_received = results["fallback_behavior"]
        logger.info(f"Fallback Behavior: Time={elapsed:.2f}s, Circuit Open={circuit_open}, Response Received={response_received}")
    else:
        logger.info("Fallback Behavior: Test failed or skipped")
    
    logger.info("Performance testing completed.") 