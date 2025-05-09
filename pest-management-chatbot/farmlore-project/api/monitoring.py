"""
Monitoring system for tracking performance and usage metrics.
"""
import time
import logging
import threading
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """
    Monitor and log performance metrics for the hybrid engine and its components.
    
    This class tracks:
    - Response times
    - Success/failure rates
    - Cache hit rates
    - LLM usage
    - Popular query types
    - System load
    """
    def __init__(self, log_interval: int = 3600):
        """
        Initialize the performance monitor.
        
        Args:
            log_interval: How often to log stats (in seconds)
        """
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
        
        self.log_interval = log_interval
        self.start_time = time.time()
        self.last_log_time = self.start_time
        
        # Start background logging thread
        self.lock = threading.RLock()
        self.running = True
        self.log_thread = threading.Thread(target=self._periodic_logging, daemon=True)
        self.log_thread.start()
        
        # Set up log file
        self.log_dir = "debug_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        logger.info(f"Performance monitoring initialized. Logging to {self.log_file} every {log_interval} seconds")
    
    def _periodic_logging(self):
        """Background thread for periodic logging of metrics"""
        while self.running:
            time.sleep(10)  # Check every 10 seconds
            
            current_time = time.time()
            if current_time - self.last_log_time >= self.log_interval:
                self.log_metrics()
                self.last_log_time = current_time
    
    def record_query(self, query_type: str, success: bool, response_time: float, source: str):
        """
        Record metrics for a query.
        
        Args:
            query_type: Type of query processed
            success: Whether the query was successfully processed
            response_time: Time taken to process the query in seconds
            source: Source of the response (e.g., "ollama", "prolog", "hybrid")
        """
        with self.lock:
            # Update query counts
            self.metrics["queries"]["total"] += 1
            if success:
                self.metrics["queries"]["success"] += 1
            else:
                self.metrics["queries"]["fail"] += 1
            
            # Update by query type
            if query_type not in self.metrics["queries"]["by_type"]:
                self.metrics["queries"]["by_type"][query_type] = 0
            self.metrics["queries"]["by_type"][query_type] += 1
            
            # Update by source
            if source not in self.metrics["queries"]["by_source"]:
                self.metrics["queries"]["by_source"][source] = 0
            self.metrics["queries"]["by_source"][source] += 1
            
            # Update response time metrics
            self.metrics["response_times"]["samples"] += 1
            self.metrics["response_times"]["sum"] += response_time
            self.metrics["response_times"]["avg"] = self.metrics["response_times"]["sum"] / self.metrics["response_times"]["samples"]
            self.metrics["response_times"]["min"] = min(self.metrics["response_times"]["min"], response_time)
            self.metrics["response_times"]["max"] = max(self.metrics["response_times"]["max"], response_time)
    
    def record_cache_event(self, hit: bool):
        """Record a cache hit or miss"""
        with self.lock:
            if hit:
                self.metrics["cache"]["hits"] += 1
            else:
                self.metrics["cache"]["misses"] += 1
    
    def record_llm_call(self, success: bool, response_time: float):
        """Record metrics for an LLM call"""
        with self.lock:
            self.metrics["llm"]["calls"] += 1
            if not success:
                self.metrics["llm"]["failures"] += 1
            
            # Update LLM response time metrics
            self.metrics["llm"]["total_time"] += response_time
            self.metrics["llm"]["avg_response_time"] = self.metrics["llm"]["total_time"] / self.metrics["llm"]["calls"]
    
    def record_prolog_call(self, success: bool):
        """Record metrics for a Prolog engine call"""
        with self.lock:
            self.metrics["prolog"]["calls"] += 1
            if not success:
                self.metrics["prolog"]["failures"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get the current metrics"""
        with self.lock:
            uptime = time.time() - self.start_time
            
            # Calculate derived metrics
            metrics_copy = self._deep_copy_metrics()
            
            # Add calculated metrics
            metrics_copy["uptime_seconds"] = uptime
            metrics_copy["uptime_formatted"] = self._format_duration(uptime)
            
            if metrics_copy["queries"]["total"] > 0:
                metrics_copy["queries"]["success_rate"] = metrics_copy["queries"]["success"] / metrics_copy["queries"]["total"]
            else:
                metrics_copy["queries"]["success_rate"] = 0
                
            cache_total = metrics_copy["cache"]["hits"] + metrics_copy["cache"]["misses"]
            if cache_total > 0:
                metrics_copy["cache"]["hit_rate"] = metrics_copy["cache"]["hits"] / cache_total
            else:
                metrics_copy["cache"]["hit_rate"] = 0
                
            if metrics_copy["llm"]["calls"] > 0:
                metrics_copy["llm"]["success_rate"] = 1 - (metrics_copy["llm"]["failures"] / metrics_copy["llm"]["calls"])
            else:
                metrics_copy["llm"]["success_rate"] = 0
                
            if metrics_copy["prolog"]["calls"] > 0:
                metrics_copy["prolog"]["success_rate"] = 1 - (metrics_copy["prolog"]["failures"] / metrics_copy["prolog"]["calls"])
            else:
                metrics_copy["prolog"]["success_rate"] = 0
                
            # Get queries per minute
            metrics_copy["queries_per_minute"] = metrics_copy["queries"]["total"] / (uptime / 60) if uptime > 0 else 0
            
            return metrics_copy
    
    def log_metrics(self):
        """Log the current metrics to file and reset certain counters"""
        try:
            metrics = self.get_metrics()
            
            # Log to console
            logger.info("======== Performance Metrics ========")
            logger.info(f"Uptime: {metrics['uptime_formatted']}")
            logger.info(f"Queries: {metrics['queries']['total']} (Success rate: {metrics['queries']['success_rate']:.2%})")
            logger.info(f"Avg response time: {metrics['response_times']['avg']:.4f}s")
            logger.info(f"Cache hit rate: {metrics['cache']['hit_rate']:.2%}")
            logger.info(f"Response sources: {metrics['queries']['by_source']}")
            logger.info("===================================")
            
            # Write to JSON file
            try:
                with open(self.log_file, 'a') as f:
                    timestamp = datetime.now().isoformat()
                    log_entry = {"timestamp": timestamp, "metrics": metrics}
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as e:
                logger.error(f"Error writing metrics to log file: {str(e)}")
        except Exception as e:
            logger.error(f"Error logging metrics: {str(e)}")
    
    def _deep_copy_metrics(self) -> Dict[str, Any]:
        """Create a deep copy of the metrics"""
        with self.lock:
            return json.loads(json.dumps(self.metrics))
    
    def _format_duration(self, seconds: float) -> str:
        """Format a duration in seconds as a human-readable string"""
        td = timedelta(seconds=seconds)
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")
            
        return " ".join(parts)
    
    def shutdown(self):
        """Shutdown the performance monitor"""
        self.running = False
        if self.log_thread.is_alive():
            self.log_thread.join(timeout=1.0)
        self.log_metrics()  # Final log before shutting down
        logger.info("Performance monitoring shutdown")

# Global instance of the performance monitor
monitor = PerformanceMonitor(log_interval=1800)  # Log every 30 minutes

def record_query_performance(func):
    """
    Decorator to monitor query performance.
    
    Usage:
        @record_query_performance
        def query(self, query_type, params=None):
            ...
    """
    def wrapper(self, query_type, params=None):
        start_time = time.time()
        success = True
        source = "unknown"
        
        try:
            result = func(self, query_type, params)
            source = result.get("source", "unknown")
            return result
        except Exception as e:
            success = False
            raise e
        finally:
            response_time = time.time() - start_time
            monitor.record_query(query_type, success, response_time, source)
    
    return wrapper

def record_llm_performance(func):
    """
    Decorator to monitor LLM call performance.
    
    Usage:
        @record_llm_performance
        def generate_response(self, prompt, model=None, ...):
            ...
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise e
        finally:
            response_time = time.time() - start_time
            monitor.record_llm_call(success, response_time)
    
    return wrapper 