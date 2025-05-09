FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (minimized for resource-constrained systems)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    sqlite3 \
    libsqlite3-dev \
    postgresql-client \
    swi-prolog \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN swipl --version # Print SWI-Prolog version

# Set UTF-8 Locale and SWI-Prolog Home
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV SWI_HOME_DIR /usr/lib/swi-prolog

# Copy requirements first for better cache usage
COPY pest-management-chatbot/farmlore-project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the farmlore project into app directory
COPY pest-management-chatbot/farmlore-project /app/

# Make sure scripts are executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/init_ollama_models.sh
RUN chmod +x /app/start_web.sh

# Make port 8000 available
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# These are better set in docker-compose.yml for flexibility
# ENV USE_PROLOG_PRIMARY=true 
# ENV OLLAMA_MODEL=mistral

# ENTRYPOINT ["/app/entrypoint.sh"] # This will be overridden by docker-compose.yml command
# Set a default CMD that can be overridden, or rely on docker-compose.yml command
CMD ["/app/start_web.sh"] # Optional: set start_web.sh as default CMD