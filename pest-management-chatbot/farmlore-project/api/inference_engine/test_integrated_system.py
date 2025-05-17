import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import using absolute paths
from api.inference_engine.hybrid_engine import HybridEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_integrated_system():
    """Test the integrated system with TinyLlama."""
    print("Initializing HybridEngine...")
    engine = HybridEngine()
    
    try:
        # Test 1: Clear query with specific pest and intent
        print("\n=== Test 1: Clear Query ===")
        query = "How do I control aphids on tomatoes?"
        print(f"Query: {query}")
        result = engine.query(query_type="general_query", params={"query": query})
        print(f"Response: {result.get('response', 'No response text')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        
        # Test 2: Follow-up query that relies on context
        print("\n=== Test 2: Follow-up Query ===")
        query = "What's the best organic method?"
        print(f"Query: {query}")
        result = engine.query(query_type="general_query", params={"query": query})
        print(f"Response: {result.get('response', 'No response text')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        
        # Test 3: Vague query that should trigger a follow-up question
        print("\n=== Test 3: Vague Query ===")
        # Reset context for this test
        engine.conversation_context = {
            'current_pest': None,
            'current_crop': None,
            'last_topic': None
        }
        query = "My plants look bad"
        print(f"Query: {query}")
        result = engine.query(query_type="general_query", params={"query": query})
        print(f"Response: {result.get('response', 'No response text')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_integrated_system()
