"""
URL configuration for the FarmLore community features.

This module defines the URL patterns for both API endpoints and web views
for the community interface.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .auth_views import register_view
from .views import (
    KnowledgeKeeperViewSet, IndigenousKnowledgeViewSet,
    RegionalObservationViewSet, CommunityValidationViewSet,
    SesothoTermViewSet
)

# Create a router for API views
router = DefaultRouter()
router.register(r'keepers', KnowledgeKeeperViewSet)
router.register(r'knowledge', IndigenousKnowledgeViewSet)
router.register(r'observations', RegionalObservationViewSet)
router.register(r'validations', CommunityValidationViewSet)
router.register(r'terms', SesothoTermViewSet)

# URL patterns for the community app
app_name = 'community'
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Web views
    path('', views.CommunityDashboardView.as_view(), name='dashboard'),
    path('knowledge/<int:pk>/', views.KnowledgeDetailView.as_view(), name='knowledge_detail'),
    path('knowledge/create/', views.KnowledgeCreateView.as_view(), name='knowledge_create'),
    path('knowledge/<int:knowledge_id>/validate/', views.ValidationCreateView.as_view(), name='validation_create'),
    path('observation/create/', views.ObservationCreateView.as_view(), name='observation_create'),
    path('export/', views.export_knowledge_view, name='export_knowledge'),
    path('register/', register_view, name='register'),
    path('debug/', views.debug_knowledge_view, name='debug_knowledge'),
    
    # Knowledge Keeper Application URLs
    path('apply/', views.apply_knowledge_keeper, name='apply_knowledge_keeper'),
    path('admin/applications/', views.admin_application_list, name='admin_application_list'),
    path('admin/applications/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
]
