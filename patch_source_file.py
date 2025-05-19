#!/usr/bin/env python
"""
Patch Source File

This script directly modifies the prompt_templates.py file in the Docker container
to permanently fix the query classification issue.
"""

import os
import sys
import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patch_source")

def patch_prompt_templates_file():
    """
    Directly modify the prompt_templates.py file in the Docker container
    """
    try:
        # Path to the prompt_templates.py file in the Docker container
        file_path = "/app/api/inference_engine/prompt_templates.py"
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Read the original file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Make a backup of the original file
        backup_path = file_path + '.bak'
        with open(backup_path, 'w') as f:
            f.write(content)
        logger.info(f"Created backup at {backup_path}")
        
        # Find the detect_prompt_type function
        detect_pattern = r"(def detect_prompt_type.*?return PromptType.GENERAL\s*$)"
        match = re.search(detect_pattern, content, re.DOTALL | re.MULTILINE)
        
        if not match:
            logger.error("Could not find detect_prompt_type function in the file")
            return False
        
        original_function = match.group(1)
        
        # Define the new function
        new_function = '''def detect_prompt_type(query: str) -> PromptType:
    """
    Detect the appropriate prompt type based on query content.
    
    Args:
        query: The user's query
        
    Returns:
        The detected prompt type
    """
    query_lower = query.lower()
    
    # Define expanded pest management keywords
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
        return PromptType.PEST_MANAGEMENT
    
    # Pest identification keywords and patterns
    pest_id_keywords = [
        "identify", "what pest", "what insect", "what disease", "what bug", 
        "found insects", "found bugs", "found pests", "insect on", "bug on", "pest on",
        "insects on my", "bugs on my", "pests on my", "eating my plant", "eating my crop",
        "damaging my", "holes in leaves", "yellowing leaves", "spots on leaves",
        "what is this", "what are these", "can you identify", "help identify"
    ]
    
    if any(term in query_lower for term in pest_id_keywords):
        return PromptType.PEST_IDENTIFICATION
    
    # Soil analysis keywords
    if any(term in query_lower for term in ["soil", "fertility", "nutrients", "ph", "drainage"]):
        return PromptType.SOIL_ANALYSIS
    
    # Indigenous knowledge keywords
    if any(term in query_lower for term in ["traditional", "indigenous", "ancestors", "cultural", "old methods"]):
        return PromptType.INDIGENOUS_KNOWLEDGE
    
    # Default to general if no specific type is detected
    return PromptType.GENERAL'''
        
        # Replace the function in the content
        new_content = content.replace(original_function, new_function)
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully patched {file_path}")
        
        # Test the patch by importing the module
        sys.path.insert(0, '/app')
        try:
            from api.inference_engine.prompt_templates import detect_prompt_type, PromptType
            
            # Test queries
            test_queries = [
                "What are natural predators for aphids?",
                "How do I control aphids on roses?",
                "What beneficial insects eat aphids?",
                "How to get rid of pests on my tomatoes?",
                "What is the soil pH for growing carrots?"
            ]
            
            logger.info("Testing source file patch:")
            for query in test_queries:
                prompt_type = detect_prompt_type(query)
                logger.info(f"Query: '{query}' -> Type: {prompt_type}")
                
            return True
        except Exception as e:
            logger.error(f"Error testing patched module: {str(e)}")
            # Restore from backup if testing fails
            with open(backup_path, 'r') as f:
                original_content = f.read()
            with open(file_path, 'w') as f:
                f.write(original_content)
            logger.info("Restored original file from backup due to test failure")
            return False
    
    except Exception as e:
        logger.error(f"Error patching source file: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting source file patch...")
    success = patch_prompt_templates_file()
    if success:
        logger.info("Successfully patched source file!")
        sys.exit(0)
    else:
        logger.error("Failed to patch source file")
        sys.exit(1) 