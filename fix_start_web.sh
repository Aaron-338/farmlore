#!/bin/bash

echo "Starting web service..."
set -e

# Wait for postgres to be ready
echo "Waiting for PostgreSQL..."
RETRIES=0
MAX_RETRIES=30
while ! pg_isready -h "db" -p "5432" -U "postgres" -q; do
  RETRIES=$((RETRIES+1))
  if [ $RETRIES -gt $MAX_RETRIES ]; then
    echo "ERROR: PostgreSQL did not become ready. Exiting."
    exit 1
  fi
  echo "PostgreSQL is unavailable - sleeping for 1 second (attempt $RETRIES/$MAX_RETRIES)"
  sleep 1
done
echo "PostgreSQL is up."

# Apply database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Initialize RAG if enabled
if [ "$USE_RAG" = "true" ]; then
  echo "Initializing RAG system..."
  python initialize_rag.py
fi

# Start Gunicorn
echo "Starting Gunicorn server..."
gunicorn farmlore.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --threads 2 \
  --worker-class gthread \
  --timeout 300 \
  --log-level info \
  --access-logfile '-' \
  --error-logfile '-' 