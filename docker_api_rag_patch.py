#!/usr/bin/env python
"""
Docker API RAG Patch

This script patches the API views to use the direct RAG integration.
"""
import os
import sys
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("docker_api_rag_patch")

def patch_api_view(api_views_path):
    """Patch the api_views.py file to use the direct RAG integration"""
    try:
        logger.info(f"Reading API views file: {api_views_path}")
        
        # Check if file exists
        if not os.path.exists(api_views_path):
            logger.error(f"API views file not found: {api_views_path}")
            return False
        
        # Read the original file
        with open(api_views_path, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if "from api.inference_engine.direct_rag_integration import enhance_response" in content:
            logger.info("API views already patched with RAG integration")
            return True
        
        # Add the import for the direct RAG integration
        import_pattern = r"from api\.inference_engine\.hybrid_engine import HybridEngine"
        if re.search(import_pattern, content):
            logger.info("Found HybridEngine import, adding direct_rag_integration import")
            new_import = "from api.inference_engine.hybrid_engine import HybridEngine\nfrom api.inference_engine.direct_rag_integration import enhance_response"
            content = re.sub(import_pattern, new_import, content)
        else:
            logger.warning("Could not find HybridEngine import, adding import at the top")
            content = "from api.inference_engine.direct_rag_integration import enhance_response\n" + content
        
        # Find the chat view function
        chat_view_pattern = r"def chat_view\(request\):"
        if not re.search(chat_view_pattern, content):
            logger.error("Could not find chat_view function in the API views")
            return False
        
        # Find where the response is generated
        response_pattern = r"response = engine\.query\('general_query', params=params\)"
        if re.search(response_pattern, content):
            logger.info("Found response generation, adding RAG enhancement")
            
            # Define the RAG enhancement code
            rag_enhancement = """
        # Get the original response from the engine
        response = engine.query('general_query', params=params)
        
        # Enhance the response with RAG if available
        try:
            if response and "result" in response:
                query = params.get("message", "") or params.get("query", "")
                original_result = response["result"]
                
                # Enhance with RAG
                enhanced_result, _ = enhance_response(query, original_result)
                response["result"] = enhanced_result
                
                # Mark as RAG-enhanced
                if "metadata" not in response:
                    response["metadata"] = {}
                response["metadata"]["rag_enhanced"] = True
        except Exception as e:
            logger.error(f"Error enhancing response with RAG: {str(e)}")
            # Continue with original response if RAG enhancement fails
"""
            
            # Replace the original response generation with RAG enhancement
            content = re.sub(response_pattern, rag_enhancement, content)
        else:
            logger.warning("Could not find response generation pattern in chat_view")
            return False
        
        # Write the patched file
        logger.info("Writing patched API views file")
        with open(api_views_path, 'w') as f:
            f.write(content)
        
        logger.info("Successfully patched API views with RAG integration")
        return True
    
    except Exception as e:
        logger.error(f"Error patching API views: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Check if api_views_path is provided as argument
    if len(sys.argv) > 1:
        api_views_path = sys.argv[1]
    else:
        # Default path in Docker container
        api_views_path = "/app/api/views.py"
    
    success = patch_api_view(api_views_path)
    
    if success:
        print("✅ Successfully patched API views with direct RAG integration")
        sys.exit(0)
    else:
        print("❌ Failed to patch API views")
        sys.exit(1) 