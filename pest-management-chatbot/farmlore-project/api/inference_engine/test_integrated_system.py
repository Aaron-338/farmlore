from hybrid_engine import HybridEngine
import logging

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
        result = engine.process_query_sync(query)
        print(f"Response: {result['response']}")
        print(f"Confidence: {result['confidence']}")
        
        # Test 2: Follow-up query that relies on context
        print("\n=== Test 2: Follow-up Query ===")
        query = "What's the best organic method?"
        print(f"Query: {query}")
        result = engine.process_query_sync(query)
        print(f"Response: {result['response']}")
        print(f"Confidence: {result['confidence']}")
        
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
        result = engine.process_query_sync(query)
        print(f"Response: {result['response']}")
        print(f"Confidence: {result['confidence']}")
        
        # Test 4: Intent classification
        print("\n=== Test 4: Intent Classification ===")
        queries = [
            "What do aphids look like?",
            "How can I get rid of spider mites?",
            "How to prevent tomato hornworms?",
            "My tomato plants have yellow leaves",
            "What's the best way to deal with garden pests?",
        ]
        
        for query in queries:
            entities = engine._simple_entity_extraction(query)
            conversation_history = engine._format_conversation_history()
            intent = engine._determine_intent(query, entities, conversation_history)
            print(f"Query: '{query}' → Intent: '{intent}'")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_integrated_system()
