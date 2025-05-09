"""
Custom login views for the FarmLore platform.

These views extend Django's built-in authentication views to implement
user group routing after login.
"""
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

class FarmLoreLoginView(LoginView):
    """
    Custom login view that redirects users to different pages based on their role.
    """
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        """
        Determine where to redirect the user after successful login.
        """
        # Get the next parameter if it exists
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
            
        # Otherwise, redirect based on user role and preferences
        if hasattr(self.request.user, 'profile'):
            redirect_path = self.request.user.profile.redirect_path
            if redirect_path == 'community:dashboard':
                return reverse_lazy('community:dashboard')
            else:
                return reverse_lazy('chatbot:index')
                
        # Default fallback
        return reverse_lazy('home')
