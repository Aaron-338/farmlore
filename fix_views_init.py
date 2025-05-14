#!/usr/bin/env python

# Create the content for api/views/__init__.py that will correctly import from parent api/views.py
init_content = """# Import everything from the parent views.py
from api.views import (
    predict, 
    available_values, 
    search_pests, 
    search_methods, 
    search_soil,
    chat_api, 
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
"""

# Write this to the file
with open("views_init_content.txt", "w") as f:
    f.write(init_content)

print("Created file with content to fix views/__init__.py") 