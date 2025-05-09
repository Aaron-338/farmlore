from django.core.management.base import BaseCommand
from ml.services.data_processing import load_dataframe
from ml.services.model_training import train_model
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Train the Random Forest model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting model training...'))
        
        try:
            # Load the combined dataset
            combined_path = os.path.join(settings.PROCESSED_DATA_DIR, 'combined.csv')
            if not os.path.exists(combined_path):
                self.stdout.write(self.style.WARNING('Combined dataset not found. Run fetch_data command first.'))
                return
            
            combined_df = load_dataframe(combined_path)
            
            # Train the model
            model, label_encoders, target_mapping, accuracy = train_model(combined_df)
            
            self.stdout.write(self.style.SUCCESS(f'Model training completed successfully! Accuracy: {accuracy:.2f}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error training model: {str(e)}'))