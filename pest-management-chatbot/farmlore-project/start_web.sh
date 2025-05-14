#!/bin/bash

echo "[START_WEB] Starting web service with Ollama integration for testing..."

# Step 0: Clean __pycache__ directories and .pyc files
echo "[START_WEB] Cleaning Python cache files..."
find /app -type d -name "__pycache__" -exec rm -r {} +
find /app -type f -name "*.pyc" -delete
echo "[START_WEB] Python cache files cleaned."

# --- CRITICAL: Ensure api/views is NOT a package directory --- 
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
    cp /app/api/views.py /tmp/views.py.tmp
    # Use a heredoc for the Python sanitization script
    python <<END_PYTHON_SCRIPT
import sys
file_path = '/tmp/views.py.tmp'
output_path = '/app/api/views.py'
content = None
try:
    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f_in:
        content = f_in.read()

    if content is not None:
        content = content.replace('\\x00', '') # Remove null bytes
        # Loop to remove any leading U+FFFD characters
        original_len = len(content)
        while content.startswith('\ufffd'): # Corrected: use '\ufffd'
            content = content[1:]
        if len(content) < original_len:
            print(f"[START_WEB_PYTHON_SANITIZE] Stripped leading U+FFFD characters. Original length: {original_len}, New length: {len(content)}")
        
        # Debug: print the first 20 characters (or fewer if shorter) after sanitization attempt
        # Represent non-printable characters with repr()
        # print(f"[START_WEB_PYTHON_SANITIZE] First 20 chars after strip: {repr(content[:20])}")
    else:
        content = "" 

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write(content)

    print(f'[START_WEB_PYTHON_SANITIZE] Successfully sanitized {output_path}')
except FileNotFoundError:
    print(f'[START_WEB_PYTHON_SANITIZE] Error: Temporary file {file_path} not found.', file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f'[START_WEB_PYTHON_SANITIZE] Error sanitizing file: {file_path} to {output_path} - {e}', file=sys.stderr)
    sys.exit(1)
END_PYTHON_SCRIPT
    
    # Check the exit status of the Python script
    if [ $? -ne 0 ]; then
        echo "[START_WEB] ERROR: Python sanitization script failed. The /app/api/views.py may still be corrupted."
        # Decide if we should exit here. For now, we'll let Django try and fail to get more logs.
    else
        echo "[START_WEB] Python sanitization script completed successfully."
    fi
    
    rm /tmp/views.py.tmp
else
    echo "[START_WEB] CRITICAL WARNING: File /app/api/views.py does NOT exist! Imports will likely fail."
fi
# --- End of critical check ---

# Enable Ollama for testing
echo "[START_WEB] Enabling Ollama integration for testing"
export USE_OLLAMA=true
export OLLAMA_BASE_URL="http://ollama:11434"
export OLLAMA_MODEL="tinyllama"

# Run database migrations
echo "[START_WEB] Running database migrations..."
python manage.py migrate --noinput

# Skip superuser creation
echo "[START_WEB] SKIPPING superuser creation"

# Run collectstatic
echo "[START_WEB] Collecting static files..."
python manage.py collectstatic --noinput

# Set Environment Variables for Ollama 
export USE_OLLAMA=true
export USE_PROLOG_PRIMARY=true
export OLLAMA_BASE_URL="http://ollama:11434"
export OLLAMA_MODEL="tinyllama"

echo "[START_WEB] Configuration:"
echo "[START_WEB] - USE_OLLAMA: $USE_OLLAMA (ENABLED FOR OLLAMA TESTING)"
echo "[START_WEB] - USE_PROLOG_PRIMARY: $USE_PROLOG_PRIMARY"
echo "[START_WEB] - OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo "[START_WEB] - OLLAMA_MODEL: $OLLAMA_MODEL"
echo "[START_WEB] - DJANGO_ALLOWED_HOSTS: $DJANGO_ALLOWED_HOSTS"

# Start Django development server for more detailed debugging output
echo "[START_WEB] Starting Django development server on 0.0.0.0:8000..."
python manage.py runserver 0.0.0.0:8000

# Original Gunicorn command (commented out for debugging)
# echo "[START_WEB] Starting Gunicorn server in debug mode..."
# gunicorn farmlore.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --workers 1 --threads 4 --log-level debug 