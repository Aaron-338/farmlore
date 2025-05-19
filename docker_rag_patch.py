#!/usr/bin/env python
"""
Docker-specific RAG patch script to apply RAG integration
to the HybridEngine in the running container.
"""
import os
import sys
import inspect
import logging
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("docker_rag_patch")

def inspect_hybrid_engine():
    """Inspect the HybridEngine to find the right query handling methods"""
    try:
        # Import HybridEngine
        logger.info("Importing HybridEngine...")
        from api.inference_engine.hybrid_engine import HybridEngine
        
        # Create instance to inspect
        engine = HybridEngine()
        
        # Get all public methods
        methods = [m for m in dir(engine) if not m.startswith('_') and callable(getattr(engine, m))]
        logger.info(f"Public methods: {methods}")
        
        # Find relevant query methods
        query_methods = [m for m in methods if any(x in m.lower() for x in ['query', 'process', 'pest', 'management', 'control'])]
        logger.info(f"Potential query methods: {query_methods}")
        
        # Get method signatures and docstrings
        for method_name in query_methods:
            method = getattr(engine, method_name)
            logger.info(f"\nMethod: {method_name}")
            signature = inspect.signature(method)
            logger.info(f"Signature: {signature}")
            if method.__doc__:
                logger.info(f"Docstring: {method.__doc__.strip()}")
            else:
                logger.info("No docstring")
        
        # Check for process_query method specifically
        if hasattr(engine, 'process_query'):
            logger.info("\nFound process_query method - this is most likely the entry point")
            return True
        else:
            logger.info("Could not find process_query method")
            return False
            
    except ImportError:
        logger.error("Could not import HybridEngine")
        return False
    except Exception as e:
        logger.error(f"Error inspecting HybridEngine: {str(e)}")
        return False

def apply_rag_patch():
    """Apply the RAG patch to the running container"""
    try:
        # Step 1: Check if RAG is already imported in api.inference_engine
        if not os.path.exists('/app/api/inference_engine/implement_rag.py'):
            logger.error("RAG implementation not found in container")
            logger.info("Run docker_update_rag.sh first to copy the implementation")
            return False
        
        # Step 2: Import implement_rag and make sure it's available
        sys.path.append('/app')
        
        # Try to reload if already imported
        if 'api.inference_engine.implement_rag' in sys.modules:
            logger.info("Reloading implement_rag module...")
            sys.modules.pop('api.inference_engine.implement_rag')
        
        try:
            logger.info("Importing RAG implementation...")
            from api.inference_engine.implement_rag import get_rag_system, extend_hybrid_engine
            logger.info("RAG implementation imported successfully")
        except ImportError as e:
            logger.error(f"Failed to import RAG implementation: {str(e)}")
            return False
        
        # Step 3: Get the current HybridEngine instance
        logger.info("Getting current HybridEngine instance...")
        try:
            # Try to get the existing instance
            from api.inference_engine import hybrid_engine as engine_module
            engine = engine_module
            logger.info("Found existing HybridEngine instance")
        except (ImportError, AttributeError):
            logger.error("Could not find existing HybridEngine instance")
            logger.info("Creating a new instance...")
            from api.inference_engine.hybrid_engine import HybridEngine
            engine = HybridEngine()
        
        # Step 4: Inspect HybridEngine before patching
        logger.info("Inspecting HybridEngine before patching...")
        inspect_hybrid_engine()
        
        # Step 5: Apply the RAG extension
        logger.info("Extending HybridEngine with RAG capabilities...")
        extend_hybrid_engine(engine)
        
        # Step 6: Verify patching
        if hasattr(engine, 'rag_system'):
            logger.info("RAG system successfully attached to HybridEngine")
            
            # Test the RAG system
            logger.info("Testing RAG system...")
            rag = get_rag_system()
            if rag:
                results = rag.query("How do I control aphids on roses?", k=2)
                if results:
                    logger.info(f"RAG query successful, found {len(results)} results")
                    for i, result in enumerate(results, 1):
                        logger.info(f"Result {i}:\n{result[:200]}...")
                else:
                    logger.warning("RAG query returned no results")
            else:
                logger.warning("Could not initialize RAG system")
            
            return True
        else:
            logger.error("Failed to attach RAG system to HybridEngine")
            return False
        
    except Exception as e:
        logger.error(f"Error applying RAG patch: {str(e)}")
        return False

def modify_startup_script():
    """Make sure RAG integration is initialized on startup"""
    try:
        # Check if start_web.sh exists
        if not os.path.exists('/app/start_web.sh'):
            logger.error("start_web.sh not found in container")
            return False
            
        # Check if start_web_rag.sh exists
        if not os.path.exists('/app/start_web_rag.sh'):
            logger.error("start_web_rag.sh not found in container")
            return False
            
        # Create a backup of the original start_web.sh
        import shutil
        logger.info("Creating backup of start_web.sh...")
        shutil.copy2('/app/start_web.sh', '/app/start_web.sh.bak')
        
        # Copy start_web_rag.sh to start_web.sh
        logger.info("Replacing start_web.sh with start_web_rag.sh...")
        shutil.copy2('/app/start_web_rag.sh', '/app/start_web.sh')
        
        # Make it executable
        os.chmod('/app/start_web.sh', 0o755)
        
        logger.info("Startup script updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error modifying startup script: {str(e)}")
        return False

def set_environment_variables():
    """Set the required environment variables for RAG"""
    try:
        # Set environment variables
        os.environ['USE_RAG'] = 'true'
        os.environ['RAG_PERSIST_DIR'] = '/app/data/chromadb'
        
        # Create the directory if it doesn't exist
        if not os.path.exists('/app/data/chromadb'):
            os.makedirs('/app/data/chromadb', exist_ok=True)
            logger.info("Created RAG data directory: /app/data/chromadb")
        
        logger.info("Environment variables set successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting environment variables: {str(e)}")
        return False

if __name__ == "__main__":
    print("===== Docker RAG Patch =====")
    
    # Set environment variables
    env_success = set_environment_variables()
    print(f"Setting environment variables: {'SUCCESS' if env_success else 'FAILED'}")
    
    # Inspect HybridEngine
    inspect_success = inspect_hybrid_engine()
    print(f"Inspecting HybridEngine: {'SUCCESS' if inspect_success else 'FAILED'}")
    
    # Apply RAG patch
    patch_success = apply_rag_patch()
    print(f"Applying RAG patch: {'SUCCESS' if patch_success else 'FAILED'}")
    
    # Modify startup script
    script_success = modify_startup_script()
    print(f"Modifying startup script: {'SUCCESS' if script_success else 'FAILED'}")
    
    if patch_success:
        print("\nRAG integration successful!")
        print("The system will now use RAG to enhance query responses.")
        print("Restart the container for changes to take full effect.")
    else:
        print("\nRAG integration encountered issues.")
        print("Check the logs for more details.") 