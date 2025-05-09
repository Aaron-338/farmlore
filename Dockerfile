FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (minimized for resource-constrained systems)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    sqlite3 \
    libsqlite3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache usage
COPY pest-management-chatbot/farmlore-project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the farmlore project into app directory
COPY pest-management-chatbot/farmlore-project /app/

# Make sure scripts are executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/init_ollama_models.sh

# Make port 8000 available
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USE_PROLOG_PRIMARY=true
ENV OLLAMA_MODEL=gemma:2b

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]