# FarmLore - Agricultural Chatbot with Specialized Models

FarmLore is an advanced agricultural chatbot system that leverages specialized language models to provide accurate and contextual responses for different types of agricultural queries.

## Specialized Models

The system uses the following specialized Ollama models for different query types:

1. **Pest Identification** (`farmlore-pest-id`): Used for identifying pests based on descriptions
2. **Pest Management** (`farmlore-pest-mgmt`): Used for pest control and management methods
3. **Indigenous Knowledge** (`farmlore-indigenous`): Used for indigenous farming practices and knowledge
4. **Crop Pests** (`farmlore-crop-pests`): Used for information about pests affecting specific crops
5. **General Query** (`farmlore-general`): Used for general agricultural queries

These models are created from specialized Modelfiles that contain tailored system instructions and parameters for each query type.

## Architecture

The FarmLore system consists of the following components:

- **API Service**: Django REST Framework application that handles user requests and routes them to the appropriate specialized model
- **Ollama Service**: Hosts the specialized language models and provides inference capabilities
- **Database**: Stores user queries, responses, and performance metrics
- **Monitoring**: Tracks model performance and provides insights into system usage

## Deployment

The system can be deployed using Docker Compose for local development and testing.

### Docker Compose Deployment

To deploy the system locally using Docker Compose, navigate to the **root directory of the `FarmLore-master` project** (the parent directory of this one) and run:

```bash
# Build and start the services
docker-compose up -d

# Check the logs
docker-compose logs -f
```

## CI/CD Pipeline

The system can be integrated with CI/CD tools for automated testing and deployment:

1. **Testing**: Run unit tests and integration tests to verify system functionality
2. **Building**: Build Docker images for the API and Ollama services
3. **Deployment**: Deploy the system to your target environment

## Monitoring and Health Checks

The system includes several endpoints for monitoring and health checks:

- `/api/v1/health`: General API health check
- `/api/v1/models/health`: Health check for specialized models
- `/api/v1/stats/models`: Performance statistics for specialized models
- `/api/v1/stats/query-types`: Statistics for different query types
- `/api/v1/dashboard`: Dashboard for visualizing model performance

## Development

### Prerequisites

- Python 3.10+
- Docker and Docker Compose


### Setting Up Development Environment

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Testing

To run the tests:

```bash
# Run all tests
pytest

# Run specific tests
pytest api/inference_engine/test_modelfiles.py
```

## Performance Optimization

The system includes several optimizations to improve performance:

1. **Caching**: Responses are cached to reduce API calls and improve response times
2. **Specialized Models**: Each query type uses a specialized model optimized for that type of query
3. **Parallel Processing**: Multiple queries can be processed in parallel
4. **Resource Optimization**: Docker Compose configuration can be adjusted to allocate appropriate resources based on workload

## License

This project is licensed under the MIT License - see the LICENSE file for details.
