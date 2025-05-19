#!/usr/bin/env python
"""
Simple RAG Test

This script tests the direct RAG integration functionality without trying to patch HybridEngine.
"""
import os
import sys
import json
import logging

# Add the current directory to the path to allow imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add api/inference_engine to the path
inference_engine_dir = os.path.join(current_dir, "api", "inference_engine")
if os.path.exists(inference_engine_dir):
    sys.path.insert(0, inference_engine_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_simple_rag")

# Sample response to enhance with RAG
SAMPLE_RESPONSE = {
    "result": "Aphids can be controlled using natural methods or pesticides.",
    "source": "general_knowledge",
    "success": True
}

def test_direct_rag():
    """Test the direct RAG integration without patching HybridEngine"""
    try:
        # Try to import the direct RAG integration module
        print("Importing Direct RAG integration...")
        
        try:
            # First try from the inference_engine directory
            from api.inference_engine.direct_rag_integration import enhance_hybrid_engine_response, enhance_response
            print("Successfully imported Direct RAG integration from api.inference_engine")
        except ImportError:
            # Try direct import
            print("Trying direct import...")
            from direct_rag_integration import enhance_hybrid_engine_response, enhance_response
            print("Successfully imported Direct RAG integration directly")
        
        # Test basic enhancement function
        query = "How do I control aphids on my tomato plants?"
        original_text = "Aphids can be controlled using various methods including natural predators and insecticides."
        
        print(f"\nTesting RAG enhancement with query: '{query}'")
        print(f"Original text: '{original_text}'")
        
        # Call the enhance_response function
        enhanced_text, sources = enhance_response(query, original_text)
        
        print(f"\nEnhanced text:\n{enhanced_text}\n")
        print(f"Enhanced text length: {len(enhanced_text)} characters")
        print(f"Enhancement added {len(enhanced_text) - len(original_text)} characters")
        print(f"Number of sources found: {len(sources)}")
        
        # Print detailed information about sources
        for i, source in enumerate(sources, 1):
            print(f"Source {i}: {source['title']} (score: {source['score']:.2f})")
        
        # Test enhancing a hybrid engine response
        params = {"query": query}
        
        print("\nTesting enhance_hybrid_engine_response function...")
        enhanced_response = enhance_hybrid_engine_response(None, params, SAMPLE_RESPONSE)
        
        print(f"\nOriginal response: {json.dumps(SAMPLE_RESPONSE, indent=2)}")
        print(f"\nEnhanced response result: {enhanced_response['result'][:200]}...")
        
        # Show if RAG added metadata
        if "metadata" in enhanced_response and "rag_sources" in enhanced_response["metadata"]:
            print("\nRAG sources in metadata:")
            for i, source in enumerate(enhanced_response["metadata"]["rag_sources"], 1):
                print(f"  {i}. {source['title']} (relevance: {source['relevance']:.2f})")
        
        print("\nDirect RAG enhancement test completed successfully")
        return True
    
    except Exception as e:
        print(f"\nError testing Direct RAG integration: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== Testing Direct RAG Integration ===")
    
    success = test_direct_rag()
    
    if success:
        print("\n✅ Direct RAG integration is working correctly")
        sys.exit(0)
    else:
        print("\n❌ Direct RAG integration test failed")
        sys.exit(1) 