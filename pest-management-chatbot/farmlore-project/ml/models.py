from django.db import models

class Dataset(models.Model):
    """Model to track datasets"""
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class TrainedModel(models.Model):
    """Model to track trained ML models"""
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (Accuracy: {self.accuracy:.2f})"