FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create directories
WORKDIR /app
RUN mkdir -p /app/modelfiles

# We'll use the mounted volume for modelfiles instead of copying them
# This allows for easier updates during development

# Install Ollama directly from GitHub release
RUN mkdir -p /tmp/ollama && \
    cd /tmp/ollama && \
    wget https://github.com/ollama/ollama/releases/download/v0.1.27/ollama-linux-amd64 && \
    chmod +x ollama-linux-amd64 && \
    mv ollama-linux-amd64 /usr/local/bin/ollama

# Copy and set permissions for the init script
COPY ollama/init.sh /app/init.sh
RUN chmod +x /app/init.sh

# Expose the Ollama API port
EXPOSE 11434

# Start initialization script
CMD ["/app/init.sh"]
