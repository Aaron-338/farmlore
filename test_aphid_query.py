"""
Test script for aphid predator query handling in HybridEngine.
This script validates the fix for queries about natural predators for aphids.
"""

import os
import sys
import logging
import importlib.util
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_module_from_path(module_name, file_path):
    """Dynamically load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module {module_name} at {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def test_aphid_query():
    """Test that queries about aphid predators are correctly handled."""
    try:
        # First, try to import the relevant modules
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define paths to the needed modules
        hybrid_engine_path = os.path.join(current_dir, "pest-management-chatbot/farmlore-project/api/inference_engine/hybrid_engine.py")
        prompt_templates_path = os.path.join(current_dir, "pest-management-chatbot/farmlore-project/api/inference_engine/prompt_templates.py")
        
        # Check if files exist
        if not os.path.exists(hybrid_engine_path):
            logger.error(f"Could not find HybridEngine at {hybrid_engine_path}")
            return False
        
        if not os.path.exists(prompt_templates_path):
            logger.error(f"Could not find prompt_templates at {prompt_templates_path}")
            return False
            
        # Load the modules
        prompt_templates = load_module_from_path("prompt_templates", prompt_templates_path)
        
        # Test the query classification
        test_queries = [
            "What are natural predators for aphids?",
            "How do I control aphids on roses?",
            "What beneficial insects eat aphids?",
            "Tell me about ladybugs as predators for aphids",
            "Which animals eat aphids?"
        ]
        
        print("\n=== Testing Query Classification ===")
        for query in test_queries:
            prompt_type = prompt_templates.detect_prompt_type(query)
            print(f"Query: '{query}' -> Classified as: {prompt_type}")
            
            # Verify that all these queries are classified as PEST_MANAGEMENT
            if prompt_type != prompt_templates.PromptType.PEST_MANAGEMENT:
                logger.error(f"Query '{query}' was incorrectly classified as {prompt_type}, should be PEST_MANAGEMENT")
                return False
                
        print("\nAll queries correctly classified as PEST_MANAGEMENT!")
        
        # Import hybrid_engine and create an instance
        print("\n=== Testing HybridEngine Query Processing ===")
        try:
            # Create a mock instance to test the _process_query_by_type method
            class MockHybridEngine:
                def __init__(self):
                    self.called_method = None
                    self.params = None
                    
                def _process_control_methods(self, params, attempt_ollama_call):
                    self.called_method = "_process_control_methods"
                    self.params = params
                    return {"response": "Mock response for pest management", "source": "mock_test"}
                    
                def _process_soil_analysis(self, params, attempt_ollama_call):
                    self.called_method = "_process_soil_analysis"
                    self.params = params
                    return {"response": "Mock response for soil analysis", "source": "mock_test"}
            
            # Create the mock engine
            mock_engine = MockHybridEngine()
            
            # Test soil_analysis that should redirect to pest_management
            query = "What are natural predators for aphids?"
            params = {"query": query, "message": query}
            
            # Test if soil_analysis query type with aphid keywords redirects to pest_management
            print(f"\nTesting soil_analysis query type with: '{query}'")
            
            # Get the hybrid_engine module's _process_query_by_type
            hybrid_engine_module = load_module_from_path("hybrid_engine", hybrid_engine_path)
            
            # Apply the _process_query_by_type method on our mock engine
            result = hybrid_engine_module.HybridEngine._process_query_by_type(
                mock_engine, 
                "soil_analysis", 
                params, 
                attempt_ollama_call=True
            )
            
            print(f"Query processed. Called method: {mock_engine.called_method}")
            
            # Verify it called the correct method
            if mock_engine.called_method != "_process_control_methods":
                logger.error(f"Query '{query}' with type 'soil_analysis' called {mock_engine.called_method} instead of _process_control_methods")
                return False
            
            print("Success! Soil analysis query about aphids was correctly redirected to pest management.")
            return True
            
        except Exception as e:
            logger.error(f"Error testing HybridEngine: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
            
    except Exception as e:
        logger.error(f"Error in test_aphid_query: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Testing aphid predator query handling...")
    success = test_aphid_query()
    if success:
        print("\nTEST PASSED: Aphid predator query handling is working correctly!")
        sys.exit(0)
    else:
        print("\nTEST FAILED: Aphid predator query handling needs further fixes.")
        sys.exit(1) 