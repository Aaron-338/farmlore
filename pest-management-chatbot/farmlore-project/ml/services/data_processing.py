import os
import pandas as pd
import numpy as np
import json
import requests
from django.conf import settings

def fetch_data_from_url(url, save_path=None):
    """Fetch data from URL and return as pandas DataFrame"""
    response = requests.get(url)
    response.raise_for_status()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
    
    # Create a DataFrame from the CSV content
    return pd.read_csv(pd.io.common.StringIO(response.content.decode('utf-8')))

def save_dataframe(df, path):
    """Save DataFrame to CSV file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved DataFrame to {path}")

def load_dataframe(path):
    """Load DataFrame from CSV file"""
    return pd.read_csv(path)

def create_combined_dataset(pests_df, methods_df):
    """Create a combined dataset for model training"""
    # Create a new dataframe with one row per pest-method combination
    pest_method_rows = []
    
    # Extract pest IDs from the Target Pests column
    methods_df['Target Pests (Pest ID)'] = methods_df['Target Pests (Pest ID)'].fillna('')
    
    for _, method_row in methods_df.iterrows():
        pest_ids = [pid.strip() for pid in method_row['Target Pests (Pest ID)'].split(',') if pid.strip()]
        for pest_id in pest_ids:
            pest_row = pests_df[pests_df['Pest ID'] == pest_id]
            if not pest_row.empty:
                row_data = {
                    'Pest ID': pest_id,
                    'Host Crops': pest_row['Host Crops'].values[0],
                    'Symptoms (Early)': pest_row['Symptoms (Early)'].values[0],
                    'Symptoms (Advanced)': pest_row['Symptoms (Advanced)'].values[0],
                    'Method ID': method_row['Method ID'],
                    'Method Name': method_row['Method Name'],
                    'Effectiveness': method_row['Effectiveness']
                }
                pest_method_rows.append(row_data)
    
    # Create the combined dataframe
    combined_df = pd.DataFrame(pest_method_rows)
    return combined_df

def process_data():
    """Process data from URLs and save to files"""
    # URLs for the datasets
    pests_url = settings.DATASET_URLS['pests']
    methods_url = settings.DATASET_URLS['methods']
    soil_url = settings.DATASET_URLS['soil']
    
    # File paths
    pests_path = os.path.join(settings.RAW_DATA_DIR, 'pests.csv')
    methods_path = os.path.join(settings.RAW_DATA_DIR, 'methods.csv')
    soil_path = os.path.join(settings.RAW_DATA_DIR, 'soil.csv')
    combined_path = os.path.join(settings.PROCESSED_DATA_DIR, 'combined.csv')
    
    # Load the datasets
    print("Loading datasets...")
    pests_df = fetch_data_from_url(pests_url, pests_path)
    methods_df = fetch_data_from_url(methods_url, methods_path)
    soil_df = fetch_data_from_url(soil_url, soil_path)
    
    # Create combined dataset
    combined_df = create_combined_dataset(pests_df, methods_df)
    save_dataframe(combined_df, combined_path)
    
    return pests_df, methods_df, soil_df, combined_df