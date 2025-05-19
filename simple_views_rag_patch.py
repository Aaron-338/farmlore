#!/usr/bin/env python
"""
Simple Views RAG Patch

This script applies a simple patch to the views.py file to add RAG functionality.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("simple_views_rag_patch")

# Define the path to the views.py file
VIEWS_PATH = "/app/api/views.py"

# Define the RAG code to add to views.py
RAG_IMPORT = """
# Import for RAG functionality
import re
import logging
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple

# Configure RAG logger
rag_logger = logging.getLogger("direct_rag")
"""

RAG_DATA = """
# Sample pest management data for RAG
PEST_DATA = [
    {
        "title": "Aphid Control on Tomatoes",
        "content": '''
Aphids are common pests on tomato plants. They are small, soft-bodied insects that can be green, yellow, brown, red, or black. They feed on plant sap and can cause stunted growth, yellowed leaves, and reduced yields.

Effective control methods for aphids on tomatoes include:

1. Biological control: Introduce natural predators like ladybugs, lacewings, and parasitic wasps that feed on aphids.
2. Neem oil: Apply neem oil spray, which disrupts the aphid life cycle and acts as a repellent.
3. Insecticidal soap: Use insecticidal soap sprays that are specifically designed for soft-bodied insects like aphids.
4. Water spray: Use a strong stream of water to physically remove aphids from plants.
5. Companion planting: Plant aphid-repelling plants like marigolds, nasturtiums, and garlic near tomatoes.
'''
    },
    {
        "title": "Spider Mite Management in Gardens",
        "content": '''
Spider mites are tiny arachnids that can cause significant damage to garden plants. They appear as tiny moving dots, often red, brown, or yellow. Signs of infestation include fine webbing on plants and stippled, discolored leaves.

Effective management strategies include:

1. Water spray: Regular, forceful spraying with water can dislodge mites and reduce populations.
2. Increase humidity: Spider mites thrive in dry conditions, so increasing humidity can discourage them.
3. Neem oil: Apply neem oil as a natural miticide that disrupts the spider mite life cycle.
4. Insecticidal soap: Use specifically formulated soaps that are effective against mites but gentle on plants.
5. Predatory mites: Introduce beneficial predatory mites that feed on spider mites.
'''
    },
    {
        "title": "Controlling Tomato Hornworms",
        "content": '''
Tomato hornworms are large, green caterpillars with white stripes and a horn-like projection on their rear end. They can quickly defoliate tomato plants and damage developing fruit.

Effective control methods include:

1. Hand-picking: Regularly inspect plants and manually remove hornworms. Drop them in soapy water or relocate them far from your garden.
2. Bacillus thuringiensis (Bt): Apply this natural bacterial insecticide that specifically targets caterpillars without harming beneficial insects.
3. Parasitic wasps: Encourage or introduce parasitic wasps like Braconid wasps that lay eggs on hornworms.
4. Companion planting: Plant dill, basil, marigold, or borage near tomatoes to repel hornworms or attract beneficial insects.
5. Crop rotation: Change where you plant tomatoes each year to disrupt the life cycle of overwintering pupae.
'''
    }
]
"""

RAG_FUNCTIONS = """
# RAG utility functions
def clean_text(text: str) -> str:
    """Clean and normalize text for better matching"""
    text = text.lower()
    text = re.sub(r'[\\n\\r\\t]+', ' ', text)  # Replace newlines, tabs with spaces
    text = re.sub(r'\\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^\\w\\s]', '', text)  # Remove punctuation
    return text.strip()

def get_keywords(text: str) -> List[str]:
    """Extract important keywords from text"""
    text = clean_text(text)
    # Remove common stop words
    stop_words = {"the", "a", "an", "in", "on", "at", "is", "are", "and", "or", "to", "of", "for", "with"}
    words = [word for word in text.split() if word not in stop_words]
    return words

def simple_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using SequenceMatcher"""
    return SequenceMatcher(None, clean_text(text1), clean_text(text2)).ratio()

def search_pest_data(query: str, top_n: int = 2) -> List[Dict[str, Any]]:
    """Search the pest data directly using keyword matching and text similarity"""
    query_keywords = set(get_keywords(query))
    results = []
    
    for item in PEST_DATA:
        title = item["title"]
        content = item["content"]
        
        # Calculate keyword matching score
        content_keywords = set(get_keywords(content))
        title_keywords = set(get_keywords(title))
        
        # Count matching keywords
        content_match_count = len(query_keywords.intersection(content_keywords))
        title_match_count = len(query_keywords.intersection(title_keywords))
        
        # Calculate similarity scores
        title_sim = simple_similarity(query, title)
        content_sim = simple_similarity(query, content)
        
        # Combined score (weight title matches more heavily)
        score = (
            (content_match_count * 0.5) + 
            (title_match_count * 2.0) + 
            (title_sim * 3.0) + 
            (content_sim * 1.0)
        )
        
        results.append({
            "title": title,
            "content": content,
            "score": score
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top_n results
    return results[:top_n]

def enhance_response_with_rag(query: str, original_response: str) -> str:
    """Enhance a response using the RAG approach with direct text search"""
    try:
        # Search for relevant information
        search_results = search_pest_data(query)
        
        if not search_results:
            return original_response
        
        top_result = search_results[0]
        
        # Check if result is highly relevant
        if top_result["score"] < 1.0:
            return original_response
        
        # Extract useful information from the top result
        top_content = top_result["content"].strip()
        
        # Combine the original response with RAG content
        enhanced_response = f"{original_response}\\n\\nAdditional information from our agricultural database:\\n\\n{top_content}"
        
        return enhanced_response
    except Exception as e:
        return original_response
"""

# Function to patch the views.py file
def patch_views_file():
    """Apply the RAG patch to the views.py file"""
    try:
        logger.info(f"Starting to patch views file at: {VIEWS_PATH}")
        
        # Check if file exists
        if not os.path.exists(VIEWS_PATH):
            logger.error(f"Views file not found at: {VIEWS_PATH}")
            return False
        
        # Read the file content
        with open(VIEWS_PATH, 'r') as f:
            content = f.read()
            logger.info(f"Successfully read views file ({len(content)} bytes)")
        
        # Make a backup of the original file
        backup_path = f"{VIEWS_PATH}.bak"
        with open(backup_path, 'w') as f:
            f.write(content)
            logger.info(f"Created backup at: {backup_path}")
        
        # Check if the file already has RAG enhancement
        if "enhance_response_with_rag" in content:
            logger.info("File already has RAG enhancement, skipping")
            return True
        
        # Find the first import line to insert our imports after
        import_pos = content.find("import ")
        if import_pos == -1:
            logger.error("Could not find import section in views.py")
            return False
        
        # Find the end of the import section
        next_line_pos = content.find("\n\n", import_pos)
        if next_line_pos == -1:
            next_line_pos = content.find("\n", import_pos)
        
        # Add the RAG imports
        new_content = content[:next_line_pos] + RAG_IMPORT + content[next_line_pos:]
        
        # Find a good position to add the RAG data and functions
        class_pos = new_content.find("class ")
        if class_pos == -1:
            func_pos = new_content.find("def ")
            if func_pos == -1:
                logger.error("Could not find a suitable position to add RAG data and functions")
                return False
            insert_pos = func_pos
        else:
            insert_pos = class_pos
        
        # Add the RAG data and functions
        new_content = new_content[:insert_pos] + RAG_DATA + RAG_FUNCTIONS + "\n\n" + new_content[insert_pos:]
        
        # Find the chat_view function to modify it to use RAG
        chat_view_pos = new_content.find("def chat_view(request):")
        if chat_view_pos == -1:
            logger.error("Could not find chat_view function in views.py")
            return False
        
        # Find the JsonResponse in the chat_view function
        json_response_pos = new_content.find("return JsonResponse(", chat_view_pos)
        if json_response_pos == -1:
            logger.error("Could not find JsonResponse in chat_view function")
            return False
        
        # Find the end of the JsonResponse line
        response_end_pos = new_content.find(")", json_response_pos)
        if response_end_pos == -1:
            logger.error("Could not find end of JsonResponse")
            return False
        
        # Find the beginning of the response assignment
        response_line_pos = new_content.rfind("response =", chat_view_pos, json_response_pos)
        if response_line_pos == -1:
            logger.error("Could not find response assignment in chat_view function")
            return False
        
        # Insert RAG enhancement before JsonResponse
        rag_enhancement = """
        # Enhance response with RAG if applicable
        query = params.get('message', '')
        original_response = response['result']
        enhanced_response = enhance_response_with_rag(query, original_response)
        response['result'] = enhanced_response
        """
        
        # Find a suitable position to insert the RAG enhancement
        insert_pos = new_content.rfind("\n", response_line_pos, json_response_pos) + 1
        
        # Insert the RAG enhancement
        new_content = new_content[:insert_pos] + rag_enhancement + new_content[insert_pos:]
        
        # Write the modified file
        with open(VIEWS_PATH, 'w') as f:
            f.write(new_content)
            logger.info("Successfully wrote modified views.py file")
        
        logger.info("Views.py successfully patched with RAG functionality")
        return True
        
    except Exception as e:
        logger.error(f"Error patching views.py: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting simple views RAG patch")
    success = patch_views_file()
    
    if success:
        print("✅ Successfully patched views.py with RAG functionality")
        sys.exit(0)
    else:
        print("❌ Failed to patch views.py")
        sys.exit(1) 