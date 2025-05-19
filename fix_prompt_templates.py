#!/usr/bin/env python
"""
Fix Prompt Templates

This script patches the prompt_templates.py file to correctly classify
'natural predators' queries as pest_management instead of soil_analysis.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fix_prompt_templates")

def fix_prompt_templates():
    """
    Fix the detect_prompt_type function in prompt_templates.py to correctly classify
    'natural predators' queries as pest_management.
    """
    try:
        # Path to the prompt_templates.py file in the Docker container
        file_path = "/app/api/inference_engine/prompt_templates.py"
        
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
        
        # Look for the pest_management_keywords list
        pest_mgmt_keywords_start = "pest_management_keywords = ["
        if pest_mgmt_keywords_start not in content:
            logger.error("Could not find the pest_management_keywords list")
            return False
        
        # Find where the list ends and add "natural predator" to it
        keyword_lines = []
        capture = False
        for line in content.splitlines():
            if pest_mgmt_keywords_start in line:
                capture = True
                keyword_lines.append(line)
            elif capture and "]" in line:
                # Ensure "natural predator" is at the top of the list
                if "natural predator" not in line and "natural predator" not in "\n".join(keyword_lines):
                    if line.strip() == "]":
                        # If the list ends without comma
                        keyword_lines[-1] = keyword_lines[-1] + ","
                        keyword_lines.append('    "natural predator",')
                    else:
                        # Insert at the beginning with correct indentation
                        keyword_lines.insert(1, '    "natural predator",')
                capture = False
                keyword_lines.append(line)
            elif capture:
                keyword_lines.append(line)
        
        # Extract the existing list from content
        start_index = content.find(pest_mgmt_keywords_start)
        end_index = content.find("]", start_index) + 1
        
        if start_index == -1 or end_index == 0:
            logger.error("Could not find the pest_management_keywords list boundaries")
            return False
        
        # Create the modified list as a string
        modified_list = "\n".join(keyword_lines)
        
        # Replace the old list with the new one
        new_content = content[:start_index] + modified_list + content[end_index:]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully patched {file_path} to prioritize natural predator queries")
        
        # Set priority order for classification
        # Make sure pest_management check happens before soil_analysis
        # Find the detect_prompt_type function
        detect_prompt_start = "def detect_prompt_type(query):"
        if detect_prompt_start not in new_content:
            logger.error("Could not find the detect_prompt_type function")
            return False
        
        # Split the function's content
        func_start_index = new_content.find(detect_prompt_start)
        func_end_index = new_content.find("def ", func_start_index + 1)
        
        if func_start_index == -1 or func_end_index == -1:
            logger.error("Could not find the function boundaries")
            return False
        
        # Extract the function code
        function_code = new_content[func_start_index:func_end_index]
        
        # Replace the function with a fixed version ensuring correct ordering
        # Use single quotes for triple-quoted strings to avoid syntax issues
        fixed_function = '''def detect_prompt_type(query):
    """Detect the type of prompt based on the query content."""
    query_lower = query.lower()

    # Check for pest management keywords first
    if any(keyword in query_lower for keyword in pest_management_keywords):
        logger.info(f"Classified as PEST_MANAGEMENT due to keywords match: {query}")
        return PromptType.PEST_MANAGEMENT

    # Check for pest identification keywords
    if any(keyword in query_lower for keyword in pest_identification_keywords):
        return PromptType.PEST_IDENTIFICATION
        
    # Check for crop pests keywords
    if any(keyword in query_lower for keyword in crop_pests_keywords):
        return PromptType.CROP_PESTS
        
    # Check for indigenous knowledge keywords
    if any(keyword in query_lower for keyword in indigenous_knowledge_keywords):
        return PromptType.INDIGENOUS_KNOWLEDGE
        
    # Check for soil analysis keywords last
    if any(keyword in query_lower for keyword in soil_analysis_keywords):
        return PromptType.SOIL_ANALYSIS
        
    # Default to general query if no specific keywords are found
    return PromptType.GENERAL_QUERY
'''
        
        # Replace the old function with the fixed one
        new_content = new_content[:func_start_index] + fixed_function + new_content[func_end_index:]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Successfully patched {file_path} to prioritize pest management classification")
        
        # Restart the web server to apply changes
        logger.info("For changes to take effect, restart the container")
        
        return True
    
    except Exception as e:
        logger.error(f"Error patching prompt_templates.py: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting prompt template fix...")
    success = fix_prompt_templates()
    if success:
        logger.info("Successfully fixed prompt classification!")
        sys.exit(0)
    else:
        logger.error("Failed to fix prompt classification")
        sys.exit(1) 