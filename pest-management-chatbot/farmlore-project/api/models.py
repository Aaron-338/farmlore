from django.db import models
from django.utils.translation import gettext_lazy as _

# Existing Dataset model
class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# New TrainedModel model
class TrainedModel(models.Model):
    """Model representing a trained machine learning model."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OllamaModel(models.Model):
    """Model to manage Ollama LLM models and their configuration."""
    
    name = models.CharField(max_length=100, unique=True, help_text=_("Model name as recognized by Ollama (e.g., 'tinyllama', 'llama2')"))
    display_name = models.CharField(max_length=100, help_text=_("Human-readable name for display"))
    description = models.TextField(blank=True, help_text=_("Description of the model's capabilities"))
    
    is_active = models.BooleanField(default=False, help_text=_("Whether this model is active and available for use"))
    is_default = models.BooleanField(default=False, help_text=_("Whether this is the default model"))
    
    default_temperature = models.FloatField(default=0.7, help_text=_("Default temperature parameter (0.0-1.0)"))
    default_max_tokens = models.IntegerField(default=500, help_text=_("Default max tokens for response generation"))
    
    date_added = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Model capabilities
    supports_chat = models.BooleanField(default=True, help_text=_("Whether the model supports chat completions"))
    supports_function_calling = models.BooleanField(default=False, help_text=_("Whether the model supports function calling"))
    supports_vision = models.BooleanField(default=False, help_text=_("Whether the model supports vision/image inputs"))
    
    class Meta:
        verbose_name = _("Ollama Model")
        verbose_name_plural = _("Ollama Models")
        ordering = ['-is_default', '-is_active', 'display_name']
    
    def __str__(self):
        return f"{self.display_name} ({'active' if self.is_active else 'inactive'})"
    
    def save(self, *args, **kwargs):
        # Ensure only one default model
        if self.is_default:
            OllamaModel.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

class ResponseFeedback(models.Model):
    """Model to store user feedback on responses."""
    FEEDBACK_TYPES = (
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    )
    
    message_id = models.CharField(max_length=100)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    message_content = models.TextField()
    message_source = models.CharField(max_length=20, default='unknown')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Response Feedback'
        verbose_name_plural = 'Response Feedback'
    
    def __str__(self):
        return f"{self.feedback_type} feedback on {self.message_id}"