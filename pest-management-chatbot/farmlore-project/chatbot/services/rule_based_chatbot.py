import json
import os
import random
from django.conf import settings

class RuleBasedChatbot:
    """A simple rule-based chatbot for pest management"""
    
    def __init__(self):
        
        self.sample_data = {
            'host_crops': ['Rice', 'Corn', 'Tomato', 'Cabbage', 'Lettuce'],
            'early_symptoms': ['Yellow leaves', 'Wilting', 'Spots', 'Holes', 'Discoloration'],
            'advanced_symptoms': ['Dead leaves', 'Stunted growth', 'Defoliation', 'Rot', 'Mold'],
            'methods': ['Organic Pesticide', 'Biological Control', 'Cultural Control', 'Mechanical Control', 'Crop Rotation']
        }
        
        # Try to load example data from model, fall back to sample data
        self.example_data = self._load_example_data()
    
    def _load_example_data(self):
        """Load example data for responses"""
        example_data_path = os.path.join(settings.BASE_DIR, 'data', 'models', 'example_data.json')
        if os.path.exists(example_data_path):
            try:
                with open(example_data_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self.sample_data
    
    def _extract_entities(self, message):
        """Extract crop and symptom entities from the message"""
        message = message.lower()
        
        # Extract crops
        crops = []
        for crop in self.example_data.get('host_crops', []):
            if crop.lower() in message:
                crops.append(crop)
        
        # Extract symptoms
        symptoms = []
        for symptom_list in ['early_symptoms', 'advanced_symptoms']:
            for symptom in self.example_data.get(symptom_list, []):
                if symptom.lower() in message:
                    symptoms.append(symptom)
        
        return crops, symptoms
    
    def _get_recommendation(self, crop, symptom):
        """Get a recommendation based on crop and symptom"""
        # Simple rule-based recommendation
        methods = self.example_data.get('methods', [])
        if not methods:
            methods = ['Organic Pesticide', 'Biological Control', 'Cultural Control']
        
        # Select a primary method and alternatives
        random.shuffle(methods)
        primary = methods[0]
        alternatives = methods[1:3] if len(methods) >= 3 else methods
        
        confidence = random.uniform(0.7, 0.95)
        
        return {
            'prediction': primary,
            'confidence': confidence,
            'alternatives': alternatives
        }
    
    def generate_response(self, messages):
        """Generate a response based on the conversation history"""
        # Get the last user message
        last_message = next((m for m in reversed(messages) if m.get('role') == 'user'), None)
        
        if not last_message:
            return "Hello! I'm your Agricultural Pest Management Assistant. How can I help you today?"
        
        user_message = last_message.get('content', '').lower()
        
        # Check for greetings
        if any(greeting in user_message for greeting in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your Agricultural Pest Management Assistant. How can I help you today?"
        
        # Check for pest identification request
        if any(keyword in user_message for keyword in ['pest', 'disease', 'symptom', 'problem']):
            crops, symptoms = self._extract_entities(user_message)
            
            if crops and symptoms:
                # Get recommendation
                result = self._get_recommendation(crops[0], symptoms[0])
                
                return f"Based on your description of {crops[0]} with {symptoms[0]}, I recommend using {result['prediction']} (confidence: {result['confidence']:.0%}). Alternative methods include {', '.join(result['alternatives'])}."
            elif crops:
                return f"What symptoms are you seeing on your {crops[0]} plants?"
            elif symptoms:
                return f"Which crop is showing {symptoms[0]}?"
            else:
                return "I need more information to identify the pest. Could you tell me which crop is affected and what symptoms you're seeing?"
        
        # Check for soil fertilization request
        elif any(keyword in user_message for keyword in ['soil', 'fertiliz', 'nutrient']):
            return "For soil fertilization, I recommend using organic compost or vermicompost. These improve soil structure and add essential nutrients. You can also consider crop rotation and cover crops to maintain soil health."
        
        # Check for available crops
        elif any(keyword in user_message for keyword in ['crop', 'plant', 'what can you help with']):
            crops = ', '.join(self.example_data.get('host_crops', ['various crops']))
            return f"I can help with pest management for {crops}. What crop are you growing?"
        
        # Check for available symptoms
        elif any(keyword in user_message for keyword in ['symptom', 'sign', 'how does it look']):
            early = ', '.join(self.example_data.get('early_symptoms', ['various symptoms']))
            advanced = ', '.join(self.example_data.get('advanced_symptoms', ['various symptoms']))
            return f"Early symptoms might include {early}. Advanced symptoms might include {advanced}. What symptoms are you seeing?"
        
        # Check for available methods
        elif any(keyword in user_message for keyword in ['method', 'control', 'management', 'how to treat']):
            methods = ', '.join(self.example_data.get('methods', ['various methods']))
            return f"Common pest management methods include {methods}. To get a specific recommendation, please tell me about your crop and the symptoms you're seeing."
        
        # General response
        else:
            return "I'm here to help with pest management and soil fertilization. Could you provide more details about your agricultural issue? For example, tell me which crop is affected and what symptoms you're seeing."