"""
Script to update the __init__.py file in the api/inference_engine directory
to automatically integrate RAG into the standard query pipeline when the module is loaded.
"""

import os
import logging
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_init_file():
    """
    Update the __init__.py file to integrate RAG into the standard query pipeline.
    """
    try:
        # Find the __init__.py file
        init_file_path = "pest-management-chatbot/farmlore-project/api/inference_engine/__init__.py"
        
        # Check if the file exists
        if not os.path.exists(init_file_path):
            logger.error(f"__init__.py file not found at {init_file_path}")
            return False
        
        # Read the current content of the file
        with open(init_file_path, 'r') as f:
            content = f.read()
        
        # Check if the file already has RAG integration code
        if "integrate_rag_into_query_pipeline" in content:
            logger.info("RAG integration code already present in __init__.py file")
            return True
        
        # Define the code to add
        rag_integration_code = """
# Ensure logging is configured
import logging
logger = logging.getLogger(__name__)

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
"""
        
        # Find where to add the new code
        # If RAG is already used in some way, add our code after existing RAG code
        rag_section_match = re.search(r'# Apply RAG integration to HybridEngine.*?(?=\n\n|\Z)', content, re.DOTALL)
        
        if rag_section_match:
            # Add after existing RAG section
            rag_section_end = rag_section_match.end()
            new_content = content[:rag_section_end] + "\n" + rag_integration_code + content[rag_section_end:]
            
        else:
            # If no RAG section exists, add at the end
            new_content = content + "\n" + rag_integration_code
        
        # Write the updated content to the file
        with open(init_file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully updated {init_file_path} with RAG integration code")
        return True
        
    except Exception as e:
        logger.error(f"Error updating __init__.py file: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Updating __init__.py to integrate RAG into the standard query pipeline...")
    success = update_init_file()
    if success:
        print("__init__.py successfully updated!")
    else:
        print("Failed to update __init__.py") 