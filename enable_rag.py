#!/usr/bin/env python
"""
Enable RAG Functionality

This script patches the HybridEngine to properly utilize RAG capabilities
for pest management queries.
"""

import os
import sys
import logging
import re
import importlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enable_rag")

def patch_hybrid_engine():
    """
    Directly modify the HybridEngine to ensure RAG is used for pest management queries
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
        
        # Find the process_pest_management method and modify it to use RAG
        pest_mgmt_pattern = r"(def process_pest_management.*?return .*?\n\s*})"
        match = re.search(pest_mgmt_pattern, content, re.DOTALL | re.MULTILINE)
        
        if not match:
            logger.error("Could not find process_pest_management method in the file")
            return False
        
        original_method = match.group(1)
        
        # Define improved method that uses RAG
        new_method = '''def process_pest_management(self, params):
        """
        Process pest management queries, checking RAG first for relevant context
        """
        query = params.get('query', '') or params.get('message', '')
        logger.info(f"Processing query of type: pest_management with params: {params}")

        # Try to use RAG first to find relevant context
        rag_context = None
        if hasattr(self, 'rag_system') and self.rag_system:
            try:
                logger.info("Querying RAG system for pest management knowledge...")
                rag_results = self.rag_system.query(query, k=3)
                
                if rag_results:
                    rag_context = "\\n\\n".join(rag_results)
                    logger.info(f"Found relevant RAG context ({len(rag_context)} chars)")
            except Exception as e:
                logger.error(f"Error using RAG for pest management: {str(e)}")

        # Try to extract specific pest name for more targeted response
        pest_name = None
        for pest in ['aphid', 'beetle', 'caterpillar', 'worm', 'moth', 'fly', 'mite', 'thrip', 'weevil']:
            if pest in query.lower():
                pest_name = pest
                break
        
        if pest_name:
            logger.info(f"Identified specific pest in query: {pest_name}")
        else:
            logger.info("No specific pest name provided for Prolog lookup in control methods.")

        # Determine if Prolog is sufficient or we need Ollama
        prolog_sufficient = False  # Default to using Ollama for more complex responses
        attempt_ollama_call = False  # For tracking decision logic
        
        # Record decision for debugging
        logger.info(f"[QUERY_METHOD] Decision for query_type 'pest_management': attempt_ollama_call = {attempt_ollama_call}")
        
        if prolog_sufficient:
            # Use Prolog logic
            logger.info("[CONTROL_METHODS] Using Prolog for response")
            # Prolog implementation would be here
        else:
            # Use Ollama with RAG enhancement
            logger.info("[CONTROL_METHODS] Using Ollama (prolog_sufficient=False, attempt_ollama_call=False).")
            
            if rag_context and self.ollama_handler:
                # Construct an enhanced prompt with RAG context
                logger.info("Enhancing Ollama prompt with RAG context")
                ollama_prompt = f"""Based on the following information from our knowledge base about pest management, 
answer the user's question about managing pests: {query}

KNOWLEDGE BASE INFORMATION:
{rag_context}

Please provide a detailed and accurate answer about how to manage this pest problem,
focusing on integrated pest management principles:
1. Identification
2. Cultural controls
3. Biological controls (natural predators, beneficial insects)
4. Mechanical controls
5. Chemical controls (as a last resort)
"""
                response = self.ollama_handler.generate_response(ollama_prompt, model_name="farmlore-pest-mgmt")
                return {"response": response, "source": "rag_ollama"}
            elif self.ollama_handler:
                # Fallback to regular Ollama with pest management template
                response = self.ollama_handler.generate_response(query, model_name="farmlore-pest-mgmt")
                return {"response": response, "source": "ollama"}
                
        # Default response if all else fails
        return {"response": "I couldn't find specific information about pest management for your query.", "source": "default"}'''
        
        # Replace the method in the content
        new_content = content.replace(original_method, new_method)
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully patched {file_path}")
        
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
    logger.info("Starting RAG enablement...")
    success = patch_hybrid_engine()
    if success:
        logger.info("Successfully enabled RAG for pest management queries!")
        logger.info("NOTE: For changes to take full effect, restart the container with:")
        logger.info("docker restart farmlore-web-1")
        sys.exit(0)
    else:
        logger.error("Failed to enable RAG")
        sys.exit(1) 