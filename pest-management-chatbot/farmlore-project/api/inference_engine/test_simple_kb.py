from pyswip import Prolog
import os

def test_simple_kb():
    print("Testing simple knowledge base loading...")
    
    try:
        # Create a new Prolog instance
        prolog = Prolog()
        
        # Get the path to the simple knowledge base (in the same directory)
        kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_kb.pl")
        kb_path = kb_path.replace('\\', '/')  # Convert backslashes to forward slashes
        
        print(f"\nTrying to load knowledge base from: {kb_path}")
        
        # Load the knowledge base
        prolog.consult(kb_path)
        
        print("Knowledge base loaded successfully!")
        
        # Test queries
        print("\nTesting query: pest(aphid)")
        result = list(prolog.query("pest(aphid)"))
        print(f"Query result: {result}")
        
        print("\nTesting query: affects(aphid, tomato)")
        result = list(prolog.query("affects(aphid, tomato)"))
        print(f"Query result: {result}")
        
        print("\nTesting query: symptom(aphid, yellowing)")
        result = list(prolog.query("symptom(aphid, yellowing)"))
        print(f"Query result: {result}")
        
        print("\nTesting query: control_method(aphid, soap)")
        result = list(prolog.query("control_method(aphid, soap)"))
        print(f"Query result: {result}")
        
        print("\nTesting query with variable: affects(Pest, tomato)")
        result = list(prolog.query("affects(Pest, tomato)"))
        print(f"Query result: {result}")
        
        print("\nTesting query with variable: symptom(aphid, Symptom)")
        result = list(prolog.query("symptom(aphid, Symptom)"))
        print(f"Query result: {result}")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_kb()
