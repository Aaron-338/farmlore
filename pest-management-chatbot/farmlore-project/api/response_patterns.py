"""
Response patterns for the chat API.

This module contains the patterns and responses used by the chat API
for matching user queries to specific agricultural knowledge.
"""

# Response patterns with keywords for matching
RESPONSE_PATTERNS = [
    {
        'keywords': ['tomato', 'pest'],
        'name': 'tomato_pests',
        'response': """Common pests affecting tomatoes include tomato hornworms, aphids, whiteflies, spider mites, thrips, and cutworms. These pests can damage leaves, stems, and fruits. Regular inspection and integrated pest management helps prevent severe damage."""
    },
    {
        'keywords': ['cabbage', 'aphid'],
        'name': 'cabbage_aphids',
        'response': """To control aphids on cabbage: 1) Use insecticidal soap or neem oil spray, 2) Introduce beneficial insects like ladybugs, 3) Use a strong water spray to dislodge them, 4) Apply diatomaceous earth around plants, and 5) For severe infestations, consider organic pyrethrins. Regularly check the undersides of leaves where aphids often hide."""
    },
    {
        'keywords': ['rice', 'yellow'],
        'name': 'rice_yellow_leaves',
        'response': """Yellow leaves in rice plants often indicate nutrient deficiency, particularly nitrogen. They could also be a sign of diseases like Rice Yellow Mottle Virus, bacterial leaf blight, or pest infestations like leafhoppers. Examine the pattern of yellowing - if older leaves yellow first, it's likely nitrogen deficiency. If new leaves yellow, it might be iron or zinc deficiency. Check also for water management issues."""
    },
    {
        'keywords': ['soil', 'fertil'],
        'name': 'soil_fertilization',
        'response': """Natural methods for soil fertilization include: 1) Composting kitchen scraps and yard waste, 2) Using cover crops like legumes to fix nitrogen, 3) Applying well-rotted manure, 4) Making compost tea, 5) Adding worm castings, and 6) Utilizing green manures. These methods improve soil structure, add nutrients gradually, and promote beneficial soil organisms."""
    },
    {
        'keywords': ['tomato', 'wilt'],
        'name': 'tomato_wilting',
        'response': """Wilting in tomato plants can be caused by several factors: 1) Fusarium wilt - a fungal disease that causes progressive wilting and yellowing, 2) Verticillium wilt - another fungal pathogen affecting the vascular system, 3) Bacterial wilt - causing rapid collapse of the plant, 4) Root-knot nematodes - damaging roots and reducing water uptake, 5) Drought stress - insufficient water, or 6) Excessive heat. Check the soil moisture, look for discoloration in stem cross-sections, and examine roots for damage to help diagnose the specific cause."""
    },
    {
        'keywords': ['aphid', 'affect'],
        'name': 'aphid_crops',
        'response': """Aphids can affect many crops, but are particularly problematic for: 1) Cabbage and brassicas, 2) Lettuce and leafy greens, 3) Tomatoes, 4) Peppers, 5) Cucumbers and squash, and 6) Beans. Aphids tend to target tender new growth and suck sap from the plants, causing stunted growth, yellowing, and leaf curling."""
    },
    {
        'keywords': ['tomato', 'brown'],
        'name': 'tomato_brown_leaves',
        'response': """Brown leaves on tomato plants can indicate several problems: 1) Early blight - fungal disease causing brown spots with concentric rings, 2) Late blight - dark brown lesions that spread rapidly in humid conditions, 3) Bacterial spot - small, dark spots that may have yellow halos, 4) Sunscald - from excessive direct sunlight, 5) Nutrient deficiency - particularly potassium, or 6) Water stress - either too much or too little water. Check the pattern of browning and examine the undersides of leaves for signs of disease."""
    },
    {
        'keywords': ['corn', 'pest'],
        'name': 'corn_pests',
        'response': """Major corn pests include: 1) Corn earworm - feeding on silks and kernels, 2) European corn borer - tunneling through stalks, 3) Fall armyworm - causing leaf damage, 4) Corn rootworm - damaging roots, and 5) Aphids - sucking sap. Management strategies include crop rotation, resistant varieties, biological controls, and carefully timed insecticide applications."""
    },
    {
        'keywords': ['potato', 'blight'],
        'name': 'potato_blight',
        'response': """Potato blight (Phytophthora infestans) is a destructive disease causing water-soaked lesions that rapidly turn brown/black on leaves and stems. To manage: 1) Plant resistant varieties, 2) Ensure good air circulation, 3) Avoid overhead irrigation, 4) Remove infected plants immediately, 5) Apply copper-based fungicides preventatively, and 6) Practice crop rotation. Early detection and prompt action are critical."""
    },
    {
        'keywords': ['organic', 'control'],
        'name': 'organic_pest_control',
        'response': """Organic pest control methods include: 1) Beneficial insects (ladybugs, lacewings, parasitic wasps), 2) Botanical insecticides (neem oil, pyrethrum), 3) Microbial controls (Bacillus thuringiensis), 4) Physical barriers (row covers, sticky traps), 5) Companion planting (marigolds, basil, garlic), and 6) Cultural practices (crop rotation, proper spacing, sanitation). These approaches work best as part of an integrated pest management system."""
    },
    {
        'keywords': ['crop', 'rotation'],
        'name': 'crop_rotation',
        'response': """Crop rotation helps break pest and disease cycles by changing what you grow in each area. Effective rotation groups: 1) Brassicas (cabbage, broccoli), 2) Legumes (beans, peas), 3) Solanaceae (tomatoes, potatoes), 4) Cucurbits (cucumbers, squash), 5) Alliums (onions, garlic), and 6) Root crops (carrots, beets). Wait 3-4 years before growing plants from the same family in the same location for best results."""
    },
    {
        'keywords': ['bean', 'rust'],
        'name': 'bean_rust',
        'response': """Bean rust is a fungal disease causing rusty orange or brown spots on leaves. For control: 1) Use resistant varieties, 2) Improve air circulation with proper spacing, 3) Avoid overhead watering, 4) Remove and destroy infected plants, 5) Apply sulfur or copper-based fungicides early, and 6) Rotate crops to non-legumes for 2-3 years to break the disease cycle."""
    },
    {
        'keywords': ['cucumber', 'beetle'],
        'name': 'cucumber_beetles',
        'response': """Cucumber beetles damage plants by feeding on leaves, stems, flowers, and fruits, and can transmit bacterial wilt. Management strategies include: 1) Row covers until flowering, 2) Yellow sticky traps, 3) Diatomaceous earth applications, 4) Timely removal of affected plants, 5) Beneficial nematodes for larvae, and 6) Evening application of organic insecticides like neem oil or pyrethrin when beetles are active."""
    },
    {
        'keywords': ['rice', 'pest'],
        'name': 'rice_pests',
        'response': """Common rice pests include: 1) Rice stem borers - causing "deadhearts" and "whiteheads", 2) Rice leafhoppers and planthoppers - transmitting viral diseases, 3) Rice water weevil - damaging roots, 4) Rice gall midge - creating galls on developing tillers, and 5) Armyworms - feeding on foliage. Integrated pest management combining resistant varieties, cultural practices, and judicious pesticide use works best."""
    }
]

# Intent-based fallback responses
INTENT_RESPONSES = {
    "pest_general": """To effectively manage pests, it's important to correctly identify the specific pest affecting your crops. Different pests require different control strategies. Could you describe what the pest looks like or what symptoms you're seeing on your plants? If possible, include the crop affected and what part of the plant shows damage.""",
    
    "disease_general": """Plant diseases can be caused by fungi, bacteria, viruses, or environmental conditions. For accurate diagnosis, consider: 1) What parts of the plant are affected? 2) What do the symptoms look like? 3) How quickly is it spreading? 4) What crop is affected? With more specific information, I can provide targeted advice for managing the disease.""",
    
    "soil_general": """Healthy soil is the foundation of successful farming. To improve soil fertility, consider testing your soil to determine its current nutrient levels and pH. Based on those results, you can add organic matter like compost, use cover crops, practice crop rotation, or add specific amendments to address deficiencies. What specific soil challenges are you facing?""",
    
    "cultivation_general": """Successful crop cultivation requires attention to proper planting times, spacing, watering schedules, and nutrient management. Different crops have different requirements. To provide specific advice, I'd need to know which crop you're growing, your climate region, and what stage of growth the plants are in.""",
    
    "general": """I understand you're asking about agricultural pest management or soil fertility. For specific advice, please mention the crop, symptoms, or pests you're dealing with. I can help with pest identification, control methods, soil fertility, and sustainable farming practices."""
}

# Keyword groups for intent detection
INTENT_KEYWORDS = {
    "pest_general": ['pest', 'bug', 'insect', 'worm', 'beetle', 'caterpillar', 'mite', 'aphid', 'thrips'],
    "disease_general": ['disease', 'fungus', 'rot', 'blight', 'mold', 'mildew', 'virus', 'bacterial', 'infection'],
    "soil_general": ['soil', 'fertilizer', 'nutrient', 'compost', 'manure', 'amendment', 'organic matter'],
    "cultivation_general": ['plant', 'grow', 'sow', 'cultivate', 'water', 'irrigation', 'spacing', 'harvest', 'prune']
} 