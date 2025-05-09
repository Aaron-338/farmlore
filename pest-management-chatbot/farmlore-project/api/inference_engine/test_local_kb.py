from pyswip import Prolog

def test_local_kb():
    print("Testing local knowledge base loading...")
    
    try:
        # Create a new Prolog instance
        prolog = Prolog()
        
        # Use a simple filename in the current directory
        kb_path = "kb.pl"
        
        print(f"\nTrying to load knowledge base from: {kb_path}")
        
        # Load the knowledge base
        prolog.consult(kb_path)
        
        print("Knowledge base loaded successfully!")
        
        # Test queries
        print("\nTesting query: pest(aphid)")
        result = list(prolog.query("pest(aphid)"))
        print(f"Query result: {result}")
        
        print("\nTesting query with variable: affects(Pest, tomato)")
        result = list(prolog.query("affects(Pest, tomato)"))
        print(f"Query result: {result}")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_local_kb(