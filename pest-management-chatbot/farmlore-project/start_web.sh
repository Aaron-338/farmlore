#!/bin/bash

echo "[START_WEB] Starting web service..."

# Exit on error
set -e

# --- Environment Variables (Defaults if not set) ---
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres} # Be cautious with default passwords
DB_NAME=${DB_NAME:-farmlore}
CREATE_SUPERUSER_SCRIPT=${CREATE_SUPERUSER_SCRIPT:-./create_superuser.py} # Path to your script
SHOULD_CREATE_SUPERUSER=${SHOULD_CREATE_SUPERUSER:-true} # Set to false to skip

GUNICORN_WORKERS=${GUNICORN_WORKERS:-1} # Defaulting to 1 as in original entrypoint for resource-constrained
GUNICORN_THREADS=${GUNICORN_THREADS:-2} # As in original entrypoint
GUNICORN_WORKER_CLASS=${GUNICORN_WORKER_CLASS:-gthread}
GUNICORN_WORKER_CONNECTIONS=${GUNICORN_WORKER_CONNECTIONS:-500}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-300}
GUNICORN_PRELOAD=${GUNICORN_PRELOAD:-true} # Add --preload if this var is true
GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}

# Function to check if postgres is ready
postgres_ready() {
  # Ensure pg_isready is available; it's in postgresql-client which is in Dockerfile
  pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -q # -q for quiet
}

# Wait for postgres to be ready
echo "[START_WEB] Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
RETRIES=0
MAX_RETRIES=30 # Approx 30 seconds
while ! postgres_ready; do
  RETRIES=$((RETRIES+1))
  if [ $RETRIES -gt $MAX_RETRIES ]; then
    echo "[START_WEB] ERROR: PostgreSQL did not become ready after $MAX_RETRIES attempts. Exiting."
    exit 1
  fi
  >&2 echo "[START_WEB] PostgreSQL is unavailable - sleeping for 1 second (attempt $RETRIES/$MAX_RETRIES)"
  sleep 1
done
>&2 echo "[START_WEB] PostgreSQL is up."

# Create database if it doesn't exist
# Note: PGPASSWORD is used by psql. Ensure DB_PASSWORD is set.
echo "[START_WEB] Checking if database '$DB_NAME' exists..."
if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "[START_WEB] Database '$DB_NAME' already exists."
else
    echo "[START_WEB] Database '$DB_NAME' does not exist. Creating..."
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -c "CREATE DATABASE "$DB_NAME""; then
        echo "[START_WEB] Database '$DB_NAME' created successfully."
    else
        echo "[START_WEB] ERROR: Failed to create database '$DB_NAME'. Please check logs and permissions."
        # exit 1 # Optional: exit if DB creation fails
    fi
fi
echo "[START_WEB] Database setup check complete."


# Step 0: Clean __pycache__ directories and .pyc files (Kept from original start_web.sh)
# PYTHONDONTWRITEBYTECODE=1 in Dockerfile should prevent .pyc, but this is belt-and-suspenders
echo "[START_WEB] Cleaning Python cache files..."
find /app -type d -name "__pycache__" -exec rm -r {} +
find /app -type f -name "*.pyc" -delete
echo "[START_WEB] Python cache files cleaned."

# --- CRITICAL: File/Directory Handling for /app/api/views --- (Kept from original start_web.sh)
# This section should ideally be removed once the underlying issue is fixed.
echo "[START_WEB] Ensuring /app/api/views is not a conflicting package..."
if [ -d "/app/api/views" ]; then
    echo "[START_WEB] Found directory /app/api/views. Removing it and its contents (like __init__.py)."
    rm -rf "/app/api/views/"
    if [ -d "/app/api/views" ]; then
        echo "[START_WEB] ERROR: Failed to remove /app/api/views directory!"
    else
        echo "[START_WEB] Successfully removed /app/api/views directory."
    fi
fi

# Check that /app/api/views.py (the file we want) exists
if [ -f "/app/api/views.py" ]; then
    echo "[START_WEB] File /app/api/views.py exists."
    echo "[START_WEB] Attempting to sanitize /app/api/views.py..."
    # Create a temporary copy for sanitization
    cp /app/api/views.py /tmp/views.py.tmp
    # Use a heredoc for the Python sanitization script
    python <<END_PYTHON_SCRIPT
import sys
file_path = '/tmp/views.py.tmp'
output_path = '/app/api/views.py' # Sanitize in place after copying
content = None
try:
    # Try reading with utf-8-sig first to handle potential BOM
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f_in:
            content = f_in.read()
    except UnicodeDecodeError:
        # Fallback to utf-8 if utf-8-sig fails (e.g. no BOM but other issues)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f_in:
            content = f_in.read()
    
    if content is not None:
        # Remove null bytes first, as they can interfere with other string ops
        original_len_null = len(content)
        content = content.replace('\x00', '') 
        if len(content) < original_len_null:
            print(f"[START_WEB_PYTHON_SANITIZE] Removed null bytes. Original length: {original_len_null}, New length: {len(content)}")

        # Remove BOM if present (utf-8-sig might have handled it, but this is a safeguard)
        # BOM is U+FEFF
        if content.startswith('\ufeff'):
            content = content[1:]
            print(f"[START_WEB_PYTHON_SANITIZE] Stripped leading BOM (U+FEFF).")

        # Loop to remove any leading U+FFFD (REPLACEMENT CHARACTER)
        # These might appear if there was a decoding error before this script
        original_len_fffd = len(content)
        while content.startswith('\ufffd'):
            content = content[1:]
        if len(content) < original_len_fffd:
            print(f"[START_WEB_PYTHON_SANITIZE] Stripped leading U+FFFD characters. Original length: {original_len_fffd}, New length: {len(content)}")
        
    else: # Should not happen if file exists, but as a guard
        content = "" 

    with open(output_path, 'w', encoding='utf-8') as f_out: # Always write back as plain UTF-8
        f_out.write(content)

    print(f'[START_WEB_PYTHON_SANITIZE] Successfully sanitized {output_path}')
except FileNotFoundError:
    print(f'[START_WEB_PYTHON_SANITIZE] Error: Temporary file {file_path} not found.', file=sys.stderr)
    sys.exit(1) # Exit if sanitization fails critically
except Exception as e:
    print(f'[START_WEB_PYTHON_SANITIZE] Error sanitizing file: {file_path} to {output_path} - {e}', file=sys.stderr)
    sys.exit(1) # Exit if sanitization fails critically
END_PYTHON_SCRIPT
    
    # Check the exit status of the Python script
    if [ $? -ne 0 ]; then
        echo "[START_WEB] ERROR: Python sanitization script failed for /app/api/views.py. Exiting."
        exit 1 # Exit if sanitization failed, as it's marked critical
    else
        echo "[START_WEB] Python sanitization script completed successfully for /app/api/views.py."
    fi
    
    rm /tmp/views.py.tmp # Clean up temp file
else
    echo "[START_WEB] CRITICAL WARNING: File /app/api/views.py does NOT exist! Django will likely fail."
    # Not exiting here to allow Django to try and log more specific errors if views.py is truly missing.
fi
# --- End of critical file handling ---

# Apply database migrations
echo "[START_WEB] Running database migrations..."
python manage.py migrate --noinput

# Create required user groups and permissions (from entrypoint.sh)
# Assumes 'create_groups' is a custom management command in your Django app
if python manage.py help create_groups > /dev/null 2>&1; then
    echo "[START_WEB] Setting up user groups and permissions via manage.py create_groups..."
    python manage.py create_groups
else
    echo "[START_WEB] WARNING: Management command 'create_groups' not found. Skipping group creation."
fi

# Create superuser if needed (from entrypoint.sh, made conditional)
if [ "$SHOULD_CREATE_SUPERUSER" = "true" ]; then
    if [ -f "$CREATE_SUPERUSER_SCRIPT" ]; then
        echo "[START_WEB] Creating superuser via $CREATE_SUPERUSER_SCRIPT..."
        python "$CREATE_SUPERUSER_SCRIPT"
    else
        echo "[START_WEB] WARNING: Superuser creation script '$CREATE_SUPERUSER_SCRIPT' not found, but SHOULD_CREATE_SUPERUSER is true. Skipping."
    fi
else
    echo "[START_WEB] SKIPPING superuser creation as per SHOULD_CREATE_SUPERUSER environment variable."
fi

# Collect static files
echo "[START_WEB] Collecting static files..."
python manage.py collectstatic --noinput --clear # Added --clear for cleaner collectstatic

# Environment variables for application logic (can be overridden by docker-compose)
# These were in start_web.sh and entrypoint.sh, consolidated here.
export USE_OLLAMA=${USE_OLLAMA:-true}
export USE_PROLOG_PRIMARY=${USE_PROLOG_PRIMARY:-true}
export OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-http://ollama:11434}
export OLLAMA_MODEL=${OLLAMA_MODEL:-tinyllama} # entrypoint.sh had :latest, choose one. tinyllama is simpler.

echo "[START_WEB] Final Configuration for Application Logic:"
echo "[START_WEB] - USE_OLLAMA: $USE_OLLAMA"
echo "[START_WEB] - USE_PROLOG_PRIMARY: $USE_PROLOG_PRIMARY"
echo "[START_WEB] - OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo "[START_WEB] - OLLAMA_MODEL: $OLLAMA_MODEL"
echo "[START_WEB] - DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS (from docker-compose)"
echo "[START_WEB] - DEBUG: $DEBUG (from docker-compose)"

# Prepare Gunicorn command
GUNICORN_CMD="
# Initialize RAG if enabled
if [ \"$USE_RAG\" = \"true\" ]; then
    echo \"======================================\"
    echo \"Initializing RAG system...\"
    echo \"======================================\"
    
    # Create data directory if it doesn't exist
    if [ ! -d \"$RAG_PERSIST_DIR\" ]; then
        echo \"Creating directory: $RAG_PERSIST_DIR\"
        mkdir -p \"$RAG_PERSIST_DIR\"
    fi
    
    # Run the initialization script
    python /app/initialize_rag.py
    
    # Check exit code
    if [ \$? -eq 0 ]; then
        echo \"RAG initialization completed\"
    else
        echo \"WARNING: RAG initialization encountered issues, but continuing startup\"
    fi
    
    echo \"======================================\"
fi
gunicorn farmlore.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $GUNICORN_WORKERS \
    --threads $GUNICORN_THREADS \
    --worker-class $GUNICORN_WORKER_CLASS \
    --worker-connections $GUNICORN_WORKER_CONNECTIONS \
    --log-level $GUNICORN_LOG_LEVEL \
    --access-logfile '-' \
    --error-logfile '-' \
    --timeout $GUNICORN_TIMEOUT"

if [ "$GUNICORN_PRELOAD" = "true" ]; then
    GUNICORN_CMD="$GUNICORN_CMD --preload"
fi

echo "[START_WEB] Gunicorn Command to be executed:"
echo "$GUNICORN_CMD"

echo "[START_WEB] Starting Gunicorn server..."
exec $GUNICORN_CMD 