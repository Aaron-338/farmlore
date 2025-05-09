from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    KnowledgeKeeper, 
    IndigenousKnowledge, 
    CommunityValidation, 
    RegionalObservation, 
    UserProfile,
    KnowledgeKeeperApplication
)

# Register the UserProfile inline with the User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# Extend the User admin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_role')
    list_filter = UserAdmin.list_filter + ('profile__role',)
    
    def get_user_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else '-'
    
    get_user_role.short_description = 'Role'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Unregister the default User admin and register our custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # User model is not registered, so no need to unregister it
admin.site.register(User, CustomUserAdmin)

# Register other models
@admin.register(KnowledgeKeeper)
class KnowledgeKeeperAdmin(admin.ModelAdmin):
    list_display = ('user', 'village', 'district', 'years_experience')
    search_fields = ('user__username', 'user__email', 'village', 'district')
    list_filter = ('district',)

@admin.register(IndigenousKnowledge)
class IndigenousKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'keeper', 'practice_type', 'verification_status', 'date_added', 'is_exported')
    list_filter = ('practice_type', 'verification_status', 'is_exported')
    search_fields = ('title', 'description', 'keeper__user__username')
    readonly_fields = ('date_added', 'last_exported')

@admin.register(CommunityValidation)
class CommunityValidationAdmin(admin.ModelAdmin):
    list_display = ('knowledge', 'validator', 'rating', 'date_added')
    list_filter = ('rating',)
    search_fields = ('knowledge__title', 'validator__username')
    readonly_fields = ('date_added',)

@admin.register(RegionalObservation)
class RegionalObservationAdmin(admin.ModelAdmin):
    list_display = ('title', 'observer', 'observation_type', 'location', 'date_observed')
    list_filter = ('observation_type', 'location')
    search_fields = ('title', 'description', 'observer__username', 'location')
    readonly_fields = ('date_added', 'date_observed')

@admin.register(KnowledgeKeeperApplication)
class KnowledgeKeeperApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'village', 'district', 'status', 'created_at')
    list_filter = ('status', 'district')
    search_fields = ('user__username', 'user__email', 'village', 'district')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        for application in queryset.filter(status='pending'):
            application.approve(request.user)
        self.message_user(request, f"{queryset.filter(status='pending').count()} applications have been approved.")
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        for application in queryset.filter(status='pending'):
            application.reject(request.user)
        self.message_user(request, f"{queryset.filter(status='pending').count()} applications have been rejected.")
    reject_applications.short_description = "Reject selected applications"
