#!/usr/bin/env python
"""
Docker Views RAG Patch

This script directly modifies the views.py file in the Docker container to add RAG functionality.
"""
import os
import sys
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("docker_views_rag_patch")

def patch_views_file(views_path):
    """Directly patch the views.py file to use RAG"""
    try:
        logger.info(f"Starting to patch views file at: {views_path}")
        
        # Check if file exists
        if not os.path.exists(views_path):
            logger.error(f"Views file not found at: {views_path}")
            return False
        
        # Read the file content
        with open(views_path, 'r') as f:
            content = f.read()
            logger.info(f"Successfully read views file ({len(content)} bytes)")
        
        # Write a backup of the original file
        backup_path = f"{views_path}.bak"
        with open(backup_path, 'w') as f:
            f.write(content)
            logger.info(f"Created backup at: {backup_path}")
        
        # Add our direct RAG code at the top of the file, making it self-contained
        rag_code = """
import os
import re
import logging
from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional, Tuple

# Configure logging for RAG
rag_logger = logging.getLogger("direct_rag")

# Sample pest management data
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

6. Diatomaceous earth: Apply food-grade diatomaceous earth around plants to control aphid populations.

7. Pruning: Remove heavily infested leaves and stems to prevent spread.

8. Aluminum foil mulch: Place aluminum foil around the base of plants to repel aphids with reflective light.

For severe infestations, organic or synthetic insecticides may be necessary, but always follow label instructions and consider the environmental impact.
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

6. Proper plant spacing: Ensure good air circulation between plants to prevent infestations.

7. Avoid drought stress: Keep plants well-watered as stressed plants are more susceptible to mite damage.

8. Diatomaceous earth: Apply around plants to control mite populations.

For severe infestations, miticides may be necessary, but rotate different products to prevent resistance development.
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

6. Tilling soil: In fall, till the soil to expose overwintering pupae to predators and cold temperatures.

7. Row covers: Use lightweight row covers to prevent adult moths from laying eggs on plants.

8. Black light traps: Set up black light traps to catch adult moths at night before they lay eggs.

Regular monitoring is key to preventing severe infestations, as hornworms can cause extensive damage quickly.
'''
    },
    {
        "title": "Managing Colorado Potato Beetles",
        "content": '''
Colorado potato beetles are striped beetles that feed on potato plants, as well as eggplant and tomatoes. Adults have distinctive yellow and black stripes, while larvae are reddish with black spots.

Effective management approaches include:

1. Hand-picking: Regularly remove adults, larvae, and egg clusters from plants and destroy them.

2. Row covers: Use floating row covers to prevent beetles from reaching plants, removing covers during flowering if pollination is needed.

3. Crop rotation: Rotate nightshade family crops (potatoes, tomatoes, eggplants) to different locations each year.

4. Mulching: Use straw mulch, which creates habitat for predatory insects that feed on the beetles.

5. Neem oil: Apply neem oil as a repellent and growth regulator for the beetles.

6. Spinosad: Use this organic insecticide derived from soil bacteria that is effective against Colorado potato beetles.

7. Beneficial insects: Encourage predatory stink bugs, ladybugs, and lacewings that feed on beetle eggs and larvae.

8. Trap crops: Plant eggplants as trap crops around potato patches, then treat or remove the trap crops when infested.

Monitoring early in the season is crucial, as controlling the first generation prevents larger second-generation populations.
'''
    },
    {
        "title": "Dealing with Squash Bugs in Vegetable Gardens",
        "content": '''
Squash bugs are common pests of squash, pumpkins, and other cucurbits. Adults are brownish-black with flat backs, while nymphs are gray with black legs.

Effective control methods include:

1. Monitoring: Check under leaves for characteristic bronze-colored egg clusters and crush them.

2. Trap boards: Place boards near plants; squash bugs will hide under them at night and can be collected in the morning.

3. Row covers: Use until flowering, then remove for pollination.

4. Companion planting: Interplant with nasturtiums, marigolds, or radishes to repel squash bugs.

5. Timing plantings: Plant early or late to avoid peak squash bug season.

6. Diatomaceous earth: Apply around the base of plants to control nymphs.

7. Neem oil or insecticidal soap: Apply to target nymphs, as adults are resistant to many treatments.

8. Clean cultivation: Remove garden debris and old cucurbit plants after harvest to eliminate overwintering sites.

9. Resistant varieties: Choose squash varieties less susceptible to squash bug damage.

Controlling young nymphs is much more effective than trying to manage adult populations, so early detection is key.
'''
    }
]

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
    stop_words = {"the", "a", "an", "in", "on", "at", "is", "are", "and", "or", "to", "of", "for", "with", "how", "do", "i", "can", "what", "when", "why"}
    words = [word for word in text.split() if word not in stop_words]
    return words

def simple_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using SequenceMatcher"""
    return SequenceMatcher(None, clean_text(text1), clean_text(text2)).ratio()

def search_pest_data(query: str, top_n: int = 2) -> List[Dict[str, Any]]:
    """Search the pest data directly using keyword matching and text similarity"""
    query_keywords = set(get_keywords(query))
    results = []
    
    rag_logger.info(f"Searching for: '{query}' with keywords: {query_keywords}")
    
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
            rag_logger.info("No relevant information found to enhance response")
            return original_response
        
        top_result = search_results[0]
        
        rag_logger.info(f"Found relevant information: {top_result['title']}")
        
        # Check if result is highly relevant
        if top_result["score"] < 1.0:
            rag_logger.info(f"Top result score ({top_result['score']}) below threshold, not enhancing")
            return original_response
        
        # Extract useful information from the top result
        top_content = top_result["content"].strip()
        
        # Combine the original response with RAG content
        enhanced_response = f"{original_response}\\n\\nAdditional information from our agricultural database:\\n\\n{top_content}"
        
        rag_logger.info("Successfully enhanced response with RAG")
        return enhanced_response
    except Exception as e:
        rag_logger.error(f"Error enhancing response: {str(e)}")
        return original_response
"""
        
        # Check if the RAG code is already in the file
        if "def enhance_response_with_rag" in content:
            logger.info("RAG code already appears to be in the file")
        else:
            logger.info("Adding RAG code to the file")
            content = rag_code + "\n\n" + content
        
        # Now find the chat_view function and modify it to use our RAG enhancement
        chat_view_pattern = r"def chat_view\(request\):"
        if not re.search(chat_view_pattern, content):
            logger.error("Could not find chat_view function")
            return False
        
        # Find the JSON response part
        json_response_pattern = r"return JsonResponse\(\{\s*'response': response\['result'\],\s*'source': response\['source'\]\s*\}\)"
        
        if re.search(json_response_pattern, content):
            logger.info("Found JSON response pattern, modifying it to use RAG")
            
            # Define our replacement with RAG enhancement
            rag_json_response = """
        # Enhance response with RAG if applicable
        query = params.get('message', '')
        original_response = response['result']
        try:
            enhanced_response = enhance_response_with_rag(query, original_response)
            logger.info("Response enhanced with RAG")
        except Exception as e:
            logger.error(f"Error using RAG enhancement: {str(e)}")
            enhanced_response = original_response

        return JsonResponse({
            'response': enhanced_response,
            'source': response['source']
        })"""
            
            # Replace the JSON response with our RAG-enhanced version
            content = re.sub(json_response_pattern, rag_json_response, content)
        else:
            logger.warning("Could not find JSON response pattern")
            return False
        
        # Write the modified file
        logger.info("Writing modified views.py file")
        with open(views_path, 'w') as f:
            f.write(content)
        
        logger.info("Successfully patched views.py file with direct RAG integration")
        return True
    
    except Exception as e:
        logger.error(f"Error patching views.py: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("Starting RAG patch script")
    
    # Use the path provided as argument or the default path
    if len(sys.argv) > 1:
        views_path = sys.argv[1]
    else:
        views_path = "/app/api/views.py"
    
    logger.info(f"Using views path: {views_path}")
    success = patch_views_file(views_path)
    
    if success:
        print("✅ Successfully patched views.py with direct RAG integration")
        sys.exit(0)
    else:
        print("❌ Failed to patch views.py")
        sys.exit(1) 