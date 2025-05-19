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
    path('rag-chat/', views.rag_chat, name='rag_chat'),
    
    # Add new API endpoints for the RAG interface
    path('system-status/', views.system_status, name='system_status'),
    path('rag-api/', views.rag_api, name='rag_api'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]