#!/bin/bash

echo "[START_WEB] Starting web service initialization..."

# Step 1: Initialize Ollama Models
echo "[START_WEB] Running Ollama model initialization script..."
/app/init_ollama_models.sh
INIT_OLLAMA_EXIT_CODE=$?

if [ $INIT_OLLAMA_EXIT_CODE -ne 0 ]; then
    echo "[START_WEB] CRITICAL: /app/init_ollama_models.sh failed with exit code $INIT_OLLAMA_EXIT_CODE. Web service will not start."
    exit $INIT_OLLAMA_EXIT_CODE
else
    echo "[START_WEB] /app/init_ollama_models.sh completed successfully."
fi

# Step 2: Run Django Migrations
echo "[START_WEB] Applying database migrations..."
python manage.py migrate

# Step 3: Create Superuser (if needed by your app logic)
echo "[START_WEB] Running create_superuser.py..."
python create_superuser.py

# Step 4: Collect Static Files
echo "[START_WEB] Collecting static files..."
python manage.py collectstatic --noinput

# Step 5: Set Environment Variables (already set in Docker Compose, but can be reinforced if needed)
export USE_OLLAMA=${USE_OLLAMA:-true} # Default to true if not set
export USE_PROLOG_PRIMARY=${USE_PROLOG_PRIMARY:-true} # Default to true if not set

echo "[START_WEB] Configuration:"
echo "[START_WEB] - USE_OLLAMA: $USE_OLLAMA"
echo "[START_WEB] - USE_PROLOG_PRIMARY: $USE_PROLOG_PRIMARY"
echo "[START_WEB] - Ollama model from env: $OLLAMA_MODEL"

# Step 6: Start Gunicorn
echo "[START_WEB] Starting Gunicorn server..."
gunicorn farmlore.wsgi:application --bind 0.0.0.0:8000 --timeout 300 --workers 1 --worker-class gthread --worker-connections 500 --threads 2 