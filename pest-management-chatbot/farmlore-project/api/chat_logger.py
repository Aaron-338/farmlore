"""
Chat processing logger to track messages through the system.

This module provides functions to log the progress of chat messages through
various components: API → Engine → (Ollama/Prolog)
"""
import time
import logging
import functools
import threading

# Create a dedicated logger for chat processing
logger = logging.getLogger('chat_processing')
logger.setLevel(logging.INFO)

# Chat tracking data - thread-local storage for tracking chat progress
_chat_data = threading.local()

def start_chat_tracking(message_id=None, query=None):
    """Start tracking a chat message through the system."""
    if not hasattr(_chat_data, 'tracking'):
        _chat_data.tracking = {}
    
    # Generate a message ID if none provided
    if message_id is None:
        message_id = f"msg_{int(time.time() * 1000)}"
    
    # Initialize tracking for this message
    _chat_data.tracking[message_id] = {
        'id': message_id,
        'query': query,
        'start_time': time.time(),
        'steps': []
    }
    
    # Log the start of processing
    logger.info(f"[CHAT:{message_id}] 🚀 STARTING CHAT PROCESSING: '{query}'")
    return message_id

def log_chat_step(message_id, step, details=None):
    """Log a step in the chat processing pipeline."""
    if not hasattr(_chat_data, 'tracking') or message_id not in _chat_data.tracking:
        # No tracking data, just log the message
        logger.info(f"[CHAT:{message_id}] {step}: {details}")
        return
    
    # Calculate elapsed time
    elapsed = time.time() - _chat_data.tracking[message_id]['start_time']
    
    # Add step to tracking data
    _chat_data.tracking[message_id]['steps'].append({
        'step': step,
        'details': details,
        'elapsed': elapsed
    })
    
    # Log the step with visual indicators
    indicator = get_step_indicator(step)
    logger.info(f"[CHAT:{message_id}] {indicator} {step} [{elapsed:.2f}s]: {details}")

def end_chat_tracking(message_id, response=None, source=None):
    """End tracking for a chat message."""
    if not hasattr(_chat_data, 'tracking') or message_id not in _chat_data.tracking:
        return
    
    # Calculate total processing time
    total_time = time.time() - _chat_data.tracking[message_id]['start_time']
    
    # Log completion
    logger.info(f"[CHAT:{message_id}] ✅ COMPLETED [{total_time:.2f}s] - Source: {source}")
    
    # Truncate response for logging
    if response and len(response) > 100:
        response_preview = response[:100] + "..."
    else:
        response_preview = response
    
    logger.info(f"[CHAT:{message_id}] 📝 RESPONSE: {response_preview}")
    
    # Clean up tracking data
    del _chat_data.tracking[message_id]
    
    return total_time

def get_step_indicator(step):
    """Get a visual indicator for the processing step."""
    step = step.lower()
    if 'api' in step:
        return "🔄 API"
    elif 'engine' in step:
        return "⚙️ ENGINE"
    elif 'ollama' in step:
        return "🤖 OLLAMA"
    elif 'prolog' in step:
        return "🧠 PROLOG"
    elif 'cache' in step:
        return "💾 CACHE"
    elif 'error' in step:
        return "❌ ERROR"
    else:
        return "➡️ STEP"

def track_function(step_name):
    """Decorator to track a function as a chat processing step."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to find message_id in args or kwargs
            message_id = kwargs.get('message_id', None)
            if message_id is None and args and hasattr(args[0], 'message_id'):
                message_id = args[0].message_id
            
            # Log step start
            if message_id:
                log_chat_step(message_id, f"{step_name} START")
            
            # Call the original function
            try:
                result = func(*args, **kwargs)
                
                # Log step completion
                if message_id:
                    log_chat_step(message_id, f"{step_name} COMPLETE")
                
                return result
            except Exception as e:
                # Log step error
                if message_id:
                    log_chat_step(message_id, f"{step_name} ERROR", str(e))
                raise
        return wrapper
    return decorator 