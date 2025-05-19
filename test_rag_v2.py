#!/usr/bin/env python
"""
Test script for RAG integration with the direct query wrapper v2
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_rag_v2")

def test_rag_integration():
    """Test if RAG integration is working correctly"""
    # Add app directory to path if needed
    if os.path.exists('/app') and '/app' not in sys.path:
        sys.path.append('/app')
    
    try:
        # Import HybridEngine
        from api.inference_engine.hybrid_engine import HybridEngine
        
        # Create an instance
        engine = HybridEngine()
        
        # Check if it has RAG capability
        has_rag = hasattr(engine, 'rag_system') or hasattr(HybridEngine, 'rag_system') or hasattr(engine, '_rag_enhanced') or hasattr(HybridEngine, '_rag_enhanced')
        
        if has_rag:
            print("✅ RAG integration successful! HybridEngine has RAG capabilities.")
            
            # Try to use RAG
            query_text = "How do I control aphids on tomatoes?"
            
            if hasattr(engine, 'rag_system') and callable(getattr(engine.rag_system, 'query', None)):
                print(f"Testing RAG query with: '{query_text}'")
                results = engine.rag_system.query(query_text)
                
                if results:
                    print(f"RAG query returned {len(results)} results:")
                    for i, result in enumerate(results, 1):
                        print(f"Result {i}: {result[:200]}...")
                else:
                    print("RAG query returned no results.")
            
            return True
        else:
            print("❌ RAG integration failed! HybridEngine does not have RAG capabilities.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing RAG integration: {e}")
        return False

if __name__ == "__main__":
    print("===== Testing RAG Integration V2 =====")
    test_rag_integration()
