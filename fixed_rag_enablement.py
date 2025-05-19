#!/usr/bin/env python
"""
Fixed RAG Enablement for Pest Management

This script patches the _process_control_methods method in hybrid_engine.py
to ensure RAG is used for pest management queries, with proper indentation.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fixed_rag")

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
        
        # Instead of regex search and replace, add a manual small patch
        # Find a specific marker string in the _process_control_methods method
        marker = "def _process_control_methods(self, params: Dict, attempt_ollama_call: bool) -> Dict[str, Any]:"
        
        if marker not in content:
            logger.error(f"Could not find the marker string in {file_path}")
            return False
        
        # Find code to modify
        target_code = "if (not prolog_sufficient or attempt_ollama_call) and self.ollama_handler:"
        
        if target_code not in content:
            logger.error(f"Could not find the target code in {file_path}")
            return False
        
        # Add RAG code before the target line
        rag_code = """        # Check if we have RAG capabilities
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
                
"""
        
        # Add the RAG code before the target code
        content = content.replace(target_code, rag_code + "        " + target_code)
        
        # Find the code that sets ollama_context
        target_context = "ollama_context = user_query"
        
        if target_context not in content:
            logger.error(f"Could not find the context setting code in {file_path}")
            return False
        
        # Replace the if prolog_data_found condition
        old_if_code = """            if prolog_data_found:
                ollama_context = "Based on our knowledge base for " + pest_name + ":\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking for control methods: " + user_query"""
        
        if old_if_code not in content:
            logger.error(f"Could not find the if prolog_data_found condition in {file_path}")
            return False
        
        # New if code with RAG enhancements
        new_if_code = """            if rag_context:
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
            elif prolog_data_found:
                ollama_context = "Based on our knowledge base for " + pest_name + ":\\n" + "\\n".join(prolog_info_parts) + "\\n\\nUser is asking for control methods: " + user_query"""
        
        # Replace the old if code with the new if code
        content = content.replace(old_if_code, new_if_code)
        
        # Replace the response source
        old_source = 'return {"response": llm_response, "source": "ollama"}'
        new_source = 'return {"response": llm_response, "source": "rag_ollama" if rag_context else "ollama"}'
        
        if old_source not in content:
            logger.error(f"Could not find the response source code in {file_path}")
            return False
        
        content = content.replace(old_source, new_source)
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(content)
        
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
    logger.info("Starting fixed RAG enablement for pest management...")
    success = patch_hybrid_engine()
    if success:
        logger.info("Successfully enabled RAG for pest management queries!")
        logger.info("NOTE: For changes to take full effect, restart the container with:")
        logger.info("docker restart farmlore-web-1")
        sys.exit(0)
    else:
        logger.error("Failed to enable RAG")
        sys.exit(1) 