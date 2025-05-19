import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ml.services.data_processing import fetch_data_from_url, save_dataframe, create_combined_dataset

class Command(BaseCommand):
    help = 'Fetch and process datasets'

    def handle(self, *args, **options):
        self.stdout.write('Fetching and processing datasets...')
        
        # Fetch the data
        pests_df = fetch_data_from_url(settings.DATASET_URLS['pests'], os.path.join(settings.RAW_DATA_DIR, 'pests.csv'))
        methods_df = fetch_data_from_url(settings.DATASET_URLS['methods'], os.path.join(settings.RAW_DATA_DIR, 'methods.csv'))
        soil_df = fetch_data_from_url(settings.DATASET_URLS['soil'], os.path.join(settings.RAW_DATA_DIR, 'soil.csv'))
        
        # Create combined dataset
        combined_df = create_combined_dataset(pests_df, methods_df)
        save_dataframe(combined_df, os.path.join(settings.PROCESSED_DATA_DIR, 'combined.csv'))
        
        # Print dataset info
        self.stdout.write(f'Pests dataset: {len(pests_df)} rows')
        self.stdout.write(f'Methods dataset: {len(methods_df)} rows')
        self.stdout.write(f'Soil dataset: {len(soil_df)} rows')
        self.stdout.write(f'Combined dataset: {len(combined_df)} rows')
        
        self.stdout.write(self.style.SUCCESS('Successfully fetched and processed datasets'))