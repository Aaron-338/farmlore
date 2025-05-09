"""
Signal handlers for the FarmLore community app.

These signals handle events like post-save for models to trigger
actions like updating verification status or exporting knowledge.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django.contrib.auth.models import User

from .models import IndigenousKnowledge, CommunityValidation, KnowledgeKeeper


@receiver(post_save, sender=User)
def create_knowledge_keeper(sender, instance, created, **kwargs):
    """
    Create a KnowledgeKeeper profile when a new User is created.
    """
    if created:
        KnowledgeKeeper.objects.get_or_create(
            user=instance,
            defaults={
                'village': 'Unknown',
                'district': 'Unknown',
                'years_experience': 0
            }
        )


@receiver(post_save, sender=CommunityValidation)
def update_verification_status(sender, instance, created, **kwargs):
    """
    Update the verification status of an IndigenousKnowledge entry
    when a new validation is added.
    """
    if created:
        # Get the knowledge entry
        knowledge = instance.knowledge
        
        # Count the validations
        validation_count = CommunityValidation.objects.filter(
            knowledge=knowledge
        ).count()
        
        # Update the verification count
        knowledge.verification_count = validation_count
        
        # Update the verification status if the count reaches the threshold
        if validation_count >= 5 and knowledge.verification_status != 'verified':
            knowledge.verification_status = 'verified'
        
        # Save the knowledge entry
        knowledge.save(update_fields=['verification_count', 'verification_status'])
