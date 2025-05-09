from django.core.management.base import BaseCommand
from ml.services.data_processing import process_data
from ml.models import Dataset
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fetch and process datasets'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data fetch and processing...'))
        
        try:
            pests_df, methods_df, soil_df, combined_df = process_data()
            
            # Update dataset records in the database
            for name, url in settings.DATASET_URLS.items():
                file_path = os.path.join(settings.RAW_DATA_DIR, f'{name}.csv')
                Dataset.objects.update_or_create(
                    name=name,
                    defaults={
                        'file_path': file_path,
                        'url': url
                    }
                )
            
            # Add combined dataset
            combined_path = os.path.join(settings.PROCESSED_DATA_DIR, 'combined.csv')
            Dataset.objects.update_or_create(
                name='combined',
                defaults={
                    'file_path': combined_path,
                    'url': ''  # No URL for combined dataset
                }
            )
            
            self.stdout.write(self.style.SUCCESS('Data processing completed successfully!'))
            
            # Print dataset info
            self.stdout.write(f'Pests dataset: {len(pests_df)} rows')
            self.stdout.write(f'Methods dataset: {len(methods_df)} rows')
            self.stdout.write(f'Soil dataset: {len(soil_df)} rows')
            self.stdout.write(f'Combined dataset: {len(combined_df)} rows')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing data: {str(e)}'))