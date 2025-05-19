# Inference Engine initialization


# Initialize RAG integration if enabled
import os

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
        import logging
        logging.error(f"Error integrating RAG with HybridEngine: {str(e)}")
        print(f"Error integrating RAG with HybridEngine: {str(e)}")
