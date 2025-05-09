"""
Django management command to test the chat API directly
"""
import json
import os
import logging
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand

# Disable Ollama integration
os.environ['USE_OLLAMA'] = 'false'

class Command(BaseCommand):
    help = 'Tests the chat API pattern matching directly'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Query to test')

    def handle(self, *args, **options):
        query = options['query']
        self.stdout.write(f"Testing query: {query}")
        
        # Define patterns and responses (copied from api/views.py)
        patterns = [
            {
                'keywords': ['tomato', 'pest'],
                'name': 'tomato_pests',
                'response': "Common pests affecting tomatoes include tomato hornworms, aphids, whiteflies, spider mites, thrips, and cutworms. These pests can damage leaves, stems, and fruits. Regular inspection and integrated pest management helps prevent severe damage."
            },
            {
                'keywords': ['cabbage', 'aphid'],
                'name': 'cabbage_aphids',
                'response': "To control aphids on cabbage: 1) Use insecticidal soap or neem oil spray, 2) Introduce beneficial insects like ladybugs, 3) Use a strong water spray to dislodge them, 4) Apply diatomaceous earth around plants, and 5) For severe infestations, consider organic pyrethrins. Regularly check the undersides of leaves where aphids often hide."
            },
            {
                'keywords': ['rice', 'yellow'],
                'name': 'rice_yellow_leaves',
                'response': "Yellow leaves in rice plants often indicate nutrient deficiency, particularly nitrogen. They could also be a sign of diseases like Rice Yellow Mottle Virus, bacterial leaf blight, or pest infestations like leafhoppers. Examine the pattern of yellowing - if older leaves yellow first, it's likely nitrogen deficiency. If new leaves yellow, it might be iron or zinc deficiency. Check also for water management issues."
            },
            {
                'keywords': ['soil', 'fertil'],
                'name': 'soil_fertilization',
                'response': "Natural methods for soil fertilization include: 1) Composting kitchen scraps and yard waste, 2) Using cover crops like legumes to fix nitrogen, 3) Applying well-rotted manure, 4) Making compost tea, 5) Adding worm castings, and 6) Utilizing green manures. These methods improve soil structure, add nutrients gradually, and promote beneficial soil organisms."
            },
            {
                'keywords': ['rice', 'pest'],
                'name': 'rice_pests',
                'response': "Common rice pests include: 1) Rice stem borers - causing deadhearts and whiteheads, 2) Rice leafhoppers and planthoppers - transmitting viral diseases, 3) Rice water weevil - damaging roots, 4) Rice gall midge - creating galls on developing tillers, and 5) Armyworms - feeding on foliage. Integrated pest management combining resistant varieties, cultural practices, and judicious pesticide use works best."
            },
            {
                'keywords': ['maize', 'pest'],
                'name': 'maize_pests',
                'response': "Common pests in maize include: 1) Fall armyworm - feeding on leaves and ears, 2) Stem borers - tunneling through stalks, 3) Corn earworm - damaging kernels, 4) Rootworms - attacking roots, and 5) Aphids - sucking sap and transmitting diseases. Integrated pest management approaches including crop rotation, timely planting, and resistant varieties are effective control strategies."
            }
        ]
        
        message_lower = query.lower()
        
        # Try exact pattern matching first
        for pattern in patterns:
            if all(keyword in message_lower for keyword in pattern['keywords']):
                self.stdout.write(self.style.SUCCESS(f"EXACT MATCH PATTERN: {pattern['name']}"))
                self.stdout.write(self.style.SUCCESS(f"RESPONSE: {pattern['response']}"))
                return
        
        # Helper function for fuzzy matching
        def keyword_similarity(word, text):
            # Check for exact substring first
            if word in text:
                return 1.0
            
            # Otherwise, check similarity with words in text
            text_words = text.split()
            max_similarity = 0
            for text_word in text_words:
                similarity = SequenceMatcher(None, word, text_word).ratio()
                max_similarity = max(max_similarity, similarity)
            return max_similarity
        
        # Try fuzzy matching if no exact match
        best_pattern = None
        best_score = 0.6  # Threshold for fuzzy matching
        
        for pattern in patterns:
            # Calculate average similarity score for all keywords
            total_score = 0
            keyword_scores = []
            
            for keyword in pattern['keywords']:
                similarity = keyword_similarity(keyword, message_lower)
                total_score += similarity
                keyword_scores.append((keyword, similarity))
            
            avg_score = total_score / len(pattern['keywords'])
            self.stdout.write(f"Pattern {pattern['name']} fuzzy match score: {avg_score:.2f} - Keyword scores: {keyword_scores}")
            
            if avg_score > best_score:
                best_score = avg_score
                best_pattern = pattern
        
        # Use the best fuzzy match if one was found
        if best_pattern:
            self.stdout.write(self.style.SUCCESS(f"FUZZY MATCH PATTERN: {best_pattern['name']} (score: {best_score:.2f})"))
            self.stdout.write(self.style.SUCCESS(f"RESPONSE: {best_pattern['response']}"))
            return
        
        self.stdout.write(self.style.WARNING("No pattern match found"))
        self.stdout.write("Default response: I understand you're asking about agricultural pest management or soil fertility. For specific advice, please mention the crop, symptoms, or pests you're dealing with. I can help with pest identification, control methods, soil fertility, and sustainable farming practices.") 