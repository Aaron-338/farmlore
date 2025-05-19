#!/usr/bin/env python
"""
Updated RAG Enablement for Pest Management

This script patches the _process_control_methods method in hybrid_engine.py
to ensure RAG is used for pest management queries.
"""

import os
import sys
import logging
import re
import importlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("updated_rag")

def patch_hybrid_engine():
    """
    Directly modify the hybrid_engine.py file to use RAG for pest management queries
    """
    try:
        # Path to the hybrid_engine.py file in the Docker container
        file_path = "/app/api/inference_engine/hybrid_engine.py"
        
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Read the original file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Make a backup of the original file
        backup_path = file_path + '.bak'
        with open(backup_path, 'w') as f:
            f.write(content)
        logger.info(f"Created backup at {backup_path}")
        
        # Find the _process_control_methods method and modify it to use RAG
        # Using regex pattern that matches the entire method
        control_methods_pattern = r"def _process_control_methods\(self, params: Dict, attempt_ollama_call: bool\) -> Dict\[str, Any\]:(.*?)def "
        match = re.search(control_methods_pattern, content, re.DOTALL)
        
        if not match:
            logger.error("Could not find _process_control_methods method in the file")
            return False
        
        method_body = match.group(1)
        # Find the position where we need to insert RAG code
        # Looking for the pattern where Ollama is used
        ollama_usage_pattern = r"if \(not prolog_sufficient or attempt_ollama_call\) and self\.ollama_handler:"
        ollama_match = re.search(ollama_usage_pattern, method_body)
        
        if not ollama_match:
            logger.error("Could not find Ollama usage pattern in _process_control_methods")
            return False
        
        # Generate the new method with RAG integration
        new_method_body = method_body.replace(
            "if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:",
            """# Check if we have RAG capabilities
        rag_context = None
        if hasattr(self, 'rag_system') and self.rag_system:
            try:
                logger.info("Querying RAG system for pest management knowledge...")
                rag_results = self.rag_system.query(user_query, k=3)
                
                if rag_results:
                    rag_context = "\\n\\n".join(rag_results)
                    logger.info(f"Found relevant RAG context ({len(rag_context)} chars)")
            except Exception as e:
                logger.error(f"Error using RAG for pest management: {str(e)}")
                
        if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:"""
        )
        
        # Also enhance the Ollama prompt creation with RAG context
        new_method_body = new_method_body.replace(
            "ollama_context = user_query",
            "ollama_context = user_query"  # Keep this line unchanged
        )
        
        new_method_body = new_method_body.replace(
            "if prolog_data_found:",
            """if rag_context:
                # First use RAG context if available
                ollama_context = f\"\"\"Based on the following information from our knowledge base about pest management, 
answer the user's question: {user_query}

KNOWLEDGE BASE INFORMATION:
{rag_context}

\"\"\"
                if prolog_data_found:
                    # Add Prolog data to the context if available
                    ollama_context += f\"\"\"
ADDITIONAL SPECIFIC INFORMATION:
{' '.join(prolog_info_parts)}
\"\"\"
            elif prolog_data_found:"""
        )
        
        # Update the response source
        new_method_body = new_method_body.replace(
            'return {"response": llm_response, "source": "ollama"}',
            'return {"response": llm_response, "source": "rag_ollama" if rag_context else "ollama"}'
        )
        
        # Replace the old method body with the new one
        new_content = content.replace(match.group(0), f"def _process_control_methods(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:{new_method_body}def ")
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully patched {file_path} to use RAG for pest management queries")
        
        # Set environment variables for RAG
        logger.info("Setting environment variables for RAG...")
        os.environ["USE_RAG"] = "true"
        os.environ["RAG_PERSIST_DIR"] = "/app/data/chromadb"
        
        # Try to import and use the modified code
        sys.path.insert(0, '/app')
        try:
            # Clear any cached imports
            if 'api.inference_engine.hybrid_engine' in sys.modules:
                del sys.modules['api.inference_engine.hybrid_engine']
            if 'api.inference_engine.implement_rag' in sys.modules:
                del sys.modules['api.inference_engine.implement_rag']
                
            # Reload the RAG system to ensure it's active
            from api.inference_engine.implement_rag import extend_hybrid_engine
            logger.info("Successfully imported RAG implementation")
            
            # If we can access current engine instance (not guaranteed in script)
            try:
                from api.views import engine_instance
                logger.info("Found existing engine instance, extending with RAG")
                extend_hybrid_engine(engine_instance)
                logger.info("Successfully extended HybridEngine with RAG capabilities")
            except Exception as e:
                logger.info(f"Note: Engine instance not directly accessible from script: {e}")
                logger.info("The patch will take effect on next application restart")
                
            return True
        except Exception as e:
            logger.error(f"Error importing modified modules: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Restore from backup if testing fails
            with open(backup_path, 'r') as f:
                original_content = f.read()
            with open(file_path, 'w') as f:
                f.write(original_content)
            logger.info("Restored original file from backup due to test failure")
            return False
    
    except Exception as e:
        logger.error(f"Error patching HybridEngine: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting RAG enablement for pest management...")
    success = patch_hybrid_engine()
    if success:
        logger.info("Successfully enabled RAG for pest management queries!")
        logger.info("NOTE: For changes to take full effect, restart the container with:")
        logger.info("docker restart farmlore-web-1")
        sys.exit(0)
    else:
        logger.error("Failed to enable RAG")
        sys.exit(1) 