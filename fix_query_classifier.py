#!/usr/bin/env python
"""
Fix Query Classifier

This script patches the query classification logic in the prompt_templates module
to correctly identify pest-related queries.
"""

import os
import sys
import logging
import importlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fix_query_classifier")

def fix_query_classifier():
    """
    Fix the query classification logic in the prompt_templates module
    """
    try:
        # Set up Django environment
        logger.info("Setting up Django environment...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmlore.settings')
        
        # Import Django and set up settings
        import django
        django.setup()
        
        logger.info("Django environment set up successfully")
        
        # Import the prompt_templates module
        logger.info("Importing prompt_templates module...")
        from api.inference_engine import prompt_templates
        
        # Check if the detect_prompt_type function exists
        if not hasattr(prompt_templates, 'detect_prompt_type'):
            logger.error("Could not find detect_prompt_type function in prompt_templates")
            return False
        
        # Store the original function
        original_detect_prompt_type = prompt_templates.detect_prompt_type
        
        # Define the improved function
        def improved_detect_prompt_type(message):
            """
            Improved prompt type detection with better pest management detection
            """
            # Define keywords for different query types
            pest_keywords = [
                'pest', 'insect', 'bug', 'aphid', 'beetle', 'caterpillar', 'worm', 'moth', 'fly', 'mite',
                'control', 'kill', 'spray', 'predator', 'natural enemy', 'beneficial', 'ladybug', 'ladybird',
                'lacewing', 'parasitic wasp', 'nematode', 'predatory'
            ]
            
            # Convert message to lowercase for case-insensitive matching
            message_lower = message.lower()
            
            # Check for pest management keywords first
            for keyword in pest_keywords:
                if keyword in message_lower:
                    logger.info(f"Detected pest_management prompt due to keyword: {keyword}")
                    return prompt_templates.PromptType.PEST_MANAGEMENT
            
            # Fall back to original function for other query types
            return original_detect_prompt_type(message)
        
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