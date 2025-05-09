# Pest Management Chatbot System Architecture Guide

## System Overview

This pest management chatbot leverages indigenous agricultural knowledge for pest management using a hybrid approach that combines rule-based systems and language models. Here's a comprehensive guide to the system architecture:

## Key Components

### 1. Docker Container Architecture

The system uses Docker Compose with four main services:
- `web`: Django application running the main system (Python 3.10)
- `db`: PostgreSQL 14 database for data storage
- `nginx`: Web server handling HTTP requests and serving static files
- `ollama`: Language model service for advanced reasoning capabilities (newly added)

### 2. Core Application Structure

```
/app/
├── farmlore/               # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py             # Root URL routing
│   └── wsgi.py             # WSGI application entry point
├── api/                    # API application
│   ├── inference_engine/   # Core reasoning components
│   │   ├── hybrid_engine.py     # Combines different inference methods
│   │   └── prolog_engine.py     # Mock Prolog implementation (can use Ollama)
│   └── views.py            # API endpoints
├── community/              # Community features and validation
│   ├── models.py           # Data models for community content
│   ├── migrations/         # Database migrations
│   └── views.py            # Views for community pages
├── core/                   # Core application features
│   ├── urls.py             # URL routing for core features
│   └── auth_views.py       # Authentication views
├── chatbot/                # Chatbot interface
└── ml/                     # Machine learning components
```

### 3. Key Classes and Their Interactions

#### Inference Engine Architecture
- `HybridEngine`: Main entry point for all inference operations
  - Located in `/app/api/inference_engine/hybrid_engine.py`
  - Combines rule-based and ML approaches
  - Uses `PrologEngine` for logical reasoning

- `PrologEngine`: Handles rule-based reasoning
  - Located in `/app/api/inference_engine/prolog_engine.py`
  - Currently uses a mock implementation
  - Can be configured to use Ollama for more advanced reasoning

- `OllamaEngine` (newly added):
  - Connects to the Ollama service for LLM capabilities
  - Uses environment variables for configuration
  - Can be enabled/disabled via the `USE_OLLAMA` environment variable

#### Web Application Architecture
- Django application structure follows MVT (Model-View-Template) pattern
- `community` app handles user-contributed knowledge and validation
- `api` app exposes REST endpoints for chatbot interaction
- `core` app provides basic functionality and authentication

## UML Diagrams

### Class Diagram

```
+------------------+         +----------------------+         +------------------+
|   HybridEngine   |         |    PrologEngine      |         |   OllamaEngine   |
+------------------+         +----------------------+         +------------------+
| - prolog_engine  |<>------>| - prolog/ollama      |<------->| - base_url       |
+------------------+         +----------------------+         | - model          |
| + __init__()     |         | + __init__()         |         +------------------+
| + query()        |         | + load_knowledge()   |         | + __init__()     |
| + _mock_pest_id()|         | + query()            |         | + _pull_model()  |
| + _mock_control()|         | + assert_fact()      |         | + query()        |
| + _mock_crop()   |         | + consult_file()     |         +------------------+
| + _mock_indig()  |         +----------------------+
+------------------+                   ^
                                       |
                                       |
+------------------+         +----------------------+
|  Prolog (Mock)   |<>------>|    API Views         |
+------------------+         +----------------------+
| - facts          |         | - engine: HybridEngine|
+------------------+         +----------------------+
| + __init__()     |         | + pest_id_api()      |
| + consult()      |         | + control_methods()  |
| + assertz()      |         | + crop_pests()       |
| + query()        |         | + indigenous_know()  |
+------------------+         +----------------------+
                                       ^
                                       |
                                       |
+------------------+         +----------------------+         +------------------+
|   ChatbotViews   |         |   CommunityModels    |         |  CoreViews       |
+------------------+         +----------------------+         +------------------+
| + chat()         |         | - UserProfile        |         | + home_view()    |
| + chat_api()     |         | - IndigenousKnowledge|         | + about_view()   |
| + chat_history() |         | - Pest               |         | + database_view()|
+------------------+         | - CommunityValidation|         | + custom_logout()|
                             +----------------------+         +------------------+
```

### Sequence Diagram - Chatbot Query Flow

```
+----------+    +----------+    +-------------+    +-------------+    +-------------+
|  User    |    |  Views   |    | HybridEngine|    | PrologEngine|    | OllamaEngine|
+----------+    +----------+    +-------------+    +-------------+    +-------------+
     |               |                |                  |                  |
     | Query         |                |                  |                  |
     |-------------->|                |                  |                  |
     |               | process_query()|                  |                  |
     |               |--------------->|                  |                  |
     |               |                | query()          |                  |
     |               |                |----------------->|                  |
     |               |                |                  | process query    |
     |               |                |                  |----------------->|
     |               |                |                  |                  | generate 
     |               |                |                  |                  | response
     |               |                |                  |                  |<-------->
     |               |                |                  |<-----------------|
     |               |                |<-----------------|                  |
     |               |<---------------|                  |                  |
     | Response      |                |                  |                  |
     |<--------------|                |                  |                  |
```

### Sequence Diagram - Community Knowledge Validation

```
+----------+    +-------------+    +----------------+    +------------+    +-------------+
|  User    |    | CommunityUI |    | ValidationView |    | ModelsView |    | DatabaseAPI |
+----------+    +-------------+    +----------------+    +------------+    +-------------+
     |               |                    |                   |                 |
     | Submit        |                    |                   |                 |
     | Knowledge     |                    |                   |                 |
     |-------------->|                    |                   |                 |
     |               | create_submission()|                   |                 |
     |               |------------------->|                   |                 |
     |               |                    | validate_input()  |                 |
     |               |                    |------------------>|                 |
     |               |                    |                   | save_knowledge()|
     |               |                    |                   |---------------->|
     |               |                    |                   |                 | store in DB
     |               |                    |                   |                 |<---------->
     |               |                    |                   |<----------------|
     |               |                    |<------------------|                 |
     |               |<-------------------|                   |                 |
     | Confirmation  |                    |                   |                 |
     |<--------------|                    |                   |                 |
```

### Sequence Diagram - Ollama Integration Flow 

```
+----------+    +----------+    +-------------+    +-------------+    +-------------+
|  System  |    |  Django  |    | HybridEngine|    | PrologEngine|    | OllamaEngine|
+----------+    +----------+    +-------------+    +-------------+    +-------------+
     |               |                |                  |                  |
     | Start         |                |                  |                  |
     | containers    |                |                  |                  |
     |-------------->|                |                  |                  |
     |               | initialize app |                  |                  |
     |               |--------------->|                  |                  |
     |               |                | create engine    |                  |
     |               |                |----------------->|                  |
     |               |                |                  | check USE_OLLAMA |
     |               |                |                  |------------------>
     |               |                |                  |                  | connect
     |               |                |                  |                  | to Ollama
     |               |                |                  |                  |<-------->
     |               |                |                  |                  | check
     |               |                |                  |                  | models
     |               |                |                  |                  |<-------->
     |               |                |                  |<-----------------|
     |               |                |<-----------------|                  |
     |               |<---------------|                  |                  |
     | System Ready  |                |                  |                  |
     |<--------------|                |                  |                  |
```

## Running the System

### Starting the Application

1. Start all containers:
   ```bash
   docker compose up -d
   ```

2. Check running containers:
   ```bash
   docker compose ps
   ```

3. View logs:
   ```bash
   docker compose logs web
   ```

### Accessing the Application

- Web Interface: http://localhost
- Admin Interface: http://localhost/admin/
- API Endpoints: http://localhost/api/

### Using the Ollama Integration

The system is now configured to use Ollama when available. Key points:

1. Environment variables control Ollama usage:
   - `USE_OLLAMA=true`: Enables Ollama integration
   - `OLLAMA_BASE_URL=http://ollama:11434`: Points to the Ollama service

2. When Ollama is enabled, the system will:
   - Connect to the Ollama service during startup
   - Use the Ollama LLM for inference instead of the mock implementation
   - Fall back to the mock implementation if Ollama is unavailable

3. To check if Ollama is being used:
   ```bash
   docker compose logs web | grep -i ollama
   ```

4. To pull a specific model:
   ```bash
   docker compose exec ollama ollama pull llama2
   ```

### Database Migrations

If you need to apply migrations:
```bash
docker compose exec web python manage.py migrate
```

## Troubleshooting

1. If containers don't start:
   ```bash
   docker compose logs
   ```

2. If the web container is restarting:
   ```bash
   docker compose logs web
   ```

3. If Ollama is not connecting:
   ```bash
   docker compose logs ollama
   ```

4. To restart a specific service:
   ```bash
   docker compose restart web
   ```

5. To rebuild after code changes:
   ```bash
   docker compose down
   docker compose build web
   docker compose up -d
   ```

## Next Steps for Development

1. **Complete Ollama Integration**: Finish implementing the real `OllamaEngine` class in the same directory as `prolog_engine.py`

2. **Test LLM Functionality**: Once implemented, test the chatbot with real LLM-powered responses

3. **UI Enhancements**: Improve the web interface to better display LLM-generated responses

4. **Performance Tuning**: Adjust Ollama parameters for optimal performance

The foundation is now set with the Docker architecture updated to include Ollama. The next step is implementing the actual integration code within the application.

## Implementing OllamaEngine

To complete the integration, you need to create the `ollama_engine.py` file in the same directory as `prolog_engine.py`. Here's the implementation:

```python
"""
Real implementation of a language model engine using Ollama
"""
import os
import logging
import requests
import json

class OllamaEngine:
    def __init__(self):
        self.base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.environ.get('OLLAMA_MODEL', 'llama2')
        logging.info(f"Initializing Ollama Engine with model {self.model} at {self.base_url}")
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                available_models = response.json().get('models', [])
                model_names = [model.get('name') for model in available_models]
                logging.info(f"Connected to Ollama. Available models: {model_names}")
                
                # Check if our model is available
                if self.model not in model_names:
                    logging.warning(f"Model {self.model} not found. Pulling it now...")
                    self._pull_model()
            else:
                logging.error(f"Failed to connect to Ollama API: {response.status_code}")
        except Exception as e:
            logging.error(f"Error connecting to Ollama: {str(e)}")

    def _pull_model(self):
        """Pull the required model from Ollama"""
        try:
            logging.info(f"Pulling model {self.model}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model}
            )
            if response.status_code == 200:
                logging.info(f"Successfully pulled model {self.model}")
            else:
                logging.error(f"Failed to pull model: {response.status_code}")
        except Exception as e:
            logging.error(f"Error pulling model: {str(e)}")

    def query(self, prompt):
        """Query the Ollama model with a prompt"""
        try:
            logging.info(f"Querying Ollama with: {prompt}")
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logging.error(f"Ollama query failed: {response.status_code}")
                return f"Error: {response.status_code}"
        except Exception as e:
            logging.error(f"Error querying Ollama: {str(e)}")
            return f"Error: {str(e)}"
```

Then modify the `prolog_engine.py` file to use this implementation when `USE_OLLAMA` is set to true. 

## Recent Improvements

The Pest Management Chatbot system has been enhanced with the following improvements:

### User Interface Enhancements

1. **Response Source Indicators**: The chat interface now displays indicators showing whether responses are generated by the AI model (LLM) or the rule-based system (Prolog). This provides transparency to users about the source of information.
   - AI-Generated responses are labeled with a blue "AI-Generated" tag
   - Rule-Based responses are labeled with a red "Rule-Based" tag

2. **Feedback Mechanism**: Users can now provide feedback on responses using thumbs up/down buttons. This feedback is stored in the database for later analysis to improve the system.

### Performance Optimizations

1. **Enhanced Caching System**:
   - **Exact Match Caching**: Stores exact matches for queries with timestamp-based expiration
   - **Semantic Caching**: Finds similar previous queries using Jaccard similarity metrics
   - **Cache Maintenance**: Background thread periodically cleans expired entries and saves cache to disk
   - **Cache Statistics**: Tracks hit rates and semantic hit rates for performance monitoring

2. **Circuit Breaker Pattern**: Implemented to prevent cascading failures when the LLM service is under stress.
   - Automatically falls back to rule-based responses when the LLM service is unstable
   - Gradually recovers when the service returns to normal

3. **Optimized HTTP Connections**: Connection pooling and retry logic for more efficient API calls.

### Backend Improvements

1. **Feedback Storage**: A new `ResponseFeedback` model stores user feedback on responses, including:
   - The message ID
   - Feedback type (positive/negative)
   - Response content
   - Source of the response (LLM or Prolog)
   - User information if available
   
2. **Admin Interface**: Enhanced admin interface for viewing user feedback and monitoring system performance.

### Next Steps

Further improvements planned for the system:

1. **Analytics Dashboard**: Create a dashboard showing feedback statistics and system performance.
2. **Model Selection UI**: Allow users to select different LLM models for specialized queries.
3. **Advanced Rate Limiting**: Implement request throttling to protect the LLM service during high traffic.
4. **A/B Testing Framework**: Test different prompt templates and response formats to optimize user experience.

These improvements enhance both the user experience and system reliability, making the Pest Management Chatbot more effective and transparent for agricultural knowledge sharing. 