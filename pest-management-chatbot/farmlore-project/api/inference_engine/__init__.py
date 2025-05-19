# This file makes the 'inference_engine' directory a Python package. 

# Inference Engine initialization
import os
import logging
logger = logging.getLogger(__name__)

# Initialize RAG integration if enabled

# Apply RAG integration to HybridEngine
if os.environ.get('USE_RAG', 'false').lower() == 'true':
    try:
        from api.inference_engine.hybrid_engine import HybridEngine
        from api.inference_engine.implement_rag import extend_hybrid_engine
        
        # Get or create the HybridEngine instance
        try:
            # Try to get the singleton instance if available
            from api.inference_engine import hybrid_engine
            engine = hybrid_engine
            print("Found existing HybridEngine instance, extending with RAG")
        except (ImportError, AttributeError):
            # Create a new instance if needed
            engine = HybridEngine()
            print("Created new HybridEngine instance, extending with RAG")
        
        # Extend the engine with RAG capabilities
        extend_hybrid_engine(engine)
        print("Successfully extended HybridEngine with RAG capabilities")
    except Exception as e:
        logging.error(f"Error integrating RAG with HybridEngine: {str(e)}")
        print(f"Error integrating RAG with HybridEngine: {str(e)}")

# Integrate RAG into the standard query pipeline
if os.environ.get('USE_RAG', 'false').lower() == 'true':
    try:
        logger.info("Integrating RAG into the standard query pipeline...")
        from api.inference_engine.integrate_rag import integrate_rag_into_query_pipeline
        
        # Get or create the HybridEngine instance
        try:
            # Try to get the singleton instance if available
            from api.inference_engine import hybrid_engine
            engine = hybrid_engine
            logger.info("Found existing HybridEngine instance")
        except (ImportError, AttributeError):
            # Create a new instance if needed
            from api.inference_engine.hybrid_engine import HybridEngine
            engine = HybridEngine()
            logger.info("Created new HybridEngine instance")
        
        # Integrate RAG into the query pipeline
        success = integrate_rag_into_query_pipeline()
        if success:
            logger.info("RAG successfully integrated into the standard query pipeline")
        else:
            logger.error("Failed to integrate RAG into the standard query pipeline")
    except Exception as e:
        logger.error(f"Error integrating RAG into the standard query pipeline: {str(e)}")
        print(f"Error integrating RAG into the standard query pipeline: {str(e)}")
