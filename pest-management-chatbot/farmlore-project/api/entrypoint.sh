#!/bin/bash
# Entrypoint script for the API container

echo "Starting FarmLore API container..."

# Fix import structure
if [ -d "/app/api/views" ]; then
    echo "Fixing import structure for views package..."
    
    # Create a symlink to views.py in the api/views directory
    if [ -f "/app/api/views.py" ]; then
        echo "Creating symlink for views.py..."
        ln -sf /app/api/views.py /app/api/views/__init__.py
        echo "Symlink created."
    else
        echo "Warning: views.py not found in /app/api/"
    fi
    
    echo "Import structure fixed."
fi

# Update the urls.py file to use absolute imports
if [ -f "/app/api/urls.py" ]; then
    echo "Updating urls.py to use absolute imports..."
    sed -i 's/from \.views import/from api.views import/g' /app/api/urls.py
    echo "urls.py updated."
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up - continuing"

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
while ! nc -z ollama 11434; do
  echo "Ollama is unavailable - sleeping"
  sleep 1
done
echo "Ollama is up - continuing"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Run the application
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 farmlore.wsgi
