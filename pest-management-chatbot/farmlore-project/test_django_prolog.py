"""Test script for Django and Prolog integration."""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pest_management_chatbot.settings')
django.setup()

# Import the HybridEngine after Django setup
from api.inference_engine.prolog_engine import PrologEngine

def test_prolog_engine():
    """Test the Prolog engine with Django environment."""
    print("Testing Prolog Engine in Django environment...")
    
    try:
        # Initialize the Prolog engine
        engine = PrologEngine()
        
        # Test 1: Query pests for tomato
        print("\nTest 1: Query pests for tomato")
        pests = engine.query_pests_for_crop("tomato")
        print(f"Pests for tomato: {pests}")
        
        # Test 2: Query control methods for aphid
        print("\nTest 2: Query control methods for aphid")
        methods = engine.query_control_methods("aphid")
        print(f"Control methods for aphid: {methods}")
        
        # Test 3: Get pest details
        print("\nTest 3: Get details for aphid")
        details = engine.get_pest_details("aphid")
        print(f"Aphid details: {details}")
        
        print("\nAll tests passed! The Prolog engine is working correctly with Django.")
        return True
    except Exception as e:
        print(f"Error testing Prolog engine: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_prolog_engine()
