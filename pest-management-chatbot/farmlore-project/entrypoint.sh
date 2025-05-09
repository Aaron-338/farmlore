#!/bin/bash

set -e

# Function to check if postgres is ready
postgres_ready() {
  pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
}

# Wait for postgres to be ready
until postgres_ready; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
>&2 echo "PostgreSQL is up - executing commands"

# Create database if it doesn't exist
echo "Checking if database exists..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME"
echo "Database setup done"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create required user groups and permissions
echo "Setting up user groups and permissions..."
python manage.py create_groups

# Create superuser if needed
echo "Creating superuser if needed..."
python create_superuser.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# init_ollama_models.sh is called by docker-compose command, so no need to call here explicitly

# Set environment variables for optimized performance on resource-constrained systems
export USE_PROLOG_PRIMARY=${USE_PROLOG_PRIMARY:-true}
export OLLAMA_MODEL=${OLLAMA_MODEL:-tinyllama:latest}

echo "Configuration:"
echo "- Using Prolog as primary engine: $USE_PROLOG_PRIMARY"
echo "- Ollama model: $OLLAMA_MODEL"
echo "- Workers: 1 (optimized for resource-constrained systems)"

# Start server with optimized settings for resource-constrained systems
echo "Starting server..."
gunicorn farmlore.wsgi:application --bind 0.0.0.0:8000 --timeout 300 --workers 1 --worker-class gthread --worker-connections 500 --threads 2 --preload