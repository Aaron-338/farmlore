import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import json
from django.conf import settings
from ml.models import TrainedModel

def encode_features(df, target_column):
    """Encode categorical features and target"""
    # Encode categorical features
    label_encoders = {}
    for column in ['Host Crops', 'Symptoms (Early)', 'Symptoms (Advanced)']:
        le = LabelEncoder()
        df[column + '_encoded'] = le.fit_transform(df[column])
        label_encoders[column] = {label: index for index, label in enumerate(le.classes_)}
    
    # Encode the target variable
    target_le = LabelEncoder()
    df[target_column + '_encoded'] = target_le.fit_transform(df[target_column])
    target_mapping = {index: label for index, label in enumerate(target_le.classes_)}
    
    # Save encoders
    encoders_data = {
        'label_encoders': {k: list(v.items()) for k, v in label_encoders.items()},
        'target_mapping': list(target_mapping.items())
    }
    
    encoders_path = os.path.join(settings.MODEL_DIR, 'encoders.json')
    os.makedirs(os.path.dirname(encoders_path), exist_ok=True)
    
    with open(encoders_path, 'w') as f:
        json.dump(encoders_data, f)
    
    return df, label_encoders, target_mapping

def train_model(df, target_column='Method Name'):
    """Train a Random Forest model"""
    # Encode features
    df, label_encoders, target_mapping = encode_features(df, target_column)
    
    # Prepare features and target
    X = df[['Host Crops_encoded', 'Symptoms (Early)_encoded', 'Symptoms (Advanced)_encoded']]
    y = df[target_column + '_encoded']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Random Forest model
    print("Training Random Forest model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Evaluate the model
    accuracy = rf_model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save the model
    model_path = os.path.join(settings.MODEL_DIR, 'rf_model.joblib')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(rf_model, model_path)
    
    # Save feature importances
    feature_importances = {
        'Host Crops': float(rf_model.feature_importances_[0]),
        'Symptoms (Early)': float(rf_model.feature_importances_[1]),
        'Symptoms (Advanced)': float(rf_model.feature_importances_[2])
    }
    
    importances_path = os.path.join(settings.MODEL_DIR, 'feature_importances.json')
    with open(importances_path, 'w') as f:
        json.dump(feature_importances, f)
    
    # Create example data for the chatbot
    example_data = {
        'host_crops': list(label_encoders['Host Crops'].keys()),
        'early_symptoms': list(label_encoders['Symptoms (Early)'].keys()),
        'advanced_symptoms': list(label_encoders['Symptoms (Advanced)'].keys()),
        'methods': [v for _, v in sorted([(int(k), v) for k, v in target_mapping.items()])]
    }
    
    example_data_path = os.path.join(settings.MODEL_DIR, 'example_data.json')
    with open(example_data_path, 'w') as f:
        json.dump(example_data, f)
    
    # Save model metadata to database
    model_record, created = TrainedModel.objects.update_or_create(
        name='random_forest_pest_management',
        defaults={
            'file_path': model_path,
            'accuracy': accuracy
        }
    )
    
    print("Model training complete!")
    return rf_model, label_encoders, target_mapping, accuracy