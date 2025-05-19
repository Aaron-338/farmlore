#!/usr/bin/env python
"""
Improved Standalone RAG Module

This is an enhanced version of the standalone RAG module with improved search algorithms 
and a more robust response enhancement implementation.
"""
import re
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple, Optional

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
        "title": "Cucumber Beetle Management",
        "content": """
Cucumber beetles (both spotted and striped varieties) are common pests of cucumber plants. They feed on leaves, stems, and fruits, and can transmit bacterial wilt disease. Adults are small beetles with either spots or stripes on their yellow-green backs.

Effective control methods include:

1. Row covers: Use floating row covers until flowering to prevent beetles from reaching plants.

2. Yellow sticky traps: Deploy around plants to catch adult beetles.

3. Diatomaceous earth: Apply around the base of plants to control beetle populations.

4. Beneficial nematodes: Apply to soil to control larval stages (which feed on roots).

5. Crop rotation: Avoid planting cucurbits in the same location in consecutive years.

6. Companion planting: Plant radishes, marigolds, or nasturtiums near cucumbers to repel beetles.

7. Kaolin clay: Apply as a spray to leaves to create a physical barrier that deters feeding.

8. Delayed planting: Plant cucumbers after the peak adult emergence for your region.

9. Trap crops: Plant more attractive hosts (like blue hubbard squash) nearby to lure beetles away.

10. Cleanup: Remove plant debris after harvest to eliminate overwintering sites.

For organic control, use neem oil or pyrethrin-based insecticides. Always follow label instructions carefully.
"""
    },
    {
        "title": "Squash Bug Control for Cucumber Plants",
        "content": """
Squash bugs are common pests of cucumber and other cucurbit plants. These gray-brown, flat-backed insects can cause wilting and plant death by sucking sap from plant tissues. Nymphs are smaller with gray bodies and black legs.

Effective management strategies include:

1. Manual removal: Handpick adults, nymphs, and crush the bronze-colored egg clusters found on the undersides of leaves.

2. Trap boards: Place flat boards or shingles near plants; squash bugs will gather underneath at night and can be collected in the morning.

3. Row covers: Protect young plants with floating row covers until flowering begins.

4. Diatomaceous earth: Apply around the base of plants to control nymphs.

5. Companion planting: Interplant with repellent crops like mint, tansy, or radishes.

6. Timed planting: Plant cucumbers later in the season after the first generation of squash bugs has chosen their hosts.

7. Proper sanitation: Clean up garden debris in fall to eliminate overwintering sites.

8. Crop rotation: Avoid planting cucurbits in the same location in consecutive years.

9. Resistant varieties: Some cucumber varieties show more resistance to squash bug damage.

For severe infestations, insecticidal soaps or neem oil can help control the nymphs (though they're less effective on adults). Apply in early morning when the bugs are less active.
"""
    },
    {
        "title": "Managing Aphids on Cucumber Plants",
        "content": """
Aphids are common pests on cucumber plants. These small, soft-bodied insects cluster on the undersides of leaves and growing tips, sucking plant sap and causing leaves to curl, yellow, and become distorted. They also excrete honeydew, which can lead to sooty mold.

Effective control methods for aphids on cucumbers include:

1. Water spray: Use a strong stream of water to knock aphids off plants, repeating every few days as needed.

2. Beneficial insects: Encourage natural predators like ladybugs, lacewings, and parasitic wasps by planting flowers like dill, fennel, and alyssum nearby.

3. Insecticidal soap: Apply to the undersides of leaves where aphids congregate. Repeat applications may be necessary.

4. Neem oil: Spray as both a repellent and growth regulator that prevents aphids from maturing.

5. Reflective mulch: Use silver-colored mulch to confuse and repel aphids.

6. Companion planting: Grow plants that repel aphids, such as garlic, chives, and marigolds, near cucumbers.

7. Row covers: Protect young plants with floating row covers, but remove when plants begin to flower to allow pollination.

8. Proper fertilization: Avoid over-fertilizing with nitrogen, which promotes the tender new growth that aphids prefer.

9. Regular monitoring: Check cucumber plants at least twice weekly, focusing on the undersides of leaves and growing tips.

Early detection and intervention can prevent aphid populations from reaching damaging levels. If biological and cultural methods fail, organic insecticides containing pyrethrin can be used as a last resort.
"""
    },
    {
        "title": "Controlling Whiteflies on Cucumber Plants",
        "content": """
Whiteflies are tiny, moth-like insects that feed on the undersides of cucumber leaves. When disturbed, they fly up in a cloud of white. Their feeding causes yellowing, stunting, and reduced yields, and they can transmit plant viruses.

Effective control methods include:

1. Yellow sticky traps: Place near plants to monitor and reduce adult whitefly populations.

2. Insecticidal soap: Apply to the undersides of leaves where whiteflies congregate, focusing on all life stages.

3. Neem oil: Use as both a repellent and growth disruptor, applying thoroughly to leaf undersides.

4. Beneficial insects: Introduce natural predators like lacewings, ladybugs, and the parasitic wasp Encarsia formosa.

5. Reflective mulch: Use silver-colored mulch to confuse and repel adult whiteflies.

6. Row covers: Protect young plants with floating row covers to prevent initial infestation.

7. Vacuuming: Use a handheld vacuum in the early morning when whiteflies are less active to physically remove them.

8. Proper spacing: Ensure adequate spacing between plants for good air circulation.

9. Avoid over-fertilization: Too much nitrogen encourages whitefly-attractive new growth.

10. Remove infested leaves: Prune heavily infested leaves and immediately seal them in plastic bags for disposal.

Whiteflies can develop resistance to chemical controls, so integrated pest management using multiple strategies is recommended. For severe infestations, consider using approved organic insecticides as a last resort.
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

def search_pest_data_improved(query: str, top_n: int = 2) -> List[Dict[str, Any]]:
    """Improved search for pest data using better keyword matching and text similarity"""
    query_keywords = set(get_keywords(query))
    
    # Check for plant type mentions
    plant_types = {
        "tomato": ["tomato", "tomatoes"],
        "cucumber": ["cucumber", "cucumbers", "cucurbit"],
        "squash": ["squash", "zucchini", "pumpkin"],
        "general": ["plant", "garden", "crop"]
    }
    
    # Check for pest type mentions
    pest_types = {
        "aphid": ["aphid", "aphids", "green bug", "tiny bug", "sap", "honeydew"],
        "spider mite": ["spider mite", "mite", "webbing", "tiny", "dot", "stippling"],
        "hornworm": ["hornworm", "caterpillar", "worm", "large", "green worm", "defoliate"],
        "beetle": ["beetle", "cucumber beetle", "spotted", "striped"],
        "squash bug": ["squash bug", "flat", "gray", "brown bug"],
        "whitefly": ["whitefly", "whiteflies", "white", "fly", "flying", "moth-like"]
    }
    
    # Determine if query mentions symptoms
    symptom_terms = [
        "wilting", "wilt", "yellow", "yellowing", "stunted", "damage", "hole", "holes",
        "curl", "curling", "spot", "spots", "sticky", "dying", "weak", "deformed",
        "distorted", "discolored"
    ]
    
    # Process the query to identify plant, pest and symptoms
    query_terms = clean_text(query).split()
    
    found_plants = []
    for plant, terms in plant_types.items():
        if any(term in query_terms or any(t in query for t in terms) for term in terms):
            found_plants.append(plant)
    
    found_pests = []
    for pest, terms in pest_types.items():
        if any(term in query_terms or any(t in query for t in terms) for term in terms):
            found_pests.append(pest)
    
    has_symptoms = any(symptom in query_terms for symptom in symptom_terms)
    
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
        title_sim = simple_similarity(query, title) * 2  # Weight title matches higher
        content_sim = simple_similarity(query, content[:100])  # Only compare with beginning of content
        
        # Enhanced scoring
        base_score = title_match_count * 3 + content_match_count + title_sim * 10 + content_sim * 5
        
        # Boost score for plant and pest matches
        for plant in found_plants:
            if any(term in title.lower() or term in content.lower() for term in plant_types[plant]):
                base_score += 5
        
        for pest in found_pests:
            if any(term in title.lower() or term in content.lower() for term in pest_types[pest]):
                base_score += 10
        
        # Boost for symptom content if user asked about symptoms
        if has_symptoms and any(symptom in content.lower() for symptom in symptom_terms):
            base_score += 5
        
        results.append({
            "title": title,
            "content": content,
            "score": base_score,
            "matched_keywords": list(query_keywords.intersection(content_keywords)),
            "title_similarity": title_sim,
            "content_similarity": content_sim
        })
    
    # Sort by score and return top_n results
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

def enhance_response(query: str, original_response: str) -> str:
    """
    Enhanced function to augment an AI response with pest management information.
    
    This improved version does better matching, handles more complex queries,
    and provides clearer information sourcing.
    """
    # Skip enhancing if response is already good or query isn't pest-related
    pest_terms = ["pest", "bug", "insect", "mite", "aphid", "beetle", "hornworm", "whitefly", "caterpillar"]
    plant_terms = ["plant", "garden", "tomato", "cucumber", "crop"]
    
    # Only enhance if the query is about pests or plants
    has_pest_terms = any(term in query.lower() for term in pest_terms)
    has_plant_terms = any(term in query.lower() for term in plant_terms)
    
    # Skip if it's not clearly a pest management question
    if not (has_pest_terms or has_plant_terms):
        return original_response
    
    # Search relevant pest management info
    search_results = search_pest_data_improved(query)
    
    if not search_results:
        return original_response
    
    # Determine if we should enhance the response
    top_result = search_results[0]
    
    # Skip if match isn't strong enough
    if top_result["score"] < 10 and top_result["title_similarity"] < 0.3:
        return original_response
    
    # Extract useful information from the search results
    title = top_result["title"]
    content = top_result["content"]
    
    # Clean up content for rendering
    content_paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    # Create the enhanced response
    enhanced_response = original_response + "\n\n"
    enhanced_response += f"Here's specific information from our agricultural pest management database about **{title}**:\n\n"
    
    # Add 2-3 most relevant paragraphs from the content
    max_paras = min(3, len(content_paras))
    for i in range(max_paras):
        if i == 0 or (len(content_paras[i]) > 30):  # Skip very short paragraphs after the first
            enhanced_response += f"{content_paras[i]}\n\n"
    
    return enhanced_response

# Backwards compatibility
search_pest_data = search_pest_data_improved 