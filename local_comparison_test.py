#!/usr/bin/env python
"""
Simplified comparison test between embeddings-based and keyword-based classifiers.
Runs directly in the local environment without requiring Docker.
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Add necessary paths
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("pest-management-chatbot/farmlore-project"))

def run_comparison():
    """Run the classifier comparison"""
    try:
        # Import the embeddings classifier
        from embeddings_classifier import EmbeddingsClassifier, PromptType as EmbeddingsPromptType
        logger.info("Successfully imported embeddings classifier")
        
        # Create the embeddings classifier instance
        emb_classifier = EmbeddingsClassifier()
        logger.info("Initialized embeddings classifier\n")
        
        # Define test queries covering various scenarios
        test_queries = [
            # Regular pest management queries
            "How to control aphids on tomatoes?",
            "What's the best pesticide for cucumber beetles?",
            "Are there natural predators for whiteflies?",
            
            # Symptom-based queries (likely pest identification)
            "My tomato leaves have yellow spots",
            "What's causing holes in my plant leaves?",
            "My crops are turning purple",
            "White powdery substance on zucchini leaves",
            
            # Soil-related queries
            "What's the best soil pH for growing carrots?",
            "How can I improve clay soil for gardening?",
            
            # Indigenous knowledge queries
            "Traditional farming methods for pest control",
            "Ancient techniques for healthy soil",
            
            # General gardening queries
            "When should I plant tomatoes?",
            "How much water do pepper plants need?",
            
            # Edge cases and challenging queries
            "Plants dying despite regular watering",
            "Purple leaves but healthy fruit",
            "What's eating my plants at night?"
        ]
        
        # Simple keyword-based classifier for demonstration
        def keyword_classify(query):
            query_lower = query.lower()
            
            # Pest management keywords
            pest_keywords = ["control", "pesticide", "get rid of", "spray", "predator", "ladybug"]
            if any(keyword in query_lower for keyword in pest_keywords):
                return "pest_management"
                
            # Pest identification keywords (including symptoms)
            symptom_keywords = ["yellow", "spots", "holes", "wilting", "powdery", "purple"]
            if any(keyword in query_lower for keyword in symptom_keywords):
                return "pest_identification"
                
            # Soil keywords
            soil_keywords = ["soil", "ph", "fertilizer", "nutrient"]
            if any(keyword in query_lower for keyword in soil_keywords):
                return "soil_analysis"
                
            # Indigenous knowledge keywords
            indigenous_keywords = ["traditional", "ancient", "cultural"]
            if any(keyword in query_lower for keyword in indigenous_keywords):
                return "indigenous_knowledge"
                
            # Default to general
            return "general_query"
        
        # Compare classifications
        print("\nCOMPARING CLASSIFIERS\n" + "="*50)
        print(f"{'QUERY':<40} | {'KEYWORD-BASED':<20} | {'EMBEDDINGS-BASED':<20}")
        print("-" * 83)
        
        matches = 0
        for query in test_queries:
            # Get classifications
            kw_result = keyword_classify(query)
            
            emb_result = emb_classifier.classify(query)
            if hasattr(emb_result, "value"):
                emb_result = emb_result.value
            
            # Check if results match
            match = "✓" if kw_result == emb_result else "✗"
            if kw_result == emb_result:
                matches += 1
                
            # Print comparison
            query_trunc = query[:37] + "..." if len(query) > 40 else query.ljust(40)
            print(f"{query_trunc:<40} | {kw_result:<20} | {emb_result:<20} {match}")
        
        # Print summary
        match_percentage = (matches / len(test_queries)) * 100
        print("\nSUMMARY")
        print(f"Total queries: {len(test_queries)}")
        print(f"Matching classifications: {matches} ({match_percentage:.1f}%)")
        
    except Exception as e:
        logger.error(f"Error in comparison test: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
    return True

if __name__ == "__main__":
    logger.info("Starting local classifier comparison test...")
    success = run_comparison()
    if success:
        logger.info("\nTest completed successfully!")
    else:
        logger.error("\nTest failed!")
        sys.exit(1) 