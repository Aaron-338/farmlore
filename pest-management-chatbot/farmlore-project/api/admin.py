from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import OllamaModel, Dataset, TrainedModel, ResponseFeedback
from django.urls import reverse
from django.utils.html import format_html

admin.site.site_header = _("Pest Management Chatbot Administration")
admin.site.site_title = _("Pest Management Chatbot")
admin.site.index_title = _("Dashboard")

class MyAdminSite(admin.AdminSite):
    """Custom admin site with additional links"""
    
    def get_app_list(self, request):
        """Add custom links to the admin index"""
        app_list = super().get_app_list(request)
        
        # Add performance dashboard link
        # custom_app = {
        #     'name': _('Performance Monitoring'),
        #     'app_label': 'performance',
        #     'models': [{
        #         'name': _('Performance Dashboard'),
        #         'object_name': 'performance_dashboard',
        #         'admin_url': reverse('performance-dashboard'),
        #         'view_only': True,
        #     }]
        # }
        # app_list.append(custom_app)
        
        return app_list

# Replace the default admin site
admin.site = MyAdminSite(name='myadmin')
admin.sites.site = admin.site

@admin.register(OllamaModel)
class OllamaModelAdmin(admin.ModelAdmin):
    """Admin interface for managing Ollama models."""
    
    list_display = ('display_name', 'name', 'is_active', 'is_default', 'default_temperature', 'default_max_tokens')
    list_filter = ('is_active', 'is_default', 'supports_chat', 'supports_function_calling', 'supports_vision')
    search_fields = ('name', 'display_name', 'description')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'display_name', 'description')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_default')
        }),
        (_('Parameters'), {
            'fields': ('default_temperature', 'default_max_tokens')
        }),
        (_('Capabilities'), {
            'fields': ('supports_chat', 'supports_function_calling', 'supports_vision'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_added', 'last_used')
    
    actions = ['make_active', 'make_inactive', 'set_as_default']
    
    def make_active(self, request, queryset):
        """Mark selected models as active."""
        queryset.update(is_active=True)
    make_active.short_description = _("Mark selected models as active")
    
    def make_inactive(self, request, queryset):
        """Mark selected models as inactive."""
        queryset.update(is_active=False)
    make_inactive.short_description = _("Mark selected models as inactive")
    
    def set_as_default(self, request, queryset):
        """Set the selected model as the default."""
        if queryset.count() != 1:
            self.message_user(request, _("Please select exactly one model to set as default."), level='error')
            return
        
        # First, clear all existing defaults
        OllamaModel.objects.all().update(is_default=False)
        
        # Set the selected model as default and ensure it's active
        model = queryset.first()
        model.is_default = True
        model.is_active = True
        model.save()
        
        self.message_user(request, _(f"{model.display_name} has been set as the default model."))
    set_as_default.short_description = _("Set as default model")

# Register other models
admin.site.register(Dataset)
admin.site.register(TrainedModel)

@admin.register(ResponseFeedback)
class ResponseFeedbackAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'feedback_type', 'message_source', 'user', 'created_at')
    list_filter = ('feedback_type', 'message_source', 'created_at')
    search_fields = ('message_id', 'message_content', 'user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('message_id', 'feedback_type', 'message_source', 'user')
        }),
        ('Content', {
            'fields': ('message_content',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
