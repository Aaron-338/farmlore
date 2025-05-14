FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install SWI-Prolog for Prolog integration
RUN apt-get update && apt-get install -y --no-install-recommends \
    swi-prolog \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p logs/model_performance

# Fix import structure for views package
RUN if [ -d "/app/api/views" ]; then \
    echo "Fixing import structure for views package..." && \
    mv /app/api/views/* /app/api/ || true && \
    rm -rf /app/api/views && \
    mkdir -p /app/api/views && \
    touch /app/api/views/__init__.py && \
    echo "Import structure fixed." \
    ; fi

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    USE_OLLAMA=true \
    OLLAMA_BASE_URL=http://ollama:11434 \
    OLLAMA_MODEL=llama3.2 \
    OLLAMA_CACHE_TTL=86400 \
    OLLAMA_MAX_SEMANTIC_CACHE=200 \
    MODEL_PERFORMANCE_LOG_INTERVAL=3600

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Copy entrypoint script
COPY api/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run the application using our entrypoint script
CMD ["/app/entrypoint.sh"]
