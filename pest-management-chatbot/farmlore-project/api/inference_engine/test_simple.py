from pyswip import Prolog

def test_simple_prolog():
    print("Testing simple Prolog query...")
    
    try:
        # Create a new Prolog instance
        prolog = Prolog()
        
        # Assert a simple fact
        prolog.assertz("father(michael,john)")
        
        # Query the fact
        print("\nTesting query: father(michael,john)")
        result = list(prolog.query("father(michael,john)"))
        print(f"Query result: {result}")
        
        if result:
            print("Basic Prolog functionality is working!")
        else:
            print("Query returned no results.")
            
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_prolog()
