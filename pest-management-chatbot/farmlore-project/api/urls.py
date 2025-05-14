from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import the views that we want to use for the API endpoints
from api.views import (
    predict, 
    available_values, 
    search_pests, 
    search_methods, 
    search_soil,
    chat_api,  # This is the one we modified
    feedback_api, 
    DatasetViewSet,
    TrainedModelViewSet, 
    HybridEngineView, 
    EngineStatsView,
    health_check, 
    model_health, 
    test_models, 
    debug_hybrid_engine, 
    test_endpoint
)

# For any viewsets (class-based views), we would register them with a router
router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'trained-models', TrainedModelViewSet, basename='trainedmodel')

# urlpatterns for function-based views and router-included viewsets
urlpatterns = [
    # Include URLs from the router
    path('', include(router.urls)),
    
    # Function-based views
    path('predict/', predict, name='predict'),
    path('available-values/', available_values, name='available-values'),
    path('search-pests/', search_pests, name='search-pests'),
    path('search-methods/', search_methods, name='search-methods'),
    path('search-soil/', search_soil, name='search-soil'),
    path('chat/', chat_api, name='chat-api'),  # Pointing to our modified chat_api
    path('feedback/', feedback_api, name='feedback-api'),
    path('health/', health_check, name='health-check'),
    path('model-health/', model_health, name='model-health'),
    path('test-models/', test_models, name='test-models'),
    path('debug-hybrid/', debug_hybrid_engine, name='debug-hybrid-engine'),
    path('test-endpoint/', test_endpoint, name='test-endpoint'), 
    
    # Class-based views (if not using a router for them explicitly)
    path('hybrid-engine/', HybridEngineView.as_view(), name='hybrid-engine'),
    path('engine-stats/', EngineStatsView.as_view(), name='engine-stats'),
] 