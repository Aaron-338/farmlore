#!/usr/bin/env python
"""
Improved Patch for Query Classifier

This script permanently modifies the prompt_templates.py file in the Docker container
to ensure that natural predator queries are correctly classified as pest_management.
It also adds symptom classification capabilities to properly handle descriptive symptom queries.
"""

import os
import sys
import re
import logging
from pathlib import Path
import importlib
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("improved_patch")

def patch_prompt_templates_file():
    """
    Directly modify the prompt_templates.py file in the Docker container
    with comprehensive keyword additions for pest management
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
        
        # Define the new function with comprehensive keywords and prioritization
        new_function = '''def detect_prompt_type(query: str) -> PromptType:
    """
    Detect the appropriate prompt type based on query content.
    
    Args:
        query: The user's query
        
    Returns:
        The detected prompt type
    """
    query_lower = query.lower()
    
    # Define comprehensive pest management keywords
    pest_management_keywords = [
        # Control keywords
        "control", "manage", "get rid of", "treat", "pesticide", "spray", "kill",
        
        # Pest types
        "pest", "insect", "bug", "aphid", "beetle", "caterpillar", "worm", 
        "moth", "fly", "mite", "thrip", "weevil", "nematode", "spider mite",
        
        # Natural enemies and predators
        "predator", "natural enemy", "beneficial", "ladybug", "ladybird",
        "lacewing", "parasitic wasp", "nematode", "predatory", "biological control",
        "natural control", "eat aphid", "eat pest", "consume pest", "prey on",
        
        # Prevention and management
        "prevent", "deter", "repel", "trap", "barrier", "protect plant"
    ]
    
    # Plant disease and symptom keywords 
    disease_symptom_keywords = [
        # Common disease terms
        "disease", "infection", "fungus", "bacterial", "virus", "mold", "mildew", 
        "rot", "blight", "rust", "wilt", "powdery", "downy", "fusarium", "verticillium",
        
        # Symptom descriptions
        "yellow leaves", "yellowing", "wilting", "spots", "lesion", "hole", "curling",
        "turning purple", "purple leaves", "purple", "stunted", "deformed", "distorted",
        "brown spots", "black spots", "discolored", "dying", "dropping", "falling off",
        
        # Symptom query patterns
        "why are my plants", "why is my plant", "why are my crops", "what's wrong with my",
        "what is wrong with my", "my plants are", "my plant is", "my crops are",
        "leaves turning", "leaves are turning", "plant looks", "plants look", "symptom"
    ]
    
    # Check for pest management keywords FIRST (this is the key fix)
    if any(keyword in query_lower for keyword in pest_management_keywords):
        logger.info(f"Classified as PEST_MANAGEMENT due to keywords match: {query}")
        return PromptType.PEST_MANAGEMENT
    
    # Check for disease/symptom queries SECOND (new addition)
    if any(keyword in query_lower for keyword in disease_symptom_keywords):
        logger.info(f"Classified as PEST_IDENTIFICATION due to symptom/disease match: {query}")
        return PromptType.PEST_IDENTIFICATION
    
    # Pest identification keywords and patterns 
    pest_id_keywords = [
        "identify", "what pest", "what insect", "what disease", "what bug", 
        "found insects", "found bugs", "found pests", "insect on", "bug on", "pest on",
        "insects on my", "bugs on my", "pests on my", "eating my plant", "eating my crop",
        "damaging my", "holes in leaves", "yellowing leaves", "spots on leaves",
        "what is this", "what are these", "can you identify", "help identify"
    ]
    
    if any(keyword in query_lower for keyword in pest_id_keywords):
        logger.info(f"Classified as PEST_IDENTIFICATION due to keywords match: {query}")
        return PromptType.PEST_IDENTIFICATION
    
    # Soil analysis keywords
    soil_keywords = ["soil", "fertility", "nutrients", "ph", "drainage"]
    if any(keyword in query_lower for keyword in soil_keywords):
        logger.info(f"Classified as SOIL_ANALYSIS due to keywords match: {query}")
        return PromptType.SOIL_ANALYSIS
    
    # Indigenous knowledge keywords
    indigenous_keywords = ["traditional", "indigenous", "ancestors", "cultural", "old methods"]
    if any(keyword in query_lower for keyword in indigenous_keywords):
        logger.info(f"Classified as INDIGENOUS_KNOWLEDGE due to keywords match: {query}")
        return PromptType.INDIGENOUS_KNOWLEDGE
    
    # Default to general if no specific type is detected
    logger.info(f"Classified as GENERAL (default): {query}")
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
            # Clear any cached imports
            if 'api.inference_engine.prompt_templates' in sys.modules:
                del sys.modules['api.inference_engine.prompt_templates']
            
            # Import the patched module
            from api.inference_engine.prompt_templates import detect_prompt_type, PromptType
            
            # Test queries
            test_queries = [
                "What are natural predators for aphids?",
                "How do I control aphids on roses?",
                "What beneficial insects eat aphids?",
                "How to get rid of pests on my tomatoes?",
                "What is the soil pH for growing carrots?",
                "My plants are turning purple",
                "Why are my tomato plants wilting?",
                "My crops have yellow spots on the leaves",
                "What's wrong with my plants that have purple leaves?"
            ]
            
            logger.info("Testing source file patch:")
            for query in test_queries:
                prompt_type = detect_prompt_type(query)
                logger.info(f"Query: '{query}' -> Type: {prompt_type}")
            
            # Try to trigger a Django app reload - only works in some configurations
            try:
                import django.core.management
                logger.info("Attempting to trigger Django app reload (may not work in all configurations)")
                
                # This is a backup approach in case the app doesn't automatically reload
                logger.info("Patch applied successfully! To ensure changes take effect, restart the Django application if needed.")
                
            except Exception as e:
                logger.info(f"Django reload attempt note: {e}")
                
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
    logger.info("Starting improved patch for query classifier with symptom detection...")
    success = patch_prompt_templates_file()
    if success:
        logger.info("Successfully patched query classifier with symptom detection!")
        sys.exit(0)
    else:
        logger.error("Failed to patch query classifier")
        sys.exit(1) 