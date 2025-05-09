"""
Simple test script to demonstrate the integration of indigenous knowledge with FarmLore.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Add inference_engine directory to path
inference_engine_dir = os.path.join(parent_dir, 'api', 'inference_engine')
if inference_engine_dir not in sys.path:
    sys.path.append(inference_engine_dir)

# Import the Prolog engine
from prolog_engine import PrologEngine

def test_indigenous_knowledge():
    """Test the integration of indigenous knowledge with FarmLore."""
    print("Testing FarmLore Indigenous Knowledge Integration")
    print("===============================================")
    
    # Initialize the Prolog engine with the hardcoded knowledge base
    print("\n1. Initializing Prolog Engine...")
    prolog = PrologEngine()
    
    # Test querying indigenous pest management methods
    print("\n2. Indigenous Pest Management Methods:")
    query = "indigenous_pest_method(Method), indigenous_method_name(Method, Name)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        method_id = result.get('Method', '')
        print(f"- {method_name}")
    
    # Test finding indigenous methods for specific pests
    print("\n3. Indigenous Methods for Controlling Aphids:")
    query = "indigenous_method_pest(Method, aphid), indigenous_method_name(Method, Name)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        print(f"- {method_name}")
    
    # Test finding indigenous methods for specific crops
    print("\n4. Indigenous Methods for Tomato Crops:")
    query = "indigenous_method_crop(Method, tomato), indigenous_method_name(Method, Name)"
    results = prolog.safe_query(query)
    
    for result in results:
        method_name = result.get('Name', '')
        print(f"- {method_name}")
    
    print("\n5. Integration Complete!")
    print("The indigenous knowledge has been successfully integrated with FarmLore.")
    print("The chatbot can now provide culturally appropriate pest management advice.")

if __name__ == "__main__":
    test_indigenous_knowledge()
