# Test script to directly interact with the HybridEngine
import sys
import json

# Function to generate a response using HybridEngine
def test_hybrid_engine():
    try:
        # Import directly within container's context
        import os
        sys.path.append('/app')
        from api.inference_engine.hybrid_engine import HybridEngine
        
        print("1. Creating HybridEngine instance...")
        engine = HybridEngine()
        
        print("2. Testing engine with greeting...")
        result = engine.query("general_query", {"query": "hello"})
        
        print("3. Result JSON:")
        print(json.dumps(result, indent=2))
        
        print("4. Looking for error key:", "error" in result)
        if "error" in result:
            print("   Error value:", result["error"])
            
        print("5. Looking for response key:", "response" in result)
        if "response" in result:
            print("   Response value:", result["response"])
        
        return result
    except Exception as e:
        print(f"Error testing hybrid engine: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    print("\n===== DIRECT HYBRID ENGINE TEST =====\n")
    result = test_hybrid_engine()
    print("\n===== TEST COMPLETE =====\n") 