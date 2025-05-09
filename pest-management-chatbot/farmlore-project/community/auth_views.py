"""
Authentication views for the FarmLore community app.

These views handle user registration and profile management.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import UserProfile


class ExtendedUserCreationForm(UserCreationForm):
    """Extended user creation form with additional fields."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
        return user


def register_view(request):
    """View for user registration."""
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # The UserProfile with 'knowledge_seeker' role is automatically created
            # via the post_save signal in models.py
            
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created for {username}! You are now logged in.')
            
            # Direct new users to the chatbot by default, not the community dashboard
            return redirect('chatbot:index')
    else:
        form = ExtendedUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
