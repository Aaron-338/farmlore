import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import the hybrid engine
sys.path.append('/app')  # Ensure we can import from the app root
from api.inference_engine.hybrid_engine import HybridEngine

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
    test_hybrid_engine() 