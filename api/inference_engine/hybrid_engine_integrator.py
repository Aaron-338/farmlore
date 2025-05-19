#!/usr/bin/env python
"""
HybridEngine RAG Integrator

This script patches the HybridEngine class to use the Direct RAG integration.
"""
import os
import sys
import logging
import importlib
from types import MethodType
import functools

# Add the parent directory to the path to allow imports to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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
        
        # Try to directly import the hybrid_engine module
        try:
            # First try to import from the standard API path
            import api.inference_engine.hybrid_engine as hybrid_engine_module
            logger.info("Successfully imported HybridEngine from api.inference_engine")
        except ImportError:
            # Fallback to direct import from the root
            logger.info("Trying direct import from root...")
            import hybrid_engine as hybrid_engine_module
            logger.info("Successfully imported HybridEngine from root")
        
        HybridEngine = hybrid_engine_module.HybridEngine
        logger.info("Successfully loaded HybridEngine class")
        
        # Check if we need to perform the patching
        if hasattr(HybridEngine, "_original_query"):
            logger.info("HybridEngine already patched, skipping")
            return True
        
        # Import the direct RAG integration
        logger.info("Importing Direct RAG integration...")
        try:
            # Try standard API path first
            import api.inference_engine.direct_rag_integration as direct_rag
            logger.info("Successfully imported Direct RAG integration from api.inference_engine")
        except ImportError:
            # Try relative import
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            import direct_rag_integration as direct_rag
            logger.info("Successfully imported Direct RAG integration from current directory")
            
        enhance_hybrid_engine_response = direct_rag.enhance_hybrid_engine_response
        logger.info("Successfully imported enhance_hybrid_engine_response function")
        
        # Store the original query method
        original_query = HybridEngine.query
        
        # Define the monkey patching wrapper
        @functools.wraps(original_query)
        def patched_query(self, query_type, **params):
            """Patched query method that enhances responses with RAG"""
            logger.info(f"Patched query called with type: {query_type}")
            
            # Call the original query method
            original_response = original_query(self, query_type, **params)
            
            try:
                # Enhance the response with RAG
                enhanced_response = enhance_hybrid_engine_response(self, params, original_response)
                logger.info("Enhanced response with RAG")
                return enhanced_response
            except Exception as e:
                logger.error(f"Error enhancing response: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                return original_response
        
        # Apply the monkey patch
        logger.info("Applying monkey patch to HybridEngine.query...")
        HybridEngine._original_query = original_query
        HybridEngine.query = patched_query
        
        # Add a flag to indicate RAG is active
        HybridEngine.rag_integration_active = True
        
        # Test the patch with a simple query
        logger.info("Patch applied successfully. HybridEngine now has RAG capabilities.")
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