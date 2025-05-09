# chatbot/urls.py
from django.urls import path
from django.contrib import admin  # Add this import
from django.urls import include  # Add this import
from . import views

app_name = 'chatbot'  # Add app_name to create a namespace

urlpatterns = [
    # Keep your existing URL patterns
    path('', views.home, name='index'),  # Renamed to 'index' to match template references
    path('chat/', views.chat, name='chat'),
    path('about/', views.about, name='about'),
]