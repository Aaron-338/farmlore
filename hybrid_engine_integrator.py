#!/usr/bin/env python 
HybridEngine RAG Integrator
 
This script patches the HybridEngine class to use the Direct RAG integration.
import os
import sys
import logging
import importlib
from types import MethodType
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("hybrid_engine_integrator")
 
def patch_hybrid_engine():
    """Patch the HybridEngine class with RAG capabilities"""
    try:
        # Import the HybridEngine module
        logger.info("Importing HybridEngine module...")
        hybrid_engine_module = importlib.import_module("api.inference_engine.hybrid_engine")
        HybridEngine = hybrid_engine_module.HybridEngine
        logger.info("Successfully imported HybridEngine")
 
        # Import the direct RAG integration
        logger.info("Importing Direct RAG integration...")
        direct_rag = importlib.import_module("api.inference_engine.direct_rag_integration")
        enhance_hybrid_engine_response = direct_rag.enhance_hybrid_engine_response
        logger.info("Successfully imported Direct RAG integration")
 
        # Create a proxy for the query method
        def patched_query(self, query_type, **params):
            """Patched query method that enhances responses with RAG"""
            logger.info(f"Patched HybridEngine.query called with type: {query_type}")
 
            # Call the original query method
            original_response = self._original_query(query_type, **params)
 
            # Enhance the response with RAG
            enhanced_response = enhance_hybrid_engine_response(self, params, original_response)
 
            logger.info("Processed query with RAG enhancement")
            return enhanced_response
 
        # Get a reference to the original query method
        original_query = HybridEngine.query
 
        # Patch the HybridEngine class
        logger.info("Patching HybridEngine.query method...")
        HybridEngine._original_query = original_query
        HybridEngine.query = patched_query
 
        # Test the patch with a simple instance
        logger.info("Creating test HybridEngine instance...")
        engine = HybridEngine()
        engine.rag_integration_active = True
 
        logger.info("Successfully patched HybridEngine with RAG capabilities")
        return True
 
    except Exception as e:
        logger.error(f"Error patching HybridEngine: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
 
if __name__ == "__main__":
    success = patch_hybrid_engine()
 
    if success:
        print("✅ Successfully patched HybridEngine with Direct RAG integration")
        sys.exit(0)
    else:
        print("❌ Failed to patch HybridEngine")
        sys.exit(1)
