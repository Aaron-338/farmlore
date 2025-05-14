"""
Model performance monitoring for the FarmLore system.
This module tracks and analyzes the performance of specialized models.
"""
import os
import json
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class ModelPerformanceMonitor:
    """
    Monitor and analyze the performance of specialized models.
    
    This class tracks:
    - Response times
    - Token usage
    - Success rates
    - Usage frequency
    - User feedback
    """
    
    def __init__(self, log_dir: str = None):
        """
        Initialize the performance monitor.
        
        Args:
            log_dir: Directory to store performance logs
        """
        # Set log directory
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                  "logs", "model_performance")
        
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Initialize performance metrics
        self.metrics = {
            "response_times": defaultdict(list),
            "token_usage": defaultdict(list),
            "success_rates": defaultdict(lambda: {"success": 0, "failure": 0}),
            "usage_frequency": defaultdict(int),
            "user_feedback": defaultdict(lambda: {"positive": 0, "negative": 0, "neutral": 0})
        }
        
        # Initialize lock for thread safety
        self.lock = threading.RLock()
        
        # Start background thread for periodic logging
        self.should_run = True
        self.log_interval = int(os.environ.get('MODEL_PERFORMANCE_LOG_INTERVAL', 3600))  # Default: 1 hour
        self.log_thread = threading.Thread(target=self._periodic_logging, daemon=True)
        self.log_thread.start()
        
        logger.info(f"Model performance monitor initialized. Logging to {self.log_dir}")
    
    def record_response(self, model_name: str, query_type: str, response_time: float, 
                       tokens_in: int, tokens_out: int, success: bool):
        """
        Record a model response.
        
        Args:
            model_name: Name of the model used
            query_type: Type of query processed
            response_time: Time taken to generate the response in seconds
            tokens_in: Number of input tokens
            tokens_out: Number of output tokens
            success: Whether the response was successful
        """
        with self.lock:
            # Record response time
            self.metrics["response_times"][model_name].append(response_time)
            
            # Record token usage
            self.metrics["token_usage"][model_name].append({
                "input": tokens_in,
                "output": tokens_out,
                "total": tokens_in + tokens_out
            })
            
            # Record success/failure
            if success:
                self.metrics["success_rates"][model_name]["success"] += 1
            else:
                self.metrics["success_rates"][model_name]["failure"] += 1
            
            # Record usage frequency
            self.metrics["usage_frequency"][model_name] += 1
            
            # Also track by query type
            self.metrics["usage_frequency"][f"{query_type}"] += 1
    
    def record_feedback(self, model_name: str, feedback: str):
        """
        Record user feedback on a model response.
        
        Args:
            model_name: Name of the model used
            feedback: User feedback (positive, negative, neutral)
        """
        with self.lock:
            if feedback in ["positive", "negative", "neutral"]:
                self.metrics["user_feedback"][model_name][feedback] += 1
    
    def get_model_stats(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for a specific model or all models.
        
        Args:
            model_name: Name of the model to get stats for, or None for all models
            
        Returns:
            Dictionary of model statistics
        """
        with self.lock:
            if model_name:
                return self._calculate_stats_for_model(model_name)
            else:
                stats = {}
                # Get all unique model names across all metric categories
                model_names = set()
                for category in self.metrics.values():
                    model_names.update(category.keys())
                
                # Calculate stats for each model
                for name in model_names:
                    if name.startswith("farmlore-"):  # Only include our specialized models
                        stats[name] = self._calculate_stats_for_model(name)
                
                return stats
    
    def get_query_type_stats(self) -> Dict[str, Any]:
        """
        Get statistics by query type.
        
        Returns:
            Dictionary of query type statistics
        """
        with self.lock:
            stats = {}
            query_types = [
                "pest_identification",
                "pest_management",
                "indigenous_knowledge",
                "crop_pests",
                "general_query"
            ]
            
            for query_type in query_types:
                count = self.metrics["usage_frequency"].get(query_type, 0)
                stats[query_type] = {
                    "count": count,
                    "percentage": 0  # Will calculate below
                }
            
            # Calculate percentages
            total = sum(stats[qt]["count"] for qt in query_types)
            if total > 0:
                for query_type in query_types:
                    stats[query_type]["percentage"] = (stats[query_type]["count"] / total) * 100
            
            return stats
    
    def _calculate_stats_for_model(self, model_name: str) -> Dict[str, Any]:
        """
        Calculate statistics for a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary of model statistics
        """
        stats = {}
        
        # Response time stats
        response_times = self.metrics["response_times"].get(model_name, [])
        if response_times:
            stats["response_time"] = {
                "avg": sum(response_times) / len(response_times),
                "min": min(response_times),
                "max": max(response_times),
                "count": len(response_times)
            }
        
        # Token usage stats
        token_usage = self.metrics["token_usage"].get(model_name, [])
        if token_usage:
            stats["token_usage"] = {
                "avg_input": sum(item["input"] for item in token_usage) / len(token_usage),
                "avg_output": sum(item["output"] for item in token_usage) / len(token_usage),
                "avg_total": sum(item["total"] for item in token_usage) / len(token_usage),
                "count": len(token_usage)
            }
        
        # Success rate stats
        success_data = self.metrics["success_rates"].get(model_name, {"success": 0, "failure": 0})
        total_calls = success_data["success"] + success_data["failure"]
        if total_calls > 0:
            stats["success_rate"] = {
                "rate": (success_data["success"] / total_calls) * 100,
                "success_count": success_data["success"],
                "failure_count": success_data["failure"],
                "total": total_calls
            }
        
        # Usage frequency
        stats["usage_frequency"] = self.metrics["usage_frequency"].get(model_name, 0)
        
        # User feedback
        feedback_data = self.metrics["user_feedback"].get(model_name, {"positive": 0, "negative": 0, "neutral": 0})
        total_feedback = sum(feedback_data.values())
        if total_feedback > 0:
            stats["user_feedback"] = {
                "positive_rate": (feedback_data["positive"] / total_feedback) * 100,
                "negative_rate": (feedback_data["negative"] / total_feedback) * 100,
                "neutral_rate": (feedback_data["neutral"] / total_feedback) * 100,
                "total": total_feedback
            }
        
        return stats
    
    def save_metrics_to_file(self):
        """Save the current metrics to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.log_dir, f"model_performance_{timestamp}.json")
        
        with self.lock:
            # Convert defaultdicts to regular dicts for JSON serialization
            serializable_metrics = {}
            for category, data in self.metrics.items():
                serializable_metrics[category] = {}
                for key, value in data.items():
                    if isinstance(value, defaultdict):
                        serializable_metrics[category][key] = dict(value)
                    else:
                        serializable_metrics[category][key] = value
            
            try:
                with open(filename, 'w') as f:
                    json.dump(serializable_metrics, f, indent=2)
                logger.info(f"Saved model performance metrics to {filename}")
            except Exception as e:
                logger.error(f"Failed to save model performance metrics: {str(e)}")
    
    def _periodic_logging(self):
        """Periodically log metrics to file."""
        while self.should_run:
            time.sleep(self.log_interval)
            self.save_metrics_to_file()
    
    def shutdown(self):
        """Shutdown the monitor and save final metrics."""
        self.should_run = False
        self.save_metrics_to_file()
        logger.info("Model performance monitor shutdown")

# Initialize the global monitor instance
monitor = ModelPerformanceMonitor()

def record_model_response(model_name, query_type, response_time, tokens_in, tokens_out, success=True):
    """
    Record a model response in the global monitor.
    
    This function is designed to be used as a decorator or called directly.
    """
    monitor.record_response(model_name, query_type, response_time, tokens_in, tokens_out, success)

def record_model_feedback(model_name, feedback):
    """Record user feedback in the global monitor."""
    monitor.record_feedback(model_name, feedback)

def get_model_performance_stats(model_name=None):
    """Get model performance statistics from the global monitor."""
    return monitor.get_model_stats(model_name)

def get_query_type_stats():
    """Get query type statistics from the global monitor."""
    return monitor.get_query_type_stats()

def save_current_metrics():
    """Save the current metrics to a file."""
    monitor.save_metrics_to_file()
