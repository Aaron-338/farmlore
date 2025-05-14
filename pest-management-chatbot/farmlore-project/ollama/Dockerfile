FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create directories
WORKDIR /app
RUN mkdir -p /app/modelfiles

# We'll use the mounted volume for modelfiles instead of copying them
# This allows for easier updates during development

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the initialization script
COPY ollama/init-models.sh /app/init.sh

RUN chmod +x /app/init.sh

# Expose the Ollama API port
EXPOSE 11434

# Start initialization script
CMD ["/app/init.sh"]
