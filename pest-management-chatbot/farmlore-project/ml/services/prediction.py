import os
import numpy as np
import joblib
import json
from django.conf import settings

class PestPredictor:
    def __init__(self, model_path=None, encoders_path=None):
        """Initialize the predictor with model and encoders"""
        # Set default paths if not provided
        if model_path is None:
            model_path = os.path.join(settings.MODEL_DIR, 'rf_model.joblib')
        if encoders_path is None:
            encoders_path = os.path.join(settings.MODEL_DIR, 'encoders.json')
        
        # Load model
        self.model = joblib.load(model_path)
        
        # Load encoders
        with open(encoders_path, 'r') as f:
            encoders_data = json.load(f)
        
        # Convert encoders from list to dict
        self.label_encoders = {}
        for key, value in encoders_data['label_encoders'].items():
            self.label_encoders[key] = {k: int(v) for k, v in value}
        
        # Convert target mapping from list to dict
        self.target_mapping = {int(k): v for k, v in encoders_data['target_mapping']}
    
    def predict(self, host_crops, early_symptoms, advanced_symptoms=None):
        """Predict method based on input features"""
        # Use early symptoms as advanced symptoms if not provided
        if advanced_symptoms is None:
            advanced_symptoms = early_symptoms
            
        # Encode the input features
        try:
            host_encoded = self.label_encoders['Host Crops'].get(host_crops, -1)
            early_encoded = self.label_encoders['Symptoms (Early)'].get(early_symptoms, -1)
            advanced_encoded = self.label_encoders['Symptoms (Advanced)'].get(advanced_symptoms, -1)
            
            # If any encoding failed, return an error
            if -1 in [host_encoded, early_encoded, advanced_encoded]:
                return {
                    "error": "Unknown input values",
                    "details": {
                        "host_crops": host_crops in self.label_encoders['Host Crops'],
                        "early_symptoms": early_symptoms in self.label_encoders['Symptoms (Early)'],
                        "advanced_symptoms": advanced_symptoms in self.label_encoders['Symptoms (Advanced)']
                    }
                }
            
            # Make prediction
            features = np.array([[host_encoded, early_encoded, advanced_encoded]])
            method_index = self.model.predict(features)[0]
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(features)[0]
            
            # Get top 3 predictions with probabilities
            top_indices = np.argsort(probabilities)[::-1][:3]
            top_methods = [self.target_mapping[i] for i in top_indices]
            top_probs = [float(probabilities[i]) for i in top_indices]
            
            return {
                "prediction": self.target_mapping[method_index],
                "confidence": float(probabilities[method_index]),
                "alternatives": [
                    {"method": method, "probability": prob}
                    for method, prob in zip(top_methods, top_probs)
                ]
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_available_values(self):
        """Get available values for input features"""
        return {
            "host_crops": list(self.label_encoders['Host Crops'].keys()),
            "early_symptoms": list(self.label_encoders['Symptoms (Early)'].keys()),
            "advanced_symptoms": list(self.label_encoders['Symptoms (Advanced)'].keys()),
            "methods": list(self.target_mapping.values())
        }