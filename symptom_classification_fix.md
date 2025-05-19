# Symptom Classification Fix for RAG System

## Problem Description

The RAG (Retrieval-Augmented Generation) system was experiencing issues with symptom-based queries. When users entered queries describing plant symptoms such as "my crops are turning purple," the system was unable to properly classify these queries and returned an "Unknown query type" error. 

The issue occurred because the query classification system was using a keyword-based approach that could recognize explicit pest mentions and soil-related queries, but lacked the ability to recognize descriptive symptom queries.

## Solution Overview

We enhanced the query classification system by adding support for symptom-based queries. Specifically:

1. Added a comprehensive set of symptom and disease-related keywords to the classification system
2. Created a new classification branch specifically for symptom detection
3. Directed symptom queries to the `PEST_IDENTIFICATION` handler, which has access to the disease database
4. Maintained the existing classification hierarchy and priorities
5. Added test cases to verify the fix works properly

## Implementation Details

The solution was implemented by modifying the `improved_patch_classifier.py` file to include additional keywords and patterns for detecting symptom descriptions. This expanded the classification logic to identify symptom descriptions and direct them to the appropriate handler.

### Key Components Added

1. **Symptom keywords collection**: Added common disease terms, symptom descriptions, and query patterns that indicate a user is asking about plant symptoms:

```python
disease_symptom_keywords = [
    # Common disease terms
    "disease", "infection", "fungus", "bacterial", "virus", "mold", "mildew", 
    "rot", "blight", "rust", "wilt", "powdery", "downy", "fusarium", "verticillium",
    
    # Symptom descriptions
    "yellow leaves", "yellowing", "wilting", "spots", "lesion", "hole", "curling",
    "turning purple", "purple leaves", "purple", "stunted", "deformed", "distorted",
    "brown spots", "black spots", "discolored", "dying", "dropping", "falling off",
    
    # Symptom query patterns
    "why are my plants", "why is my plant", "why are my crops", "what's wrong with my",
    "what is wrong with my", "my plants are", "my plant is", "my crops are",
    "leaves turning", "leaves are turning", "plant looks", "plants look", "symptom"
]
```

2. **Classification logic**: Added a new check for symptom descriptions in the classification function:

```python
# Check for disease/symptom queries SECOND (new addition)
if any(keyword in query_lower for keyword in disease_symptom_keywords):
    logger.info(f"Classified as PEST_IDENTIFICATION due to symptom/disease match: {query}")
    return PromptType.PEST_IDENTIFICATION
```

3. **Testing**: Created comprehensive tests in `test_symptom_classification.py` to validate that various symptom queries are correctly classified.

## Deployment Instructions

### For Linux/macOS:

1. Ensure Docker is running
2. Execute the deployment script:
```
chmod +x deploy_symptom_classifier_fix.sh
./deploy_symptom_classifier_fix.sh
```

### For Windows:

1. Ensure Docker is running
2. Double-click `deploy_symptom_classifier_fix.bat` or run it from the command line

## Verification

After deploying the fix, the system will be able to properly handle symptom-based queries like:

- "My crops are turning purple"
- "Why are my tomato leaves yellow?"
- "My plants are wilting despite watering"
- "What's wrong with my plant with holes in the leaves?"
- "My tomatoes are developing brown spots"

These will now correctly be identified as `PEST_IDENTIFICATION` queries and routed to the appropriate handler, which has access to both pest and disease information in the knowledge base.

## Background Information

The system uses the following disease and symptom data sources:
1. Plant disease reference knowledge base (in Prolog format)
2. Crop-specific disease information
3. Nutrient disorder information (including phosphorus deficiency that causes purple leaves)

With this fix, the symptom data already present in the system can now be properly accessed when users describe symptoms rather than explicitly mentioning diseases or pests. 