"""
Models for the FarmLore community features.

These models support the collection, validation, and sharing of indigenous
technical knowledge related to pest management, crop disease management,
and soil fertilization.
"""
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class KnowledgeKeeper(models.Model):
    """
    A knowledge keeper who contributes indigenous technical knowledge.
    
    Knowledge keepers are community members who share their traditional
    farming practices and expertise with the FarmLore community.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='knowledge_keeper')
    village = models.CharField(_('Village'), max_length=100)
    district = models.CharField(_('District'), max_length=100)
    years_experience = models.PositiveIntegerField(_('Years of Experience'))
    specialization = models.CharField(_('Area of Specialization'), max_length=200, blank=True)
    bio = models.TextField(_('Biography'), blank=True)
    
    class Meta:
        verbose_name = _('Knowledge Keeper')
        verbose_name_plural = _('Knowledge Keepers')
        indexes = [
            models.Index(fields=['village'], name='kk_village_idx'),
            models.Index(fields=['district'], name='kk_district_idx'),
            models.Index(fields=['specialization'], name='kk_specialization_idx'),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} from {self.village}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()

class IndigenousKnowledge(models.Model):
    """
    Indigenous technical knowledge contributed by knowledge keepers.
    
    This model stores traditional Basotho farming practices related to
    pest management, crop disease management, and soil fertilization.
    """
    PRACTICE_TYPES = (
        ('pest_control', _('Pest Control')),
        ('disease_management', _('Disease Management')),
        ('soil_fertility', _('Soil Fertility')),
        ('water_conservation', _('Water Conservation')),
        ('seed_preservation', _('Seed Preservation')),
        ('weather_prediction', _('Weather Prediction')),
        ('other', _('Other')),
    )
    
    VERIFICATION_STATUS = (
        ('pending', _('Pending')),
        ('verified', _('Verified')),
        ('rejected', _('Rejected')),
    )
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    practice_type = models.CharField(_('Practice Type'), max_length=50, choices=PRACTICE_TYPES)
    materials = models.JSONField(_('Materials'), default=list)
    crops = models.JSONField(_('Applicable Crops'), default=list)
    pests = models.JSONField(_('Target Pests'), default=list, blank=True)
    seasons = models.JSONField(_('Applicable Seasons'), default=list)
    keeper = models.ForeignKey(KnowledgeKeeper, on_delete=models.CASCADE, related_name='knowledge_entries')
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Date Modified'), auto_now=True)
    verification_status = models.CharField(_('Verification Status'), max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verification_count = models.PositiveIntegerField(_('Verification Count'), default=0)
    
    # Export tracking fields
    prolog_name = models.CharField(_('Prolog Name'), max_length=200, blank=True, null=True)
    last_exported = models.DateTimeField(_('Last Exported'), blank=True, null=True)
    is_exported = models.BooleanField(_('Is Exported'), default=False)
    
    class Meta:
        verbose_name = _('Indigenous Knowledge')
        verbose_name_plural = _('Indigenous Knowledge Entries')
        indexes = [
            models.Index(fields=['title'], name='ik_title_idx'),
            models.Index(fields=['practice_type'], name='ik_practice_type_idx'),
            models.Index(fields=['verification_status'], name='ik_verification_status_idx'),
            models.Index(fields=['date_added'], name='ik_date_added_idx'),
            models.Index(fields=['date_modified'], name='ik_date_modified_idx'),
            models.Index(fields=['is_exported'], name='ik_is_exported_idx'),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_verified(self):
        """Check if the knowledge entry is verified."""
        return self.verification_status == 'verified'
    
    def get_prolog_name(self):
        """Convert title to a valid Prolog atom (lowercase, underscores)."""
        return self.title.lower().replace(' ', '_')
    
    def mark_as_exported(self):
        """Mark the knowledge entry as exported."""
        self.is_exported = True
        self.last_exported = timezone.now()
        self.save(update_fields=['is_exported', 'last_exported'])
        
        # If prolog_name is not set, set it now
        if not self.prolog_name:
            self.prolog_name = self.get_prolog_name()
            self.save(update_fields=['prolog_name'])

class RegionalObservation(models.Model):
    """
    Regional observations about pests, diseases, and ecological indicators.
    
    This model stores observations made by community members about pest outbreaks,
    disease occurrences, and ecological indicators in their regions.
    """
    OBSERVATION_TYPES = (
        ('pest_outbreak', _('Pest Outbreak')),
        ('disease_occurrence', _('Disease Occurrence')),
        ('ecological_indicator', _('Ecological Indicator')),
        ('weather_pattern', _('Weather Pattern')),
        ('other', _('Other')),
    )
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    observation_type = models.CharField(_('Observation Type'), max_length=50, choices=OBSERVATION_TYPES)
    location = models.CharField(_('Location'), max_length=200)
    date_observed = models.DateField(_('Date Observed'))
    observer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observations')
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Regional Observation')
        verbose_name_plural = _('Regional Observations')
        indexes = [
            models.Index(fields=['observation_type'], name='ro_observation_type_idx'),
            models.Index(fields=['location'], name='ro_location_idx'),
            models.Index(fields=['date_observed'], name='ro_date_observed_idx'),
            models.Index(fields=['date_added'], name='ro_date_added_idx'),
        ]
    
    def __str__(self):
        return self.title

class CommunityValidation(models.Model):
    """
    Community validation of indigenous knowledge.
    
    This model stores validations made by community members for indigenous knowledge entries.
    Each validation includes a rating and optional comments.
    """
    knowledge = models.ForeignKey(IndigenousKnowledge, on_delete=models.CASCADE, related_name='validations')
    validator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validations')
    rating = models.PositiveSmallIntegerField(_('Rating'), choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(_('Comments'), blank=True)
    has_used = models.BooleanField(_('Has Used or Observed'), default=False, help_text=_('Whether the validator has personally used or observed this practice'))
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Community Validation')
        verbose_name_plural = _('Community Validations')
        unique_together = ('knowledge', 'validator')
        indexes = [
            models.Index(fields=['rating'], name='cv_rating_idx'),
            models.Index(fields=['date_added'], name='cv_date_added_idx'),
        ]
    
    def __str__(self):
        return f"Validation by {self.validator.username} for {self.knowledge.title}"
    
    def save(self, *args, **kwargs):
        """Override save to update the verification count of the knowledge entry."""
        super().save(*args, **kwargs)
        
        # Update the verification count of the knowledge entry
        knowledge = self.knowledge
        knowledge.verification_count = knowledge.validations.count()
        
        # Get all validations for this knowledge entry
        validations = knowledge.validations.all()
        
        if validations:
            # If there are at least 3 validations with an average rating of 3 or higher,
            # mark the knowledge as verified
            if knowledge.verification_count >= 3:
                avg_rating = sum(v.rating for v in validations) / knowledge.verification_count
                if avg_rating >= 3:
                    knowledge.verification_status = 'verified'
                    knowledge.save()

class SesothoTerm(models.Model):
    """
    Sesotho terminology related to farming practices.
    
    This model stores Sesotho terms and their English translations
    to preserve indigenous language and knowledge.
    """
    term = models.CharField(_('Sesotho Term'), max_length=100)
    english = models.CharField(_('English Translation'), max_length=100)
    description = models.TextField(_('Description'))
    contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contributed_terms')
    date_added = models.DateTimeField(_('Date Added'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Sesotho Term')
        verbose_name_plural = _('Sesotho Terms')
        unique_together = ('term', 'english')
        indexes = [
            models.Index(fields=['term'], name='st_term_idx'),
            models.Index(fields=['english'], name='st_english_idx'),
            models.Index(fields=['date_added'], name='st_date_added_idx'),
        ]
    
    def __str__(self):
        return f"{self.term} ({self.english})"

class UserProfile(models.Model):
    """
    Extended user profile with role information that can only be set by administrators.
    """
    USER_ROLES = (
        ('knowledge_keeper', _('Knowledge Keeper')),
        ('community_member', _('Community Member')),
        ('knowledge_seeker', _('Knowledge Seeker')),
        ('administrator', _('Administrator')),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(_('User Role'), max_length=50, choices=USER_ROLES, default='knowledge_seeker')
    bio = models.TextField(_('Biography'), blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['role'], name='up_role_idx'),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s profile"

# Create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile with default 'knowledge_seeker' role
        UserProfile.objects.create(user=instance, role='knowledge_seeker')
        
        # Add user to the knowledge_seeker group
        try:
            knowledge_seeker_group = Group.objects.get(name='knowledge_seeker')
            instance.groups.add(knowledge_seeker_group)
        except Group.DoesNotExist:
            # Group doesn't exist yet, this can happen during initial migrations
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance, role='knowledge_seeker')
        
        # Add user to the knowledge_seeker group
        try:
            knowledge_seeker_group = Group.objects.get(name='knowledge_seeker')
            instance.groups.add(knowledge_seeker_group)
        except Group.DoesNotExist:
            # Group doesn't exist yet, this can happen during initial migrations
            pass
            
    instance.profile.save()

# Update user's group when their role changes
@receiver(post_save, sender=UserProfile)
def update_user_groups(sender, instance, **kwargs):
    """
    When a user's role changes, update their group membership accordingly.
    This ensures permissions are always in sync with the user's role.
    """
    user = instance.user
    
    # Remove user from all role-based groups first
    role_groups = Group.objects.filter(name__in=['knowledge_keeper', 'community_member', 'knowledge_seeker', 'administrator'])
    for group in role_groups:
        user.groups.remove(group)
    
    # Add user to the appropriate group based on their role
    try:
        role_group = Group.objects.get(name=instance.role)
        user.groups.add(role_group)
    except Group.DoesNotExist:
        # Group doesn't exist yet, this can happen during initial migrations
        pass

class KnowledgeKeeperApplication(models.Model):
    """
    Application to become a knowledge keeper.
    
    This tracks requests from users who want to be knowledge keepers
    and the approval process by administrators.
    """
    STATUS_CHOICES = (
        ('pending', _('Pending Review')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='keeper_applications')
    village = models.CharField(_('Village'), max_length=100)
    district = models.CharField(_('District'), max_length=100)
    years_experience = models.PositiveIntegerField(_('Years of Experience'))
    specialization = models.CharField(_('Area of Specialization'), max_length=200, blank=True)
    bio = models.TextField(_('Biography'), blank=True)
    reason = models.TextField(_('Reason for Application'), help_text=_('Why do you want to become a knowledge keeper?'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    review_notes = models.TextField(_('Review Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Knowledge Keeper Application')
        verbose_name_plural = _('Knowledge Keeper Applications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Application by {self.user.username} ({self.get_status_display()})"
    
    def approve(self, reviewer):
        """Approve the application and create a KnowledgeKeeper profile."""
        if self.status == 'approved':
            return
            
        self.status = 'approved'
        self.reviewed_by = reviewer
        self.save()
        
        # Create KnowledgeKeeper profile if it doesn't exist
        if not hasattr(self.user, 'knowledge_keeper'):
            keeper = KnowledgeKeeper.objects.create(
                user=self.user,
                village=self.village,
                district=self.district,
                years_experience=self.years_experience,
                specialization=self.specialization,
                bio=self.bio
            )
        
        # Update user profile and group
        try:
            profile = self.user.profile
            profile.role = 'knowledge_keeper'
            profile.save()
        except:
            pass
            
        # Add user to knowledge_keeper group
        try:
            group = Group.objects.get(name='knowledge_keeper')
            self.user.groups.add(group)
        except Group.DoesNotExist:
            pass
            
        # Send notification email
        self.send_approval_notification()
        
    def reject(self, reviewer, notes=''):
        """Reject the application."""
        self.status = 'rejected'
        self.reviewed_by = reviewer
        self.review_notes = notes
        self.save()
        
        # Send notification email
        self.send_rejection_notification()
    
    def send_approval_notification(self):
        """Send email notification about approval."""
        if not self.user.email:
            return
            
        subject = "Your Knowledge Keeper Application Has Been Approved"
        message = f"""
        Dear {self.user.get_full_name() or self.user.username},
        
        We're pleased to inform you that your application to become a Knowledge Keeper has been approved!
        
        You can now contribute indigenous knowledge to the FarmLore platform. Your expertise and wisdom
        will help preserve valuable traditional practices and benefit the wider farming community.
        
        To start contributing, please visit the dashboard and look for the "Add Knowledge" option.
        
        Thank you for joining our community of Knowledge Keepers!
        
        The FarmLore Team
        """
        
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=True,
            )
        except:
            # Log the error but don't break the application flow
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Failed to send approval notification email")
        
    def send_rejection_notification(self):
        """Send email notification about rejection."""
        if not self.user.email:
            return
            
        subject = "Update on Your Knowledge Keeper Application"
        message = f"""
        Dear {self.user.get_full_name() or self.user.username},
        
        We regret to inform you that your application to become a Knowledge Keeper could not be approved at this time.
        
        {self.review_notes if self.review_notes else 'You are still a valued member of our community, and we encourage you to continue participating in other ways.'}
        
        If you believe this decision was made in error or if you have additional information that might support your application,
        please feel free to contact us or submit a new application in the future.
        
        The FarmLore Team
        """
        
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=True,
            )
        except:
            # Log the error but don't break the application flow
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Failed to send rejection notification email")
