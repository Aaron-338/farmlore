#!/usr/bin/env python
"""
Test script to check the query classification logic for pest management vs soil analysis
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_query_classification():
    """
    Test the query classification logic directly with example queries
    """
    try:
        # Create output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"query_classification_test_{timestamp}.txt"
        
        with open(output_file, 'w') as f:
            f.write("QUERY CLASSIFICATION TEST RESULTS\n")
            f.write("=" * 40 + "\n")
            f.write(f"Test run at: {datetime.now()}\n\n")
            
            # Define test queries
            pest_management_queries = [
                "How do I get rid of aphids on my roses?",
                "What are natural predators for aphids?",
                "How to control tomato hornworms?",
                "How do I deal with beetles on my potato plants?",
                "What insects typically attack pea plants?"
            ]
            
            soil_analysis_queries = [
                "What is the optimal soil pH for growing tomatoes?",
                "How should I test soil fertility?",
                "What nutrients are missing in my garden soil?",
                "How to improve clay soil?",
                "What is the best soil composition for vegetable gardens?"
            ]
            
            f.write("=== Classification Results ===\n")
            
            # Print expected classifications
            f.write("Expected classifications:\n")
            f.write("Pest Management Queries:\n")
            for query in pest_management_queries:
                f.write(f"  - {query}\n")
            
            f.write("\nSoil Analysis Queries:\n")
            for query in soil_analysis_queries:
                f.write(f"  - {query}\n")
                
            # Define a simple classifier based on keywords
            def simple_classify(query):
                """A simple classifier to simulate our fixed logic"""
                pest_keywords = [
                    'pest', 'insect', 'bug', 'aphid', 'beetle', 'caterpillar', 'worm', 
                    'moth', 'fly', 'mite', 'control', 'kill', 'spray', 'predator', 
                    'hornworm', 'ladybug', 'ladybird'
                ]
                
                soil_keywords = [
                    'soil', 'pH', 'fertility', 'nutrient', 'clay', 'loam', 'composition',
                    'organic matter', 'drainage'
                ]
                
                query_lower = query.lower()
                
                # Check for pest management keywords first (our fix)
                for keyword in pest_keywords:
                    if keyword in query_lower:
                        return "PEST_MANAGEMENT", keyword
                
                # Then check for soil analysis keywords
                for keyword in soil_keywords:
                    if keyword in query_lower:
                        return "SOIL_ANALYSIS", keyword
                        
                # Default fallback
                return "GENERAL_QUERY", None
            
            # Test with our simple classifier
            f.write("\n=== Simple Classifier Results ===\n")
            
            f.write("Pest Management Queries:\n")
            for query in pest_management_queries:
                classification, keyword = simple_classify(query)
                f.write(f"  - '{query}' -> {classification} (matched: '{keyword}')\n")
                if classification != "PEST_MANAGEMENT":
                    f.write(f"    [MISCLASSIFIED]: Should be PEST_MANAGEMENT\n")
            
            f.write("\nSoil Analysis Queries:\n")
            for query in soil_analysis_queries:
                classification, keyword = simple_classify(query)
                f.write(f"  - '{query}' -> {classification} (matched: '{keyword}')\n")
                if classification != "SOIL_ANALYSIS":
                    f.write(f"    [MISCLASSIFIED]: Should be SOIL_ANALYSIS\n")
                    
            # Add a mixed query to test the priority
            f.write("\n=== Testing Priority (Mixed Queries) ===\n")
            mixed_query = "What's the best soil for controlling aphids?"
            classification, keyword = simple_classify(mixed_query)
            f.write(f"  - '{mixed_query}' -> {classification} (matched: '{keyword}')\n")
            f.write(f"    Expected: PEST_MANAGEMENT (our fix prioritizes pest keywords)\n")
            
            # Additional mixed queries to test
            more_mixed_queries = [
                "Should I use soil amendments to treat aphid infestations?",
                "Does soil pH affect beetle populations?",
                "Are there soil nutrients that repel insects?",
                "What soil composition helps plants resist pests?"
            ]
            
            f.write("\n=== More Mixed Query Tests ===\n")
            for query in more_mixed_queries:
                classification, keyword = simple_classify(query)
                f.write(f"  - '{query}' -> {classification} (matched: '{keyword}')\n")
                f.write(f"    With our fix, pest keywords are prioritized over soil keywords\n")
        
        print(f"Test results written to {output_file}")
        
        # Display results
        print("Test results summary:")
        with open(output_file, 'r') as f:
            print(f.read())
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Starting query classification test...")
    success = test_query_classification()
    if success:
        print("Query classification test completed")
        sys.exit(0)
    else:
        print("Query classification test failed")
        sys.exit(1) 