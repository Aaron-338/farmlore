"""
Compatibility layer for the monitoring system.
This module provides compatibility with older monitoring code.
"""
import time
import logging
from .model_performance import monitor as performance_monitor, record_model_response

logger = logging.getLogger(__name__)

class ModelPerformanceTracker:
    """
    Compatibility class for the model_health.py file.
    This class provides the same interface as the original ModelPerformanceTracker class.
    """
    
    def __init__(self):
        self.model_performance_monitor = performance_monitor
    
    def get_all_model_stats(self):
        """
        Get statistics for all models grouped by query type.
        
        Returns:
            Dictionary of model statistics by query type
        """
        try:
            # Get model stats from the performance monitor
            model_stats = self.model_performance_monitor.get_model_stats()
            query_type_stats = self.model_performance_monitor.get_query_type_stats()
            
            # Convert to the expected format
            result = {}
            for model_name, stats in model_stats.items():
                # Extract query type from model name (e.g., farmlore-pest-id -> pest_identification)
                query_type = None
                if model_name.startswith('farmlore-'):
                    model_suffix = model_name.replace('farmlore-', '')
                    if model_suffix == 'pest-id':
                        query_type = 'pest_identification'
                    elif model_suffix == 'pest-mgmt':
                        query_type = 'pest_management'
                    elif model_suffix == 'indigenous':
                        query_type = 'indigenous_knowledge'
                    elif model_suffix == 'crop-pests':
                        query_type = 'crop_pests'
                    elif model_suffix == 'general':
                        query_type = 'general_query'
                    else:
                        query_type = model_suffix
                else:
                    query_type = 'unknown'
                
                result[query_type] = {
                    'response_time': stats.get('response_time', {'avg': 0, 'min': 0, 'max': 0, 'count': 0}),
                    'success_rate': stats.get('success_rate', {'rate': 0, 'success_count': 0, 'failure_count': 0, 'total': 0}),
                    'usage_count': stats.get('usage_frequency', 0),
                    'token_usage': stats.get('token_usage', {'avg_input': 0, 'avg_output': 0, 'avg_total': 0, 'count': 0})
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting all model stats: {str(e)}")
            return {}


class MonitorCompatibilityWrapper:
    """
    Wrapper class to provide backward compatibility with the old monitoring interface.
    """
    def __init__(self, model_performance_monitor):
        self.model_performance_monitor = model_performance_monitor
        self.start_time = time.time()
        
        # Initialize metrics structure expected by admin_views
        self.metrics = {
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
    
    def get_metrics(self):
        """
        Get metrics in the format expected by the admin dashboard.
        """
        # Get the latest stats from the performance monitor
        model_stats = self.model_performance_monitor.get_model_stats()
        query_stats = self.model_performance_monitor.get_query_type_stats()
        
        # Update our compatibility metrics structure
        for model_name, stats in model_stats.items():
            if 'response_time' in stats:
                rt = stats['response_time']
                self.metrics['response_times']['avg'] = rt.get('avg', 0)
                self.metrics['response_times']['min'] = rt.get('min', 0)
                self.metrics['response_times']['max'] = rt.get('max', 0)
                self.metrics['response_times']['samples'] = rt.get('count', 0)
            
            if 'success_rate' in stats:
                sr = stats['success_rate']
                self.metrics['queries']['success'] += sr.get('success_count', 0)
                self.metrics['queries']['fail'] += sr.get('failure_count', 0)
                self.metrics['queries']['total'] += sr.get('total', 0)
                
                # Track LLM calls
                self.metrics['llm']['calls'] += sr.get('total', 0)
                self.metrics['llm']['failures'] += sr.get('failure_count', 0)
                
                if 'response_time' in stats:
                    rt = stats['response_time']
                    self.metrics['llm']['avg_response_time'] = rt.get('avg', 0)
                    self.metrics['llm']['total_time'] = rt.get('avg', 0) * rt.get('count', 0)
        
        # Update query type stats
        for query_type, count in query_stats.items():
            self.metrics['queries']['by_type'][query_type] = count
        
        return self.metrics

# Create a compatibility wrapper around the performance monitor
monitor = MonitorCompatibilityWrapper(performance_monitor)


def record_query_performance(func_or_query_type=None, response_time=None, success=True, source="hybrid"):
    """
    Record query performance metrics.
    This is a compatibility function that maps to the new model_performance tracking system.
    
    Can be used as a decorator or as a direct function call:
    
    As decorator:
    @record_query_performance
    def query(self, query_type, params=None):
        ...
        
    As function:
    record_query_performance(query_type, response_time, success, source)
    """
    # Check if being used as a decorator
    if callable(func_or_query_type) and response_time is None:
        # This is being used as a decorator
        func = func_or_query_type
        
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                
                # Try to extract query_type from function call
                query_type = "unknown"
                
                # Check if query_type is in the arguments
                if len(args) > 1:
                    query_type = args[1]  # Assuming the query_type is the 2nd argument
                elif 'query_type' in kwargs:
                    query_type = kwargs['query_type']
                
                # Record performance
                try:
                    model_name = f"farmlore-{source}"
                    record_model_response(model_name, query_type, elapsed_time, 0, 0, True)
                    logger.debug(f"Recorded query performance for {query_type} from {source}: {elapsed_time:.2f}s")
                except Exception as e:
                    logger.error(f"Error recording query performance in decorator: {str(e)}")
                
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                try:
                    model_name = f"farmlore-{source}"
                    record_model_response(model_name, "unknown", elapsed_time, 0, 0, False)
                except Exception as log_error:
                    logger.error(f"Error recording query failure: {str(log_error)}")
                raise e
        
        return wrapper
    else:
        # This is being used as a direct function call
        try:
            query_type = func_or_query_type if func_or_query_type else "unknown"
            model_name = f"farmlore-{source}"
            record_model_response(model_name, query_type, response_time or 0, 0, 0, success)
            if response_time:
                logger.debug(f"Recorded query performance for {query_type} from {source}: {response_time:.2f}s, success={success}")
        except Exception as e:
            logger.error(f"Error recording query performance: {str(e)}")


def record_llm_performance(func_or_model_name=None, query_type=None, response_time=None, tokens_in=0, tokens_out=0, success=True):
    """
    Record LLM performance metrics.
    This is a compatibility function that maps to the new model_performance.record_model_response function.
    
    Can be used as a decorator or as a direct function call:
    
    As decorator:
    @record_llm_performance
    def generate_response(self, prompt, query_type):
        ...
        
    As function:
    record_llm_performance(model_name, query_type, response_time, tokens_in, tokens_out, success)
    """
    # Check if being used as a decorator
    if callable(func_or_model_name) and query_type is None and response_time is None:
        # This is being used as a decorator
        func = func_or_model_name
        
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                
                # Try to extract model_name and query_type from function call
                model_name = "unknown"
                query_type = "unknown"
                
                # args[0] is typically 'self' for methods
                if len(args) > 0 and hasattr(args[0], 'ollama_model'):
                    model_name = args[0].ollama_model
                
                # Check if query_type is in the arguments
                if len(args) > 2:
                    query_type = args[2]  # Assuming the query_type is the 3rd argument
                elif 'query_type' in kwargs:
                    query_type = kwargs['query_type']
                
                # Record performance
                try:
                    record_model_response(model_name, query_type, elapsed_time, 0, 0, True)
                    logger.debug(f"Recorded LLM performance for {model_name}: {elapsed_time:.2f}s")
                except Exception as e:
                    logger.error(f"Error recording LLM performance in decorator: {str(e)}")
                
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                try:
                    record_model_response("unknown", "unknown", elapsed_time, 0, 0, False)
                except Exception as log_error:
                    logger.error(f"Error recording LLM failure: {str(log_error)}")
                raise e
        
        return wrapper
    else:
        # This is being used as a direct function call
        try:
            model_name = func_or_model_name if func_or_model_name else "unknown"
            record_model_response(model_name, query_type or "unknown", response_time or 0, tokens_in, tokens_out, success)
            if response_time:
                logger.debug(f"Recorded LLM performance for {model_name}: {response_time:.2f}s, success={success}")
        except Exception as e:
            logger.error(f"Error recording LLM performance: {str(e)}")

