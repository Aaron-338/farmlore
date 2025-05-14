import requests
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
import time
import re
from core.data_structures import ConcurrentCache
from datetime import datetime, timedelta
import threading
import os
import pickle
import random
from pathlib import Path

# Import prompt template system
from .prompt_templates import PromptType, format_prompt, detect_prompt_type
# Import response processor
from .response_processor import process_response
# Import performance monitoring
from api.monitoring import record_llm_performance

logger = logging.getLogger(__name__)

# Define path to modelfiles directory
MODELFILES_DIR = os.path.join(os.path.dirname(__file__), "modelfiles")

# Import OllamaModel only when needed to avoid circular imports
def get_default_model():
    """Get the default Ollama model from the database."""
    try:
        from api.models import OllamaModel
        default_model = OllamaModel.objects.filter(is_default=True, is_active=True).first()
        if default_model:
            return default_model.name, default_model.default_temperature, default_model.default_max_tokens
        
        # If no default, try to get any active model
        active_model = OllamaModel.objects.filter(is_active=True).first()
        if active_model:
            return active_model.name, active_model.default_temperature, active_model.default_max_tokens
    except Exception as e:
        logger.warning(f"Error getting default model from database: {str(e)}")
    
    # Default fallback values
    return "gemma:2b", 0.7, 500

def get_model_settings(model_name):
    """Get settings for a specific model from the database."""
    try:
        from api.models import OllamaModel
        model = OllamaModel.objects.filter(name=model_name, is_active=True).first()
        if model:
            # Update last_used timestamp
            model.last_used = datetime.now()
            model.save(update_fields=['last_used'])
            return model.default_temperature, model.default_max_tokens
    except Exception as e:
        logger.warning(f"Error getting model settings from database: {str(e)}")
    
    # Default fallback values
    return 0.7, 500

def get_available_model_names():
    """Get all available model names from the database."""
    try:
        from api.models import OllamaModel
        return list(OllamaModel.objects.filter(is_active=True).values_list('name', flat=True))
    except Exception as e:
        logger.warning(f"Error getting available models from database: {str(e)}")
    
    # Default fallback
    return ["gemma:2b"]

class CircuitBreaker:
    """
    Implements the circuit breaker pattern to prevent cascading failures.
    
    States:
    - CLOSED: Normal operation, requests flow through
    - OPEN: Failing state, requests are immediately rejected
    - HALF_OPEN: Testing state, allowing a limited number of requests through
    """
    
    # Circuit states
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    HALF_OPEN = 'HALF_OPEN'
    
    def __init__(self, failure_threshold=5, recovery_timeout=180, half_open_max_calls=5):
        """
        Initialize the circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening the circuit
            recovery_timeout: Seconds to wait before transitioning to half-open
            half_open_max_calls: Maximum test calls in half-open state
        """
        self.state = self.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # Increased from 60s to 180s
        self.last_failure_time = None
        self.half_open_calls = 0
        self.half_open_max_calls = half_open_max_calls  # Increased from 3 to 5
        self.lock = threading.RLock()
        
    def can_execute(self) -> bool:
        """Check if a request can be executed based on circuit state."""
        with self.lock:
            if self.state == self.CLOSED:
                return True
                
            if self.state == self.OPEN:
                # Check if recovery timeout has elapsed
                if (self.last_failure_time and 
                    datetime.now() > self.last_failure_time + timedelta(seconds=self.recovery_timeout)):
                    logger.info("Circuit transitioning from OPEN to HALF_OPEN after recovery timeout")
                    self.state = self.HALF_OPEN
                    self.half_open_calls = 0
                    return True
                return False
                
            if self.state == self.HALF_OPEN:
                # Allow limited test requests in half-open state
                if self.half_open_calls < self.half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False
                
            return False
    
    def on_success(self):
        """Handle a successful operation."""
        with self.lock:
            if self.state == self.HALF_OPEN:
                logger.info("Circuit transitioning from HALF_OPEN to CLOSED after successful test calls")
                self.state = self.CLOSED
                
            self.failure_count = 0
    
    def on_failure(self):
        """Handle a failed operation."""
        with self.lock:
            self.last_failure_time = datetime.now()
            
            if self.state == self.HALF_OPEN:
                logger.warning("Circuit transitioning from HALF_OPEN to OPEN after test call failure")
                self.state = self.OPEN
                return
                
            if self.state == self.CLOSED:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    logger.warning(f"Circuit OPENING after {self.failure_count} consecutive failures")
                    self.state = self.OPEN
    
    def get_state(self) -> str:
        """Get the current circuit state."""
        with self.lock:
            return self.state


class OllamaHandler:
    """Handler for interacting with Ollama API with robust error handling."""
    
    def __init__(self, base_url="http://localhost:11434", default_model_name="nous-hermes2", request_timeout=120, max_retries=2, initial_backoff=5, use_disk_cache=True, disk_cache_dir=".ollama_cache", semantic_cache_threshold=0.85):
        """
        Initialize the Ollama handler with enhanced error handling.
        
        Args:
            base_url: Base URL for the Ollama API (default: from OLLAMA_BASE_URL env var or "http://localhost:11434")
            timeout: Request timeout in seconds (increased from 60s to 180s)
            retry_attempts: Number of retry attempts for transient failures (increased from 3 to 5)
            retry_delay: Delay between retries in seconds (increased from 2s to 3s)
        """
        self.base_url = base_url.rstrip('/')
        self.default_model_name = default_model_name  # Store default_model_name
        self.ollama_model = os.environ.get('OLLAMA_MODEL', default_model_name)  # Get model from env or use default
        self.request_timeout = request_timeout
        
        # Try multiple potential Ollama hosts if primary fails
        self.fallback_urls = [
            "http://localhost:11434",
            "http://ollama:11434",
            "http://host.docker.internal:11434",  # For Docker on Windows/Mac
            "http://172.17.0.1:11434"  # Common Docker bridge network
        ]
        
        # Set API endpoints
        self.api_generate = f"{self.base_url}/api/generate"
        self.api_chat = f"{self.base_url}/api/chat"
        self.api_tags = f"{self.base_url}/api/tags"
        self.api_create = f"{self.base_url}/api/create"
        
        self.timeout = request_timeout
        self.retry_attempts = max_retries
        self.retry_delay = initial_backoff
        
        # Create a session object for connection pooling
        self.session = requests.Session()
        
        # Initialize circuit breakers for different operations
        self.generate_circuit = CircuitBreaker()
        self.availability_circuit = CircuitBreaker()
        
        # Add model registry for specialized models
        self.specialized_models = {
            'pest_identification': 'farmlore-pest-id',
            'pest_management': 'farmlore-pest-mgmt',
            'indigenous_knowledge': 'farmlore-indigenous',
            'crop_pests': 'farmlore-crop-pests',
            'general_query': 'farmlore-general'
        }
        
        # Map modelfile paths to model names
        self.modelfile_paths = {
            'farmlore-pest-id': os.path.join(MODELFILES_DIR, 'pest_identification.modelfile'),
            'farmlore-pest-mgmt': os.path.join(MODELFILES_DIR, 'pest_management.modelfile'),
            'farmlore-indigenous': os.path.join(MODELFILES_DIR, 'indigenous_knowledge.modelfile'),
            'farmlore-crop-pests': os.path.join(MODELFILES_DIR, 'crop_pests.modelfile'),
            'farmlore-general': os.path.join(MODELFILES_DIR, 'general_query.modelfile')
        }
        self.chat_circuit = CircuitBreaker()
        self.tags_circuit = CircuitBreaker()
        
        # Initialize cache settings
        self.cache_ttl = int(os.environ.get('OLLAMA_CACHE_TTL', 3600 * 24)) # Default 24 hours
        self.max_semantic_cache_size = int(os.environ.get('OLLAMA_MAX_SEMANTIC_CACHE', 200))
        
        # Initialize cache storage and stats
        self.response_cache = ConcurrentCache(max_size=500) # For exact matches
        self.semantic_cache = [] # Initialize as empty list for semantic matches
        self.cache_hits = 0
        self.semantic_cache_hits = 0
        self.cache_misses = 0
        
        self.is_available = False
        self._model_info = None
        self.last_success_time = None # Track last successful operation
        
        # Thread-safe flag to track initialization status
        self._initialization_complete = threading.Event()
        self._initialization_success = False
        
        # Load cache from disk if available
        self._load_disk_cache()
        
        # Start background thread for cache maintenance
        self._start_cache_maintenance()
        
        # Start non-blocking initialization
        self._initialize_non_blocking()
        
    def _initialize_non_blocking(self):
        """
        Initialize the Ollama handler in a background thread without blocking the application startup.
        This allows the web server to start while Ollama availability check runs in background.
        """
        def initialization_worker():
            try:
                logger.info(f"Starting non-blocking initialization of Ollama handler with endpoint: {self.base_url}")
                # Check availability, this might take time but won't block startup
                self.is_available = self._check_availability()
                if self.is_available:
                    logger.info("Ollama is available and will be used for response generation.")
                    # Sync models with database in background
                    self.sync_models_with_db()
                    # Initialize specialized models
                    self._initialize_specialized_models()
                else:
                    logger.warning("Ollama is not available. Using Prolog-based fallback.")
                
                self._initialization_success = self.is_available
            except Exception as e:
                logger.error(f"Error during non-blocking Ollama initialization: {str(e)}")
                self.is_available = False
                self._initialization_success = False
            finally:
                # Signal that initialization is complete
                self._initialization_complete.set()
        
        # Start initialization in a background thread
        init_thread = threading.Thread(target=initialization_worker, daemon=True)
        init_thread.start()
        
    def _initialize_specialized_models(self):
        """
        Create specialized models using Modelfiles if they don't exist
        """
        try:
            # Get list of existing models
            existing_models_at_start = self._get_available_models()
            logger.info(f"OllamaHandler: Initializing specialized models. Existing models: {existing_models_at_start}")
            
            all_specialized_models_ready = True # Track overall success

            # Initialize each specialized model if needed
            for model_name, modelfile_path in self.modelfile_paths.items():
                # model_name is like 'farmlore-pest-id'
                # existing_models_at_start contains entries like 'farmlore-pest-id:latest'
                model_exists_as_is = model_name in existing_models_at_start
                model_exists_with_latest_tag = f"{model_name}:latest" in existing_models_at_start

                if not model_exists_as_is and not model_exists_with_latest_tag:
                    logger.info(f"OllamaHandler: Specialized model {model_name} does not appear to exist. Attempting to create from {modelfile_path}")
                    # _create_model_from_file now handles streaming and returns True only on definitive success from stream
                    creation_stream_successful = self._create_model_from_file(model_name, modelfile_path)
                    
                    if creation_stream_successful:
                        logger.info(f"OllamaHandler: Streamed creation for {model_name} reported success. Verifying presence in /api/tags...")
                        
                        # Poll /api/tags to confirm model availability after successful stream creation
                        verified_in_tags = False
                        for attempt in range(6): # Poll for up to 60 seconds (6 attempts * 10s delay)
                            time.sleep(10) 
                            current_models_after_creation = self._get_available_models()
                            if model_name in current_models_after_creation:
                                logger.info(f"OllamaHandler: Specialized model {model_name} CONFIRMED in /api/tags (attempt {attempt + 1}).")
                                verified_in_tags = True
                                break
                            else:
                                logger.info(f"OllamaHandler: Specialized model {model_name} not yet in /api/tags (attempt {attempt + 1}). Checking again soon. Models: {current_models_after_creation}")
                        
                        if not verified_in_tags:
                            logger.warning(f"OllamaHandler: Specialized model {model_name} was reported as successfully created by stream, BUT NOT found in /api/tags after polling for 60s. This may indicate an issue.")
                            all_specialized_models_ready = False # Mark as not fully ready if not in tags
                        # If verified_in_tags is true, it remains ready, no change to all_specialized_models_ready needed here unless it was already false

                    else:
                        logger.warning(f"OllamaHandler: Streamed creation for specialized model {model_name} FAILED or did not report success.")
                        all_specialized_models_ready = False # Mark as not ready if stream creation failed
                else:
                    # logger.info(f"OllamaHandler: Specialized model already exists: {model_name} (found as '{model_name if model_exists_as_is else f"{model_name}:latest"}'). Skipping creation.")
                    found_as_str = model_name if model_exists_as_is else model_name + ":latest"
                    logger.info(f"OllamaHandler: Specialized model already exists: {model_name} (found as '{found_as_str}'). Skipping creation.")
            
            if all_specialized_models_ready:
                logger.info("OllamaHandler: All specialized models appear ready (either pre-existing or created and verified).")
            else:
                logger.warning("OllamaHandler: Not all specialized models are confirmed ready after creation and verification attempts.")
                # self._initialization_success could be set to False here if all specialized models are strictly required.
                # For now, allow the main _initialization_success to be True if the base Ollama is responsive,
                # even if some specialized models failed. The system can fall back to the default model.

            logger.info("OllamaHandler: Specialized models initialization process complete.")
        except Exception as e:
            logger.error(f"Error initializing specialized models: {str(e)}")
            # self._initialization_success = False # Consider this if errors here are critical
            
    def _get_available_models(self):
        """
        Get list of available models from Ollama
        """
        try:
            response = self.session.get(self.api_tags, timeout=self.timeout)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            logger.warning(f"Failed to get available models: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []
            
    def _create_model_from_file(self, model_name, modelfile_path):
        """
        Create a model from a Modelfile
        """
        try:
            # Check if modelfile exists
            if not os.path.exists(modelfile_path):
                logger.error(f"Modelfile not found: {modelfile_path}")
                return False
                
            # Read the Modelfile content with explicit UTF-8 encoding
            with open(modelfile_path, 'r', encoding='utf-8') as f:
                lines = f.readlines() # New: read all lines
            
            # Log original length (less relevant now, but harmless)
            # logger.info(f"OllamaHandler: Modelfile {model_name} raw length: {len(modelfile_content_raw)}") # Original content_raw not defined here

            # New: Process lines to remove BOM and strip individual lines, then rejoin
            if lines and lines[0].startswith('\ufeff'):
                lines[0] = lines[0][1:] # Remove BOM from first line
            
            # Strip whitespace from each line and filter out empty lines that are NOT part of a multi-line directive
            processed_lines = [line.strip() for line in lines if line.strip()] # Keep this simple for now
            modelfile_content = "\n".join(processed_lines)
            
            # Targeted fix for 'SYSTEM """..."""' or "SYSTEM '''...'''" issue
            # This function will be defined and used locally or inline.
            # It looks for a SYSTEM directive followed by triple quotes on its own line (after stripping),
            # captures the content between them, and removes the triple quotes.
            def replace_system_quotes(content):
                # Simpler, more direct replacement for opening quotes
                content = content.replace('SYSTEM """', 'SYSTEM')
                content = content.replace("SYSTEM '''", 'SYSTEM')
                
                # Simpler, more direct replacement for closing quotes
                # Assuming the system prompt is the last part of the modelfile content or followed by newlines
                if content.endswith('"""'):
                    content = content[:-3]
                elif content.endswith("'''"):
                    content = content[:-3]
                
                # Remove any leading/trailing whitespace that might have been left from replacements
                # and ensure SYSTEM keyword is followed by a newline if content was just "SYSTEM"
                # Split into lines, process SYSTEM line, then rejoin
                lines = content.split('\n')
                processed_lines = []
                system_keyword_found = False
                for i, line in enumerate(lines):
                    stripped_line = line.strip()
                    if stripped_line == "SYSTEM":
                        processed_lines.append("SYSTEM") # Just the keyword
                        system_keyword_found = True
                    elif system_keyword_found and stripped_line == "" and بعدی_line_is_not_directive (lines, i+1):
                        # If we had SYSTEM, then an empty line from quote removal, and next is not a directive, skip this empty line.
                        # This avoids an extra blank line between SYSTEM and its content if quotes were on their own lines.
                        pass # Skip adding this effectively empty line
                    else:
                        processed_lines.append(line) # Keep other lines as they are (stripped or original based on previous logic)
                        if system_keyword_found and stripped_line != "": # Content for system prompt started
                            system_keyword_found = False # Reset flag after first content line of system prompt
                
                content = "\n".join(processed_lines).strip() # Strip leading/trailing whitespace from the whole content again
                return content
            
            # Helper for replace_system_quotes logic
            def بعدی_line_is_not_directive(all_lines, index):
                if index >= len(all_lines):
                    return True # No next line, so not a directive
                next_line_stripped = all_lines[index].strip()
                known_directives = ["FROM", "PARAMETER", "TEMPLATE", "SYSTEM", "LICENSE", "MIROSTAT", "MIROSTAT_ETA", "MIROSTAT_TAU", "NUM_CTX", "NUM_GQA", "NUM_GPU", "NUM_THREAD", "REPEAT_LAST_N", "REPEAT_PENALTY", "SEED", "STOP", "TEMPERATURE", "TOP_K", "TOP_P", "USER", "ASSISTANT"]
                for directive in known_directives:
                    if next_line_stripped.startswith(directive):
                        return False
                return True

            modelfile_content = replace_system_quotes(modelfile_content)

            logger.info(f"OllamaHandler: Modelfile {model_name} length after line-by-line processing and quote cleaning: {len(modelfile_content)}")
            logger.info(f"OllamaHandler: Modelfile content type for {model_name}: {type(modelfile_content)}")

            # Diagnostic: Log ord() of first few characters
            if modelfile_content:
                logger.info(f"OllamaHandler: ord() of first 20 chars of modelfile_content for {model_name}: {[ord(c) for c in modelfile_content[:20]]}")
                # Also log if it starts with FROM, as a sanity check string comparison
                if modelfile_content.startswith("FROM"):
                    logger.info(f"OllamaHandler: modelfile_content for {model_name} DOES start with 'FROM'.")
                else:
                    logger.warning(f"OllamaHandler: modelfile_content for {model_name} DOES NOT start with 'FROM'. First 20 chars: {modelfile_content[:20]}")
            else:
                logger.warning(f"OllamaHandler: modelfile_content for {model_name} is empty before payload creation.")

            # Log the exact Modelfile content being sent, its type, and final length
            logger.info(f"OllamaHandler: Modelfile content for {model_name} being sent (normalized):\n{modelfile_content[:500]}... (showing first 500 chars)")

            # Create the model
            create_payload = {
                'name': model_name,
                'modelfile': modelfile_content,
                'stream': True  # Enable streaming
            }
            
            # Log the full payload before sending
            try:
                # Attempt to log a JSON representation for readability, but handle if it's not serializable for some reason
                payload_log_str = json.dumps(create_payload, indent=2)
                if len(payload_log_str) > 1000: # Avoid excessively long logs for the Modelfile part
                    payload_log_str = json.dumps({'name': create_payload['name'], 'modelfile': create_payload['modelfile'][:200] + '...', 'stream': create_payload['stream']}, indent=2)
            except Exception:
                payload_log_str = str(create_payload) # Fallback to string representation
            logger.info(f"OllamaHandler: Full create_payload for {model_name}:\\n{payload_log_str}")
            
            logger.info(f"Creating model {model_name} with Modelfile from {modelfile_path} (streaming)")
            
            # Use a longer timeout for model creation, and stream the response
            response = self.session.post(
                self.api_create, 
                json=create_payload,
                timeout=1800,  # 30 minutes, as model creation can be very long
                stream=True      # Ensure requests library streams the response body
            )
            
            # Check initial response status code
            if response.status_code != 200:
                logger.error(f"Failed to initiate model creation for {model_name}: {response.status_code} - {response.text}")
                return False

            # Process the streaming response
            creation_successful = False
            for line in response.iter_lines():
                if line:
                    try:
                        status_obj = json.loads(line.decode('utf-8'))
                        status_message_raw = status_obj.get("status") # Get raw status
                        
                        # Log the raw status for better debugging
                        logger.info(f"Model creation status for {model_name} (raw): {status_message_raw}")

                        # Log the error field if present in the status object
                        if "error" in status_obj:
                            logger.error(f"Ollama model creation error details for {model_name}: {status_obj.get('error')}")

                        if isinstance(status_message_raw, str):
                            status_message_str = status_message_raw
                            # Check for various success messages that might indicate completion
                            if "success" in status_message_str.lower() and len(status_obj) == 1: # Specifically {"status": "success"}
                                logger.info(f"Model creation for {model_name} reported final success via string status.")
                                creation_successful = True
                                break # Success confirmed by a simple "success" status message
                            elif "verifying sha256 digest" in status_message_str.lower():
                                logger.info(f"Model {model_name}: Verification of sha256 digest in progress...")
                                # This is an intermediate step, continue processing
                            elif "writing manifest" in status_message_str.lower():
                                logger.info(f"Model {model_name}: Writing manifest...")
                                # This is an intermediate step, continue processing
                            elif "removing" in status_message_str.lower() and "temp" in status_message_str.lower():
                                logger.info(f"Model {model_name}: Cleaning up temporary files...")
                                # This is an intermediate step, continue processing
                            # Add other known intermediate string statuses if necessary
                            
                            # If it's a string but not a known success or intermediate message, log it but don't assume error yet
                            # unless it's the only thing we get and it doesn't look like progress.
                            # The loop will continue, and `creation_successful` remains False unless explicitly set.

                        elif isinstance(status_message_raw, int): # Typically error codes from Ollama like 400, 500
                            logger.error(f"Model creation for {model_name} received integer status: {status_message_raw}. Treating as error.")
                            creation_successful = False
                            break # Stop processing stream on integer status code
                        
                        elif status_obj.get("digest") and status_obj.get("total") and status_obj.get("completed"):
                            # This is a progress object, e.g. {"status":"pulling manifest","digest":"sha256:...", "total":12345, "completed":1234}
                            # For creation, this might be less common than for pulling, but good to log progress
                            progress = (status_obj.get("completed", 0) / status_obj.get("total", 1)) * 100
                            logger.info(f"Model creation progress for {model_name}: {status_message_raw} - {progress:.2f}%")
                            # Check if "completed" equals "total" as a success condition
                            if status_obj.get("completed") == status_obj.get("total") and status_obj.get("total", 0) > 0:
                                logger.info(f"Model creation for {model_name} implied success from progress data (completed == total).")
                                # Sometimes the final "status":"success" is missing, this can be a backup
                                # However, rely on explicit success or wait for stream end if this is not the final message.
                                # For now, we don't set creation_successful = True solely based on this,
                                # to avoid premature success declaration if more critical messages follow.


                        else: # Not a string, not an int, not a known progress object - unexpected format
                            logger.warning(f"Model creation for {model_name} returned unknown status format: {status_message_raw}. Full object: {status_obj}")
                            # If not already marked successful by a previous message, keep creation_successful as False or let it be set by later messages.
                            # No break here, to allow processing further messages if any.

                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to decode JSON from model creation stream for {model_name}: {line.decode('utf-8')}, Error: {e}")
                        # Continue to next line if possible, or break if this indicates a fatal stream error
                        # For now, we continue, but this could be a point of failure.
                    except Exception as e:
                        logger.error(f"Error processing model creation stream for {model_name}: {e}")
                        creation_successful = False # Unhandled error during stream processing
                        break
            
            # After the loop, check the final status
            if creation_successful:
                logger.info(f"OllamaHandler: Successfully created specialized model: {model_name}")
            else:
                logger.error(f"Model creation stream for {model_name} did not end with a recognized success status or encountered an error.")

            return creation_successful
                
        except requests.exceptions.RequestException as e: # More specific exception for network/request issues
            logger.error(f"RequestException creating model {model_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Generic error creating model {model_name}: {str(e)}")
            return False
        
    def wait_for_initialization(self, timeout=None):
        """
        Wait for the initialization to complete.
        
        Args:
            timeout: Maximum time to wait in seconds, or None to wait indefinitely
            
        Returns:
            bool: True if initialization completed successfully, False otherwise
        """
        # Wait for the initialization event
        initialized = self._initialization_complete.wait(timeout=timeout)
        if not initialized:
            logger.warning(f"Timed out waiting for Ollama initialization after {timeout} seconds")
            return False
        
        return self._initialization_success

    def _load_disk_cache(self):
        """Load cached responses from disk."""
        try:
            # Load main cache
            cache_file = os.path.join(os.path.dirname(__file__), "cache", "response_cache.pkl")
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    disk_cache = pickle.load(f)
                    
                    # Check TTL for each entry
                    now = datetime.now()
                    valid_entries = {}
                    for key, (value, timestamp) in disk_cache.items():
                        if now - timestamp < timedelta(seconds=self.cache_ttl):
                            valid_entries[key] = value
                            
                    # Add valid entries to cache
                    for key, value in valid_entries.items():
                        self.response_cache.put(key, (value, datetime.now()))
                        
                logger.info(f"Loaded {len(valid_entries)} entries from disk cache (out of {len(disk_cache)} total)")
            
            # Load semantic cache
            semantic_cache_file = os.path.join(os.path.dirname(__file__), "cache", "semantic_cache.pkl")
            if os.path.exists(semantic_cache_file):
                with open(semantic_cache_file, 'rb') as f:
                    self.semantic_cache = pickle.load(f)
                    
                # Filter entries by TTL
                now = datetime.now()
                self.semantic_cache = [
                    (query, response, timestamp) 
                    for query, response, timestamp in self.semantic_cache
                    if now - timestamp < timedelta(seconds=self.cache_ttl)
                ]
                    
                logger.info(f"Loaded {len(self.semantic_cache)} entries from semantic cache")
                
        except Exception as e:
            logger.error(f"Error loading disk cache: {str(e)}")
            
    def _save_disk_cache(self):
        """Save cached responses to disk."""
        try:
            # Save main cache
            cache_file = os.path.join(os.path.dirname(__file__), "cache", "response_cache.pkl")
            with open(cache_file, 'wb') as f:
                pickle.dump(dict(self.response_cache.cache), f)
                
            # Save semantic cache
            semantic_cache_file = os.path.join(os.path.dirname(__file__), "cache", "semantic_cache.pkl")
            with open(semantic_cache_file, 'wb') as f:
                pickle.dump(self.semantic_cache, f)
                
            logger.info(f"Saved {len(self.response_cache.cache)} entries to disk cache and {len(self.semantic_cache)} to semantic cache")
        except Exception as e:
            logger.error(f"Error saving disk cache: {str(e)}")
            
    def _start_cache_maintenance(self):
        """Start a background thread for cache maintenance."""
        def maintenance_worker():
            while True:
                try:
                    # Sleep for 30 minutes
                    time.sleep(30 * 60)
                    
                    # Clean up expired entries
                    self._cleanup_expired_cache()
                    
                    # Save cache to disk
                    self._save_disk_cache()
                    
                    # Log cache statistics
                    total_requests = self.cache_hits + self.cache_misses
                    hit_rate = (self.cache_hits + self.semantic_cache_hits) / total_requests if total_requests > 0 else 0
                    
                    logger.info(f"Cache statistics - Hits: {self.cache_hits}, Semantic hits: {self.semantic_cache_hits}, "
                               f"Misses: {self.cache_misses}, Hit rate: {hit_rate:.2%}")
                    
                except Exception as e:
                    logger.error(f"Error in cache maintenance: {str(e)}")
        
        # Start the maintenance thread
        maintenance_thread = threading.Thread(target=maintenance_worker, daemon=True)
        maintenance_thread.start()
        
    def _cleanup_expired_cache(self):
        """Remove expired entries from caches."""
        try:
            # Clean main cache
            now = datetime.now()
            expired_keys = []
            
            for key, (_, timestamp) in self.response_cache.cache.items():
                if now - timestamp > timedelta(seconds=self.cache_ttl):
                    expired_keys.append(key)
                    
            for key in expired_keys:
                self.response_cache.cache.pop(key, None)
                
            # Clean semantic cache
            self.semantic_cache = [
                (query, response, timestamp) 
                for query, response, timestamp in self.semantic_cache
                if now - timestamp < timedelta(seconds=self.cache_ttl)
            ]
            
            # Trim semantic cache if it's too large
            if len(self.semantic_cache) > self.max_semantic_cache_size:
                # Sort by timestamp (newest first) and keep only max size
                self.semantic_cache.sort(key=lambda x: x[2], reverse=True)
                self.semantic_cache = self.semantic_cache[:self.max_semantic_cache_size]
                
            logger.info(f"Cleaned {len(expired_keys)} expired entries from main cache and maintained semantic cache size at {len(self.semantic_cache)}")
            
        except Exception as e:
            logger.error(f"Error cleaning expired cache: {str(e)}")
            
    def _find_semantic_match(self, query, threshold=0.85):
        """
        Find semantically similar queries in the cache.
        
        Args:
            query: The query to match
            threshold: Similarity threshold (0-1)
            
        Returns:
            Cached response if a match is found, None otherwise
        """
        if not self.semantic_cache:
            return None
            
        # Simple word overlap similarity for now
        # In a production system, you would use embeddings or more sophisticated similarity measures
        def jaccard_similarity(query1, query2):
            # Convert to sets of words
            set1 = set(query1.lower().split())
            set2 = set(query2.lower().split())
            
            # Calculate Jaccard similarity
            intersection = len(set1.intersection(set2))
            union = len(set1) + len(set2) - intersection
            
            return intersection / union if union > 0 else 0
        
        # Find best match
        best_match = None
        best_score = 0
        
        for cached_query, response, timestamp in self.semantic_cache:
            score = jaccard_similarity(query, cached_query)
            
            if score > threshold and score > best_score:
                best_score = score
                best_match = (response, score, timestamp)
                
        if best_match:
            response, score, _ = best_match
            logger.info(f"Semantic cache hit with score {score:.2f} for query: {query}")
            self.semantic_cache_hits += 1
            return response
            
        return None

    def _retry_operation(self, operation, *args, **kwargs) -> Tuple[bool, Any]:
        """
        Retry an operation with exponential backoff.
        
        Args:
            operation: Function to retry
            *args, **kwargs: Arguments to pass to the operation
            
        Returns:
            Tuple[bool, Any]: (success, result)
        """
        attempt = 0
        last_error = None
        
        while attempt < self.retry_attempts:
            try:
                result = operation(*args, **kwargs)
                return True, result
            except Exception as e:
                attempt += 1
                last_error = e
                
                if attempt < self.retry_attempts:
                    # Calculate backoff time with jitter
                    backoff = self.retry_delay * (2 ** (attempt - 1))
                    jitter = backoff * 0.1 * (time.time() % 1)  # 10% jitter
                    sleep_time = backoff + jitter
                    
                    logger.warning(f"Retry attempt {attempt}/{self.retry_attempts} after error: {str(e)}. "
                                  f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"All {self.retry_attempts} retry attempts failed: {str(e)}")
        
        return False, last_error
    
    def _check_availability(self) -> bool:
        """
        Check if Ollama is available and fully operational with circuit breaker protection.
        
        Returns:
            bool: True if Ollama is available, False otherwise
        """
        # Skip check if circuit is open
        if not self.availability_circuit.can_execute():
            logger.warning("Skipping availability check: availability_circuit is OPEN")
            return False
            
        try:
            # Step 1: Check basic connectivity with retry
            def get_tags():
                return self.session.get(self.api_tags, timeout=5)
                
            success, response = self._retry_operation(get_tags)
            
            if not success:
                logger.warning(f"Failed to connect to Ollama (tags endpoint) after {self.retry_attempts} attempts")
                self.availability_circuit.on_failure()
                return False
                
            if response.status_code != 200:
                logger.warning(f"Ollama (tags endpoint) returned non-200 status: {response.status_code}")
                self.availability_circuit.on_failure()
                return False
            
            # Step 2: Try to get the list of models
            try:
                tags_data = response.json()
                logger.info(f"Ollama model tags: {tags_data}")
                
                # Ensure there's at least one model available
                if "models" not in tags_data or not tags_data["models"]:
                    logger.warning("No models available in Ollama")
                    self.availability_circuit.on_failure()
                    return False
                    
            except json.JSONDecodeError:
                logger.warning("Failed to parse Ollama tags response as JSON")
                self.availability_circuit.on_failure()
                return False
            
            # Step 3: Test minimal generation with the first available model
            first_model = tags_data["models"][0]["model"]
            logger.info(f"Testing Ollama with model: {first_model}")
            
            test_payload = {
                "model": first_model,
                "prompt": "test",
                "stream": False
            }
            
            def test_generate():
                logger.info(f"Testing Ollama API with endpoint: {self.api_generate}")
                logger.info(f"This may take up to 120 seconds for the first inference...")
                return self.session.post(
                    self.api_generate,
                    json=test_payload, 
                    timeout=180  # Increased timeout for first inference from 60s to 180s
                )
            
            # Execute with retry
            success, test_response = self._retry_operation(test_generate)
            
            if not success:
                logger.warning("Generate test failed after retries")
                self.availability_circuit.on_failure()
                return False
                
            logger.info(f"Ollama API test response status: {test_response.status_code}")
            
            if test_response.status_code == 404:
                # Log error details
                logger.warning(f"API endpoint not found. Response: {test_response.text}")
                self.availability_circuit.on_failure()
                return False
            
            if test_response.status_code != 200:
                logger.warning(f"Ollama API test failed with status: {test_response.status_code}")
                self.availability_circuit.on_failure()
                return False
                
            # Try to parse the response as JSON
            try:
                test_result = test_response.json()
                logger.info(f"Ollama API test response: {json.dumps(test_result)[:100]}...")
                
                if "response" not in test_result:
                    logger.warning("Ollama API test returned unexpected response format")
                    self.availability_circuit.on_failure()
                    return False
                    
                # All checks passed, mark as success
                self.availability_circuit.on_success()
                return True
                
            except json.JSONDecodeError:
                logger.warning("Failed to parse Ollama test response as JSON")
                self.availability_circuit.on_failure()
                return False
                
        except Exception as e:
            logger.warning(f"Ollama availability check failed: {str(e)}")
            self.availability_circuit.on_failure()
            return False
    
    def generate_response_with_specialized_model(self, prompt: str, query_type: str = "general_query", model_name: Optional[str] = None, temperature: Optional[float] = None, max_tokens: Optional[int] = None, stream: bool = False) -> Optional[str]:
        """Generates a response using a specialized model if available, otherwise falls back to the default model."""
        # Use the provided model_name, or the specialized model for the query_type, or the handler's default model
        target_model_name = model_name or self.specialized_models.get(query_type, self.default_model_name)

        if not target_model_name:
            logger.error("[OLLAMA_HANDLER] No target model could be determined (specialized or default). Cannot generate response.")
            return None

        logger.info(f"[OLLAMA_HANDLER] Using model '{target_model_name}' for query_type '{query_type}' (specialized lookup: {self.specialized_models.get(query_type)}, explicit model_name: {model_name})")
        
        # Generate response using the selected model
        return self.generate_response(prompt=prompt, model=target_model_name, temperature=temperature, max_tokens=max_tokens)
    
    def _validate_and_clean_response(self, response_text, query=None):
        """
        Clean and validate the response from Ollama API.
        
        Args:
            response_text (str): The raw response text from Ollama API
            query (str, optional): Original query for context-aware processing
            
        Returns:
            str: Cleaned and validated response text
        """
        if not response_text or not isinstance(response_text, str):
            logger.warning(f"Invalid response type: {type(response_text)}")
            return ""
        
        # Use the response processor if a query is provided
        if query:
            try:
                return process_response(response_text, query)
            except Exception as e:
                logger.error(f"Error in response processor: {str(e)}")
                # Fall back to basic cleaning if processing fails
        
        # Basic cleaning (simplified version of what's in response_processor)
        cleaned = re.sub(r'```[a-zA-Z]*\n|```', '', response_text)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = cleaned.strip()
        
        # Check if the response is too short or meaningless
        if len(cleaned) < 5 or cleaned.lower() in ["i don't know", "unknown", "error"]:
            logger.warning(f"Response too short or meaningless: '{cleaned}'")
            return ""
        
        return cleaned
        
    def _generate_fallback_response(self, prompt):
        """Generate a fallback response when Ollama is unavailable."""
        logger.info("Generating fallback response")
        
        # Enhanced fallback responses for agricultural queries
        if any(term in prompt.lower() for term in ["pest", "insect", "bug"]):
            return "I'm currently unable to provide specific pest information. Common approaches include identifying the pest through visual inspection, researching organic control methods, and considering both cultural practices and natural predators for sustainable management."
        
        if any(term in prompt.lower() for term in ["soil", "fertilizer", "nutrient"]):
            return "I'm currently unable to provide detailed soil information. Consider testing your soil pH and nutrient levels, using compost to improve soil structure, and choosing plants suited to your local soil conditions."
            
        if any(term in prompt.lower() for term in ["crop", "plant", "grow"]):
            return "I'm currently unable to provide specific crop information. Key factors for successful cultivation include choosing varieties adapted to your local climate, ensuring proper spacing, regular watering, and monitoring for pests and diseases."
        
        # General fallback
        return "I apologize, but I'm experiencing technical difficulties. Please try again later, or contact support if the problem persists."
        
    def refresh_availability(self) -> bool:
        """
        Refresh the availability status of Ollama.
        
        Returns:
            bool: True if Ollama is now available, False otherwise
        """
        # Only refresh if enough time has passed since last check
        last_check_threshold = datetime.now() - timedelta(minutes=5)
        if self.last_success_time and self.last_success_time > last_check_threshold:
            logger.debug("Skipping availability refresh: recent successful operation")
            return self.is_available
            
        self.is_available = self._check_availability()
        if self.is_available:
            logger.info("Ollama is now available")
            self.last_success_time = datetime.now()
        else:
            logger.warning("Ollama is still unavailable")
            
        return self.is_available
    
    def sync_models_with_db(self):
        """Sync available Ollama models with the database."""
        try:
            # Get models from Ollama API
            ollama_models = self.get_available_models()
            if not ollama_models:
                logger.warning("No models available from Ollama API")
                return
                
            # Update or create models in database
            from api.models import OllamaModel
            
            for model_name in ollama_models:
                # Skip if model name is too long (shouldn't happen, but just in case)
                if len(model_name) > 100:
                    continue
                    
                # Check if model exists
                db_model, created = OllamaModel.objects.get_or_create(
                    name=model_name,
                    defaults={
                        'display_name': model_name.title().replace('-', ' '),
                        'is_active': True,
                        'is_default': False,
                        'description': f"Ollama model: {model_name}"
                    }
                )
                
                if created:
                    logger.info(f"Added new Ollama model to database: {model_name}")
                    
                    # If this is the first model, make it default
                    if OllamaModel.objects.count() == 1:
                        db_model.is_default = True
                        db_model.save(update_fields=['is_default'])
                        logger.info(f"Set {model_name} as default model")
                
            logger.info(f"Successfully synced {len(ollama_models)} models with database")
            
        except Exception as e:
            logger.error(f"Error syncing models with database: {str(e)}")
    
    @record_llm_performance
    def generate_response(self, prompt, model=None, temperature=None, max_tokens=None, 
                         prompt_type: Optional[Union[PromptType, str]] = None, **prompt_vars):
        """
        Generate a response using the Ollama API with circuit breaker protection.
        
        Args:
            prompt: The user's input prompt
            model: LLM model to use (if None, uses default from database)
            temperature: Controls randomness (0-1) (if None, uses default from model settings)
            max_tokens: Maximum tokens in response (if None, uses default from model settings)
            prompt_type: Type of prompt to use (if None, auto-detected)
            **prompt_vars: Additional variables for the prompt template
            
        Returns:
            str: Generated response or fallback message
        """
        # Get model and default parameters from database if not provided
        if model is None:
            model, default_temp, default_max = get_default_model()
            temperature = default_temp if temperature is None else temperature
            max_tokens = default_max if max_tokens is None else max_tokens
        else:
            # If model is provided but not other parameters, get defaults for that model
            if temperature is None or max_tokens is None:
                model_temp, model_max = get_model_settings(model)
                temperature = model_temp if temperature is None else temperature
                max_tokens = model_max if max_tokens is None else max_tokens
        
        # Process prompt using templates if appropriate
        final_prompt = prompt
        system_prompt = None
        
        try:
            # Convert string prompt_type to enum if needed
            if isinstance(prompt_type, str):
                try:
                    prompt_type = PromptType(prompt_type)
                except ValueError:
                    prompt_type = None
                    
            # Auto-detect prompt type if not specified
            if prompt_type is None:
                prompt_type = detect_prompt_type(prompt)
                
            # Include the original query in prompt_vars
            prompt_vars['query'] = prompt
            
            # Format the prompt using the template
            formatted = format_prompt(prompt_type, **prompt_vars)
            system_prompt = formatted['system_prompt']
            final_prompt = formatted['user_prompt']
            
            logger.info(f"Using prompt template: {prompt_type.value}")
            
        except Exception as e:
            logger.warning(f"Error using prompt template: {str(e)}. Using original prompt.")
            # Continue with original prompt if template processing fails
                
        # Create a cache key based on the prompt and parameters
        cache_key = f"{final_prompt}_{model}_{temperature}_{max_tokens}"
        if system_prompt:
            cache_key = f"{system_prompt}_{cache_key}"
        
        # Check if we have a cached response with exact match
        cached_data = self.response_cache.get(cache_key)
        if cached_data is not None:
            cached_response, _ = cached_data  # Unpack value and timestamp
            logger.info("Cache hit: Using cached LLM response")
            self.cache_hits += 1
            return cached_response
        
        # Try semantic matching if exact match fails
        semantic_response = self._find_semantic_match(prompt)
        if semantic_response is not None:
            logger.info("Semantic cache hit: Using semantically similar cached response")
            return semantic_response
            
        # Log cache miss
        self.cache_misses += 1
        
        # Always keep fallback ready in case of any issues
        fallback_response = self._generate_fallback_response(prompt)
        
        # Check if service is available, try to refresh if not
        if not self.is_available:
            self.refresh_availability()
            
        if not self.is_available:
            logger.info("Ollama not available, using fallback response")
            return fallback_response
            
        # Check circuit breaker before making request
        if not self.generate_circuit.can_execute():
            logger.warning(f"Circuit OPEN. Generate request rejected. Circuit state: {self.generate_circuit.get_state()}")
            return fallback_response
        
        try:
            logger.info(f"Sending request to Ollama API with model {model}")
            
            # Prepare the payload
            payload = {
                "model": model,
                "prompt": final_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            # Add system prompt if available
            if system_prompt:
                payload["system"] = system_prompt
            
            # Log the request
            logger.debug(f"Request payload: {json.dumps({k: v for k, v in payload.items() if k != 'system'})}")
            
            # Define the API request function for retry mechanism
            def make_api_request():
                return self.session.post(
                    self.api_generate, 
                    json=payload, 
                    timeout=180  # Increased from default timeout to 180s for handling large responses
                )
                
            # Execute with retry mechanism
            start_time = time.time()
            success, response = self._retry_operation(make_api_request)
            response_time = time.time() - start_time
            
            if not success:
                logger.error("All retry attempts failed for generate request")
                self.generate_circuit.on_failure()
                return fallback_response
                
            logger.info(f"Ollama response received in {response_time:.2f} seconds")
            logger.debug(f"Response status: {response.status_code}")
            
            # Check status code before proceeding
            if response.status_code != 200:
                logger.error(f"Ollama returned non-200 status: {response.status_code}")
                self.generate_circuit.on_failure()
                return fallback_response
            
            try:
                # Try to parse as JSON
                result = response.json()
                logger.debug(f"Parsed JSON response with keys: {', '.join(result.keys())}")
                
                if "response" in result:
                    raw_response = result["response"]
                    # Validate and clean the response, passing the original query
                    cleaned_response = self._validate_and_clean_response(raw_response, prompt)
                    
                    # Only cache if we got a valid response
                    if cleaned_response and len(cleaned_response) > 10:
                        # Add to exact match cache with timestamp
                        self.response_cache.put(cache_key, (cleaned_response, datetime.now()))
                        
                        # Save cache to disk periodically
                        if random.random() < 0.05:  # 5% chance to save on each successful request
                            self._save_disk_cache()
                        
                        # Register success with circuit breaker
                        self.generate_circuit.on_success()
                        self.last_success_time = datetime.now()
                        
                        # Update model usage in the database
                        try:
                            from api.models import OllamaModel
                            OllamaModel.objects.filter(name=model).update(last_used=datetime.now())
                        except Exception as e:
                            logger.warning(f"Could not update model usage: {str(e)}")
                            
                        return cleaned_response
                    else:
                        logger.warning("Ollama returned empty or invalid response")
                        self.generate_circuit.on_failure()
                        return fallback_response
                else:
                    logger.warning("No 'response' field in Ollama API response")
                    self.generate_circuit.on_failure()
                    return fallback_response
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing Ollama response as JSON: {str(e)}")
                self.generate_circuit.on_failure()
                return fallback_response
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while waiting for Ollama response (timeout={self.timeout}s)")
            self.generate_circuit.on_failure()
            return fallback_response
            
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            self.generate_circuit.on_failure()
            return fallback_response

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Ollama.
        
        Returns:
            List[str]: List of model names, or empty list if unavailable
        """
        if not self.tags_circuit.can_execute():
            logger.warning("Circuit OPEN. Tags request rejected.")
            return []
            
        try:
            success, response = self._retry_operation(
                lambda: self.session.get(self.api_tags, timeout=10)
            )
            
            if not success or response.status_code != 200:
                self.tags_circuit.on_failure()
                return []
                
            data = response.json()
            self.tags_circuit.on_success()
            
            if "models" in data and isinstance(data["models"], list):
                return [model["model"] for model in data["models"]]
            return []
            
        except Exception as e:
            logger.error(f"Error getting models from Ollama: {str(e)}")
            self.tags_circuit.on_failure()
            return []
            
    @record_llm_performance
    def generate_response_with_specialized_model(self, prompt, query_type):
        """
        Generate a response using the appropriate specialized model for the query type
        
        Args:
            prompt: The prompt to send to the model
            query_type: The type of query (pest_identification, pest_management, etc.)
            
        Returns:
            The generated response text or None if an error occurred
        """
        # Select the appropriate model based on query type
        default_model = self.ollama_model if hasattr(self, 'ollama_model') else self.default_model_name
        model = self.specialized_models.get(query_type, default_model)
        
        logger.info(f"[OLLAMA_HANDLER] Using model '{model}' for query_type '{query_type}' (specialized lookup: {self.specialized_models.get(query_type, 'not found')}, explicit model_name: None)")
        
        # Generate response using the selected model
        return self.generate_response(prompt=prompt, model=model)
        
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the Ollama service.
        
        Returns:
            Dict[str, Any]: Health status information
        """
        is_available = self.refresh_availability()
        models = self.get_available_models() if is_available else []
        
        return {
            "status": "available" if is_available else "unavailable",
            "base_url": self.base_url,
            "models": models,
            "tags_circuit": self.tags_circuit.get_state(),
            "generate_circuit": self.generate_circuit.get_state(),
            "availability_circuit": self.availability_circuit.get_state(),
            "last_success": self.last_success_time.isoformat() if self.last_success_time else None,
        } 