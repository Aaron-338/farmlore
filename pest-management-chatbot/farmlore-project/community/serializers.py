"""
Serializers for the FarmLore community features.

These serializers support the API endpoints for the community interface,
allowing knowledge keepers to share indigenous technical knowledge and
community members to validate and access this knowledge.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import KnowledgeKeeper, IndigenousKnowledge, RegionalObservation, CommunityValidation, SesothoTerm

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class KnowledgeKeeperSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeKeeper model."""
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = KnowledgeKeeper
        fields = ['id', 'user', 'full_name', 'village', 'district', 'years_experience', 'specialization', 'bio']

class IndigenousKnowledgeSerializer(serializers.ModelSerializer):
    """Serializer for IndigenousKnowledge model."""
    keeper = KnowledgeKeeperSerializer(read_only=True)
    keeper_id = serializers.PrimaryKeyRelatedField(
        queryset=KnowledgeKeeper.objects.all(),
        write_only=True,
        source='keeper'
    )
    practice_type_display = serializers.CharField(source='get_practice_type_display', read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    is_verified = serializers.ReadOnlyField()
    prolog_name = serializers.ReadOnlyField()
    
    class Meta:
        model = IndigenousKnowledge
        fields = [
            'id', 'title', 'description', 'practice_type', 'practice_type_display',
            'materials', 'crops', 'pests', 'seasons', 'keeper', 'keeper_id',
            'date_added', 'date_modified', 'verification_status',
            'verification_status_display', 'verification_count', 'is_verified',
            'prolog_name'
        ]

class RegionalObservationSerializer(serializers.ModelSerializer):
    """Serializer for RegionalObservation model."""
    observer = UserSerializer(read_only=True)
    observer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='observer'
    )
    observation_type_display = serializers.CharField(source='get_observation_type_display', read_only=True)
    
    class Meta:
        model = RegionalObservation
        fields = [
            'id', 'title', 'description', 'observation_type', 'observation_type_display',
            'village', 'district', 'crops_affected', 'date_observed',
            'observer', 'observer_id', 'date_added'
        ]

class CommunityValidationSerializer(serializers.ModelSerializer):
    """Serializer for CommunityValidation model."""
    validator = UserSerializer(read_only=True)
    validator_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='validator'
    )
    knowledge_title = serializers.CharField(source='knowledge.title', read_only=True)
    
    class Meta:
        model = CommunityValidation
        fields = [
            'id', 'knowledge', 'knowledge_title', 'validator', 'validator_id',
            'rating', 'comments', 'has_used', 'date_added'
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CommunityValidation.objects.all(),
                fields=['knowledge', 'validator_id'],
                message="You have already validated this knowledge entry."
            )
        ]

class SesothoTermSerializer(serializers.ModelSerializer):
    """Serializer for SesothoTerm model."""
    contributor = UserSerializer(read_only=True)
    contributor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='contributor',
        required=False
    )
    
    class Meta:
        model = SesothoTerm
        fields = [
            'id', 'term', 'english', 'description',
            'contributor', 'contributor_id', 'date_added'
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=SesothoTerm.objects.all(),
                fields=['term', 'english'],
                message="This Sesotho term and translation combination already exists."
            )
        ]
