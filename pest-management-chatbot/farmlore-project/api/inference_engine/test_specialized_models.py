"""
Test script to verify specialized model assignments in the FarmLore system.
This script will print out the specialized model mappings and help diagnose any issues.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the OllamaHandler and HybridEngine
from api.inference_engine.ollama_handler import OllamaHandler
from api.inference_engine.hybrid_engine import HybridEngine
from api.inference_engine.prompt_templates import PromptType, format_prompt

def test_specialized_model_mappings():
    """Test the specialized model mappings in the OllamaHandler."""
    logger.info("Testing specialized model mappings...")
    
    # Initialize the OllamaHandler
    handler = OllamaHandler(base_url="http://localhost:11434")
    
    # Print the specialized model mappings
    logger.info("Specialized model mappings:")
    for query_type, model_name in handler.specialized_models.items():
        logger.info(f"  {query_type}: {model_name}")
    
    # Print the modelfile paths
    logger.info("Modelfile paths:")
    for model_name, modelfile_path in handler.modelfile_paths.items():
        logger.info(f"  {model_name}: {modelfile_path}")
        
    return handler

def test_hybrid_engine_model_usage():
    """Test how the HybridEngine uses specialized models."""
    logger.info("Testing HybridEngine model usage...")
    
    # Initialize the HybridEngine
    engine = HybridEngine()
    
    # Test each query type
    query_types = [
        "pest_identification",
        "control_methods",
        "crop_pests",
        "indigenous_knowledge",
        "general_query"
    ]
    
    # Create a test prompt for each query type
    for query_type in query_types:
        logger.info(f"Testing query type: {query_type}")
        
        # Create a test prompt
        if query_type == "pest_identification":
            prompt_type = PromptType.PEST_IDENTIFICATION
            params = {"query": "What pest is this?", "pest": "aphid", "crop": "tomato"}
        elif query_type == "control_methods":
            prompt_type = PromptType.PEST_MANAGEMENT
            params = {"query": "How do I control this pest?", "pest": "aphid", "crop": "tomato"}
        elif query_type == "crop_pests":
            prompt_type = PromptType.GENERAL
            params = {"query": "What pests affect this crop?", "crop": "tomato"}
        elif query_type == "indigenous_knowledge":
            prompt_type = PromptType.INDIGENOUS_KNOWLEDGE
            params = {"query": "Tell me about indigenous practices", "practice_name": "ash sprinkle", "purpose": "pest control"}
        else:  # general_query
            prompt_type = PromptType.GENERAL
            params = {"query": "Tell me about farming"}
        
        # Format the prompt
        prompt_content = format_prompt(prompt_type, **params)
        
        # Print the query type and the specialized model that would be used
        if engine.ollama_handler:
            model = engine.ollama_handler.specialized_models.get(query_type, engine.ollama_handler.ollama_model)
            logger.info(f"  Would use model '{model}' for query type '{query_type}'")
        else:
            logger.info("  OllamaHandler not available")

def main():
    """Main function to run the tests."""
    logger.info("Starting specialized model tests...")
    
    # Test the specialized model mappings
    handler = test_specialized_model_mappings()
    
    # Test the HybridEngine model usage
    test_hybrid_engine_model_usage()
    
    logger.info("Specialized model tests complete.")

if __name__ == "__main__":
    main()
