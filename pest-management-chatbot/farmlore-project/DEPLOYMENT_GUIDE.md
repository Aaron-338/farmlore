# FarmLore Deployment Guide

This guide outlines the steps to deploy the updated FarmLore system with Ollama Modelfiles integration using the **single `docker-compose.yml` file located in the project root directory**.

## Prerequisites

- Docker and Docker Compose installed
- Access to a server with at least 8GB RAM and 4 CPU cores (adjust based on chosen Ollama models)
- Git access to the FarmLore repository

## Deployment Steps

### 1. Prepare the Environment

Navigate to the **root directory** of the cloned FarmLore repository (e.g., `FarmLore-master`).

```bash
# cd /path/to/FarmLore-master
```

If your Django application (`web` service) requires specific runtime environment variables (e.g., `SECRET_KEY`, database credentials if not using defaults, `USE_OLLAMA`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` for the *web app*), create or ensure a `.env` file exists in this root directory. The `docker-compose.yml` is set up to use it for the `web` service.

Example content for `.env` for the `web` service:
```
DEBUG=True
SECRET_KEY=your_production_secret_key_here
DB_NAME=farmlore
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 your_server_ip

# Ollama settings for the web application (OllamaHandler)
USE_OLLAMA=true
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=tinyllama # Default model for the web app if no specialized one is chosen
# OLLAMA_CACHE_TTL=86400
# OLLAMA_MAX_SEMANTIC_CACHE=200
```
Note: The `ollama` service itself builds models from modelfiles and does not require these specific `OLLAMA_MODEL` or `OLLAMA_BASE_URL` variables for its own build process.

### 2. Build and Start the Services

From the **project root directory**: 
```bash
# Build the Docker images (including the custom ollama service image)
docker-compose build

# Start the services in detached mode
docker-compose up -d
```
This command will also start the `ollama` service, which will internally create its specialized models from the modelfiles included during its build.

### 3. Initialize the Specialized Models (Verification)

The `ollama` service automatically creates the specialized models (e.g., `farmlore-pest-id`, `farmlore-pest-mgmt`, etc.) from the modelfiles located in `pest-management-chatbot/farmlore-project/api/inference_engine/modelfiles/` during its startup if they don't already exist within its volume.

You can verify their creation by checking the `ollama` service logs shortly after startup:

```bash
docker-compose logs -f ollama
```
Look for messages indicating model creation or availability.

Additionally, the `web` service (Django application) logs will show the `OllamaHandler` detecting these models:
```bash
docker-compose logs -f web
```
Look for messages like "OllamaHandler: Specialized model already exists..." or successful initialization of `OllamaHandler`.

### 4. Verify the Deployment

Access the FarmLore application via your server's IP or `localhost` (if deploying locally):
- Web Interface: `http://your-server-ip/` (or `http://localhost/`)
- Admin Interface: `http://your-server-ip/admin/`
- Chat API Endpoint: `http://your-server-ip/api/chat/`

(Swagger/OpenAPI docs, if available, might be at an endpoint like `http://your-server-ip/api/schema/swagger-ui/` or similar, check your `api/urls.py`)

## Monitoring and Maintenance

### Performance Monitoring

If performance monitoring endpoints are exposed by the `web` service (e.g., through Django admin or custom views), refer to their specific URLs. Example from another doc was `/api/v1/stats`, ensure this is correct and active.

### Log Monitoring

Monitor the logs for any issues (run from project root):

```bash
docker-compose logs -f web
docker-compose logs -f ollama
docker-compose logs -f nginx
docker-compose logs -f db
```

### Updating Modelfiles

If you need to update a modelfile (e.g., change a `SYSTEM` prompt or a `PARAMETER`):

1.  Edit the specific modelfile in the `pest-management-chatbot/farmlore-project/api/inference_engine/modelfiles/` directory.
2.  Rebuild the `ollama` service image and restart all services (from project root):
    ```bash
    docker-compose up -d --build ollama 
    # Or to rebuild all services if other changes were made:
    # docker-compose up -d --build
    ```
    Ollama should automatically use the updated modelfile to recreate/update the corresponding model internally when its container restarts with the new image.
3.  The `web` application, through `OllamaHandler`, will use the updated model on subsequent requests.

## Troubleshooting

### Common Issues

1.  **Model Creation Fails within Ollama Service**
    *   Check the Ollama service logs: `docker-compose logs ollama` (from project root).
    *   Verify that the modelfiles in `pest-management-chatbot/farmlore-project/api/inference_engine/modelfiles/` are correctly formatted (e.g., `FROM` directive, `PARAMETER`, `SYSTEM`).
    *   Ensure the base model specified in the `FROM` directive of your modelfiles (e.g., `tinyllama:latest`) is accessible to Ollama or has been pulled into the `ollama` service (`docker-compose exec ollama ollama pull tinyllama:latest`).
    *   Ensure Ollama has enough disk space and memory allocated via Docker Desktop settings or server configuration.

2.  **`web` Service (Django App) Fails to Connect to `ollama` or Models**
    *   Check `web` service logs: `docker-compose logs web`.
    *   Ensure `OLLAMA_BASE_URL` in the `web` service's environment is `http://ollama:11434`.
    *   Verify `ollama` service is running: `docker-compose ps`.
    *   Verify specialized models are listed by `OllamaHandler` in `web` logs.

3.  **Slow Response Times**
    *   Consider Ollama model sizes and server resources. Larger models require more resources.
    *   Check `web` service caching configurations (if any beyond OllamaHandler's own).
    *   Optimize prompt templates if they are overly verbose.

4.  **High Memory Usage by `ollama` service**
    *   Reduce the `num_ctx` parameter in the modelfiles.
    *   For the `ollama` service in `docker-compose.yml`, you can add resource limits (e.g., `mem_limit`), but ensure it's enough for your models.

## Rollback Procedure

If you need to roll back to a previous version of the application code:

```bash
# Stop the current services (from project root)
docker-compose down

# Check out the previous version using Git
git checkout <your-previous-commit-hash-or-tag>

# Rebuild images with the old code and restart
docker-compose up -d --build
```
