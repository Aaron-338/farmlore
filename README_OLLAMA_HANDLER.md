# OllamaHandler Implementation

This file contains the implementation of the `OllamaHandler` class which is responsible for interfacing between the pest management chatbot application and the Ollama LLM service.

## Overview

The `OllamaHandler` class provides a clean interface for sending prompts to the Ollama API and retrieving responses. It includes:

- Connection management with the Ollama service
- Response validation and cleaning
- Error handling and fallback mechanisms
- Response caching for performance optimization
- Health checks for the Ollama service

## Key Methods

- `__init__(base_url, timeout)`: Initializes the handler with connection settings
- `_check_availability()`: Verifies if the Ollama service is operational
- `generate_response(prompt, model, temperature, max_tokens)`: Core method to generate responses from Ollama
- `_validate_and_clean_response(response_text)`: Cleans and validates the raw response
- `_generate_fallback_response(prompt)`: Provides fallback responses when Ollama is unavailable

## How to Use

### Basic Usage

```python
from api.inference_engine.ollama_handler import OllamaHandler

# Initialize the handler (pointing to Ollama container)
handler = OllamaHandler(base_url="http://ollama:11434", timeout=30)

# Generate a response
response = handler.generate_response(
    prompt="What are common pests affecting tomato plants?",
    model="tinyllama",  # Or another model you have pulled
    temperature=0.7
)

# Use the response
print(response)
```

### Integration with Docker

The handler is designed to work with an Ollama service running in a Docker container. Ensure you have:

1. Added the Ollama service to your `docker-compose.yml` file
2. Set environment variables in your web service:
   - `USE_OLLAMA=true`
   - `OLLAMA_BASE_URL=http://ollama:11434`

### Installing Models

Before using the handler with a particular model, make sure it's pulled into your Ollama instance:

```bash
docker compose exec ollama ollama pull tinyllama
```

## Fallback Behavior

If the Ollama service is not available, the handler will automatically fall back to providing generic responses. This ensures the application remains functional even when the LLM service is down.

## Troubleshooting

- If you see "Ollama is not available" warnings in logs, check:
  - Is the Ollama container running? (`docker compose ps`)
  - Has the model been pulled? 
  - Are network connections correct in the docker-compose file?
  - Does Ollama have enough resources?

- If responses are empty or unexpected:
  - Check Ollama container logs (`docker compose logs ollama`)
  - Try a simpler prompt for testing
  - Ensure the model name in `generate_response()` matches a pulled model

## Patching the Implementation

To replace the application's existing handler with this implementation:

```bash
# Copy the file to the container
docker compose cp ollama_handler_patched.py web:/app/api/inference_engine/ollama_handler.py

# Restart the web service
docker compose restart web
``` 