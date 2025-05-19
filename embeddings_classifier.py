#!/usr/bin/env python
"""
Embeddings-based Query Classifier

This module uses semantic embeddings to classify agricultural queries without hardcoded rules.
"""

import numpy as np
import logging
from enum import Enum
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("embeddings_classifier")

# Define the prompt types enum to match the one in prompt_templates.py
class PromptType(str, Enum):
    PEST_MANAGEMENT = "pest_management"
    PEST_IDENTIFICATION = "pest_identification"
    SOIL_ANALYSIS = "soil_analysis" 
    INDIGENOUS_KNOWLEDGE = "indigenous_knowledge"
    GENERAL = "general_query"

class EmbeddingsClassifier:
    """
    Classifies agricultural queries using vector embeddings and semantic similarity.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the classifier with a pre-trained sentence transformer model.
        
        Args:
            model_name: The name of the pre-trained model to use
        """
        logger.info(f"Initializing EmbeddingsClassifier with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("Model loaded successfully")
            
            # Define example queries for each category
            self.category_examples = {
                PromptType.PEST_MANAGEMENT: [
                    "how to control aphids on my tomatoes",
                    "what's the best way to get rid of beetles",
                    "natural ways to manage whiteflies",
                    "organic pesticides for vegetable garden",
                    "how to prevent pests in my garden",
                    "controlling spider mites on cucumber plants",
                    "best spray for tomato hornworm",
                    "how to kill garden pests without chemicals",
                    "beneficial insects to control aphids",
                    "how do ladybugs help with pest control",
                ],
                PromptType.PEST_IDENTIFICATION: [
                    "what are these black spots on my tomato leaves",
                    "my plants have yellow leaves what could it be",
                    "what pest causes holes in cucumber leaves",
                    "white powdery coating on my zucchini plants",
                    "why are my plant's leaves curling",
                    "what's eating my tomato fruit",
                    "small white insects on the underside of leaves",
                    "my plants are wilting despite watering",
                    "brown patches on my crops",
                    "what disease causes purple stems on tomatoes",
                ],
                PromptType.SOIL_ANALYSIS: [
                    "what nutrients do tomatoes need",
                    "best soil pH for growing peppers",
                    "how to improve clay soil for gardening",
                    "signs of nitrogen deficiency in plants",
                    "how to test soil fertility at home",
                    "best fertilizer for vegetable gardens",
                    "organic soil amendments for tomatoes",
                    "why is my soil compacted",
                    "how much compost to add to garden soil",
                    "fixing phosphorus deficiency in plants",
                ],
                PromptType.INDIGENOUS_KNOWLEDGE: [
                    "traditional farming methods for corn",
                    "ancient techniques for pest control",
                    "indigenous crop rotation practices",
                    "how did ancestors predict weather for farming",
                    "cultural farming practices for sustainability",
                    "native american three sisters planting",
                    "traditional ways to preserve seeds",
                    "old farming wisdom about pest management",
                    "indigenous plant companion planting",
                    "historical farming methods without chemicals",
                ],
                PromptType.GENERAL: [
                    "when to plant tomatoes",
                    "how much water do peppers need",
                    "best time to harvest carrots",
                    "how to increase tomato yield",
                    "growing vegetables in containers",
                    "starting seeds indoors guide",
                    "vegetable garden layout ideas",
                    "how to grow organic vegetables",
                    "winter gardening tips",
                    "crop rotation basics",
                ]
            }
            
            # Generate and store embeddings for each category
            self.category_embeddings = self._generate_category_embeddings()
            logger.info("Category embeddings generated successfully")
            
        except Exception as e:
            logger.error(f"Error initializing embeddings classifier: {str(e)}")
            raise
    
    def _generate_category_embeddings(self):
        """
        Generate embeddings for each category from the example queries.
        
        Returns:
            Dictionary mapping categories to their embedding vectors
        """
        category_embeddings = {}
        
        for category, examples in self.category_examples.items():
            # Generate embeddings for all examples
            embeddings = self.model.encode(examples)
            
            # Average the embeddings to get a representative vector for the category
            category_embeddings[category] = np.mean(embeddings, axis=0)
            
            logger.info(f"Generated embedding for category: {category}")
        
        return category_embeddings
    
    def classify(self, query):
        """
        Classify a query into one of the predefined categories.
        
        Args:
            query: The user query string to classify
            
        Returns:
            The classified prompt type
        """
        try:
            # Generate embedding for the query
            query_embedding = self.model.encode([query])[0]
            
            # Calculate similarity with each category
            similarities = {}
            for category, embedding in self.category_embeddings.items():
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
                similarities[category] = similarity
                logger.debug(f"Similarity with {category}: {similarity:.4f}")
            
            # Find the category with the highest similarity
            best_category = max(similarities.items(), key=lambda x: x[1])
            category, similarity = best_category
            
            logger.info(f"Classified '{query}' as {category} with confidence {similarity:.4f}")
            
            # Define a confidence threshold
            if similarity < 0.5:
                logger.info(f"Confidence too low ({similarity:.4f}), falling back to GENERAL")
                return PromptType.GENERAL
                
            return category
            
        except Exception as e:
            logger.error(f"Error classifying query: {str(e)}")
            # In case of error, return GENERAL as a safe fallback
            return PromptType.GENERAL

# Function to match the interface in prompt_templates.py
def detect_prompt_type_embeddings(query):
    """
    Detect the appropriate prompt type using embeddings-based classification.
    
    Args:
        query: The user's query
        
    Returns:
        The detected prompt type
    """
    global classifier_instance
    
    # Lazy-load the classifier instance
    if 'classifier_instance' not in globals() or classifier_instance is None:
        try:
            classifier_instance = EmbeddingsClassifier()
        except Exception as e:
            logger.error(f"Failed to initialize EmbeddingsClassifier: {str(e)}")
            # Return GENERAL as fallback if classifier initialization fails
            return PromptType.GENERAL
    
    return classifier_instance.classify(query)

if __name__ == "__main__":
    # Test the classifier with some example queries
    classifier = EmbeddingsClassifier()
    
    test_queries = [
        # Pest management queries
        "How can I control aphids on my tomato plants?",
        "What's a good natural way to get rid of pests?",
        "Are there predatory insects that eat aphids?",
        
        # Pest identification queries
        "My tomato leaves have yellow spots, what could it be?", 
        "What's causing holes in my plant leaves?",
        "My crops are turning purple",
        
        # Soil analysis queries
        "What's the best soil pH for growing carrots?",
        "How can I improve clay soil for gardening?",
        "Why are my plants showing nutrient deficiency?",
        
        # Indigenous knowledge queries
        "What traditional farming methods help with pest control?",
        "How did ancient farmers deal with plant diseases?",
        "Indigenous techniques for soil health",
        
        # General queries
        "When should I plant tomatoes?",
        "How much water do peppers need?",
        "What's the best way to stake tomato plants?"
    ]
    
    print("\nTESTING EMBEDDINGS CLASSIFIER\n" + "="*30)
    for query in test_queries:
        classification = classifier.classify(query)
        print(f"Query: '{query}'")
        print(f"Classification: {classification}\n") 