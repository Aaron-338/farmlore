#!/usr/bin/env python
"""
Direct RAG Integration

This module provides RAG capabilities by directly matching text using simple keyword search,
bypassing the need for a vector database.
"""
import os
import re
import logging
from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("direct_rag_integration")

# Sample pest management data
PEST_DATA = [
    {
        "title": "Aphid Control on Tomatoes",
        "content": """
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
"""
    },
    {
        "title": "Spider Mite Management in Gardens",
        "content": """
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
"""
    },
    {
        "title": "Controlling Tomato Hornworms",
        "content": """
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
"""
    },
    {
        "title": "Managing Colorado Potato Beetles",
        "content": """
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
"""
    },
    {
        "title": "Dealing with Squash Bugs in Vegetable Gardens",
        "content": """
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
"""
    }
]

def clean_text(text: str) -> str:
    """Clean and normalize text for better matching"""
    text = text.lower()
    text = re.sub(r'[\n\r\t]+', ' ', text)  # Replace newlines, tabs with spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
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
    
    logger.info(f"Searching for: '{query}' with keywords: {query_keywords}")
    
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
        
        logger.debug(f"Item: {title}, Score: {score} (title_sim={title_sim}, content_sim={content_sim})")
        
        results.append({
            "title": title,
            "content": content,
            "score": score
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top_n results
    return results[:top_n]

def enhance_response(query: str, original_response: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Enhance a response using the RAG approach with direct text search"""
    # Search for relevant information
    search_results = search_pest_data(query)
    
    if not search_results:
        logger.info("No relevant information found to enhance response")
        return original_response, []
    
    top_result = search_results[0]
    
    logger.info(f"Found relevant information: {top_result['title']}")
    
    # Check if result is highly relevant
    if top_result["score"] < 1.0:
        logger.info(f"Top result score ({top_result['score']}) below threshold, not enhancing")
        return original_response, search_results
    
    # Extract useful information from the top result
    top_content = top_result["content"].strip()
    
    # Combine the original response with RAG content
    enhanced_response = f"{original_response}\n\nAdditional information from our agricultural database:\n\n{top_content}"
    
    logger.info("Successfully enhanced response with RAG information")
    return enhanced_response, search_results

def test_direct_rag():
    """Test the direct RAG integration"""
    # Define test query
    test_query = "How can I get rid of aphids on my tomatoes?"
    
    # Get original response (simulated)
    original_response = "Aphids can be controlled using insecticidal soaps or by introducing natural predators like ladybugs."
    
    # Enhance with RAG
    enhanced_response, results = enhance_response(test_query, original_response)
    
    # Print results
    print(f"Query: {test_query}")
    print(f"Original: {original_response}")
    print(f"Enhanced: {enhanced_response[:200]}...")  # Truncate for display
    print(f"Found {len(results)} relevant sources")
    
    return enhanced_response != original_response

def enhance_hybrid_engine_response(hybrid_engine, params: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance a HybridEngine response with RAG capabilities"""
    # Check if we should apply RAG
    if not response or "result" not in response:
        logger.info("No result in response to enhance")
        return response
    
    # Extract the query from parameters
    query = params.get("query", "")
    if not query:
        query = params.get("prompt", "")
    
    if not query:
        logger.info("No query found in parameters, skipping RAG enhancement")
        return response
    
    # Extract the original response
    original_result = response["result"]
    
    try:
        # Enhance with RAG
        enhanced_result, search_results = enhance_response(query, original_result)
        
        # Update the response
        response["result"] = enhanced_result
        
        # Add metadata about RAG sources (optional)
        if search_results:
            if "metadata" not in response:
                response["metadata"] = {}
            
            response["metadata"]["rag_sources"] = [
                {"title": result["title"], "relevance": result["score"]} 
                for result in search_results
            ]
            
            response["metadata"]["rag_enhanced"] = True
    
    except Exception as e:
        logger.error(f"Error enhancing response with RAG: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    return response

if __name__ == "__main__":
    print("=== Direct RAG Test ===")
    success = test_direct_rag()
    print(f"RAG Enhancement: {'✅ Successful' if success else '❌ Failed'}") 