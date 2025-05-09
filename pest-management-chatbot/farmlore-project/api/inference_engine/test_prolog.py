import os
import sys
from pathlib import Path
from prolog_engine import PrologEngine

def setup_prolog_path():
    """Add SWI-Prolog to system PATH"""
    prolog_paths = [
        r"C:\Program Files\swipl\bin",
        r"C:\Program Files (x86)\swipl\bin"
    ]
    
    for path in prolog_paths:
        if os.path.exists(path) and path not in os.environ['PATH']:
            print(f"Adding {path} to PATH")
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + path
            return True
    return False

def find_knowledge_base():
    """Find the knowledge base file"""
    # Use absolute paths
    base_dir = Path(r"c:\Users\mmmab\OneDrive\Desktop\pest-management-chatbot\pest-management-chatbot")
    possible_paths = [
        base_dir / 'api' / 'knowledge_base' / 'pest_kb.pl',
    ]
    
    print("\nLooking for knowledge base in:")
    for path in possible_paths:
        print(f"- {path}")
        if path.exists():
            print(f"Found knowledge base at: {path}")
            return path
    return None

def test_prolog_integration():
    print("Testing Prolog Integration...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Setup SWI-Prolog path
    if not setup_prolog_path():
        print("Warning: Could not find SWI-Prolog in standard locations")
    
    # Find knowledge base
    kb_path = find_knowledge_base()
    if not kb_path:
        print("Error: Could not find knowledge base file")
        return
    
    try:
        print("\nInitializing PrologEngine...")
        engine = PrologEngine()
        
        # Test 1: Query pests for a crop
        print("\nTest 1: Query pests for tomato")
        try:
            pests = engine.query_pests_for_crop("tomato")
            print(f"Pests for tomato: {pests}")
        except Exception as e:
            print(f"Error in Test 1: {str(e)}")
        
        # Test 2: Query control methods for aphid
        print("\nTest 2: Query control methods for aphid")
        try:
            methods = engine.query_control_methods("aphid")
            print(f"Control methods for aphid: {methods}")
        except Exception as e:
            print(f"Error in Test 2: {str(e)}")
        
        # Test 3: Query symptoms
        print("\nTest 3: Query symptoms for aphid")
        try:
            symptoms = engine.query_symptoms("aphid")
            print(f"Symptoms for aphid: {symptoms}")
        except Exception as e:
            print(f"Error in Test 3: {str(e)}")
        
        # Test 4: Check intervention needed
        print("\nTest 4: Check if intervention needed for aphid on tomato")
        try:
            intervention = engine.check_intervention_needed("aphid", "tomato")
            print(f"Intervention needed: {intervention}")
        except Exception as e:
            print(f"Error in Test 4: {str(e)}")
        
        # Test 5: Get pest details
        print("\nTest 5: Get details for aphid")
        try:
            details = engine.get_pest_details("aphid")
            print(f"Aphid details: {details}")
        except Exception as e:
            print(f"Error in Test 5: {str(e)}")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\nTest complete.")

if __name__ == "__main__":
    test_prolog_integration()
