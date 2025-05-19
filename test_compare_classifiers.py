#!/usr/bin/env python
"""
Test script to compare embeddings-based classification with keyword-based classification.
"""

import sys
import logging
from importlib import import_module

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_classifier(module_name, function_name):
    """
    Dynamically load a classifier function from a module.
    """
    try:
        module = import_module(module_name)
        classifier_fn = getattr(module, function_name)
        return classifier_fn
    except (ImportError, AttributeError) as e:
        logger.error(f"Error loading classifier from {module_name}.{function_name}: {str(e)}")
        return None

def compare_classifiers(queries):
    """
    Compare classification results between the embeddings-based and keyword-based classifiers.
    """
    # Load the classifiers
    try:
        # Import the keyword-based classifier
        from api.inference_engine.prompt_templates import detect_prompt_type as keyword_classifier
        logger.info("Successfully loaded keyword-based classifier")
    except ImportError:
        logger.error("Could not import keyword-based classifier. Make sure API_PATH is in sys.path")
        keyword_classifier = None

    try:
        # Import the embeddings-based classifier
        from embeddings_classifier import detect_prompt_type_embeddings as embeddings_classifier
        logger.info("Successfully loaded embeddings-based classifier")
    except ImportError:
        logger.error("Could not import embeddings-based classifier")
        embeddings_classifier = None
    
    if keyword_classifier is None or embeddings_classifier is None:
        logger.error("One or both classifiers could not be loaded. Aborting comparison.")
        return

    # Compare classifications
    print("\nCOMPARING CLASSIFIERS\n" + "="*50)
    print(f"{'QUERY':<40} | {'KEYWORD-BASED':<20} | {'EMBEDDINGS-BASED':<20}")
    print("-" * 83)
    
    matches = 0
    for query in queries:
        kw_result = keyword_classifier(query)
        emb_result = embeddings_classifier(query)
        
        # Format results for display
        kw_display = str(kw_result)
        if hasattr(kw_result, "value"):
            kw_display = kw_result.value
        
        emb_display = str(emb_result)
        if hasattr(emb_result, "value"):
            emb_display = emb_result.value
        
        # Check if results match
        match = "✓" if kw_display == emb_display else "✗"
        if kw_display == emb_display:
            matches += 1
            
        # Print comparison
        query_trunc = query[:37] + "..." if len(query) > 40 else query.ljust(40)
        print(f"{query_trunc:<40} | {kw_display:<20} | {emb_display:<20} {match}")
    
    # Print summary
    match_percentage = (matches / len(queries)) * 100
    print("\nSUMMARY")
    print(f"Total queries: {len(queries)}")
    print(f"Matching classifications: {matches} ({match_percentage:.1f}%)")

def run_comparison():
    """Run the classifier comparison"""
    # Define test queries covering various scenarios
    test_queries = [
        # Regular pest management queries
        "How to control aphids on tomatoes?",
        "What's the best pesticide for cucumber beetles?",
        "Are there natural predators for whiteflies?",
        "How to get rid of hornworms on tomato plants?",
        
        # Symptom-based queries (likely pest identification)
        "My tomato leaves have yellow spots",
        "What's causing holes in my plant leaves?",
        "My crops are turning purple",
        "White powdery substance on zucchini leaves",
        "Why are my plant leaves curling?",
        "Brown spots on my tomato fruit",
        
        # Soil-related queries
        "What's the best soil pH for growing carrots?",
        "How can I improve clay soil for gardening?",
        "Does my tomato plant have a nutrient deficiency?",
        "What fertilizer is best for peppers?",
        
        # Indigenous knowledge queries
        "Traditional pest control methods from indigenous farmers",
        "Ancient farming techniques for healthy soil",
        "Cultural practices for sustainable farming",
        
        # General gardening queries
        "When should I plant tomatoes?",
        "How much water do pepper plants need?",
        "What's the best way to stake tomato plants?",
        
        # Edge cases and challenging queries
        "My plants look sick but I don't see any insects",
        "Plants dying despite regular watering",
        "Are ladybugs good for my garden?",
        "Purple leaves but healthy fruit",
        "Can companion planting reduce pests?",
        "What's eating my plants at night?"
    ]
    
    compare_classifiers(test_queries)

if __name__ == "__main__":
    run_comparison() 