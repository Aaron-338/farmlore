from rest_framework import serializers
from ml.models import Dataset, TrainedModel

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file_path', 'url', 'last_updated']

class TrainedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedModel
        fields = ['id', 'name', 'file_path', 'accuracy', 'created_at', 'updated_at']

class PredictionRequestSerializer(serializers.Serializer):
    host_crops = serializers.CharField(max_length=100)
    early_symptoms = serializers.CharField(max_length=255)
    advanced_symptoms = serializers.CharField(max_length=255, required=False, allow_null=True)

class PestQuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)

class SoilQuerySerializer(serializers.Serializer):
    soil_type = serializers.CharField(max_length=100, required=False, allow_null=True)
    crop = serializers.CharField(max_length=100, required=False, allow_null=True)