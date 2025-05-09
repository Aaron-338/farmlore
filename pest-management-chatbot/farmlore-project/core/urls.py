from django.urls import path, include
from django.views.generic import RedirectView
from . import views

app_name = 'core'  # Add app_name for namespace

urlpatterns = [
    path('api/', include('api.urls')),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('chat/', RedirectView.as_view(url='/chatbot/chat/', permanent=True), name='chat'),  # Redirect to chatbot app
    
    # No API endpoints here - they should be in api/urls.py
]
