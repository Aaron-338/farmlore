#!/usr/bin/env python
"""
Docker Fix Query Classifier

This script patches the query classification logic in the prompt_templates module
to correctly identify pest-related queries inside the Docker container.
"""

import os
import sys
import logging
import importlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docker_fix_query_classifier")

def fix_query_classifier():
    """
    Fix the query classification logic in the prompt_templates module
    """
    try:
        # Import the prompt_templates module
        logger.info("Importing prompt_templates module...")
        
        # In Docker, the module is directly available in the Python path
        from api.inference_engine import prompt_templates
        
        # Check if the detect_prompt_type function exists
        if not hasattr(prompt_templates, 'detect_prompt_type'):
            logger.error("Could not find detect_prompt_type function in prompt_templates")
            return False
        
        # Store the original function
        original_detect_prompt_type = prompt_templates.detect_prompt_type
        
        # Define the improved function
        def improved_detect_prompt_type(query: str) -> prompt_templates.PromptType:
            """
            Improved prompt type detection with better pest management detection.
            This version prioritizes pest management keywords over soil analysis keywords.
            
            Args:
                query: The user's query
                
            Returns:
                The detected prompt type
            """
            query_lower = query.lower()
            
            # Define expanded keywords for different query types
            pest_management_keywords = [
                # Original keywords
                "control", "manage", "get rid of", "treat", "pesticide",
                # New keywords for better coverage
                "pest", "insect", "bug", "aphid", "beetle", "caterpillar", "worm", 
                "moth", "fly", "mite", "kill", "spray", "predator", 
                "natural enemy", "beneficial", "ladybug", "ladybird",
                "lacewing", "parasitic wasp", "nematode", "predatory"
            ]
            
            # Check for pest management keywords FIRST (this is the key fix)
            if any(term in query_lower for term in pest_management_keywords):
                logger.info(f"Detected PEST_MANAGEMENT prompt due to pest-related term in: {query}")
                return prompt_templates.PromptType.PEST_MANAGEMENT
                
            # --- After checking for pest keywords, we can now check the other categories ---
            
            # Pest identification keywords (from original function)
            pest_id_keywords = [
                "identify", "what pest", "what insect", "what disease", "what bug", 
                "found insects", "found bugs", "found pests", "insect on", "bug on", "pest on",
                "insects on my", "bugs on my", "pests on my", "eating my plant", "eating my crop",
                "damaging my", "holes in leaves", "yellowing leaves", "spots on leaves",
                "what is this", "what are these", "can you identify", "help identify"
            ]
            
            if any(term in query_lower for term in pest_id_keywords):
                return prompt_templates.PromptType.PEST_IDENTIFICATION
            
            # Soil analysis keywords (from original function)
            if any(term in query_lower for term in ["soil", "fertility", "nutrients", "ph", "drainage"]):
                return prompt_templates.PromptType.SOIL_ANALYSIS
            
            # Indigenous knowledge keywords (from original function)
            if any(term in query_lower for term in ["traditional", "indigenous", "ancestors", "cultural", "old methods"]):
                return prompt_templates.PromptType.INDIGENOUS_KNOWLEDGE
            
            # Default to general if no specific type is detected
            return prompt_templates.PromptType.GENERAL
        
        # Replace the original function with our improved version
        prompt_templates.detect_prompt_type = improved_detect_prompt_type
        
        logger.info("Successfully patched detect_prompt_type function")
        
        # Test the patched function
        test_queries = [
            "What are natural predators for aphids?",
            "How do I control aphids on roses?",
            "What beneficial insects eat aphids?",
            "How to get rid of pests on my tomatoes?",
            "What is the soil pH for growing carrots?"
        ]
        
        logger.info("Testing patched query classifier:")
        for query in test_queries:
            prompt_type = prompt_templates.detect_prompt_type(query)
            logger.info(f"Query: '{query}' -> Type: {prompt_type}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error fixing query classifier: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting query classifier fix...")
    success = fix_query_classifier()
    if success:
        logger.info("Successfully fixed query classifier!")
        sys.exit(0)
    else:
        logger.error("Failed to fix query classifier")
        sys.exit(1) 