from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DatasetViewSet
from . import admin_views

router = DefaultRouter()
router.register(r'datasets', views.DatasetViewSet)
router.register(r'models', views.TrainedModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', views.predict, name='predict'),
    path('available-values/', views.available_values, name='available-values'),
    path('search/pests/', views.search_pests, name='search-pests'),
    path('search/methods/', views.search_methods, name='search-methods'),
    path('search/soil/', views.search_soil, name='search-soil'),
    path('chat/', views.chat_api, name='chat-api'),
    path('feedback/', views.feedback_api, name='feedback-api'),
    
    # New hybrid engine endpoints
    path('hybrid/', views.HybridEngineView.as_view(), name='hybrid-engine'),
    path('hybrid/stats/', views.EngineStatsView.as_view(), name='engine-stats'),
    
    # Admin performance dashboard
    path('admin/performance/', admin_views.performance_dashboard, name='performance-dashboard'),
    path('admin/performance/json/', admin_views.performance_json, name='performance-json'),
    path('admin/performance/reset/', admin_views.reset_metrics, name='reset-metrics'),
]