"""
Monitoring package for the FarmLore system.
"""
from .model_performance import (
    record_model_response,
    record_model_feedback,
    get_model_performance_stats,
    get_query_type_stats,
    save_current_metrics
)

# Import the compatibility wrapper for the monitor
from .compatibility import monitor, record_llm_performance, record_query_performance, ModelPerformanceTracker

__all__ = [
    'record_model_response',
    'record_model_feedback',
    'get_model_performance_stats',
    'get_query_type_stats',
    'save_current_metrics',
    'monitor',
    'record_llm_performance',
    'record_query_performance',
    'ModelPerformanceTracker'
]
