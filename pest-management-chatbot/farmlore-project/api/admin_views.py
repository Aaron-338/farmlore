from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse

from api.monitoring import monitor
from api.inference_engine.hybrid_engine import HybridEngine
from datetime import datetime
import time

# Initialize a hybrid engine if needed for health checks
hybrid_engine = HybridEngine()

@staff_member_required
def performance_dashboard(request):
    """
    Admin view for displaying performance metrics dashboard
    """
    # Get metrics from the performance monitor
    metrics = monitor.get_metrics()
    
    # Check Ollama availability
    ollama_available = False
    ollama_models = []
    if hybrid_engine.use_ollama and hybrid_engine.ollama_handler:
        ollama_available = hybrid_engine.ollama_handler.is_available
        if ollama_available:
            ollama_models = hybrid_engine.ollama_handler.get_available_models()
    
    # Format start time
    start_time = datetime.fromtimestamp(monitor.start_time).strftime('%Y-%m-%d %H:%M:%S')
    
    return render(request, 'admin/performance_dashboard.html', {
        'title': 'Performance Dashboard',
        'metrics': metrics,
        'start_time': start_time,
        'ollama_available': ollama_available,
        'ollama_models': ollama_models,
        'current_time': now().strftime('%Y-%m-%d %H:%M:%S'),
    })

@staff_member_required
def performance_json(request):
    """
    API endpoint for getting performance metrics as JSON
    This can be used for real-time updates of the dashboard
    """
    metrics = monitor.get_metrics()
    return JsonResponse({
        'metrics': metrics,
        'timestamp': now().isoformat(),
    })

@staff_member_required
def reset_metrics(request):
    """
    Reset the performance metrics
    """
    if request.method == 'POST':
        monitor.metrics = {
            "queries": {
                "total": 0,
                "success": 0,
                "fail": 0,
                "by_type": {},
                "by_source": {}
            },
            "response_times": {
                "avg": 0,
                "min": float('inf'),
                "max": 0,
                "samples": 0,
                "sum": 0
            },
            "cache": {
                "hits": 0,
                "misses": 0
            },
            "llm": {
                "calls": 0,
                "failures": 0,
                "avg_response_time": 0,
                "total_time": 0
            },
            "prolog": {
                "calls": 0,
                "failures": 0
            }
        }
        monitor.start_time = time.time()
        return JsonResponse({'success': True, 'message': 'Metrics have been reset'})
    
    return JsonResponse({'success': False, 'message': 'This endpoint requires a POST request'}, status=405) 