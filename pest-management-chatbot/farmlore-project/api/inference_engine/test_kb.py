from pyswip import Prolog
from pathlib import Path

def test_kb_loading():
    print("Testing knowledge base loading...")
    
    try:
        # Create a new Prolog instance
        prolog = Prolog()
        
        # Get the absolute path to the knowledge base
        kb_path = Path(r"c:\Users\mmmab\OneDrive\Desktop\pest-management-chatbot\pest-management-chatbot\api\knowledge_base\pest_kb.pl")
        kb_path_str = str(kb_path).replace('\\', '/')
        
        print(f"\nTrying to load knowledge base from: {kb_path_str}")
        
        # Load the knowledge base
        prolog.consult(kb_path_str)
        
        print("Knowledge base loaded successfully!")
        
        # Test a simple query
        print("\nTesting query: pest(aphid)")
        result = list(prolog.query("pest(aphid)"))
        print(f"Query result: {result}")
        
        if result:
            print("Successfully queried the knowledge base!")
        else:
            print("Query returned no results.")
            
        # Test another query
        print("\nTesting query: affects(aphid, tomato)")
        result = list(prolog.query("affects(aphid, tomato)"))
        print(f"Query result: {result}")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_kb_loading()
