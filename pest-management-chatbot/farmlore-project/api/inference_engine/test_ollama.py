import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import using absolute paths
from api.inference_engine.ollama_handler import OllamaHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_ollama():
    print("Testing Ollama connectivity...")
    handler = OllamaHandler()
    
    try:
        # Test basic response generation
        response = handler.generate_response("What are common garden pests?")
        print(f"\nBasic response test:\n{response}\n")
        
        # Test intent classification
        query = "How do I get rid of aphids?"
        intent = handler.classify_intent(query)
        print(f"Intent classification for '{query}':\n{intent}\n")
        
        # Test humanized response prompt
        prolog_data = {
            "name": "aphid",
            "symptoms": ["yellowing_leaves", "stunted_growth", "sticky_residue"],
            "control_methods": ["neem_oil", "insecticidal_soap", "ladybugs"]
        }
        prompt = handler.create_humanized_response_prompt(prolog_data, "How do I control aphids?")
        response = handler.generate_response(prompt)
        print(f"Humanized response test:\n{response}\n")
        
        # Test follow-up question generation
        conversation = "User: My plants don't look good\nAssistant: Could you describe the symptoms?"
        prompt = handler.create_followup_prompt("They're just not growing well", conversation)
        response = handler.generate_response(prompt)
        print(f"Follow-up question test:\n{response}\n")
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_ollama()
